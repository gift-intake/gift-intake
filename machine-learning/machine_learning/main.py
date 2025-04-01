import os
import logging
import magic  # Library to check MIME type
from fastapi import FastAPI, HTTPException, File, UploadFile
from io import BytesIO
import extract_msg
from gliner import GLiNER

# Initialize FastAPI app
app = FastAPI()

# Initialize GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define entity labels for GLiNER extraction
ENTITY_LABELS = [
    "ConstituentID", "ConstituentType", "GiftAmount", "DonorFirstName",
    "DonorMiddleName", "DonorLastName", "OrganizationName", "GiftIntakeType",
    "DonorAddress", "DonorCity", "DonorProvince", "DonorCountry", "DonorPhone",
    "DonorEmail", "GiftCurrency", "GiftDate", "PaymentMethod"
]

@app.post("/extract/outlook/")
async def extract_outlook_attachments_route(file: UploadFile = File(...)):
    """
    Extract text and entities from a .msg email file.
    """
    try:
        # Validate file type
        file_name = file.filename
        if not file_name.endswith(".msg"):
            raise HTTPException(status_code=400, detail="Only .msg files are supported.")

        # Read file bytes
        file_bytes = await file.read()
        
        # Validate MIME type
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_bytes)
        if file_type != 'application/vnd.ms-outlook':
            raise HTTPException(status_code=400, detail="Invalid .msg file format.")

        # Extract email contents directly from BytesIO
        msg = extract_msg.Message(BytesIO(file_bytes))
        msg_body = msg.body
        # If extraction failed, raise an error
        if not msg_body:
            logging.warning(f"No text extracted from file: {file_name}")
            raise HTTPException(status_code=400, detail=f"No text extracted from file: {file_name}")

        # Run entity extraction with GLiNER on the extracted body text
        entities = model.predict_entities(msg_body, ENTITY_LABELS)
        structured_entities = {label: "" for label in ENTITY_LABELS}

        # Populate extracted values into the structured entity dictionary
        for entity in entities:
            structured_entities[entity["label"]] = entity["text"]

        return structured_entities
        

    except Exception as e:
        logging.error(f"Error while processing .msg file: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")
