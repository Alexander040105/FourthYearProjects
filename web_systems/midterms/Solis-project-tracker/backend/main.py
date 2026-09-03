#not importing HTTPException
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

#added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectIn(BaseModel):
    title: str  
    tech: str


# our "database" for now: a plain list in memory
projects = [
    {"id": 1, "title": "Portfolio Site", "tech": "React", "done": False},
    {"id": 2, "title": "Weather App", "tech": "Tailwind", "done": True},
]


def next_id():
    return max((p["id"] for p in projects), default=0) + 1

# no colon 
@app.get("/projects")
def list_projects():
    return projects


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for p in projects:
        if p["id"] == project_id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@app.post("/projects", status_code=201)
def create_project(project: ProjectIn):
    new = {
        "id": next_id(),
        "title": project.title,
        "tech": project.tech,
        "done": False,
    }
    projects.append(new)
    return new

# the bug is not declaring that int is the required type for project_id
@app.patch("/projects/{project_id}")
def toggle_done(project_id: int):
    for p in projects:
        if p["id"] == project_id:
            p["done"] = not p["done"] 
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for p in projects:
        if p["id"] == project_id:
            projects.remove(p)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")