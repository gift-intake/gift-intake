import logging
import extract_msg
import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
from gliner import GLiNER
from decimal import Decimal

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

        # Extract email contents directly from BytesIO
        msg = extract_msg.Message(BytesIO(file_bytes))
        msg_body = msg.body
        
        # Log raw email body to verify extraction
        logging.info(f"Raw email body extracted: {msg_body}")

        # If extraction failed, raise an error
        if not msg_body:
            logging.warning(f"No text extracted from file: {file_name}")
            raise HTTPException(status_code=400, detail=f"No text extracted from file: {file_name}")

        # Run entity extraction with GLiNER on the extracted body text
        entities = model.predict_entities(msg_body, ENTITY_LABELS)

        # Use lists to store multiple values
        structured_entities = {label: [] for label in ENTITY_LABELS}

        # Collect extracted values
        for entity in entities:
            if entity["label"] in structured_entities:
                structured_entities[entity["label"]].append(entity["text"])

        # Log extracted entities for debugging purposes
        logging.info(f"Extracted entities: {structured_entities}")

        # Handle Organization Name extraction more carefully
        organization_names = set()

        # Updated regex to capture common organization names, including Computer Science
        potential_orgs = re.findall(
            r"(?:Department of|Faculty of|School of|College of|University of|Computer Science)\s+[A-Za-z\s]+(?:\s+Department|\s+College|\s+University)?", 
            msg_body
        )
        organization_names.update(potential_orgs)

        # If no organization names are found, set the default value
        structured_entities["OrganizationName"] = list(organization_names) if organization_names else []

        # Handle Donor First and Last Name properly
        first_names = []
        last_names = []
        middle_names = []
        for name in structured_entities["DonorFirstName"]:
            name_parts = name.split()  # Split by spaces to get first and last names
            if len(name_parts) == 1:
                first_names.append(name_parts[0])
            elif len(name_parts) == 2:
                first_names.append(name_parts[0])
                last_names.append(name_parts[1])
            elif len(name_parts) > 2:
                first_names.append(name_parts[0])
                last_names.append(name_parts[-1])
                middle_names.append(" ".join(name_parts[1:-1]))  # Middle name is the parts in between

        structured_entities["DonorFirstName"] = ", ".join(list(set(first_names))) if first_names else ""
        structured_entities["DonorLastName"] = ", ".join(list(set(last_names))) if last_names else ""
        structured_entities["DonorMiddleName"] = ", ".join(list(set(middle_names))) if middle_names else ""

        # Process Gift Amounts (ensure correct extraction and sum)
        gift_amounts = [
            Decimal(re.sub(r"[^\d.]", "", amount))  # Remove "$" and ","
            for amount in structured_entities["GiftAmount"]
            if re.sub(r"[^\d.]", "", amount).replace('.', '', 1).isdigit()
        ]


        # Convert lists with a single item to a string for cleaner JSON output
        for key in structured_entities:
            if isinstance(structured_entities[key], list) and len(structured_entities[key]) == 1:
                structured_entities[key] = structured_entities[key][0]

        # Remove keys with empty lists or empty strings
        structured_entities = {key: value for key, value in structured_entities.items() if value}

        return structured_entities

    except Exception as e:
        logging.error(f"Error while processing .msg file: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")
