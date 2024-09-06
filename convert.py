from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os
import shutil
import sys
import logging
import datetime


def resource_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)


def setup_logging():
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "convert.log")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def convert_txt_to_pdf():
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

        logging.info(f"Converting {input_file} to {output_file_path}")

        pdf = canvas.Canvas(output_file_path, pagesize=letter)
        with open(input_file, 'r', encoding='utf-8') as file:
            y_position = 10 * inch
            for line in file:
                if len(line) > 80:
                    lines = [line[i:i+60] for i in range(0, len(line), 60)]
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
        logging.info(f"Moved {input_file} to {report_dir}")

        logging.info("Conversion process completed successfully")
        return 0
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return 1


def main():
    return convert_txt_to_pdf()


if __name__ == "__main__":
    sys.exit(main())