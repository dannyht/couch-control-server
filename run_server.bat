@echo off
REM Navigate to the folder containing your Flask app
cd /d "%~dp0"

REM Run the Flask server with Python 3.13
python.exe remote.py

pause
