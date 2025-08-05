from app.services.assignment import save_uploaded_assgnment
from app.services.similarity_check import check_similarity
from fastapi import APIRouter, File, UploadFile,Form

router = APIRouter()

@router.post("/upload-assignment")
async def upload_assignment(
    file: UploadFile = File(...),
    student_id: str = Form(...),
    subject: str = Form(...),
):
    file_path = save_uploaded_assgnment(file, student_id, subject)
    
    similarity_results = check_similarity(file_path, subject)

    return {
        "message": "File Uploaded",
        "path": file_path,
        "similarity": similarity_results
    }
