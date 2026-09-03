# Problem 46: Debug: Type Hint Rejection
# Category: Python & FastAPI — Difficulty: Hard — Type: Debug
# 
# **Problem:**
# ```python
# @app.get("/projects/{project_id}")
# def get_project(project_id: int):
#     return { "id": project_id }
# ```
# A request to `GET /projects/abc` currently causes a 500 server error. FastAPI should automatically reject it with a clear validation error.
# 
# What status code and body should FastAPI return, and why? Explain the fix (no code change is necessary if the route is written correctly).
# 
# 
# **Constraints:**
# Let FastAPI's type hints do the validation.
# 
# 
# **Prelims topic:**
# type hints, validation, status 422.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
