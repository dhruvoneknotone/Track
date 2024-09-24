"""
Module for converting text files to PDF format and logging the process.
"""

import os
import shutil
import sys
import logging
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def resource_path(relative_path):
    """
    Returns the absolute path of a resource file.
    It checks if the script is running in a GitHub Actions environment 
    and returns the path accordingly.
    """
    if os.environ.get('GITHUB_ACTIONS'):
        return os.path.join(os.environ.get('GITHUB_WORKSPACE', ''), relative_path)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


def setup_logging():
    """
    Sets up the logging configuration.
    It creates a log directory with the current date and sets up a basic configuration for logging.
    """
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "convert.log")
    logging.basicConfig(
        filename=log_file, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def convert_txt_to_pdf():
    """
    Converts text files to PDF format and moves the original text files to a report directory.
    """
    setup_logging()
    logging.info("Starting conversion process")

    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    report_dir = os.path.join(log_dir, "reports", "text")

    try:
        os.makedirs(report_dir, exist_ok=True)
        logging.info(f"Directories created: {report_dir}")

        txt_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
        if not txt_files:
            logging.warning("No text files found in the directory.")
            return 0

        input_file = os.path.join(log_dir, txt_files[0])
        output_file = txt_files[0].replace('.txt', '.pdf')
        output_file_path = os.path.join(log_dir, output_file)

        logging.info("Converting %s to %s", input_file, output_file_path)  # Updated logging

        pdf = canvas.Canvas(output_file_path, pagesize=letter)
        with open(input_file, 'r', encoding='utf-8') as file:
            y_position = 10 * inch
            for line in file:
                if len(line) > 80:
                    lines = [line[i:i + 60] for i in range(0, len(line), 60)]
                    for line in lines:
                        pdf.drawString(1 * inch, y_position, line.rstrip())
                        y_position -= 0.5 * inch
                else:
                    pdf.drawString(1 * inch, y_position, line.rstrip())
                    y_position -= 0.5 * inch
                if y_position < 1 * inch:
                    pdf.showPage()
                    y_position = 10 * inch
        pdf.save()

        shutil.move(input_file, report_dir)
        logging.info("Moved %s to %s", input_file, report_dir)  # Updated logging

        logging.info("Conversion process completed successfully")
        return 0
    except (OSError, ValueError) as e:  # Catch specific exceptions
        logging.error("An error occurred: %s", str(e))  # Use lazy formatting
        return 1


def main():
    """
    This is the main function of the script.
    It starts the conversion process.
    """
    return convert_txt_to_pdf()


if __name__ == "__main__":
    sys.exit(main())
