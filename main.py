import os
import time
import logging
from process_email import process_email  # Correct import
from config import email_subject, recipient_email  # Correct import
import imaplib  # Import imaplib
import email
import os
import mimetypes
import json

def run_processes():
    """
    Connects to Gmail, fetches emails, and processes them using process_email.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Replace with your IMAP server
        mail.login("YOUR_GMAIL_USER", "YOUR_GMAIL_PASSWORD")  # Replace with your credentials
        mail.select("inbox")  # Select the inbox

        _, data = mail.search(None, "ALL")  # Fetch all emails
        email_ids = data[0].split()

        for num in email_ids:
            _, data = mail.fetch(num, "(RFC822)")
            email_message = email.message_from_bytes(data[0][1])
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get_content_maintype() == 'text':
                    continue
                filename = part.get_filename()
                if filename:
                    filepath = f"receipts/{filename}"
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    #Process the email using process_email.
                    try:
                        process_email(num, filepath)
                    except Exception as e:
                        logging.exception(f"Error processing email {num}: {e}")


        mail.close()
        mail.logout()

    except Exception as e:
        logging.exception(f"Error during email processing: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename="logs/main_process.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        run_processes()
    except Exception as e:
        logging.exception(f"Main process failed: {e}")