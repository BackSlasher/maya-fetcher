from sqlalchemy import Column,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, event

engine = create_engine('sqlite:///bla.sqlite', echo = True)
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
Session = sessionmaker(bind = engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Model = declarative_base(name='Model')
Model.query = db_session.query_property()

class Snapshot(Model):
    __tablename__ = "snapshots"
    id = Column(Integer, primary_key=True)
    date_taken = Column(DateTime)

class Shareholders(Model):
    __tablename__ = "shareholders"
    id = Column(Integer, primary_key=True)
    coporate_no = Column(Integer)


def init_db():
    Model.metadata.create_all(bind=engine)
