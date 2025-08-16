from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.subject import Subject
from app.models.teacher import Teacher

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("")
def create_subject(name: str, code: str, teacher_id: int, db: Session = Depends(get_db)):
    if not db.get(Teacher, teacher_id):
        raise HTTPException(404, "Teacher not found")
    s = Subject(name=name, code=code, teacher_id=teacher_id)
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("")
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()
