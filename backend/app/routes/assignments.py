from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.assignment import Assignment
from app.models.subject import Subject
from app.models.teacher import Teacher

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("")
def create_assignment(title: str, subject_id: int, teacher_id: int,
                      description: str = "", db: Session = Depends(get_db)):
    if not db.get(Subject, subject_id): raise HTTPException(404, "Subject not found")
    if not db.get(Teacher, teacher_id): raise HTTPException(404, "Teacher not found")
    a = Assignment(title=title, subject_id=subject_id, teacher_id=teacher_id,
                   description=description or None)
    db.add(a); db.commit(); db.refresh(a)
    return a

@router.get("")
def list_assignments(db: Session = Depends(get_db)):
    return db.query(Assignment).all()
