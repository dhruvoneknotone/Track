import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import logging
from datetime import datetime
import sys  # Import the sys module


def resource_path(relative_path):
    """
    This function returns the absolute path of a resource file.
    """
    return os.path.join(os.getcwd(), relative_path)


def setup_logging():
    """
    This function sets up the logging configuration.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join("Logs", current_date)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "mail.log")
    logging.basicConfig(
        filename=log_file, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def send_email(subject, body, attachment_path=None):
    """
    This function sends an email with optional attachment.
    """
    setup_logging()
    logging.info("Starting email sending process")

    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            smtp_server = config['smtp_server']
            smtp_port = config['smtp_port']
            smtp_user = config['smtp_user']
            smtp_password = config['smtp_password']
            from_addr = config['from_addr']
            to_addr = config['to_addr']

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            attachment = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as file:
                attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(attachment_path)}'
            )
            msg.attach(attachment)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        logging.info("Email sent successfully")
        return 0
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return 1


def main():
    """
    This is the main function of the script.
    """
    subject = "Daily Report"
    body = "Please find the attached report."
    attachment_path = resource_path("report.pdf")

    return send_email(subject, body, attachment_path)


if __name__ == "__main__":
    sys.exit(main())
