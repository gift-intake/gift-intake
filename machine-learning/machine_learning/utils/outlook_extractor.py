import extract_msg
from typing import Dict, Any

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
        msg_subject = msg.subject
        msg_body = msg.body
        msg_sender = msg.sender
        msg_date = msg.date
        msg_attachments = [att.longFilename for att in msg.attachments]  # List attachment names

        return {
            "subject": msg_subject,
            "sender": msg_sender,
            "date": msg_date,
            "body": msg_body,
            "attachments": msg_attachments
        }
    except Exception as e:
        return {"error": f"Failed to extract .msg file details: {str(e)}"}
