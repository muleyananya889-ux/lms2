#!/bin/bash

# LMS Application Setup Script
echo "🎓 Learning Management System Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "✅ Environment file created. Please edit backend/.env if needed."
fi

echo "✅ Backend setup complete"

# Setup Frontend
echo ""
echo "🌐 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Start the backend: cd backend && python app_sqlite.py"
echo "2. Start the frontend: cd frontend && npm start"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "🔐 Test Users:"
echo "   Student: jane@example.com / password123"
echo "   Instructor: john@example.com / password123"
echo "   Admin: admin@example.com / password123"
echo ""
echo "📚 For detailed instructions, see README.md"
