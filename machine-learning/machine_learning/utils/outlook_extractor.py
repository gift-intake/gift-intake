import re
import extract_msg
from typing import List, Tuple
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
    sender_name: str
    sender_email: str
    body: str
    attachments: List[OutlookAttachment]

def parse_sender(sender_string: str) -> Tuple[str, str]:
    """
    Parse a sender string in the format "Name <email>" into separate name and email components.
    
    Args:
        sender_string (str): The sender string to parse.
        
    Returns:
        Tuple[str, str]: A tuple containing (sender_name, sender_email).
    """
    # Use regex to extract email from within angle brackets
    email_match = re.search(r'<([^<>]+)>', sender_string)
    
    if email_match:
        sender_email = email_match.group(1).strip()
        # Remove the email part from the original string to get the name
        sender_name = sender_string.replace(f'<{sender_email}>', '').strip()
    else:
        # If no angle brackets, assume the whole thing is an email
        sender_email = sender_string.strip()
        sender_name = ""
    
    return sender_name, sender_email

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

        sender_name, sender_email = parse_sender(msg.sender)

        return OutlookMessage(
            sender_name=sender_name,
            sender_email=sender_email,
            body=msg.body.strip().replace("\n", " ").replace("\r", " "),
            attachments=attachment_list
        )
    except Exception as e:
        # Handle any exceptions that occur during extraction
        raise ExtractionError(f"Failed to extract .msg file details: {str(e)}")