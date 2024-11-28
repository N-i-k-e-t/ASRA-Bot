# ReceiptAce: Automated Receipt Processing

## TEAM AI TASK FORCE (ATF) or ASARA BOT
by Niket Patil

## Email niketpatil1624@gmail.com and your team ID is Data-230326

This project automates the processing of food and petrol bill receipts from emails using Datamatics TruBot, TruCap+, and Python.

**Demo Video:**

To see a demonstration of ReceiptAce in action, please watch the following video:

[https://ai.invideo.io/watch/BsD8kfR8g0v](https://ai.invideo.io/watch/BsD8kfR8g0v)

## Features

* Automated email ingestion and attachment download (TruBot).
* Data extraction using TruCap+ API.
* Data validation and error handling.
* Google Forms submission.
* Email notifications.
* (Optional) Real-time processing using Google Cloud Functions/Redis.
* (Optional) LLM-assisted template enhancement, validation, and anomaly detection.


## Requirements

* Datamatics TruBot Designer (version X.X.X)
* Datamatics TruCap+ (version X.X.X)
* Python 3.9+
* Libraries:  `imaplib`, `requests`, `google-forms-submit`, `smtplib`, `PyYAML` (or your chosen config library),  `trubot-api` (if available), etc.
* (Optional) Google Cloud Project (for real-time processing)
* (Optional) Redis (for real-time queuing)
* (Optional) OpenAI API Key (for LLM integration)


## Installation

1. Clone the repository: `git clone https://github.com/<your-username>/ReceiptAce.git`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Configure TruBot: (Provide specific instructions for setting up the TruBot workflow, including email credentials, attachment save path, Python script path, etc.)
4. Configure TruCap+: Obtain API credentials (SID and Token) and store them securely (e.g., environment variables).
5. Configure Google Forms: Create a Google Form and obtain the necessary IDs or API details for submission. Update the `config.yaml` with Google Forms details.
6. (Optional) Configure Real-time Processing: Set up Google Cloud Functions, Redis, and Gmail push notifications (if used).
7. Configure LLM (if used):  Obtain and store API key for your chosen LLM.



## Usage

1.  **Prepare Test Data:** Place sample receipt files (PDFs and images) in the `data/receipts` directory.  (Optional) You can include raw email files (.eml format) in `data/test_emails` for more realistic testing.
2.  **Update Configuration:**  Modify `config.yaml` with your specific settings (e.g., email credentials, API keys, Google Form URL, etc.).
3.  **Run TruBot Workflow:** Open and run the `ReceiptProcessingWorkflow.xaml` in TruBot Designer. 
4.  **(For real-time):** Start the real-time monitoring script `main.py`.
5.  **Testing with Python Directly:** To test the Python scripts independently, you can call `process_email.py` with the path to a receipt file as an argument:  `python src/process_email.py data/receipts/receipt1.pdf`.


## Project Structure

* `trubot/`: TruBot workflow files.
* `src/`: Python source code.
* `data/`: Sample receipts and test email data.
* `config/`: Configuration files.
* `tests/`: Unit and integration tests.


## Contributing



## License

(Specify your chosen license, e.g., MIT License)
