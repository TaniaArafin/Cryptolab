@echo off
SET PROJECT_ROOT=%~dp0

echo Launching Cryptolab Ecosystem...

:: 1. Launch Backend Server
echo Starting Backend (Uvicorn)...
start "Backend: FastAPI" cmd /k "cd /d %PROJECT_ROOT%backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

:: 2. Launch Frontend Server
echo Starting Frontend (Vite/Vue)...
start "Frontend: Vue" cmd /k "cd /d %PROJECT_ROOT%frontend && npm run dev"

echo.
echo --------------------------------------------------
echo Services are starting in separate windows.
echo Backend: http://127.0.0.1:8000
echo Frontend: Check the second terminal for local URL.
echo --------------------------------------------------
pause