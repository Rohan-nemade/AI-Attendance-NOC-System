import os
from fastapi import UploadFile
from datetime import datetime
import shutil

BASE_DIR = "assignments/original"

def save_uploaded_assgnment(file: UploadFile, student_id: str, subject: str):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    subject_folder = os.path.join(BASE_DIR, subject)
    os.makedirs(subject_folder, exist_ok=True)

    filename = f"{student_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(subject_folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path