# =====================================================================
#  Week 10 Lab — database.py
#  TODO 1: read the database URL from the environment (not hard-coded).
#  TODO 3: create the engine and a Session factory.
# =====================================================================

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models import Base

# TODO 1 — load the .env file and read DATABASE_URL from the environment.
#          Do NOT paste the real URL here.
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')  # <-- replace None with os.getenv("DATABASE_URL")


# TODO 3 — create the engine and the Session factory.
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)



def init_db():
    """Create the tables from the models. Call this once at startup."""
    # TODO 3 — once the engine exists, uncomment:
    Base.metadata.create_all(engine)
