from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def migrate():
    Base.metadata.create_all(engine)
