import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = None

def set_engine(engine_name: str):
    global engine
    if engine_name == "sqlite":
        engine = create_engine("sqlite:///bla.sqlite", echo=True)
    elif engine_name == "postgresql":
        user = os.environ.get("PGUSER")
        password = os.environ["PGPASSWORD"]
        engine = create_engine(f"postgresql://{user}:{password}@test-finance.ctkj9wimtlrm.us-east-1.rds.amazonaws.com:5432/pension", echo=True)
    else:
        raise ValueError("Engine name is unclear", engine_name)


def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
