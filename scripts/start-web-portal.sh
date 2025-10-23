#!/bin/bash
# Quick start script for NextCore AI Cloud web portal

set -e

echo "🚀 Starting NextCore AI Cloud Web Portal Setup"
echo "=============================================="
echo ""

# Navigate to web portal directory
cd "$(dirname "$0")/../apps/web-portal"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "   Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"
echo ""

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local from template..."
    cp .env.example .env.local
    echo "✅ .env.local created"
    echo ""
fi

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend is not responding on http://localhost:8000"
    echo "   Make sure Docker services are running:"
    echo "   cd /home/nick/work/NextCore-AI-Cloud && docker-compose up -d"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Starting development server..."
echo "----------------------------------------------"
echo "📱 Web Portal: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------------"
echo ""

# Start development server
npm run dev
