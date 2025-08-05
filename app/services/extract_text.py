from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return " ".join(
        page.extract_text() for page in reader.pages if page.extract_text()
    )

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join(p.text for p in doc.paragraphs)

