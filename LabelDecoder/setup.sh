#!/bin/bash

# Label Decoder Setup Script
# This script sets up the complete Label Decoder application

echo "🚀 Setting up Label Decoder Application..."

# Create virtual environment (optional but recommended)
echo "📦 Setting up Python environment..."
cd LabelDecoder

# Install required packages
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Google Gemini API key!"
else
    echo "✅ Environment file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p uploads/thumbnails
mkdir -p database

echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file and add your Google Gemini API key"
echo "2. Get your API key from: https://aistudio.google.com/app/apikey"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "🌐 The app will be available at: http://localhost:8501"
