import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob
import shutil
import time
import sys
import logging
from datetime import datetime
import socket
import json

def resource_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

def setup_logging():
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = resource_path(os.path.join("Logs", current_date))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"mail.log")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    fromaddr = os.environ.get('EMAIL_FROM')
    toaddr = os.environ.get('EMAIL_TO')
    password = os.environ.get('EMAIL_PASSWORD')
    return {'fromaddr': fromaddr, 'toaddr': toaddr, 'password': password}

def send_email(body="Please find the attached report of last 1 hour."):
    setup_logging()
    logging.info("Starting email sending process")

    config = load_config()
    
    fromaddr = config.get("fromaddr")
    toaddr = config.get("toaddr")
    password = config.get("password")
    
    if not all([fromaddr, toaddr, password]):
        logging.error("Email configuration is missing required fields.")
        return 1

    try:
        hostname = socket.gethostname()
        subject = f"{hostname} - Hourly Report"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

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

        reports_dir = os.path.join(log_dir, "reports", "pdf")
        os.makedirs(reports_dir, exist_ok=True)

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
    return send_email("Activity Report")

if __name__ == "__main__":
    sys.exit(main())
