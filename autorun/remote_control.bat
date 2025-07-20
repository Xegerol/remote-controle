@echo off
echo Starting Telegram PC Controller...

REM Change to bot directory
cd /d "%~dp0\.."

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run in tray mode
python main.py --tray

REM If error occurred, wait for user input
if errorlevel 1 (
    echo.
    echo Error occurred. Press any key to exit...
    pause >nul
)
