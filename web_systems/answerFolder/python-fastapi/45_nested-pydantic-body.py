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
