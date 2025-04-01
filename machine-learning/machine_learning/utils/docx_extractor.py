from docx import Document
from io import BytesIO

def extract_text_from_docx(docx_file: BytesIO):
    try:
        doc = Document(docx_file)
        return "\n".join(para.text for para in doc.paragraphs).strip()
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {e}")
