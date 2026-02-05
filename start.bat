@echo off
REM Learn & Earn AI - Quick Start Script for Windows

echo ======================================
echo   Learn & Earn AI Platform - Startup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Install dependencies
echo Installing required packages...
pip install -r requirements.txt
echo.

echo [OK] All dependencies are installed
echo.

REM Check if database exists
if not exist "learn_and_earn_pro.db" (
    echo [!] Warning: Database file not found. A new one will be created.
    echo.
)

echo Starting Learn ^& Earn AI Platform...
echo.
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
echo ======================================
echo.

REM Run the Streamlit app
streamlit run learn-and-earn-app.py

pause
