# PowerShell script to restart the E-commerce API server
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Restarting E-commerce API Server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Stop any existing Python processes running main.py
Write-Host "Stopping existing server processes..." -ForegroundColor Yellow
$processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*main.py*" -or $_.Path -like "*python*"
}
if ($processes) {
    $processes | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Stopped existing processes" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "✓ No existing processes found" -ForegroundColor Green
}

# Check if Python is available
Write-Host ""
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "✗ Error: main.py not found in current directory" -ForegroundColor Red
    Write-Host "Current directory: $scriptDir" -ForegroundColor Yellow
    exit 1
}

# Start the server
Write-Host ""
Write-Host "Starting server on http://localhost:9000..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start Python server in a new window
Start-Process python -ArgumentList "main.py" -WindowStyle Normal

# Wait a moment for server to start
Start-Sleep -Seconds 3

# Check if server is running
Write-Host ""
Write-Host "Checking server status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Server is running successfully!" -ForegroundColor Green
        Write-Host "✓ API available at: http://localhost:9000" -ForegroundColor Green
        Write-Host "✓ API docs at: http://localhost:9000/docs" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Server may still be starting up..." -ForegroundColor Yellow
    Write-Host "   Check the server window for any errors" -ForegroundColor Yellow
    Write-Host "   Or wait a few seconds and try: http://localhost:9000/health" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Server restart complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

