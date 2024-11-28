# process_email.py (Modified)
import os
import time
import logging
from utils import process_receipt, save_extracted_data, send_email_notification, download_attachment
from config import TRUCAP_BASE_URL, email_subject, recipient_email

def process_email(email_id, email_message):
    """Processes an email message, including attachments."""
    try:
        # Download the attachment
        receipt_path = download_attachment(email_message, "receipt.pdf", "receipts")  # Changed to 'receipt.pdf'
        if receipt_path:
            extracted_data = process_receipt(receipt_path)
            if extracted_data:
                validated_data = validate_extracted_data(extracted_data)
                if validated_data:
                    save_extracted_data(extracted_data, receipt_path)
                    send_email_notification(extracted_data, email_id, email_subject, recipient_email)
                    logging.info(f"Email {email_id} processed successfully.")
                else:
                    logging.warning(f"Invalid data from email {email_id}.")
            else:
                logging.error(f"No data extracted from email {email_id}.")

        else:
          logging.warning(f"No attachment found in email {email_id}.")
    except Exception as e:
        logging.exception(f"Error processing email {email_id}: {e}")