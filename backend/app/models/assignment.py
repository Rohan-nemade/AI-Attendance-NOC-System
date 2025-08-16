from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Assignment(Base):
    __tablename__ = "assignments"
    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title       = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    subject_id  = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id  = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    due_date    = Column(DateTime, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject")
    teacher = relationship("Teacher")
