import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Store DB at project root (you already have noc_db.sqlite3)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_FILE = os.path.join(ROOT, "noc_db.sqlite3")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
