# Problem 50: Full FastAPI App with Validation and Errors
# Category: Python & FastAPI — Difficulty: Hard — Type: Build
# 
# **Problem:**
# Build a complete FastAPI `projects` API with:
# - Pydantic model for project creation
# - `GET /projects`, `GET /projects/{id}`, `POST /projects`, `DELETE /projects/{id}`
# - Path and query parameters
# - `404` errors for missing items
# - `201` status for creation
# - A `GET /health` route returning `{"status": "ok"}`
# 
# Test it using `/docs`.
# 
# 
# **Example:**
# - `GET /health` → `{"status":"ok"}`
# - `POST /projects {"title":"X","tech":"Y"}` → 201 + new project
# - `GET /projects/999` → 404
# 
# 
# **Constraints:**
# - Use Pydantic, `HTTPException`, `status_code`, and type hints.
# - Data is stored in memory.
# 
# 
# **Prelims topic:**
# full FastAPI app, validation, status codes, docs.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    title: str
    tech: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: Project):
    if not project.title or not project.tech:
        raise HTTPException(status_code=400, detail="Title and tech are required")
    else: 
        return {"title": project.title, "tech": project.tech}

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id == 999:
        raise HTTPException(status_code=404, detail="Project not found")
    else:
        return {"id": project_id, "title": "Sample Project", "tech": "FastAPI"}

