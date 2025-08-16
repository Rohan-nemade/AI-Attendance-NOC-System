from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PlagiarismResult(Base):
    __tablename__ = "plagiarism_results"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    compared_with_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    is_plagiarized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    submission = relationship("Submission", foreign_keys=[submission_id])
    compared_with = relationship("Submission", foreign_keys=[compared_with_id])
