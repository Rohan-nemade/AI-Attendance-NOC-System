from sqlalchemy import Column, Integer, Date, Enum, ForeignKey
from app.db import Base
import enum

class Presence(str, enum.Enum):
    present = "present"
    absent  = "absent"

class Attendance(Base):
    __tablename__ = "attendance"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    date       = Column(Date, nullable=False)
    status     = Column(Enum(Presence), nullable=False)
