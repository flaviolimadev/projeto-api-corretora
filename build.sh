#!/bin/bash

# Build script for Nixpacks
echo "🚀 Building TradingView API with Nixpacks"

# Install dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Create logs directory
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p export

echo "✅ Build completed successfully!"