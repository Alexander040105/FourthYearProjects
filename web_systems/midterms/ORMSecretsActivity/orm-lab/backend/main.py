# =====================================================================
#  Week 10 Lab — main.py  (STARTER)
#  This API still uses an in-memory list. Your job is to replace it
#  with the database, through the ORM.  Follow the TODOs in order.
#
#  Run it:   fastapi dev main.py     (http://localhost:8000/docs)
# =====================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Session
from models import Project

app = FastAPI()
from database import Session, init_db
init_db()   

class ProjectIn(BaseModel):
    title: str
    tech: str


# -------------------------------------------------------------------
#  The old in-memory "database". You will delete this in TODO 4.
# -------------------------------------------------------------------
projects = [
    {"id": 1, "title": "Weather App", "tech": "React", "done": False},
]


@app.get("/projects")
def list_projects():
    # TODO 4 — read from the database with a session instead of the list:
    #     with Session() as session:
    #         return session.query(Project).all()
    with Session() as session:
        return session.query(Project).all()


@app.post("/projects", status_code=201)
def create_project(data: ProjectIn):
    # TODO 5 — create a Project, add() it, commit(), and return it.
    with Session() as session:
        try:
            new_project = Project(
                title=data.title,
                tech=data.tech,
                done=False
            )
            session.add(new_project)
            session.commit()
            session.refresh(new_project)
            return new_project
        except Exception as e:
            session.rollback()
            raise HTTPException(500, f"Failed to create project: {e}")


@app.patch("/projects/{project_id}")
def toggle_done(project_id: int):
    # TODO 6 — load the Project by id (404 if missing), flip done, commit.
    with Session() as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(404, "Project not found")
        project.done = not project.done
        session.commit()
        session.refresh(project)
        return project
    
