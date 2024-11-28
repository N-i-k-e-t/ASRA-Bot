import json
import os
import re
import time
import logging
import requests
import imaplib
import email
import mimetypes
from config import TRUCAP_BASE_URL, email_subject, recipient_email  # Import config variables

# Replace with your TruCap+ API details
TRUCAP_BASE_URL = "YOUR_TRUCAP_API_BASE_URL"  # Crucial: Replace with your actual URL
TRUCAP_AUTH_HEADER = "YOUR_TRUCAP_AUTH_HEADER" #  Crucial: Replace with your actual authentication header

def download_attachment(email_message, filename, save_path):
    """Downloads an email attachment."""
    try:
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_maintype() == 'text':
                continue
            if part.get_filename():
                filepath = os.path.join(save_path, part.get_filename())
                logging.info(f"Saving attachment to {filepath}")
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                return filepath
        return None  # No attachment found
    except Exception as e:
        logging.exception(f"Error downloading attachment: {e}")
        return None


def extract_data_from_json(json_data):
    try:
        # Parse JSON (error handling is important)
        data = json.loads(json_data)

        #  Extract data from the parsed JSON
        vendor = data.get("vendor")
        date = data.get("date")
        total = data.get("total")
        items = data.get("items")
        return {
            "vendor": vendor,
            "date": date,
            "total": total,
            "items": items
        }

    except (json.JSONDecodeError, TypeError) as e:
        logging.error(f"Error extracting data from JSON: {e}")
        return None  # Or raise an exception


def validate_extracted_data(data):
    # (Validate fields like date format, numeric values etc.)
    # Example: Validate date format:
    import datetime
    try:
        datetime.datetime.strptime(data['date'], '%Y-%m-%d')  # Example date format. Change as needed
        return True
    except ValueError:
        logging.error(f"Invalid date format in data: {data}")
        return False
    
def process_receipt(receipt_path):
    """Processes a single receipt using TruCap+."""
    if not os.path.exists(receipt_path):
        logging.error(f"File not found: {receipt_path}")
        return None

    try:
        files = {'file': open(receipt_path, 'rb')}
        # crucial - add the authorization header
        headers = {'Authorization': TRUCAP_AUTH_HEADER}
        response = requests.post(f"{TRUCAP_BASE_URL}/process", files=files, headers=headers)  
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        extracted_data = response.json()
        return extracted_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error processing receipt {receipt_path}: {e}")
        return None  # Or handle the error appropriately
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON response from TruCap+: {e}, Response: {response.text}")  # Log the response
        return None
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return None
    finally:
        # Important: Close the file, even on errors
        try:
            open(receipt_path, 'rb').close()
        except Exception as e:
            logging.error(f"Error closing file {receipt_path}: {e}")



def save_extracted_data(data, receipt_path):
    """Saves the extracted data to the data directory."""
    if data is None:  # Check for None
        logging.warning(f"Skipping save; no data to save for {receipt_path}")
        return

    dirname = os.path.dirname(receipt_path)
    filename = os.path.basename(receipt_path).replace(".pdf", "_data.json")
    filepath = os.path.join(dirname.replace("receipts", "data"), filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"Extracted data saved to {filepath}")


def send_email_notification(data, email_id, email_subject="Receipt Summary", recipient_email="recipient@example.com"):  # Added defaults
    """Sends email notification using a placeholder."""
    try:
        logging.info(f"Sending email notification for {email_id} with data: {data}")
        # Replace this with your actual email sending code using smtplib or similar
        #  Crucial - Add recipient email address!
        print(f"Sending email to {recipient_email} with subject: {email_subject} and data: {data}")  # Print for demonstration
    except Exception as e:
        logging.exception(f"Error sending email notification for {email_id}: {e}")
    