from reportlab.pdfgen import canvas  # Importing the canvas module from reportlab.pdfgen for PDF generation
from reportlab.lib.pagesizes import letter  # Importing the letter page size from reportlab.lib.pagesizes for PDF layout
from reportlab.lib.units import inch  # Importing the inch unit from reportlab.lib.units for PDF layout
import os  # Importing the os module for file operations
import shutil  # Importing the shutil module for file copying and moving
import sys  # Importing the sys module for system-specific parameters and functions
import logging  # Importing the logging module for logging events
import datetime  # Importing the datetime module for date and time operations

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
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')  # Get the current date
    log_dir = os.path.join(resource_path("Logs"), current_date)  # Create a log directory with the current date
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    log_file = os.path.join(log_dir, "convert.log")  # Define the log file path
    logging.basicConfig(filename=log_file, level=logging.INFO,  # Set up basic configuration
                        format='%(asctime)s - %(levelname)s - %(message)s')

def convert_txt_to_pdf():
    """
    This function converts a text file to a PDF file.
    It sets up logging, finds the first text file in the log directory, converts it to PDF, and moves the text file to a reports directory.
    """
    setup_logging()  # Set up logging
    logging.info("Starting conversion process")  # Log the start of the conversion process

    current_date = datetime.datetime.now().strftime('%d-%m-%Y')  # Get the current date
    log_dir = os.path.join(resource_path("Logs"), current_date)  # Create a log directory with the current date
    report_dir = os.path.join(log_dir, "reports", "text")  # Define the reports directory

    try:
        os.makedirs(report_dir, exist_ok=True)  # Ensure the reports directory exists
        logging.info(f"Directories created: {report_dir}")  # Log the creation of directories

        txt_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]  # Find all text files in the log directory
        if not txt_files:
            logging.warning("No text files found in the directory.")  # Log a warning if no text files are found
            return 0  # Exit the function if no text files are found

        input_file = os.path.join(log_dir, txt_files[0])  # Get the path of the first text file
        output_file = txt_files[0].replace('.txt', '.pdf')  # Define the output PDF file name
        output_file_path = os.path.join(log_dir, output_file)  # Define the output PDF file path

        logging.info(f"Converting {input_file} to {output_file_path}")  # Log the conversion process

        pdf = canvas.Canvas(output_file_path, pagesize=letter)  # Create a PDF canvas with letter size
        with open(input_file, 'r', encoding='utf-8') as file:
            y_position = 10*inch  # Initial y position for text
            for line in file:
                if len(line) > 80:
                    lines = [line[i:i+60] for i in range(0, len(line), 60)]  # Split long lines into multiple lines
                    for line in lines:
                        pdf.drawString(1*inch, y_position, line.rstrip())  # Draw the string on the PDF
                        y_position -= 0.5*inch  # Move down for the next line
                else:
                    pdf.drawString(1*inch, y_position, line.rstrip())  # Draw the string on the PDF
                    y_position -= 0.5*inch  # Move down for the next line
                if y_position < 1*inch:
                    pdf.showPage()  # Start a new page if the current page is full
                    y_position = 10*inch  # Reset y position for the new page
        pdf.save()  # Save the PDF

        # Move the text file to the reports directory
        shutil.move(input_file, report_dir)  # Move the text file
        logging.info(f"Moved {input_file} to {report_dir}")  # Log the move operation

        logging.info("Conversion process completed successfully")  # Log the successful completion of the conversion process
        return 0  # Return success
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")  # Log any errors that occur during the conversion process
        return 1  # Return failure

def main():
    """
    This is the main function that calls the convert_txt_to_pdf function.
    """
    return convert_txt_to_pdf()  # Call the convert_txt_to_pdf function

if __name__ == "__main__":
    sys.exit(main())  # Call the main function and exit the program