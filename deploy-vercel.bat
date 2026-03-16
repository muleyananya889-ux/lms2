@echo off
echo 🚀 Deploying LMS to Vercel

REM Move to frontend directory
cd frontend

REM Rebuild the frontend
echo 📦 Building frontend...
npm run build

if %errorlevel% neq 0 (
    echo ❌ Build failed
    exit /b 1
)

echo ✅ Build successful

REM Deploy to Vercel
echo 🌐 Deploying to Vercel...
vercel --prod

echo 🎉 Deployment complete!
echo 📱 Your app should be live on Vercel

pause
