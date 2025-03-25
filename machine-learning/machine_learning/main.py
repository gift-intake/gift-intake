from fastapi import FastAPI, HTTPException, File, UploadFile
from utils.outlook_extractor import fetch_outlook_attachments
from utils.docx_extractor import extract_text_from_docx
from utils.image_extractor import extract_text_from_image
from utils.pdf_extractor import extract_text_from_pdf
from gliner import GLiNER
from io import BytesIO
import logging

# Initialize FastAPI app
app = FastAPI()

# Initialize GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to split full name into First, Middle, and Last name
def split_name(full_name: str):
    """
    Split a full name into First, Middle, and Last name.
    """
    name_parts = full_name.split()
    if len(name_parts) == 1:
        return name_parts[0], "", ""  # Only First Name
    elif len(name_parts) == 2:
        return name_parts[0], "", name_parts[1]  # First and Last Name
    else:
        return name_parts[0], " ".join(name_parts[1:-1]), name_parts[-1]  # First, Middle(s), Last

# Helper function to extract text based on file type
def extract_text_from_file(file_data: BytesIO, file_type: str):
    """
    Extract text from the file based on the file type.
    """
    if "pdf" in file_type:
        return extract_text_from_pdf(file_data)
    elif "image" in file_type or file_type in ["png", "jpeg", "jpg"]:
        return extract_text_from_image(file_data)
    elif "word" in file_type or "msword" in file_type:
        return extract_text_from_docx(file_data)
    else:
        return None

@app.post("/extract/outlook/")
async def extract_outlook_attachments_route(username: str, password: str):
    """
    Fetch attachments from Outlook and process them using the extraction logic.
    """
    try:
        # Fetch the attachments from Outlook
        attachments = fetch_outlook_attachments(username, password)

        # If the attachments are not in the expected format, raise an error
        if not isinstance(attachments, list):
            raise HTTPException(status_code=400, detail=attachments.get("error", "Unknown error occurred."))

        # Labels for entity extraction
        labels = [
            "ConstituentID", "ConstituentType", "GiftAmount", "DonorFirstName",
            "DonorMiddleName", "DonorLastName", "OrganizationName", "GiftIntakeType",
            "DonorAddress", "DonorCity", "DonorProvince", "DonorCountry", "DonorPhone",
            "DonorEmail", "GiftCurrency", "GiftDate", "PaymentMethod"
        ]

        results = []

        for attachment in attachments:
            file_data = attachment["file_data"]
            file_type = attachment["file_type"]
            file_name = attachment["file_name"]

            # Extract text from the attachment file based on its type
            text = extract_text_from_file(BytesIO(file_data), file_type)

            if not text:
                logging.warning(f"No text extracted from file: {file_name}")
                raise HTTPException(status_code=400, detail=f"No text extracted from file: {file_name}")

            # Run entity extraction with GLiNER
            entities = model.predict_entities(text, labels)
            structured_entities = {label: "" for label in labels}

            # Populate extracted values into the structured entity dictionary
            for entity in entities:
                structured_entities[entity["label"]] = entity["text"]

            # If only "FullName" is detected but not first/last names, split it
            if not structured_entities["DonorFirstName"] and not structured_entities["DonorLastName"]:
                full_name = structured_entities.get("FullName", "").strip()
                if full_name:
                    first_name, middle_name, last_name = split_name(full_name)
                    structured_entities["DonorFirstName"] = first_name
                    structured_entities["DonorMiddleName"] = middle_name
                    structured_entities["DonorLastName"] = last_name

            # Append the result for each attachment
            results.append({
                "file_name": file_name,
                "structured_entities": structured_entities
            })

        return results

    except Exception as e:
        logging.error(f"Error while processing attachments: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")

