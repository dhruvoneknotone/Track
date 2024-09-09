# Check if Python is installed
python --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed. Installing Python..."
    winget install --id Python.Python
} else {
    Write-Host "Python is already installed."
}

# Check if pip is installed
pip --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip is not installed. Installing pip..."
    python -m ensurepip
} else {
    Write-Host "pip is already installed."
}

# Set the base path to C:/Track
$BASE_PATH = "C:/Track"

# Create the base path if it does not exist
if (-not (Test-Path $BASE_PATH)) {
    New-Item -ItemType Directory -Path $BASE_PATH -Force
}

# Check if the GitHub repository already exists in the base path
if (-not (Test-Path "$BASE_PATH/.git")) {
    # Clone the GitHub repository into the base path
    git clone https://github.com/dhruvoneknotone/Track.git "$BASE_PATH" -q
    Write-Host "Repository cloned successfully."
} else {
    # If the repository exists, pull the latest changes
    Set-Location $BASE_PATH
    git pull -q
    Write-Host "Repository updated successfully."
    Set-Location -
}

# Check if any file exists in the startup folder
$STARTUP_FOLDER = "C:\Users\DeLL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
$BAT_FILE = "$BASE_PATH\start_main.bat"
if (-not (Get-ChildItem -Path $STARTUP_FOLDER -Filter "start_main.bat" -ErrorAction SilentlyContinue)) {
    # Create a batch file to start main.bat in the base path
    Set-Content -Path $BAT_FILE -Value "cd $BASE_PATH`nmain.bat" -Force

    # Move the batch file to the startup folder and start it
    if (Test-Path "$STARTUP_FOLDER\start_main.bat") {
        Remove-Item -Path "$STARTUP_FOLDER\start_main.bat" -Force
    }
    Move-Item -Path $BAT_FILE -Destination $STARTUP_FOLDER -Force
    Start-Process "start_main.bat"
}