import os
import time
from datetime import datetime, timedelta
import psutil
import threading
import sys
import logging
import socket

def resource_path(relative_path):
    """
    This function returns the absolute path of a resource file.
    It checks if the script is running in a frozen environment (e.g., PyInstaller) and returns the path accordingly.
    """
    try:
        base_path = sys._MEIPASS  # Check if the script is running in a frozen environment
    except Exception:
        base_path = os.path.abspath(
            os.path.dirname(__file__)
        )  # If not frozen, use the directory of the script
    return os.path.join(base_path, relative_path)

def setup_logging():
    """
    This function sets up the logging configuration.
    It creates a log directory with the current date and sets up a basic configuration for logging.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')  # Get the current date
    log_dir = os.path.join(
        resource_path("Logs"), current_date
    )
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    log_file = os.path.join(
        log_dir, 
        f"system_monitor_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt"
    )
    logging.basicConfig(
        filename=log_file, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_system_startup():
    """
    This function logs the system startup information.
    It logs the computer name and system startup time.
    """
    computer_name = socket.gethostname()  # Get the computer name
    logging.info(f"Computer Name: {computer_name}")
    print(f"Computer Name: {computer_name}")
    boot_time = datetime.fromtimestamp(
        psutil.boot_time()
    ).strftime("%d-%m-%Y")  # Get the system startup time
    logging.info(f"System Startup: {boot_time}")
    print(f"System Startup: {boot_time}")

def monitor_system_processes(duration):
    """
    This function monitors system processes.
    It logs processes that have started or restarted within the last 10 minutes.
    """
    last_logged_processes = {}
    start_time = datetime.now()
    while datetime.now() - start_time < timedelta(seconds=duration):
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.info(f"Process Check: {current_time}")
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                info = proc.info
                process_key = f"{info['exe']}"
                if process_key not in last_logged_processes or \
                   datetime.now() - last_logged_processes[process_key] > timedelta(minutes=10):
                    logging.info(f"Process: {info['exe']}")
                    last_logged_processes[process_key] = datetime.now()
            except (psutil.NoSuchProcess, 
                    psutil.AccessDenied, 
                    psutil.ZombieProcess):
                pass
        time.sleep(1)  # Check every second

def monitor_system_file_operations(duration):
    """
    This function monitors system file operations.
    It logs file operations that have occurred within the last 10 minutes.
    """
    last_logged_file_operations = {}
    start_time = datetime.now()
    while datetime.now() - start_time < timedelta(seconds=duration):
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.info(f"File Operation Check: {current_time}")
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                info = proc.info
                if info['exe']:
                    file_operation_key = f"{info['exe']}"
                    if file_operation_key not in last_logged_file_operations or \
                       datetime.now() - last_logged_file_operations[file_operation_key] > timedelta(minutes=10):
                        logging.info(f"File Operation: {info['exe']}")
                        last_logged_file_operations[file_operation_key] = datetime.now()
            except (psutil.NoSuchProcess, 
                    psutil.AccessDenied, 
                    psutil.ZombieProcess):
                pass
        time.sleep(1)  # Check every second

def main():
    """
    This is the main function of the script.
    It sets up logging, logs system startup, and starts threads for process and file operation monitoring.
    """
    duration = 10  # Set duration to 10 seconds

    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(
        resource_path("Logs"), current_date
    )
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    txt_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    print("Text files found:", txt_files)  # Debug print
    if txt_files:
        print("A txt file already exists in the path. Exiting the program.")
    else:
        try:
            setup_logging()
            log_system_startup()

            process_thread = threading.Thread(
                target=monitor_system_processes,
                args=(duration,)
            )
            file_operation_thread = threading.Thread(
                target=monitor_system_file_operations,
                args=(duration,)
            )

            process_thread.start()
            file_operation_thread.start()

            process_thread.join()
            file_operation_thread.join()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return 1
        return 0

if __name__ == "__main__":
    main()  # Call the main function to start the program