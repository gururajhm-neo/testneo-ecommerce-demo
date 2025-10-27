# Start All Services
Write-Host "🚀 Starting E-Commerce Services..." -ForegroundColor Green

# Kill any existing processes
Write-Host "`nStopping existing services..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# Start Backend
Write-Host "`nStarting Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "main.py" -WindowStyle Minimized

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend  
Write-Host "Starting Frontend (React)..." -ForegroundColor Cyan
Set-Location frontend
Start-Process -FilePath "npm" -ArgumentList "run dev" -WindowStyle Minimized
Set-Location ..

Write-Host "`n✅ Services started!" -ForegroundColor Green
Write-Host "`nAccess your application:" -ForegroundColor Yellow
Write-Host "  🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  🔧 Backend API: http://localhost:9000" -ForegroundColor Cyan
Write-Host "  📚 API Docs: http://localhost:9000/docs" -ForegroundColor Cyan
Write-Host "`nAdmin Login:" -ForegroundColor Yellow
Write-Host "  Email: admin@ecommerce.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White

Write-Host "`nPress Ctrl+C or close this window to stop services" -ForegroundColor Gray

