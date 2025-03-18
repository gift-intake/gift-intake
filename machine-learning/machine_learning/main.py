from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import PyPDF2
from PIL import Image
import pytesseract
from docx import Document
from gliner import GLiNER

app = FastAPI()

# Initialize GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file: BytesIO):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""  # Handle None
            text += page_text
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading PDF: " + str(e))

# Function to extract text from PNG or any image
def extract_text_from_image(image_file: BytesIO):
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error extracting text from image: " + str(e))

# Function to extract text from DOCX file
def extract_text_from_docx(docx_file: BytesIO):
    try:
        doc = Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"  # Add newlines for better structure
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading DOCX file: " + str(e))

# Function to split full name into first and last name
def split_name(full_name: str):
    name_parts = full_name.split()
    if len(name_parts) == 1:
        first_name = name_parts[0]
        last_name = ""  # Handle case where no last name is provided
    else:
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:])  # Handles middle names, if any
    return first_name, last_name

@app.post("/extract/")
async def extract_keywords(file: UploadFile = File(...)):
    """
    Process the uploaded file and extract structured donation details.
    """
    try:
        # Read the uploaded file
        file_data = await file.read()

        # Determine file type
        file_type = file.content_type

        # Extract text based on file type
        if "pdf" in file_type:
            text = extract_text_from_pdf(BytesIO(file_data))
        elif "image" in file_type or file_type in ["png", "jpeg", "jpg"]:
            text = extract_text_from_image(BytesIO(file_data))
        elif "word" in file_type or "msword" in file_type:
            text = extract_text_from_docx(BytesIO(file_data))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file")

        # Run entity extraction using GLiNER
        labels = [
            "constituentID", "constituentType", "giftAmount", "donorFirstName", 
            "donorMiddleName", "donorLastName", "organizationName", "giftIntakeType", 
            "donorAddress", "donorCity", "donorProvince", "donorCountry", "donorPhone", 
            "donorEmail", "giftCurrency", "giftDate", "paymentMethod"
        ]

        # Perform entity extraction with the GLiNER model
        entities = model.predict_entities(text, labels)

        # Initialize structured_entities with empty strings for all labels
        structured_entities = {label: "" for label in labels}

        # Populate structured_entities with extracted values
        for entity in entities:
            structured_entities[entity["label"]] = entity["text"]

        # Extract full name only if donorFirstName or donorLastName is missing
        if not structured_entities["donorFirstName"] and not structured_entities["donorLastName"]:
            full_name = structured_entities.get("donorFirstName", "") + " " + structured_entities.get("donorLastName", "")
            full_name = full_name.strip()

            if full_name:
                first_name, last_name = split_name(full_name)
                structured_entities["donorFirstName"] = first_name
                structured_entities["donorLastName"] = last_name

        return structured_entities

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
