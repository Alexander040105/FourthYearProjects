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
