from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Subject(Base):
    __tablename__ = "subjects"
    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name       = Column(String(100), nullable=False)
    code       = Column(String(50), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher    = relationship("Teacher")
