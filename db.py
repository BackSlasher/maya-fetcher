import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def get_engine():
    # SQLite
    # return create_engine("sqlite:///bla.sqlite", echo=True)
    # PostgreSQL
    user = os.environ.get("PGUSER")
    password = os.environ["PGPASSWORD"]
    return create_engine(f"postgresql://{user}:{password}@test-finance.ctkj9wimtlrm.us-east-1.rds.amazonaws.com:5432/pension", echo=True)

engine = get_engine()


def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
