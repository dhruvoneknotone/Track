import os
import time
from datetime import datetime, timedelta
import psutil
import threading
import sys
import logging


def resource_path(relative_path):
    """
    This function returns the absolute path of a resource file.
    It checks if the script is running in a GitHub Actions environment 
    and returns the path accordingly.
    """
    if os.environ.get('GITHUB_ACTIONS'):
        return os.path.join(os.environ.get('GITHUB_WORKSPACE', ''), relative_path)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


def setup_logging():
    """
    This function sets up the logging configuration.
    It creates a log directory with the current date and sets up a basic configuration for logging.
    """
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"system_monitor_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt"
    )
    logging.basicConfig(
        filename=log_file, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def log_system_startup():
    """
    This function logs the system startup information.
    It logs the runner name and workflow run ID for GitHub Actions.
    """
    runner_name = os.environ.get('RUNNER_NAME', 'Unknown Runner')
    logging.info(f"Runner Name: {runner_name}")
    print(f"Runner Name: {runner_name}")

    run_id = os.environ.get('GITHUB_RUN_ID', 'Unknown Run ID')
    logging.info(f"Workflow Run ID: {run_id}")
    print(f"Workflow Run ID: {run_id}")


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
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                info = proc.info
                process_key = f"{info['name']}"
                if process_key not in last_logged_processes or \
                   datetime.now() - last_logged_processes[process_key] > timedelta(minutes=10):
                    logging.info(f"Process: {info['name']}")
                    last_logged_processes[process_key] = datetime.now()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(1)


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
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                info = proc.info
                if info['name']:
                    file_operation_key = f"{info['name']}"
                    if file_operation_key not in last_logged_file_operations or \
                       datetime.now() - last_logged_file_operations[file_operation_key] > timedelta(minutes=10):
                        logging.info(f"File Operation: {info['name']}")
                        last_logged_file_operations[file_operation_key] = datetime.now()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(1)


def main():
    """
    This is the main function of the script.
    It sets up logging, logs system startup, and starts threads for process and file operation monitoring.
    """
    duration = 10  # Set duration to 10 seconds

    current_date = datetime.now().strftime('%d-%m-%Y')
    log_dir = os.path.join(resource_path("Logs"), current_date)
    os.makedirs(log_dir, exist_ok=True)
    txt_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    print("Text files found:", txt_files)
    if txt_files:
        print("A txt file already exists in the path. Exiting the program.")
    else:
        try:
            setup_logging()
            log_system_startup()

            process_thread = threading.Thread(target=monitor_system_processes, args=(duration,))
            file_operation_thread = threading.Thread(target=monitor_system_file_operations, args=(duration,))

            process_thread.start()
            file_operation_thread.start()

            process_thread.join()
            file_operation_thread.join()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(main())

