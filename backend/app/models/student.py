from sqlalchemy import Column, Integer, String, Enum
from app.db import Base
import enum

class YearEnum(str, enum.Enum):
    first = "first"
    second = "second"
    third = "third"
    fourth = "fourth"

class Student(Base):
    __tablename__ = "students"
    id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name    = Column(String(100), nullable=False)            # Full name
    email   = Column(String(150), unique=True, nullable=False)
    roll_no = Column(String(50),  unique=True, nullable=False)
    prn_no  = Column(String(50),  unique=True, nullable=False)
    batch   = Column(String(50),  nullable=False)            # e.g., B1, B2
    year    = Column(Enum(YearEnum), nullable=False)         # first..fourth
