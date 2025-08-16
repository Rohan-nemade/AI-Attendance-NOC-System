from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.student import Student, YearEnum

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("")
def create_student(name: str, email: str, roll_no: str, prn_no: str,
                   batch: str, year: YearEnum, db: Session = Depends(get_db)):
    s = Student(name=name, email=email, roll_no=roll_no, prn_no=prn_no, batch=batch, year=year)
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
