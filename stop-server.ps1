# PowerShell script to stop the E-commerce API server
Write-Host "Stopping E-commerce API Server..." -ForegroundColor Yellow

# Stop any Python processes
$processes = Get-Process python -ErrorAction SilentlyContinue
if ($processes) {
    $processes | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Stopped all Python processes" -ForegroundColor Green
} else {
    Write-Host "✓ No Python processes found" -ForegroundColor Green
}

Write-Host "Server stopped." -ForegroundColor Cyan

