import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
