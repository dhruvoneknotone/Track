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
    New-Item -ItemType Directory -Path $BASE_PATH
}

# Clone the GitHub repository into the base path
git clone https://github.com/dhruvoneknotone/Track.git "$BASE_PATH/Track"

Write-Host "Repository cloned successfully."