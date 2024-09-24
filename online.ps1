function Install-Winget {
    if (-not (winget --version | Out-Null)) {
        Write-Host "winget is not installed. Installing winget..."
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-AppInstaller
    } else {
        Write-Host "winget is already installed."
    }
}

function Install-Python {
    if (-not (python --version | Out-Null)) {
        Write-Host "Python is not installed. Installing Python..."
        winget install --id Python.Python
    } else {
        Write-Host "Python is already installed."
    }
}

function Install-Pip {
    if (-not (pip --version | Out-Null)) {
        Write-Host "pip is not installed. Installing pip..."
        python -m ensurepip
    } else {
        Write-Host "pip is already installed."
    }
}

function Initialize-Track {
    $BASE_PATH = "C:/Track"
    if (-not (Test-Path $BASE_PATH)) {
        New-Item -ItemType Directory -Path $BASE_PATH -Force
    }

    if (-not (Test-Path "$BASE_PATH/.git")) {
        git clone https://github.com/dhruvoneknotone/Track.git "$BASE_PATH" -q
        Write-Host "Repository cloned successfully."
    } else {
        Set-Location $BASE_PATH
        git pull -q
        Write-Host "Repository updated successfully."
        Set-Location -
    }
}

function Configure-Startup {
    $STARTUP_FOLDER = "C:\Users\DeLL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    $BAT_FILE = "$BASE_PATH\start_main.bat"
    if (-not (Get-ChildItem -Path $STARTUP_FOLDER -Filter "start_main.bat" -ErrorAction SilentlyContinue)) {
        Set-Content -Path $BAT_FILE -Value "cd $BASE_PATH`nmain.bat" -Force
        Move-Item -Path $BAT_FILE -Destination $STARTUP_FOLDER -Force
        Start-Process -FilePath "$STARTUP_FOLDER\start_main.bat"
    }
}

Install-Winget
Install-Python
Install-Pip
Initialize-Track
Configure-Startup