# Problem 45: Nested Pydantic Body
# Category: Python & FastAPI — Difficulty: Hard — Type: Build
# 
# **Problem:**
# Define two Pydantic models:
# - `Skill` with `name: str` and `level: int` (must be ≥ 1)
# - `Project` with `title: str`, `tech: str`, and `skills: list[Skill]`
# 
# Create a `POST /projects` route that validates the nested body and returns the project as JSON.
# 
# 
# **Example:**
# ```json
# POST /projects
# {
#   "title": "Weather App",
#   "tech": "React",
#   "skills": [
#     { "name": "React", "level": 3 }
#   ]
# }
# ```
# 
# 
# **Constraints:**
# - Use nested `BaseModel`.
# - Validate `level` is a positive integer.
# 
# 
# **Prelims topic:**
# Pydantic, nested models, validation.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Skill(BaseModel):
    name: str
    level: int = Field(ge=1)

class Project(BaseModel):
    title: str
    tech: str
    skills: list[Skill]

@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: Project):
    return project
    
