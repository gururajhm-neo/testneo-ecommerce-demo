# Quick verification script for Test Components
Write-Host "Verifying Test Components setup..." -ForegroundColor Cyan
Write-Host ""

# Check if files exist
$files = @(
    "frontend/src/components/DataTable.jsx",
    "frontend/src/components/MultiStepForm.jsx",
    "frontend/src/components/FileUpload.jsx",
    "frontend/src/pages/TestComponents.jsx"
)

Write-Host "Checking component files..." -ForegroundColor Yellow
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $file NOT FOUND" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Checking AdminLayout.jsx..." -ForegroundColor Yellow
$adminLayout = Get-Content "frontend/src/components/admin/AdminLayout.jsx" -Raw
if ($adminLayout -match "Test Components") {
    Write-Host "✓ 'Test Components' found in AdminLayout.jsx" -ForegroundColor Green
} else {
    Write-Host "✗ 'Test Components' NOT found in AdminLayout.jsx" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking App.jsx routes..." -ForegroundColor Yellow
$appJsx = Get-Content "frontend/src/App.jsx" -Raw
if ($appJsx -match "/admin/test-components") {
    Write-Host "✓ Route '/admin/test-components' found in App.jsx" -ForegroundColor Green
} else {
    Write-Host "✗ Route '/admin/test-components' NOT found in App.jsx" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Access URLs:" -ForegroundColor Cyan
Write-Host "  Direct: http://localhost:3001/admin/test-components" -ForegroundColor White
Write-Host "  Admin Panel: http://localhost:3001/admin" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If menu item doesn't show, try:" -ForegroundColor Yellow
Write-Host "  1. Hard refresh: Ctrl+Shift+R" -ForegroundColor White
Write-Host "  2. Clear browser cache" -ForegroundColor White
Write-Host "  3. Logout and login again" -ForegroundColor White
Write-Host "  4. Use direct URL above" -ForegroundColor White

