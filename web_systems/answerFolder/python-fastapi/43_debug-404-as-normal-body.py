# Problem 43: Debug: 404 as Normal Body
# Category: Python & FastAPI — Difficulty: Medium — Type: Debug
# 
# **Problem:**
# ```python
# @app.get("/projects/{project_id}")
# def get_project(project_id: int):
#     if project_id != 1:
#         return { "error": "Project not found" }
#     return { "id": 1, "title": "Weather App" }
# ```
# A missing project should return HTTP 404, not a 200 response with an error body. Fix it.
# 
# 
# **Constraints:**
# Use `HTTPException`.
# 
# 
# **Prelims topic:**
# HTTP status codes, error handling.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
