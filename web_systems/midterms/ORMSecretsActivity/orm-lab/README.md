# Week 10 Lab — Give Your API a Real Database (Student)

Your Students/Projects API still keeps its data in a Python list, and its
password would be hard-coded. In this lab you will:

1. Move the database URL into a **`.env`** file (secrets management).
2. Describe your table as a **SQLAlchemy model**.
3. Wire up the **engine and session**.
4. Replace the in-memory list with **real database reads and writes**.

When you finish, your data survives a restart, and no secret lives in the code.

## What you need

- **Python 3.10+**
- **PostgreSQL 14+** running locally, with a database you can use

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then edit .env with your real values
fastapi dev main.py                # http://localhost:8000/docs
```

## Your tasks (follow the TODOs in the code, in order)

- **TODO 1** — `database.py`: read `DATABASE_URL` from the environment with
  `os.getenv`. Never paste the real URL into the code.
- **TODO 2** — `models.py`: finish the `Project` model (title, tech, done).
- **TODO 3** — `database.py`: create the `engine` and the `Session` factory,
  and let `init_db()` create the tables.
- **TODO 4** — `main.py`: make `GET /projects` read from the database.
- **TODO 5** — `main.py`: make `POST /projects` create, add, commit, return.
- **TODO 6** — `main.py`: make `PATCH /projects/{id}` load-or-404, toggle, commit.
- Finally, **delete the `projects = [...]` list** — nothing should use it anymore.

## Done when

- The app starts with no errors and `/docs` works.
- You can create a project, then **restart the server**, and it is still there.
- Toggling `done` and (stretch) deleting both work.
- There is **no password anywhere in the code**, and `.env` is git-ignored.

## Stretch

- Add `GET /projects/{id}` (404 if missing) and `DELETE /projects/{id}`.
- Add a second secret to `.env` (e.g. an `APP_NAME`) and read it the same way.
- Confirm `git status` never lists `.env`.
