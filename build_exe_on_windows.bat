@echo off
echo RGU Polygon Processor - Windows EXE Builder
echo ===========================================
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
pip install pyinstaller

echo.
echo Building Windows executable...
pyinstaller --onefile --windowed --name RGU_Polygon_Processor rgu_polygon_processor.py

echo.
echo =====================================
echo BUILD COMPLETE!
echo =====================================
echo Your .exe file is in the 'dist' folder
echo File: dist\RGU_Polygon_Processor.exe
echo.
echo You can now share this .exe file with others!
echo.

pause