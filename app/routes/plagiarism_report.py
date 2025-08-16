# app/routes/plagiarism_report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.submission import Submission
from app.models.similarity import SimilarityCheck  # assuming we store results in this table

router = APIRouter()

@router.get("/plagiarism-report/{subject_id}")
def get_plagiarism_report(subject_id: int, db: Session = Depends(get_db)):
    report = (
        db.query(SimilarityCheck)
        .join(Submission, Submission.id == SimilarityCheck.submission_id)
        .filter(
            Submission.subject_id == subject_id,
            SimilarityCheck.similarity > 0.80  # threshold
        )
        .all()
    )

    if not report:
        raise HTTPException(status_code=404, detail="No plagiarism detected for this subject")

    return [
        {
            "submission_id": r.submission_id,
            "student_id": db.query(Submission.student_id).filter(Submission.id == r.submission_id).scalar(),
            "compared_with": r.compared_with,
            "similarity": r.similarity,
            "created_at": r.created_at,
        }
        for r in report
    ]
