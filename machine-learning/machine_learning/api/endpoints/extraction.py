import logging
from fastapi import APIRouter, HTTPException, UploadFile
from io import BytesIO

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
        results.append(
            InferenceResponseData(
                file_name=file.filename,
                file_contents=outlook_file.body,
                entities=extracted_entities.results
            )
        )

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