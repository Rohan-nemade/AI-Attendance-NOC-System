# app/routers/plagiarism.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.submission import Submission
from app.models.similarity_result import SimilarityResult
from app.services.extract_text import extract_text_from_pdf, extract_text_from_docx
from app.services.preprocess import clean_text
from app.services.similarity import compute_similarity
import pickle  # for storing vectors

router = APIRouter(prefix="/plagiarism", tags=["Plagiarism"])

THRESHOLD = 0.80


def extract_and_clean_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return None
    return clean_text(raw_text)


@router.post("/check/{submission_id}")
def check_plagiarism(submission_id: int, db: Session = Depends(get_db)):
    # 1. Fetch submission
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # 2. Extract + clean text
    new_text = extract_and_clean_text(submission.file_path)
    if not new_text:
        raise HTTPException(status_code=400, detail="Unsupported or unreadable file format")

    # 3. Vectorize (always generate new for current)
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    new_vector = vectorizer.fit_transform([new_text]).toarray()[0]

    plagiarized = False
    results = []

    # 4. Compare only against UNIQUE submissions
    unique_submissions = db.query(Submission).filter(Submission.status == "unique").all()

    for existing in unique_submissions:
        existing_vector = pickle.loads(existing.vector)  # load stored numpy array
        score = compute_similarity(new_vector, existing_vector)

        sim_result = SimilarityResult(
            submission_id=submission.id,
            compared_with=existing.id,
            score=score
        )
        db.add(sim_result)

        results.append({
            "compared_with": existing.id,
            "similarity": round(score, 4)
        })

        if score >= THRESHOLD:
            # Mark both plagiarized & remove vectors
            submission.status = "plagiarized"
            existing.status = "plagiarized"
            submission.vector = None
            existing.vector = None
            plagiarized = True

    # 5. If unique → save vector in DB
    if not plagiarized:
        submission.status = "unique"
        submission.vector = pickle.dumps(new_vector)

    db.commit()

    return {
        "submission_id": submission.id,
        "status": submission.status,
        "results": results
    }
