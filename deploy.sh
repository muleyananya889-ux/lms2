#!/bin/bash

# LMS Deployment Script
echo "🚀 LMS Application Deployment"
echo "============================="

# Check if we're in production mode
if [ "$1" = "production" ]; then
    echo "🏭 Production Deployment Mode"
    
    # Build frontend
    echo "📦 Building frontend for production..."
    cd frontend
    npm run build
    
    if [ $? -eq 0 ]; then
        echo "✅ Frontend build successful"
    else
        echo "❌ Frontend build failed"
        exit 1
    fi
    
    # Setup production backend
    echo "🔧 Setting up production backend..."
    cd ../backend
    
    # Install production dependencies
    pip install -r requirements.txt
    
    # Set production environment
    export FLASK_ENV=production
    
    echo "✅ Production setup complete"
    echo ""
    echo "📋 To start the production server:"
    echo "   cd backend && python app_production.py"
    echo ""
    echo "🌐 Production URLs:"
    echo "   Frontend: Serve the build/ folder with nginx/apache"
    echo "   Backend: http://localhost:5000"
    
else
    echo "🧪 Development Deployment Mode"
    
    # Check if servers are running
    echo "🔍 Checking server status..."
    
    if curl -s http://localhost:5000/ > /dev/null; then
        echo "✅ Backend is running"
    else
        echo "❌ Backend is not running"
        echo "🔧 Starting backend..."
        cd backend
        python app_sqlite.py &
        cd ..
        sleep 3
    fi
    
    if curl -s http://localhost:3000/ > /dev/null; then
        echo "✅ Frontend is running"
    else
        echo "❌ Frontend is not running"
        echo "🔧 Starting frontend..."
        cd frontend
        npm start &
        cd ..
        sleep 10
    fi
    
    echo ""
    echo "📱 Development URLs:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend: http://localhost:5000"
    echo ""
    echo "🔍 Testing deployment..."
    
    # Test API endpoints
    if curl -s http://localhost:5000/api/courses | grep -q "courses"; then
        echo "✅ API endpoints are working"
    else
        echo "❌ API endpoints are not working"
        echo "🔧 Check backend logs for errors"
    fi
    
    echo ""
    echo "🎉 Deployment check complete!"
fi

echo ""
echo "📚 Common Deployment Issues & Solutions:"
echo "1. Network Error: Check if backend is running on port 5000"
echo "2. CORS Error: Ensure backend allows frontend origin"
echo "3. Database Error: Check if database file exists and is accessible"
echo "4. Build Error: Ensure all dependencies are installed"
echo ""
echo "🔧 For troubleshooting, check:"
echo "   - Backend logs: Python console output"
echo "   - Frontend logs: Browser console (F12)"
echo "   - Network tab: Check API requests in browser dev tools"
