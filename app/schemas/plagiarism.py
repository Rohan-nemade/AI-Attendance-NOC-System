from pydantic import BaseModel
from datetime import datetime

class PlagiarismResultBase(BaseModel):
    submission_id: int
    compared_with_id: int
    similarity_score: float
    is_plagiarized: bool

class PlagiarismResultCreate(PlagiarismResultBase):
    pass

class PlagiarismResultOut(PlagiarismResultBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
