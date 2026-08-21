@echo off
setlocal enabledelayedexpansion

echo [1/4] Checking virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
)

echo [2/4] Activating venv and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo [3/4] Checking .env file...
if not exist .env (
    echo.
    set /p API_KEY="Paste your OPENAI_API_KEY here and press Enter: "
    echo OPENAI_API_KEY=!API_KEY!> .env
    echo.
    echo Key successfully saved to .env!
    echo.
)

echo [4/4] Starting FastAPI server and opening all 3 tabs...
start http://127.0.0.1:8000/
start http://127.0.0.1:8000/admin
start http://127.0.0.1:8000/docs
uvicorn main:app --reload --port 8000
pause
