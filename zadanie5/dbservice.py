import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    SQLALCHEMY_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
else:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("://", "ql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
