import random
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, insert

DB_URL = "sqlite:///../backend/members.db"

engine = create_engine(DB_URL)
metadata = MetaData()
members_table = Table(
    "members_table", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("isBorrowing", Boolean, nullable=False, default=False),
    Column("borrowedBookIds", String, nullable=True),  # comma-separated book ids, e.g. "1342,2701"
)
metadata.create_all(engine)

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
    "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
]

members = []
used_names = set()
while len(members) < 200:
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    if name in used_names:
        continue
    used_names.add(name)
    members.append({"name": name})  # id autoincrements; isBorrowing defaults to False

with engine.connect() as connection:
    connection.execute(insert(members_table), members)
    connection.commit()
    print(f"{len(members)} members inserted successfully!")
