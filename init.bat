@echo off
echo Initializing Cryptolab setup...

:: --- Backend Setup ---
echo Setting up Python Virtual Environment...
cd /d "%~dp0backend"
python -m venv .venv

:: Use 'call' to ensure the script returns here after activation
call .venv\Scripts\activate

echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install --only-binary=:all: pydantic
pip install -r requirements.txt

:: --- Frontend Setup (Optional but recommended) ---
echo Checking Frontend dependencies...
cd /d "%~dp0frontend"
:: Uncomment the next line if you want to auto-install npm packages
:: call npm install

:: --- Start Servers ---
echo Starting all servers...

:: Start Backend in a new window
start "Backend Server" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

:: Start Frontend in a new window
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Setup Complete. Backend and Frontend are launching...
pause