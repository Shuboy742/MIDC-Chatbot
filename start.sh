#!/bin/bash
echo "🏭 Starting MIDC Land Bank RAG Chatbot..."
echo "=========================================="

# Activate virtual environment
if [ -d "rag_env" ]; then
    echo "Activating Python 3.11 virtual environment..."
    source rag_env/bin/activate
else
    echo "Creating new Python 3.11 virtual environment..."
    python3.11 -m venv rag_env
    source rag_env/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo "Starting FastAPI server with Python $(python --version)..."
python main.py