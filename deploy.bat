@echo off
REM LMS Deployment Script for Windows
echo 🚀 LMS Application Deployment
echo =============================

if "%1"=="production" (
    echo 🏭 Production Deployment Mode
    
    REM Build frontend
    echo 📦 Building frontend for production...
    cd frontend
    npm run build
    
    if %errorlevel% neq 0 (
        echo ❌ Frontend build failed
        exit /b 1
    )
    
    echo ✅ Frontend build successful
    
    REM Setup production backend
    echo 🔧 Setting up production backend...
    cd ..\backend
    
    REM Install production dependencies
    pip install -r requirements.txt
    
    REM Set production environment
    set FLASK_ENV=production
    
    echo ✅ Production setup complete
    echo.
    echo 📋 To start the production server:
    echo    cd backend ^&^& python app_production.py
    echo.
    echo 🌐 Production URLs:
    echo    Frontend: Serve the build/ folder with nginx/apache
    echo    Backend: http://localhost:5000
    
) else (
    echo 🧪 Development Deployment Mode
    
    REM Check if servers are running
    echo 🔍 Checking server status...
    
    curl -s http://localhost:5000/ >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Backend is running
    ) else (
        echo ❌ Backend is not running
        echo 🔧 Starting backend...
        cd backend
        start /b python app_sqlite.py
        cd ..
        timeout /t 3 /nobreak >nul
    )
    
    curl -s http://localhost:3000/ >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Frontend is running
    ) else (
        echo ❌ Frontend is not running
        echo 🔧 Starting frontend...
        cd frontend
        start /b npm start
        cd ..
        timeout /t 10 /nobreak >nul
    )
    
    echo.
    echo 📱 Development URLs:
    echo    Frontend: http://localhost:3000
    echo    Backend: http://localhost:5000
    echo.
    echo 🔍 Testing deployment...
    
    REM Test API endpoints
    curl -s http://localhost:5000/api/courses | findstr "courses" >nul
    if %errorlevel% equ 0 (
        echo ✅ API endpoints are working
    ) else (
        echo ❌ API endpoints are not working
        echo 🔧 Check backend logs for errors
    )
    
    echo.
    echo 🎉 Deployment check complete!
)

echo.
echo 📚 Common Deployment Issues ^& Solutions:
echo 1. Network Error: Check if backend is running on port 5000
echo 2. CORS Error: Ensure backend allows frontend origin
echo 3. Database Error: Check if database file exists and is accessible
echo 4. Build Error: Ensure all dependencies are installed
echo.
echo 🔧 For troubleshooting, check:
echo    - Backend logs: Python console output
echo    - Frontend logs: Browser console (F12)
echo    - Network tab: Check API requests in browser dev tools

pause
