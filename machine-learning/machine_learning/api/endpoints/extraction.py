import logging
from fastapi import APIRouter, HTTPException, UploadFile
from io import BytesIO

from machine_learning.models.model_results import ParsedEntity
from machine_learning.schemas.inference_response import InferenceResponse, InferenceResponseData
from machine_learning.utils.outlook_extractor import extract_msg_details
from machine_learning.models.gliner_model import extract_entities

router = APIRouter()

@router.post("/extract")
async def process_email(file: UploadFile) -> InferenceResponse: 
    """
    Process the uploaded .msg file with attachments and extract entities using GLiNER.
    """
    try:
        if not file.filename.endswith(".msg"):
            raise HTTPException(status_code=400, detail="Only .msg files are supported.")

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="File is empty.")
        
        outlook_file = extract_msg_details(BytesIO(file_bytes))
        
        if not outlook_file:
            raise HTTPException(status_code=400, detail="No text extracted from file.")

        results = []

        extracted_entities = extract_entities(outlook_file.body)

        outlook_data = InferenceResponseData(
                file_name=file.filename,
                file_contents=outlook_file.body,
                entities=extracted_entities.results
        )

        if outlook_file.sender_name:
          sender_name_exists = any(entity.entity == "Person" and entity.value == outlook_file.sender_name 
                                          for entity in outlook_data.entities)
          if not sender_name_exists:
              outlook_data.entities.append(ParsedEntity(entity="Person", value=outlook_file.sender_name))
              
        if outlook_file.sender_email:
            sender_email_exists = any(entity.entity == "Email" and entity.value == outlook_file.sender_email 
                                     for entity in outlook_data.entities)
            if not sender_email_exists:
                outlook_data.entities.append(ParsedEntity(entity="Email", value=outlook_file.sender_email))
        
        results.append(outlook_data)

        for attachment in outlook_file.attachments:
            attachment_entities = extract_entities(attachment.file_contents)
            results.append(
                InferenceResponseData(
                    file_name=attachment.file_name,
                    file_contents=attachment.file_contents,
                    entities=attachment_entities.results
                )
            )

        return InferenceResponse(results=results)
    except Exception as e:
        logging.error(f"Error while processing .msg file: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")