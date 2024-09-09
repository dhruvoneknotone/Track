import smtplib  # Import the smtplib module for sending emails
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart for creating email messages
from email.mime.text import MIMEText  # Import MIMEText for creating text parts of email messages
from email.mime.base import MIMEBase  # Import MIMEBase for creating base parts of email messages
from email import encoders  # Import encoders for encoding email attachments
import os  # Import the os module for file operations
import glob  # Import the glob module for finding files
import shutil  # Import the shutil module for file copying and moving
import time  # Import the time module for time-related operations
import sys  # Import the sys module for system-specific parameters and functions
import logging  # Import the logging module for logging events
from datetime import datetime  # Import the datetime module for date and time operations
import socket  # Add this import at the top for getting the hostname
import json  # Import the json module for reading configuration files

def resource_path(relative_path):
    """
    This function returns the absolute path of a resource file.
    It checks if the script is running in a frozen environment (e.g., PyInstaller) and returns the path accordingly.
    """
    try:
        base_path = sys._MEIPASS  # Check if the script is running in a frozen environment
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))  # If not frozen, use the directory of the script
    return os.path.join(base_path, relative_path)  # Join the base path with the relative path of the resource

def setup_logging():
    """
    This function sets up the logging configuration.
    It creates a log directory with the current date and sets up a basic configuration for logging.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')  # Get the current date in dd-mm-yyyy format
    log_dir = resource_path(os.path.join("Logs", current_date))  # Create a log directory with the current date
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    log_file = os.path.join(log_dir, f"mail.log")  # Define the log file path
    logging.basicConfig(filename=log_file, level=logging.INFO,  # Set up basic configuration
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    """
    This function loads the email configuration from a JSON file.
    """
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def send_email(body="Please find the attached report of last 1 hour."):
    """
    This function sends an email with an attachment.
    It sets up logging, constructs the email, attaches a PDF file, and sends the email.
    """
    setup_logging()  # Set up logging
    logging.info("Starting email sending process")

    # Load configuration
    config = load_config(resource_path('config.json'))
    
    fromaddr = config.get("fromaddr")
    toaddr = config.get("toaddr")
    password = config.get("password")
    
    if not all([fromaddr, toaddr, password]):
        logging.error("Email configuration is missing required fields.")
        return 1

    try:
        hostname = socket.gethostname()  # Get the hostname of the PC
        subject = f"{hostname} - Hourly Report"  # Set the subject

        msg = MIMEMultipart()  # Create a message
        msg['From'] = fromaddr  # Set the sender
        msg['To'] = toaddr  # Set the receiver
        msg['Subject'] = subject  # Updated subject

        msg.attach(MIMEText(body, 'plain'))  # Attach the body of the email

        # Search for PDF files in the Logs directory with the current date
        current_date = datetime.now().strftime('%d-%m-%Y')
        log_dir = resource_path(os.path.join("Logs", current_date))
        pdf_files = glob.glob(os.path.join(log_dir, "*.pdf"))
        if len(pdf_files) != 1:
            logging.error("There must be exactly one PDF file in the Logs directory.")
            return 1

        pdf_file = pdf_files[0]
        filename = os.path.basename(pdf_file)
        
        logging.info(f"Attaching file: {filename}")
        with open(pdf_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

        logging.info("Connecting to SMTP server")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromaddr, password)
            
            logging.info("Sending email")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)

        # Move the PDF file to the Logs/reports/pdf folder
        reports_dir = os.path.join(log_dir, "reports", "pdf")  # Updated path
        os.makedirs(reports_dir, exist_ok=True)  # Create the directory if it doesn't exist

        destination_file = os.path.join(reports_dir, filename)
        shutil.move(pdf_file, destination_file)
        logging.info(f"Moved PDF file to: {destination_file}")

        time.sleep(10)
        logging.info("Email sent successfully and PDF file moved to Logs/reports/pdf folder.")
        return 0

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return 1

def main():
    """
    This function is the entry point of the script.
    It calls the send_email function with a default body.
    """
    return send_email("Activity Report")

if __name__ == "__main__":
    sys.exit(main())
