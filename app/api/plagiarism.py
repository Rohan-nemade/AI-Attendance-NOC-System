from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.submission import Submission
from app.models.plagiarism import PlagiarismResult
from app.schemas.plagiarism import PlagiarismResultOut
from app.services.preprocess import clean_text
from app.services.similarity import compute_similarity
from app.services.extract_text import extract_text_from_docx, extract_text_from_pdf
import os

router = APIRouter(prefix="/plagiarism", tags=["Plagiarism"])

SIMILARITY_THRESHOLD = 0.80  # above this → plagiarism


def extract_and_clean_text(file_path: str):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return None
    return clean_text(raw_text)


@router.post("/check/{submission_id}", response_model=list[PlagiarismResultOut])
def check_plagiarism(submission_id: int, db: Session = get_db()):
    # Get the new submission
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    new_text = extract_and_clean_text(submission.file_path)
    if not new_text:
        raise HTTPException(status_code=400, detail="Unsupported or empty file")

    # Fetch all existing submissions except this one
    existing_submissions = (
        db.query(Submission)
        .filter(Submission.id != submission_id)
        .all()
    )

    results = []

    for existing in existing_submissions:
        existing_text = extract_and_clean_text(existing.file_path)
        if not existing_text:
            continue

        score = compute_similarity(new_text, existing_text)
        is_plagiarized = score >= SIMILARITY_THRESHOLD

        # Save result in DB
        result = PlagiarismResult(
            submission_id=submission_id,
            compared_with_id=existing.id,
            similarity_score=score,
            is_plagiarized=is_plagiarized,
        )
        db.add(result)
        db.commit()
        db.refresh(result)

        results.append(result)

    return results
