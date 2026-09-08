import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = "sqlite:///books.db"

engine = create_engine(DB_URL)
metadata = MetaData()
books_table = Table(
    "books_table", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("category", String, nullable=False),
    Column("isBorrowed", Boolean, nullable=False,default=False),
    Column("borrowedBy", String, nullable=True)
)
metadata.create_all(engine)
books = []
for page in range(1,10):
    url = f"https://gutendex.com/books/?page={page}"

    response = requests.get(url)
    if response.status_code == 200:
        # Parse the data into a Python dictionary
        data = response.json()

        for entries in data.get("results"):
            authors = entries["authors"]
            shelves = entries["bookshelves"]
            book_data = {
                "id": entries.get("id"),
                "title": entries.get("title"),
                "author": authors[0]["name"] if authors else "unknown",
                "category": shelves[0].removeprefix("Category: ") if shelves else "uncategorized"
                }
            books.append(book_data)
        print("")
        print(books)
    else:
        print(f"Error: {response.status_code}")


with engine.connect() as connection:
    connection.execute(insert(books_table), books)
    connection.commit()
    print("Records inserted successfully!")
