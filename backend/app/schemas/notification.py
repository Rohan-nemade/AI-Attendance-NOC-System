# app/schemas/notification.py
from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    submission_id: int
    type: str
    content: str

    class Config:
        orm_mode = True
