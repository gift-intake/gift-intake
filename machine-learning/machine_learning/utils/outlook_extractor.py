from exchangelib import Credentials, Account, FileAttachment, DELEGATE
from exchangelib.errors import UnauthorizedError, AutoDiscoverFailed
from fastapi import HTTPException
import logging
from enum import Enum

# Enum to handle folder options more cleanly
class Folder(Enum):
    INBOX = "inbox"
    SENT = "sent"

def fetch_outlook_attachments(username: str, password: str, folder: Folder = Folder.INBOX):
    """
    Fetch attachments from the specified folder in the Outlook account.
    """
    try:
        # Setup credentials and account access
        credentials = Credentials(username=username, password=password)
        account = Account(primary_smtp_address=username, credentials=credentials, autodiscover=True, access_type=DELEGATE)

        # Fetch the specified folder
        if folder == Folder.INBOX:
            folder = account.inbox
        elif folder == Folder.SENT:
            folder = account.sent
        else:
            raise HTTPException(status_code=400, detail="Invalid folder. Use 'inbox' or 'sent'.")

        # Fetch unread emails directly
        emails = folder.filter(is_read=False).order_by('-datetime_received')
        if not emails:
            return {"message": "No unread emails found."}

        attachments = []
        for email in emails:
            for attachment in email.attachments:
                if isinstance(attachment, FileAttachment):
                    attachments.append({
                        "file_data": attachment.content,  # Binary data
                        "file_name": attachment.name,
                        "file_type": attachment.content_type
                    })

            # Mark email as read after processing attachments
            email.is_read = True
            email.save()

        if not attachments:
            return {"message": "No attachments found in unread emails."}

        # Log the number of attachments fetched
        logging.info(f"Fetched {len(attachments)} attachments from {folder.value}.")

        return attachments

    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Invalid Outlook credentials. Please check your username and password.")
    except AutoDiscoverFailed:
        raise HTTPException(status_code=500, detail="Autodiscover failed. Check your email configuration.")
    except Exception as e:
        logging.exception("Error fetching Outlook attachments")  # Logs the actual error for debugging
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
