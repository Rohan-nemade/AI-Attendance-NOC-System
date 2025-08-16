from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    file_path: str
    status: Optional[str] = None
    remarks: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

