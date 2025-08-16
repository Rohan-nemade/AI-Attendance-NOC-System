from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.teacher import Teacher

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("")
def create_teacher(name: str, email: str, department: str = "", db: Session = Depends(get_db)):
    t = Teacher(name=name, email=email, department=department or None)
    db.add(t); db.commit(); db.refresh(t)
    return t

@router.get("")
def list_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()
