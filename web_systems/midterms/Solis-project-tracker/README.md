# Project Tracker — Debugging Challenge

A small full-stack app: a **FastAPI** back end and a **React + Tailwind** front end.
It lets you list coding projects, add one, mark it done, and delete it.

**There is a problem: the app is broken.** Ten bugs have been planted across the
stack. Your job is to find and fix all of them so the app runs correctly.

You are not writing new features. Every bug is a small mistake of the kind covered
in your learning materials — a missing import, a wrong keyword, a hook not passed
correctly, a bit of styling that never gets wired up.

---

## What you need installed

- **Python 3.10+**
- **Node.js 18+** (for the React front end)

## How to run it (two terminals)

**Terminal 1 — the back end**

```
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py              # serves http://localhost:8000
```

Check the API on its own at http://localhost:8000/docs

**Terminal 2 — the front end**

```
cd frontend
npm install
npm run dev                      # serves http://localhost:5173
```

Open http://localhost:5173 in your browser.

---

## How to work

1. Start the back end first. If it will not start, read the traceback — that is bug one.
2. Start the front end. If the page is blank or unstyled, open the browser
   **DevTools Console** (F12) and read what it says.
3. Keep the **Console** and the **Network** tab open the whole time. Most of the
   remaining bugs announce themselves there.
4. Fix one bug, save, and see what changes. Work in small steps.

## When is it "done"?

- The back end starts with no errors.
- The page loads, fully styled, showing the two starter projects.
- You can **add** a project and it appears immediately.
- You can mark a project **Done** (and undo it).
- You can **delete** a project.
- The browser console shows **no errors or warnings**.

## A few honest hints

- Bugs live in: `backend/main.py`, `frontend/src/App.jsx`,
  `frontend/src/index.css`, and the two files in `frontend/src/components/`.
- Roughly half stop something from running; the other half let it run but
  misbehave. "It loads but the button does nothing" is still a bug.
- The back end works perfectly in `/docs` even while the browser cannot reach it.
  That is a clue, not a contradiction.
- Read error messages to the end. They almost always name the file and the line.

Good luck. Fix them all and you will have debugged a real full-stack app.
