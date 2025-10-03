@echo off
REM Quick Start Script for OpenDataFitHou
REM Run this after setup to start working with the project

echo 🚀 OpenDataFitHou Quick Start
echo =============================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment  
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if in correct directory
if not exist "OverpassApi.ipynb" (
    echo ❌ Please run this script from the OpenDataFitHou project directory.
    pause
    exit /b 1
)

echo ✅ Environment activated
echo.
echo Available commands:
echo 1. jupyter notebook    - Start Jupyter Notebook
echo 2. jupyter lab         - Start JupyterLab  
echo 3. python -m notebook  - Alternative Jupyter start
echo.
echo 📓 Available notebooks:
echo • OverpassApi.ipynb   - Data collection from OpenStreetMap
echo • ParseRDF.ipynb      - RDF conversion and processing
echo.

REM Ask user what they want to do
set /p choice="Start Jupyter Notebook? (y/n): "
if /i "%choice%"=="y" (
    echo 🚀 Starting Jupyter Notebook...
    jupyter notebook
) else (
    echo 📝 Virtual environment is active. You can now run jupyter commands manually.
)

pause