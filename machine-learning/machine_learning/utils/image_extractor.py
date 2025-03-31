import os
import shutil
from PIL import Image
import pytesseract
from io import BytesIO

def find_tesseract():
    """
    Finds the Tesseract executable automatically.

    Returns:
        str: Path to the Tesseract executable.
    Raises:
        RuntimeError: If Tesseract is not found.
    """
    # 1. Check if an environment variable is set
    tesseract_path = os.getenv("TESSERACT_CMD")

    # 2. If not found, try to locate it automatically
    if not tesseract_path:
        possible_paths = [
            "tesseract",  # Default (if installed globally)
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # Windows default
            "/usr/local/bin/tesseract",  # macOS/Linux
            "/usr/bin/tesseract"  # Linux (alternative)
        ]
        for path in possible_paths:
            if shutil.which(path):
                tesseract_path = path
                break

    # 3. If still not found, raise an error
    if not tesseract_path:
        raise RuntimeError(
            "Tesseract OCR not found! Please install it from https://github.com/tesseract-ocr/tesseract"
        )

    return tesseract_path

# Set the detected Tesseract path
pytesseract.pytesseract.tesseract_cmd = find_tesseract()

def extract_text_from_image(image_file: BytesIO):
    """
    Extracts text from an image file using Tesseract OCR.

    Args:
        image_file (BytesIO): Image file in bytes.

    Returns:
        str: Extracted text from the image.
    """
    try:
        image = Image.open(image_file)
        return pytesseract.image_to_string(image).strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from image: {e}")
