#!/bin/bash

# Always run from the script's own directory
cd "$(dirname "$0")"

echo ""
echo "🎯 AI Marketing Team — Setup & Launch"
echo "======================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Install it from https://python.org then re-run this."
    exit 1
fi
echo "✅ Python found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt -q
echo "✅ Dependencies ready"

# Check API key
if grep -q "your_api_key_here" .env 2>/dev/null || [ ! -f .env ]; then
    echo ""
    echo "⚠️  Almost there! You need to add your Anthropic API key."
    echo ""
    echo "   1. Open this file:  $(pwd)/.env"
    echo "   2. Replace 'your_api_key_here' with your key from https://console.anthropic.com"
    echo "   3. Run this script again: bash run.sh"
    echo ""
    exit 1
fi
echo "✅ API key found"

# Launch
echo ""
echo "🚀 Launching your marketing team..."
echo "   Your browser will open automatically."
echo "   Press Ctrl+C to stop."
echo ""
python3 -m streamlit run app.py
