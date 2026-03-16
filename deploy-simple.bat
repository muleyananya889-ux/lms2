@echo off
echo 🚀 Deploying Simple LMS to Vercel

REM Backup current package.json
copy frontend\package.json frontend\package-backup.json

REM Use simple package.json
copy frontend\package-simple.json frontend\package.json

echo 📦 Building simple version...
cd frontend
npm run build

if %errorlevel% neq 0 (
    echo ❌ Build failed
    REM Restore backup
    copy frontend\package-backup.json frontend\package.json
    exit /b 1
)

echo ✅ Build successful

REM Use simple vercel config
copy vercel-simple.json vercel.json

echo 🌐 Deploying to Vercel...
vercel --prod

echo 🎉 Deployment complete!
echo 📱 Your app should be live on Vercel

REM Restore original package.json
copy frontend\package-backup.json frontend\package.json

pause
