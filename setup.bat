@echo off
REM OpenDataFitHou Setup Script for Windows
REM This script automates the setup process for the OpenDataFitHou project

echo 🚀 OpenDataFitHou Setup Script
echo ==============================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if Jupyter is working
echo 🧪 Testing Jupyter installation...
jupyter --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Jupyter installation failed
    pause
    exit /b 1
) else (
    echo ✅ Jupyter installed successfully
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Start Jupyter: jupyter notebook
echo 3. Open OverpassApi.ipynb to collect data
echo 4. Open ParseRDF.ipynb to convert to RDF
echo.
echo Happy coding! 🚀

pause