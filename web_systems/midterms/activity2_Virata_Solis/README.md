# Library API — Activity 2 (Virata & Solis)

FastAPI + SQLAlchemy + SQLite mini-project. Book data is scraped from the
[Gutendex](https://gutendex.com) API; members are generated dummy data.

## Project structure

```
activity2_Virata_Solis/
├── README.md
├── backend/
│   ├── main.py              # FastAPI app, CORS, router registration
│   ├── book_routes.py       # /books endpoints (CRUD + filters)
│   ├── members_routes.py    # /members endpoints — TO BE CREATED (partner)
│   ├── database_session.py  # access_db() helper (automap reflection)
│   ├── requirements.txt
│   ├── books.db             # seeded book data
│   └── members.db           # seeded member data
└── book_data/
    ├── scrapeBooks.py       # fetches ~288 books from Gutendex into books.db
    └── generateMembers.py   # generates 200 dummy members into backend/members.db
```

## Setup

```powershell
# from the repo root (FourthYearProjects/)
.venv/Scripts/Activate.ps1
pip install -r web_systems/midterms/activity2_Virata_Solis/backend/requirements.txt

# run the API — MUST be run from the backend/ folder
cd web_systems/midterms/activity2_Virata_Solis/backend
uvicorn main:app --reload
```

Swagger docs: http://127.0.0.1:8000/docs

## How the DB layer works

`database_session.access_db(databaseName, tableName)` opens
`sqlite:///{databaseName}.db` **relative to the folder uvicorn was started in**
(that's why you run it from `backend/`), reflects the table with SQLAlchemy
`automap`, and returns `(engine, TableClass)`:

```python
from database_session import access_db

db_engine, members_table = access_db('members', 'members_table')

# then use it like an ORM class:
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(db_engine) as session:
    rows = session.scalars(select(members_table)).all()
    member = session.get(members_table, member_id)
```

Column access on the automapped class: `members_table.name`, `members_table.id`.

## Schemas

### `books_table` (books.db)
| column      | type    | notes                                    |
|-------------|---------|------------------------------------------|
| id          | Integer | PK, comes from the Gutenberg id          |
| title       | String  |                                          |
| author      | String  | "unknown" if the API had none            |
| category    | String  | first bookshelf, "uncategorized" if none |
| isBorrowed  | Boolean | stored as 0/1, defaults to False         |
| borrowedBy  | String  | NULL = not borrowed; store the member id |

### `members_table` (members.db)
| column          | type    | notes                                              |
|-----------------|---------|-----------------------------------------------------|
| id              | Integer | PK, SQLite autoincrement                           |
| name            | String  | generated "First Last"                             |
| isBorrowing     | Boolean | 0/1, defaults to False                             |
| borrowedBookIds | String  | NULL = none; comma-separated book ids, e.g. "1342,2701" |

The borrow link is two-sided: `books_table.borrowedBy` holds the member id,
and `members_table.borrowedBookIds` holds the book ids. Both must be updated
together on borrow/return.

## Existing endpoints (books — done)

| Method | Path              | Success | Notes                                        |
|--------|-------------------|---------|----------------------------------------------|
| GET    | /books/           | 200     | filters: `?title=`, `?author=`, `?isBorrowed=` |
| GET    | /books/{book_id}  | 200     | 404 if missing                               |
| POST   | /books/           | 201     | body: title, author, category                |
| PATCH  | /books/{book_id}  | 200     | partial update of any field                  |
| DELETE | /books/{book_id}  | 200     | 404 if missing                               |

## What's left (members — partner)

1. Create `backend/members_routes.py` — copy the pattern in `book_routes.py`:
   `APIRouter(prefix="/members", tags=["members"])`, a `Member` Pydantic model
   (`id`, `name`, `isBorrowing: bool`, `borrowedBookIds: str | None` — set
   `model_config = {"from_attributes": True}`), and
   `access_db('members', 'members_table')`.
2. Members CRUD:
   - `GET /members/` → 200 (list)
   - `GET /members/{member_id}` → 200 / 404
   - `POST /members/` → 201 (body: `name`; id autoincrements)
   - `PATCH` or `PUT /members/{member_id}` → 200 / 404
   - `DELETE /members/{member_id}` → 200 or 204
3. Borrow relationship — nested, one level deep. Suggested routes:
   - `GET /members/{member_id}/books` → books where `books_table.borrowedBy == member_id`
   - `POST /members/{member_id}/books/{book_id}` → borrow. Update BOTH sides:
     book: `isBorrowed=True`, `borrowedBy=member_id` — member: `isBorrowing=True`,
     append book_id to `borrowedBookIds`. Reject with 409 if already borrowed.
   - `DELETE /members/{member_id}/books/{book_id}` → return. Reverse both:
     book: `isBorrowed=False`, `borrowedBy=None` — member: remove the id from
     `borrowedBookIds`, set `isBorrowing=False` when the list is empty.
4. Register the router in `main.py`:
   ```python
   from members_routes import router as member_router
   app.include_router(member_router)
   ```
5. Put the success status code on each decorator (`status_code=status.HTTP_201_CREATED` etc.).

## Gotchas

- **DB paths are relative to the run directory.** Run uvicorn from `backend/`,
  run the seed scripts from `book_data/` (they write `../backend/*.db`).
- **Reseeding:** `create_all` won't alter existing tables and re-running inserts
  duplicates. Delete the `.db` file, then re-run the script.
- **Books db:** `scrapeBooks.py` writes `book_data/books.db` by default — its
  `DB_URL` is `sqlite:///books.db`. If you reseed books, either move the file to
  `backend/` or change `DB_URL` to `sqlite:///../backend/books.db`, and make sure
  `access_db` in `book_routes.py` points at the same file.
- Re-running `generateMembers.py` appends another 200 rows (no dedup against the
  db, only within the run).
- `borrowedBy` is a plain String column, not a real FK — enforcement of the
  member link is on you in the routes.
