#!/bin/bash

# OpenDataFitHou Setup Script for Unix/macOS
# This script automates the setup process for the OpenDataFitHou project

echo "🚀 OpenDataFitHou Setup Script"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if Jupyter is working
echo "🧪 Testing Jupyter installation..."
if command -v jupyter &> /dev/null; then
    echo "✅ Jupyter installed successfully"
else
    echo "❌ Jupyter installation failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start Jupyter: jupyter notebook"
echo "3. Open OverpassApi.ipynb to collect data"
echo "4. Open ParseRDF.ipynb to convert to RDF"
echo ""
echo "Happy coding! 🚀"