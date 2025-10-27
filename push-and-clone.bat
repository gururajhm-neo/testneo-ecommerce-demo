@echo off
echo ============================================
echo TestNeo E-Commerce Demo - Push and Clone
echo ============================================
echo.

REM Step 1: Add files to git
echo [1/5] Adding files to git...
git add .
git commit -m "Add setup documentation"
if %errorlevel% neq 0 (
    echo No new changes to commit
)

REM Step 2: Add remote if not exists
echo [2/5] Adding GitHub remote...
git remote remove origin 2>nul
git remote add origin https://github.com/gururajhm-neo/testneo-ecommerce-demo.git
echo Remote added successfully!

REM Step 3: Rename branch to main
echo [3/5] Renaming branch to main...
git branch -M main

REM Step 4: Push to GitHub
echo [4/5] Pushing to GitHub...
echo Please make sure you created the repository at:
echo https://github.com/new
echo Repository name: testneo-ecommerce-demo
echo.
pause
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not push to GitHub
    echo.
    echo Please:
    echo 1. Create the repository at https://github.com/new
    echo 2. Name it: testneo-ecommerce-demo
    echo 3. Make it Public
    echo 4. Run this script again
    pause
    exit /b 1
)

echo.
echo [5/5] SUCCESS! Pushed to GitHub.
echo.
echo Repository URL: https://github.com/gururajhm-neo/testneo-ecommerce-demo
echo.
echo Now run the clone script to get it in testneoendtoend folder!
echo.

pause

