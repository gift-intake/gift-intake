import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_file: BytesIO):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")
