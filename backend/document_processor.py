import os
from pypdf import PdfReader
from docx import Document
from fastapi import UploadFile

async def extract_text_from_upload(file: UploadFile) -> str:
    text = ""
    file_bytes = await file.read()
    
    # Save temporarily to parse it
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(file_bytes)
    
    try:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(temp_file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif file.filename.endswith(".docx"):
            doc = Document(temp_file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file.filename.endswith(".txt"):
            text = file_bytes.decode("utf-8")
        else:
            raise ValueError("Unsupported file type")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    return text.strip()
