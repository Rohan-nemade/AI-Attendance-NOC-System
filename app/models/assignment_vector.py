# app/models/assignment_vector.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from app.services.database import Base

class AssignmentVector(Base):
    __tablename__ = "assignment_vectors"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    vector = Column(JSON, nullable=False)  # store TF-IDF dense array as JSON
    is_plagiarized = Column(Integer, default=0)  # 0 = unique, 1 = plagiarized
