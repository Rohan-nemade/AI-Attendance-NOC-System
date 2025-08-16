import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.assignment import Assignment
from app.models.student import Student
from app.models.submission import Submission
from app.models.notification import Notification
from app.services.file_handler import save_upload
from app.services.vectorizer import store_student_vector
from app.schemas.submission import SubmissionResponse


# Where submissions will be saved
UPLOAD_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "assignments")
)

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("", response_model=SubmissionResponse)
def submit_assignment(
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Handle student assignment submission"""

    # Validate assignment & student
    if not db.get(Assignment, assignment_id):
        raise HTTPException(404, "Assignment not found")
    if not db.get(Student, student_id):
        raise HTTPException(404, "Student not found")

    # Make sure directory exists
    target = os.path.join(UPLOAD_ROOT, str(assignment_id), "student")
    os.makedirs(target, exist_ok=True)

    # Save file
    saved_path = save_upload(target, file)

    # Create submission record
    sub = Submission(
        assignment_id=assignment_id,
        student_id=student_id,
        file_path=saved_path
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    # Store vector for similarity checking
    store_student_vector(db, sub)

    # Create notification for student
    assignment = db.get(Assignment, assignment_id)
    notification = Notification(
        student_id=student_id,
        subject_id=assignment.subject_id,
        submission_id=sub.id,
        type="waiting",
        content="Submission received and pending review."
    )
    db.add(notification)
    db.commit()

    return sub
