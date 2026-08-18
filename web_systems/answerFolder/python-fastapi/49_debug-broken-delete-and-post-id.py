# Problem 49: Debug: Broken DELETE and POST ID
# Category: Python & FastAPI — Difficulty: Hard — Type: Debug
# 
# **Problem:**
# ```python
# @app.post("/projects", status_code=201)
# def create_project(project: Project):
#     new = { "id": len(projects), "title": project.title, "tech": project.tech }
#     projects.append(new)
#     return new
# 
# @app.delete("/projects/{project_id}")
# def delete_project(project_id: int):
#     for i, p in enumerate(projects):
#         if p["id"] == project_id:
#             projects.pop(i)
# ```
# 
# There are two bugs:
# 1. New project IDs start at `0` and can collide with existing IDs.
# 2. The `DELETE` route silently fails when the project does not exist.
# 
# Fix both.
# 
# 
# **Constraints:**
# IDs must be unique. DELETE must return 404 on missing.
# 
# 
# **Prelims topic:**
# CRUD, status codes, list operations.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
