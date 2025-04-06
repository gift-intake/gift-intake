import extract_msg
from typing import List
from dataclasses import dataclass
from pkg_resources import ExtractionError
from io import BytesIO
from machine_learning.utils.pdf_extractor import extract_text_from_pdf
from machine_learning.utils.docx_extractor import extract_text_from_docx
from machine_learning.utils.image_extractor import extract_text_from_image

@dataclass
class OutlookAttachment:
    file_name: str
    file_contents: str

@dataclass
class OutlookMessage:
    sender: str
    body: str
    attachments: List[OutlookAttachment]

def extract_msg_details(msg_file: BytesIO) -> OutlookMessage:
    """
    Extract details from an Outlook .msg file.

    Args:
        msg_file (str): Path to the .msg file.

    Returns:
        OutlookMessage: Extracted details such as sender, body, and attachments.
    """
    try:
        msg = extract_msg.Message(msg_file)
        attachment_list = []
        
        for attachment in msg.attachments:
            file_name = attachment.name
            file_extension = file_name.split('.')[-1].lower() if '.' in file_name else ""

            if file_extension in ["pdf", "docx", "png", "jpg"]:
                file_data = BytesIO(attachment.data)

                if file_extension == "pdf":
                    extracted_text = extract_text_from_pdf(file_data)
                elif file_extension == "docx":
                    extracted_text = extract_text_from_docx(file_data)
                elif file_extension in ["png", "jpg"]:
                    extracted_text = extract_text_from_image(file_data)
                else:
                    extracted_text = ""

                attachment_obj = OutlookAttachment(
                    file_name=file_name,
                    file_contents=extracted_text.strip().replace("\n", " ").replace("\r", " ")
                )
                
                attachment_list.append(attachment_obj)

        return OutlookMessage(
            sender=msg.sender,
            body=msg.body.strip().replace("\n", " ").replace("\r", " "),
            attachments=attachment_list
        )
    except Exception as e:
        # Handle any exceptions that occur during extraction
        raise ExtractionError(f"Failed to extract .msg file details: {str(e)}")