#!/bin/bash
# Learn & Earn AI - Quick Start Script

echo "======================================"
echo "  Learn & Earn AI Platform - Startup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Check if streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing required packages..."
    pip install -r requirements.txt
    echo ""
fi

echo "✅ All dependencies are installed"
echo ""

# Check if database exists
if [ ! -f "learn_and_earn_pro.db" ]; then
    echo "⚠️  Warning: Database file not found. A new one will be created."
    echo ""
fi

echo "🚀 Starting Learn & Earn AI Platform..."
echo ""
echo "📱 The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "======================================"
echo ""

# Run the Streamlit app
streamlit run learn-and-earn-app.py
