# Problem 41: POST with Pydantic
# Category: Python & FastAPI — Difficulty: Medium — Type: Build
# 
# **Problem:**
# Define a Pydantic model `Project` with `title: str`, `tech: str`, and an optional `stars: int = 0`. Create a `POST /projects` route that accepts a `Project` body and returns:
# ```json
# { "created": project.title, "tech": project.tech, "stars": project.stars }
# ```
# 
# 
# **Example:**
# `POST /projects` with body `{"title":"X","tech":"Y"}` returns:
# ```json
# { "created": "X", "tech": "Y", "stars": 0 }
# ```
# 
# 
# **Constraints:**
# - Inherit from `BaseModel`.
# - `stars` must have a default value.
# 
# 
# **Prelims topic:**
# Pydantic, request body, POST.

# ========================== YOUR ANSWER BELOW ==========================
# Write your Python / FastAPI answer here
