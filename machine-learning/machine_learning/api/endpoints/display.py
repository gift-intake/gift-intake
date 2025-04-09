import logging
from fastapi import APIRouter, HTTPException, UploadFile
from machine_learning.schemas.inference_request import InferenceRequest
from machine_learning.schemas.inference_response import (
    InferenceResponseData,
)
from machine_learning.utils.outlook_extractor import extract_msg_details
from machine_learning.models.gliner_model import extract_entities
from machine_learning.utils.pdf_extractor import extract_text_from_pdf
from machine_learning.utils.docx_extractor import extract_text_from_docx
from machine_learning.utils.image_extractor import extract_text_from_image

from io import BytesIO

router = APIRouter()


@router.post("/extract-file")
async def extract_file(file: UploadFile) -> InferenceResponseData:
    """
    Process the uploaded file and extracts entities using GLiNER.
    """
    try:
        if not (
            file.filename.endswith(".pdf")
            or file.filename.endswith(".docx")
            or file.filename.endswith(".png")
            or file.filename.endswith(".jpg")
        ):
            raise HTTPException(
                status_code=400,
                detail="Only .pdf, .docx, .png, and .jpg files are supported.",
            )

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="File is empty.")

        file_name = file.filename
        file_extension = file_name.split(".")[-1].lower() if "." in file_name else ""

        if file_extension == "pdf":
            extracted_text = extract_text_from_pdf(BytesIO(file_bytes))
        elif file_extension == "docx":
            extracted_text = extract_text_from_docx(BytesIO(file_bytes))
        elif file_extension in ["png", "jpg"]:
            extracted_text = extract_text_from_image(BytesIO(file_bytes))
        else:
            extracted_text = ""

        extracted_entities = extract_entities(
            extracted_text.strip().replace("\n", " ").replace("\r", " ")
        )

        return InferenceResponseData(
            file_name=file_name,
            file_contents=extracted_text,
            entities=extracted_entities.results,
        )
    except Exception as e:
        logging.error(f"Error while processing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@router.post("/extract-text")
async def extract_text(request: InferenceRequest) -> InferenceResponseData:
    """
    Process the uploaded file and extracts entities using GLiNER.
    """
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is empty.")

        extracted_text = request.text

        extracted_entities = extract_entities(
            extracted_text.strip().replace("\n", " ").replace("\r", " ")
        )

        return InferenceResponseData(
            file_name="",
            file_contents=extracted_text,
            entities=extracted_entities.results,
        )
    except Exception as e:
        logging.error(f"Error while processing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")
