# FastAPI + SQLAlchemy + SQLite Guide

A step-by-step guide for wiring a SQLite database into your FastAPI backend.

## 1. Install dependencies

```bash
pip install "fastapi[standard]" sqlalchemy uvicorn
```

`requirements.txt` (already present):

```
fastapi[standard]
sqlalchemy
uvicorn
```

## 2. Project structure

```
backend/
├── main.py          # FastAPI app + router registration
├── database.py      # engine, session, Base
├── models.py        # SQLAlchemy table models
├── schemas.py       # Pydantic request/response schemas
├── book_routes.py   # CRUD routes
└── books.db         # created automatically
```

## 3. `database.py` — engine & session

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./books.db"

# check_same_thread=False is required for SQLite + FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency: gives each request its own session and always closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 4. `models.py` — the table

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(200), default="")
```

## 5. `schemas.py` — request/response shapes (Pydantic)

Keep API schemas separate from DB models:

```python
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str = ""

class BookOut(BaseModel):
    book_id: int
    title: str
    author: str

    model_config = {"from_attributes": True}  # lets FastAPI serialize ORM objects
```

## 6. `book_routes.py` — CRUD routes

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db
from models import Book
from schemas import BookCreate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.scalars(select(Book)).all()

@router.get("/{book_id}", response_model=BookOut)
def one_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)  # reloads generated values like book_id
    return book

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
```

Notes on your current `book_routes.py`:
- `@router.get("/")` should not take a `Book` body — GET requests shouldn't require a body. Use `response_model=list[BookOut]` and return rows from the DB.
- `book_id` should come from the **path** (`/{book_id}`) or be **auto-generated** by SQLite — don't require it in the create body.

## 7. `main.py` — create tables, CORS, register router

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import book_routes

# Creates books.db and the tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Needed if your frontend runs on a different port (e.g. Vite on :5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_routes.router)
```

## 8. Run it

```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs — Swagger UI lets you test every endpoint without a frontend.

## 9. Test with curl

```bash
# Create
curl -X POST http://127.0.0.1:8000/books/ -H "Content-Type: application/json" -d "{\"title\": \"Dune\", \"author\": \"Frank Herbert\"}"

# List
curl http://127.0.0.1:8000/books/

# One
curl http://127.0.0.1:8000/books/1
```

## 10. Common gotchas

- **`response_model`** on the decorator controls what's serialized — ORM objects work because of `from_attributes`.
- Always `db.commit()` after `add`/`delete`/`setattr` changes, and `db.refresh()` to get DB-generated fields.
- `db.get(Model, id)` is the shortest way to fetch by primary key.
- SQLite is file-based — `books.db` appears next to where you run uvicorn. Add it to `.gitignore`.
- For async later, look at `aiosqlite` + `create_async_engine`, but sync SQLAlchemy is fine for a mini-project.
