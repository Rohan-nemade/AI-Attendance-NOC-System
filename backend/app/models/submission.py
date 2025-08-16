import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

import enum

class Submission(Base):
    __tablename__ = "submissions"
    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id= Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id   = Column(Integer, ForeignKey("students.id"), nullable=False)
    file_path    = Column(String, nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)
    status       = Column(String, default="pending")  # pending/approved/rejected
    grade        = Column(Float, nullable=True)        # optional marking
    remarks      = Column(String, nullable=True)

    assignment   = relationship("Assignment")
    student      = relationship("Student")
