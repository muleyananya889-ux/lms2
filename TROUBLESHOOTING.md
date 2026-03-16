# LMS Application Troubleshooting Guide

## Common Deployment Issues & Solutions

### 1. "Failed to fetch courses" / "Network Error"

**Symptoms**: 
- Frontend shows "Failed to fetch courses" or "API Error: Network Error"
- Browser console shows network connection errors

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:5000/api/courses

# If not running, start backend:
cd backend
python app_sqlite.py

# Check frontend proxy configuration
# Ensure frontend/src/services/api.js uses:
const API_BASE_URL = '/api';
```

### 2. CORS Errors

**Symptoms**:
- Browser console shows CORS policy errors
- API requests blocked by cross-origin policy

**Solutions**:
```python
# In backend app.py, ensure CORS is properly configured:
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
```

### 3. Database Connection Errors

**Symptoms**:
- Backend shows database connection errors
- API returns 500 errors

**Solutions**:
```bash
# Check if database file exists
ls -la backend/*.db

# If not exists, initialize database:
cd backend
python app_sqlite.py  # This will auto-initialize the database
```

### 4. Build Errors

**Symptoms**:
- Frontend fails to build
- npm install errors
- Module not found errors

**Solutions**:
```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# For production build:
npm run build
```

### 5. Port Conflicts

**Symptoms**:
- Servers fail to start
- "Port already in use" errors

**Solutions**:
```bash
# Check what's using ports 3000 and 5000
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# Kill processes using ports
taskkill /F /PID <PID>

# Or use different ports:
# Frontend: PORT=3001 npm start
# Backend: python app_sqlite.py --port=5001
```

### 6. Environment Variable Issues

**Symptoms**:
- Authentication fails
- JWT errors
- Configuration errors

**Solutions**:
```bash
# Create environment file
cd backend
cp .env.example .env

# Edit .env with proper values:
# SECRET_KEY=your-secret-key
# JWT_SECRET_KEY=your-jwt-secret
```

## Quick Fix Script

```bash
# Complete reset and restart
echo "🔄 Resetting LMS Application..."

# Kill existing processes
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

# Wait for processes to stop
timeout /t 3 /nobreak >nul

# Start backend
cd backend
start /b python app_sqlite.py
cd ..

# Wait for backend to start
timeout /t 5 /nobreak >nul

# Start frontend
cd frontend
start /b npm start
cd ..

# Wait for frontend to start
timeout /t 10 /nobreak >nul

# Test API
curl -s http://localhost:5000/api/courses >nul
if %errorlevel% equ 0 (
    echo ✅ Application is running successfully
    echo 🌐 Frontend: http://localhost:3000
    echo 🔧 Backend: http://localhost:5000
) else (
    echo ❌ Application failed to start
    echo 🔍 Check console for errors
)

echo 🎉 Reset complete!
```

## Production Deployment

### For Production (Vercel, Netlify, etc.)

1. **Frontend Build**:
```bash
cd frontend
npm run build
# Upload the build/ folder to your hosting provider
```

2. **Backend Deployment**:
```bash
cd backend
pip install -r requirements.txt
python app_production.py
# Use a WSGI server like Gunicorn for production
```

3. **Environment Variables**:
- Set `REACT_APP_API_URL` to your backend URL
- Configure CORS origins for your domain
- Set production database URL

### Docker Deployment

```dockerfile
# Dockerfile for backend
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app_production.py"]
```

## Support

If you're still experiencing issues:

1. Check browser console (F12) for JavaScript errors
2. Check backend terminal for Python errors
3. Verify both servers are running on correct ports
4. Ensure database file exists and is accessible
5. Check network connectivity between frontend and backend

## Test Users

- **Student**: jane@example.com / password123
- **Instructor**: john@example.com / password123
- **Admin**: admin@example.com / password123
