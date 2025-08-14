# Install Python 3.12.5 (x64) directly from python.org, refresh PATH in-session,
# create .venv and activate it. No winget, no Store. Run as Administrator.

$ErrorActionPreference = "Stop"

# 1) Ensure TLS 1.2 and download to TEMP
Write-Host "Downloading Python 3.12.5 x64 from python.org..."
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Version = "3.12.5"
$Installer = "python-$Version-amd64.exe"
$Url = "https://www.python.org/ftp/python/$Version/$Installer"
$Dest = Join-Path $env:TEMP $Installer

Invoke-WebRequest -Uri $Url -OutFile $Dest

if (!(Test-Path $Dest) -or ((Get-Item $Dest).Length -lt 5000000)) {
    throw "Download failed or file too small: $Dest"
}

# 2) Silent install for all users with PATH and launcher
Write-Host "Installing Python silently (all users, add to PATH, include pip and launcher)..."
$Args = @(
    "/quiet",
    "InstallAllUsers=1",
    "PrependPath=1",
    "Include_pip=1",
    "Include_launcher=1",
    "Include_test=0"
) -join " "

Start-Process -FilePath $Dest -ArgumentList $Args -Wait

# 3) Try to locate real python.exe (prefer Program Files over Store alias)
Write-Host "Locating Python installation..."
$Candidates = @()
$Candidates += "C:\Program Files\Python312\python.exe"
$Candidates += Get-ChildItem "C:\Program Files" -Directory -Filter "Python3*" -ErrorAction SilentlyContinue | ForEach-Object {
    Join-Path $_.FullName "python.exe"
}
$PythonExe = $null
foreach ($c in $Candidates) {
    if (Test-Path $c) { $PythonExe = $c; break }
}
if (-not $PythonExe) {
    # Last resort: try where.exe but we will filter out WindowsApps alias
    $whereOut = & where.exe python 2>$null
    if ($whereOut) {
        foreach ($p in $whereOut) {
            if ($p -and ($p -notlike "*WindowsApps*")) {
                $PythonExe = $p
                break
            }
        }
    }
}
if (-not $PythonExe) {
    Write-Host "Python not found in Program Files yet."
    Write-Host "If App Execution Aliases for python/python3 are ON, switch them OFF:"
    Write-Host "Settings > Apps > Advanced app settings > App execution aliases."
    throw "Cannot find a real python.exe"
}

Write-Host "Python executable: $PythonExe"

# 4) Refresh PATH for THIS PowerShell process to include python directory
$PyDir = Split-Path -Parent $PythonExe
$machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$userPath    = [System.Environment]::GetEnvironmentVariable("Path", "User")
$processPath = $PyDir + ";" + $machinePath + ";" + $userPath
[System.Environment]::SetEnvironmentVariable("Path", $processPath, "Process")

# 5) Verify version using the located python.exe (avoid Store alias)
& "$PythonExe" --version

# 6) Create venv at .\.venv using the located python.exe
Write-Host "Creating virtual environment at .\.venv ..."
& "$PythonExe" -m venv .venv

if (!(Test-Path ".\.venv\Scripts\Activate.ps1")) {
    throw "Venv creation failed."
}

# 7) Activate venv in current session
Write-Host "Activating .venv for current session..."
. .\.venv\Scripts\Activate.ps1

# 8) Upgrade pip toolchain and install dev tools
Write-Host "Upgrading pip/setuptools/wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing dev tools: black, flake8, mypy..."
python -m pip install black flake8 mypy

Write-Host ""
Write-Host "DONE."
Write-Host "To activate venv in future sessions: .\.venv\Scripts\Activate.ps1"
