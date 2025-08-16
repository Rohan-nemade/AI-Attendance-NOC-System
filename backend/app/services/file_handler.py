import os
from fastapi import UploadFile
from PyPDF2 import PdfReader
import docx

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload(folder_path: str, file: UploadFile):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path


def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF or DOCX file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text.strip()
