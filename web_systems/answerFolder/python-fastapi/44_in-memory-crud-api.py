# Problem 44: In-Memory CRUD API
# Category: Python & FastAPI — Difficulty: Medium — Type: Build
# 
# **Problem:**
# Build a full in-memory CRUD API for `projects`:
# - `GET /projects` — list all
# - `GET /projects/{project_id}` — get one or 404
# - `POST /projects` — create with status 201
# - `DELETE /projects/{project_id}` — delete or 404
# 
# Use a Pydantic model for creation. Store data in a global Python list.
# 
# 
# **Example:**
# After `POST /projects {"title":"X","tech":"Y"}`, `GET /projects` includes the new item. After `DELETE /projects/1`, it is gone.
# 
# 
# **Constraints:**
# - Use proper status codes (`201`, `404`).
# - IDs should be unique and auto-incrementing.
# 
# 
# **Prelims topic:**
# CRUD, REST, FastAPI, HTTP methods.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class ProjectCreate(BaseModel):
    title: str
    tech: str


class Project(BaseModel):
    project_id: int
    title: str
    tech: str


projects_db: list[Project] = []
_next_id = 1


@app.get('/projects')
def list_projects():
    return projects_db


@app.get('/projects/{project_id}')
def get_project(project_id: int):
    for project in projects_db:
        if project.project_id == project_id:
            return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')


@app.post('/projects', status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate):
    global _next_id
    project = Project(
        project_id=_next_id,
        title=project_in.title,
        tech=project_in.tech,
    )
    projects_db.append(project)
    _next_id += 1
    return project


@app.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for i, project in enumerate(projects_db):
        if project.project_id == project_id:
            projects_db.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')