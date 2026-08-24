# Problem 40: Debug: Create Returns 200 Not 201
# Category: Python & FastAPI — Difficulty: Medium — Type: Debug
# 
# **Problem:**
# ```python
# @app.post("/projects")
# def create_project(project: Project):
#     new_project = { "id": 1, "title": project.title }
#     return new_project
# ```
# A successful create should return HTTP 201. Fix the route decorator.
# 
# 
# **Constraints:**
# Do not return `200` for a creation endpoint.
# 
# 
# **Prelims topic:**
# HTTP status codes, POST.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    id = int
    title = str

@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: Project):
    new_project = { "id": 1, "title": project.title }
    return new_project