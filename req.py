import subprocess  # Import the subprocess module for running system commands
import time  # Import the time module for time-related operations
import os  # Import the os module for operating system-specific functionalities
import sys  # Import the sys module for system-specific parameters and functions

def run_command(command):
    """
    This function runs a system command and checks for errors.
    It uses subprocess.check_call to execute the command and catches CalledProcessError to handle errors.
    """
    try:
        subprocess.check_call(command, shell=True)  # Execute the command and check for errors
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")  # Print the error message with the error code
        sys.exit(e.returncode)  # Exit the program with the error code

def upgrade_pip():
    """
    This function upgrades pip to the latest version.
    It prints a message indicating the upgrade process and calls run_command to execute the upgrade.
    """
    print("Upgrading pip...")  # Print a message indicating the upgrade process
    run_command("python -m pip install --upgrade pip")  # Call run_command to execute the upgrade

def install_requirements():
    """
    This function installs required packages.
    It defines a list of required packages, prints a message indicating the installation process,
    and calls run_command to install each package.
    """
    required_packages = [
        "psutil",  # Package for system and process utilities
        "reportlab",  # Package for generating PDF documents
        # Add the names of the packages you want to install here
    ]

    print("Installing required packages...")  # Print a message indicating the installation process
    for package in required_packages:
        run_command(f"python -m pip install --upgrade {package}")  # Call run_command to install each package

def main():
    """
    This is the main function of the script.
    It calls the functions to upgrade pip and install required packages.
    """
    upgrade_pip()  # Call the function to upgrade pip
    install_requirements()  # Call the function to install required packages
    print("Done!")  # Print a message indicating the completion of the process

if __name__ == "__main__":
    main()  # Call the main function to start the script
