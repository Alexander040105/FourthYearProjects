from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

class Book(BaseModel):
    book_id: int
    title: str

class 

@router.get("/")
def get_books(book: Book):
    return book

@router.get("/{book_id}")
def one_book(book_id: int):
    return {}