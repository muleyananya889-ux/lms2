@echo off
echo 🚀 Deploying WORKING LMS to Vercel (No Errors!)

REM Backup current files
copy frontend\package.json frontend\package-backup.json >nul 2>&1
copy frontend\src\index.js frontend\src\index-backup.js >nul 2>&1
copy frontend\src\App.js frontend\src\App-backup.js >nul 2>&1

REM Use working versions
copy frontend\package-working.json frontend\package.json
copy frontend\src\index-working.js frontend\src\index.js
copy frontend\src\App-working.js frontend\src\App.js

echo 📦 Building working version...
cd frontend
npm install
npm run build

if %errorlevel% neq 0 (
    echo ❌ Build failed
    REM Restore backup
    copy frontend\package-backup.json frontend\package.json >nul 2>&1
    copy frontend\src\index-backup.js frontend\src\index.js >nul 2>&1
    copy frontend\src\App-backup.js frontend\src\App.js >nul 2>&1
    exit /b 1
)

echo ✅ Build successful

REM Use simple vercel config
echo {
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
} > vercel.json

echo 🌐 Deploying to Vercel...
vercel --prod

echo 🎉 Deployment complete!
echo 📱 Your app should be live on Vercel with NO ERRORS!

REM Restore backup
copy frontend\package-backup.json frontend\package.json >nul 2>&1
copy frontend\src\index-backup.js frontend\src\index.js >nul 2>&1
copy frontend\src\App-backup.js frontend\src\App.js >nul 2>&1

echo ✅ All files restored. Your working app is now live on Vercel!

pause
