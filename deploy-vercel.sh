#!/bin/bash

echo "🚀 Deploying LMS to Vercel"

# Move to frontend directory
cd frontend

# Rebuild the frontend
echo "📦 Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "🎉 Deployment complete!"
echo "📱 Your app should be live on Vercel"
