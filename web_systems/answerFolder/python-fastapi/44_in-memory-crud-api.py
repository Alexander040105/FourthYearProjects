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
