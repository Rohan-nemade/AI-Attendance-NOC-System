import os 
from app.services.extract_text import extract_text_from_docx,extract_text_from_pdf
from app.services.preprocess import clean_text
from app.services.similarity import compute_similarity

def get_all_existing_files(subject_folder):
    return[
        os.path.join(subject_folder,f)
        for f in os.listdir(subject_folder)
        if f.endswith((".pdf", ".docx"))
    ]

def extract_and_clean_text(file_path):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return None
    return clean_text(raw_text)

def check_similarity(new_file_path, subject):
    subject_folder = os.path.join("assignments/original",subject)
    existing_files =get_all_existing_files(subject_folder)

    new_text = extract_and_clean_text(new_file_path)
    if not new_text:
        return{"error":"Unsupported file format or failed to extact"}
    
    similarities = []
    for existing_file in existing_files:
        if existing_file == new_file_path:
            continue
        existing_text = extract_and_clean_text(existing_file)
        if existing_text:
            score = compute_similarity(new_text,existing_text)
            similarities.append({
                "compared_with": os.path.basename(existing_file),
                "similarity": round(score,4)
            })

    return sorted(similarities,key=lambda x: x["similarity"], reverse=True)