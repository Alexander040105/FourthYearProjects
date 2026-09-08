from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from book_routes import router as book_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router)

@app.get("/")
def main():
    return {"message":"the API runs!"}