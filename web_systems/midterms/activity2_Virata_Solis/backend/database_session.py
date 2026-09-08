from sqlalchemy import create_engine, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

def access_db(databaseName, tableName):
    engine = create_engine(f"sqlite:///{databaseName}.db")
    Base = automap_base()
    Base.prepare(autoload_with=engine)
    return engine, Base.classes[tableName]