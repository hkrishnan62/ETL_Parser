@echo off
REM ETL Parser Desktop - Windows Installation Script
REM This script installs dependencies and runs the desktop application

echo ================================================================================
echo                   ETL Parser - Desktop Application Setup
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Step 1/3: Checking Python installation...
python --version
echo.

echo Step 2/3: Installing desktop requirements...
python -m pip install --upgrade pip
python -m pip install -r desktop_requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)
echo.

echo Step 3/3: Starting ETL Parser Desktop Application...
echo.
echo The desktop application window will open in a few seconds...
echo.

REM Start the desktop app
python desktop_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    pause
    exit /b 1
)

pause
