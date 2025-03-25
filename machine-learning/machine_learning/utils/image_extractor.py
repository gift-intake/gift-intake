from PIL import Image
import pytesseract
from io import BytesIO

# Set the path to Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_file: BytesIO):
    try:
        image = Image.open(image_file)
        return pytesseract.image_to_string(image).strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from image: {e}")
