from sqlalchemy.orm import Session
from app.models.assignment_vector import AssignmentVector, VectorType
from app.models.submission import Submission
from app.models.assignment import Assignment
from app.services.file_handler import extract_text
from app.utils.tfhash import text_to_tfhash
from app.utils.bert import text_to_bert

def store_student_vector(db: Session, submission: Submission) -> AssignmentVector:
    text = extract_text(submission.file_path)
    vec  = text_to_tfhash(text)
    av = AssignmentVector(submission_id=submission.id, vector_type=VectorType.tfhash, vector_data=vec)
    db.add(av); db.commit(); db.refresh(av)
    return av

def store_teacher_ref_vector(db: Session, assignment: Assignment, teacher_doc_path: str) -> AssignmentVector:
    text = extract_text(teacher_doc_path)
    vec  = text_to_bert(text)
    av = AssignmentVector(assignment_id=assignment.id, vector_type=VectorType.bert, vector_data=vec)
    db.add(av); db.commit(); db.refresh(av)
    return av
