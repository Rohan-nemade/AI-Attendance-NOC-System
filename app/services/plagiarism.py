# app/services/plagiarism.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models.assignment_vector import AssignmentVector
from app.services.extract_text import extract_text_from_docx, extract_text_from_pdf
from app.services.preprocess import clean_text

vectorizer = TfidfVectorizer()

def extract_and_clean(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return None
    return clean_text(raw_text)

def check_and_save_plagiarism(db: Session, student_id: int, subject: str, file_path: str):
    # Step 1: Extract and clean text
    text = extract_and_clean(file_path)
    if not text:
        return {"error": "Unsupported file or extraction failed"}

    # Step 2: Convert to vector
    new_vec = vectorizer.fit_transform([text]).toarray()[0].tolist()

    # Step 3: Fetch all existing vectors for subject
    existing = db.query(AssignmentVector).filter(AssignmentVector.subject == subject).all()

    plagiarized = []
    for record in existing:
        existing_vec = np.array(record.vector).reshape(1, -1)
        new_vec_array = np.array(new_vec).reshape(1, -1)

        score = cosine_similarity(new_vec_array, existing_vec)[0][0]

        if score > 0.80:  # Threshold
            record.is_plagiarized = 1
            db.add(record)
            plagiarized.append({
                "compared_with": record.file_path,
                "similarity": round(float(score), 4)
            })

    # Step 4: Save new file only if unique
    if not plagiarized:
        new_entry = AssignmentVector(
            student_id=student_id,
            subject=subject,
            file_path=file_path,
            vector=new_vec,
            is_plagiarized=0
        )
        db.add(new_entry)

    db.commit()

    return {"plagiarized": plagiarized, "is_unique": len(plagiarized) == 0}
