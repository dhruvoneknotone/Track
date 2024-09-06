#!/bin/bash

# Check if this is a GitHub Actions environment
if [ -n "$GITHUB_ACTIONS" ]; then
    echo "Running in GitHub Actions environment. Skipping Python execution."
    exit 0
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    # Note: 'winget' is Windows-specific. You might need to use a different package manager.
    echo "Please install Python manually on your system."
else
    echo "Python is already installed."
fi

# Get the directory of the script
BASE_PATH="$(dirname "$0")"

# Execute Python scripts
python "${BASE_PATH}/req.py" || { echo "Error in req.py"; exit 1; }

while true; do
    # Check if required files exist
    for file in logger.py convert.py mail.py; do
        if [ ! -f "${BASE_PATH}/${file}" ]; then
            echo "Error: ${file} not found in ${BASE_PATH}"
            exit 1
        fi
    done

    python "${BASE_PATH}/logger.py" || { echo "Error in logger.py"; exit 1; }
    python "${BASE_PATH}/convert.py" || { echo "Error in convert.py"; exit 1; }

    sleep 5

    python "${BASE_PATH}/mail.py" || { echo "Error in mail.py"; exit 1; }
done