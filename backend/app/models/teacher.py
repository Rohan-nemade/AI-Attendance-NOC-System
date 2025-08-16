from sqlalchemy import Column, Integer, String
from app.db import Base

class Teacher(Base):
    __tablename__ = "teachers"
    id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name  = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(100), nullable=True)
