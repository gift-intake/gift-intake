import extract_msg
from typing import Dict, Any

from pkg_resources import ExtractionError

def extract_msg_details(msg_file_path: str) -> Dict[str, Any]:
    """
    Extract details from an Outlook .msg file.

    Args:
        msg_file_path (str): Path to the .msg file.

    Returns:
        dict: Extracted details such as subject, body, sender, date, and attachments.
    """
    try:
        # Open the .msg file using extract_msg
        msg = extract_msg.Message(msg_file_path)

        # Extract various details from the .msg file
        msg_body = msg.body
        msg_attachments = [att.longFilename for att in msg.attachments]  # List attachment names
       
        return {
            "body": msg_body,
            "attachments": msg_attachments
        }
    except Exception as e:
        # Handle any exceptions that occur during extraction
        raise ExtractionError (f"Failed to extract .msg file details: {str(e)}")
