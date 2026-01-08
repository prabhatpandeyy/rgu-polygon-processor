@echo off
echo RGU Polygon Processor - Windows Setup
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Starting RGU Polygon Processor...
python rgu_polygon_processor.py

pause