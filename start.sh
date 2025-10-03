#!/bin/bash

# Quick Start Script for OpenDataFitHou
# Run this after setup to start working with the project

echo "🚀 OpenDataFitHou Quick Start"
echo "============================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if in correct directory
if [ ! -f "OverpassApi.ipynb" ]; then
    echo "❌ Please run this script from the OpenDataFitHou project directory."
    exit 1
fi

echo "✅ Environment activated"
echo ""
echo "Available commands:"
echo "1. jupyter notebook    - Start Jupyter Notebook"
echo "2. jupyter lab         - Start JupyterLab"
echo "3. python -m notebook  - Alternative Jupyter start"
echo ""
echo "📓 Available notebooks:"
echo "• OverpassApi.ipynb   - Data collection from OpenStreetMap"
echo "• ParseRDF.ipynb      - RDF conversion and processing"
echo ""

# Ask user what they want to do
read -p "Start Jupyter Notebook? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting Jupyter Notebook..."
    jupyter notebook
fi