from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Notification(Base):
    __tablename__ = "notifications"
    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id    = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id    = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=True)
    type          = Column(String, nullable=False)   # success/fail/waiting/info
    content       = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow)
    read_at       = Column(DateTime, nullable=True)

    student    = relationship("Student")
    subject    = relationship("Subject")
