from sqlalchemy import Column, Integer, Enum, JSON, ForeignKey, DateTime
from datetime import datetime
from app.db import Base
import enum

class VectorType(str, enum.Enum):
    tfhash = "tfhash"   # student vectors (fast TF hashing)
    bert   = "bert"     # teacher reference vectors

class AssignmentVector(Base):
    __tablename__ = "assignment_vectors"
    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=True)  # student
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=True)  # teacher reference
    vector_type   = Column(Enum(VectorType), nullable=False)
    vector_data   = Column(JSON, nullable=False)            # list[float], stored JSON
    created_at    = Column(DateTime, default=datetime.utcnow)
