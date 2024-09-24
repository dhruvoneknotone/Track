# logger.py
"""
Module for system monitoring and logging.
"""

import os
import time
from datetime import datetime, timedelta
import sys
import logging
import socket
import threading
import psutil

def resource_path(relative_path):
    """
    Returns the absolute path to a resource file.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def setup_logging():
    """
    Sets up the logging configuration.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, 
        f"system_monitor_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt"
    )
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_system_startup():
    """
    Logs system startup information.
    """
    computer_name = socket.gethostname()
    logging.info("Computer Name: %s", computer_name)
    print(f"Computer Name: {computer_name}")
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m-%Y")
    logging.info("System Startup: %s", boot_time)
    print(f"System Startup: {boot_time}")

def monitor_system_processes():
    """
    Monitors system processes for a specified duration.
    """
    last_logged_processes = {}
    start_time = datetime.now()
    while datetime.now() - start_time < timedelta(hours=1):
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.info("Process Check: %s", current_time)
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                info = proc.info
                process_key = f"{info['exe']}"
                if process_key not in last_logged_processes or datetime.now() - last_logged_processes[process_key] > timedelta(minutes=10):
                    logging.info("Process: %s", info['exe'])
                    last_logged_processes[process_key] = datetime.now()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(60)

def monitor_system_file_operations():
    """
    Monitors system file operations for a specified duration.
    """
    last_logged_file_operations = {}
    start_time = datetime.now()
    while datetime.now() - start_time < timedelta(hours=1):
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.info("File Operation Check: %s", current_time)
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                info = proc.info
                if info['exe']:
                    file_operation_key = f"{info['exe']}"
                    if file_operation_key not in last_logged_file_operations or datetime.now() - last_logged_file_operations[file_operation_key] > timedelta(minutes=10):
                        logging.info("File Operation: %s", info['exe'])
                        last_logged_file_operations[file_operation_key] = datetime.now()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(60)

def main():
    """
    Main function to execute the system monitoring tasks.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    txt_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    print("Text files found:", txt_files)
    if txt_files:
        print("A txt file already exists in the path. Exiting the program.")
        return 1  # Ensure consistent return

    setup_logging()
    log_system_startup()

    process_thread = threading.Thread(target=monitor_system_processes)
    file_operation_thread = threading.Thread(target=monitor_system_file_operations)

    process_thread.start()
    file_operation_thread.start()

    process_thread.join()
    file_operation_thread.join()

    return 0

if __name__ == "__main__":
    main()