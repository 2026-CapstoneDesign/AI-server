import fitz  # PyMuPDF
import os


def extract_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path, filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_pdf(file_path)
    
    elif ext == ".txt":
        return extract_txt(file_path)
    
    else:
        raise ValueError("현재는 PDF와 TXT 파일만 지원합니다.")