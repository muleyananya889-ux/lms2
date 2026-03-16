# Vercel Deployment Guide for LMS

## 🚀 Quick Vercel Deployment

### Option 1: Frontend Only (Recommended for Vercel)

1. **Deploy Frontend to Vercel**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend only
cd frontend
vercel --prod
```

2. **Deploy Backend Separately** (Recommended):
   - Use Render, Heroku, or Railway for backend
   - Update `REACT_APP_API_URL` environment variable in Vercel

### Option 2: Full Stack with Serverless Functions

1. **Prepare for Deployment**:
```bash
# Install dependencies for serverless functions
cd api
npm install

# Build frontend
cd ../frontend
npm run build
```

2. **Deploy to Vercel**:
```bash
# From root directory
vercel --prod
```

## 🔧 Configuration Files

### vercel.json (Root)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/package.json",
      "use": "@vercel/node"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.js"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

### Environment Variables (Vercel Dashboard)
- `REACT_APP_API_URL`: `/api` (for serverless) or your backend URL
- `NODE_ENV`: `production`

## 🌐 Deployment Options

### Option A: Vercel Frontend + Render Backend

1. **Frontend (Vercel)**:
   - Deploy only `frontend/` folder to Vercel
   - Set `REACT_APP_API_URL` to your Render backend URL

2. **Backend (Render)**:
   - Deploy `backend/` to Render
   - Use PostgreSQL database on Render

### Option B: Vercel Full Stack

1. **Use Serverless Functions**:
   - Backend runs as Vercel serverless functions
   - SQLite database (limited to 100MB)

2. **Limitations**:
   - Database persistence limited
   - Cold starts may affect performance
   - File system access restricted

## 🔍 Common Vercel Issues & Solutions

### Issue 1: "Cannot find module"
**Solution**: Ensure all dependencies are in `api/package.json`

### Issue 2: CORS errors
**Solution**: Add CORS middleware to serverless functions

### Issue 3: Database connection errors
**Solution**: Use external database service (Render, Supabase)

### Issue 4: Build failures
**Solution**: Check `vercel.json` configuration

## 📋 Pre-Deployment Checklist

- [ ] Frontend builds successfully (`npm run build`)
- [ ] API endpoints work locally
- [ ] Environment variables set
- [ ] `vercel.json` configured
- [ ] Serverless functions tested

## 🚀 Deploy Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Check deployment
vercel ls
```

## 🌍 Production URLs

After deployment:
- Frontend: `https://your-app.vercel.app`
- API: `https://your-app.vercel.app/api`

## 🔧 Troubleshooting

### Check Logs
```bash
vercel logs
```

### Check Function Logs
```bash
vercel logs --filter=function
```

### Redeploy
```bash
vercel --prod --force
```

## 📚 Alternative Deployment Platforms

If Vercel doesn't work well for your full-stack app:

1. **Netlify**: Frontend only
2. **Render**: Full stack with PostgreSQL
3. **Railway**: Full stack with database
4. **Heroku**: Full stack (paid tier)
5. **DigitalOcean**: Full stack with Droplets

## 🎯 Recommended Setup

For best results with LMS:

1. **Vercel**: Frontend only
2. **Render**: Backend with PostgreSQL
3. **Environment**: Set `REACT_APP_API_URL` to Render URL

This gives you:
- ✅ Fast frontend deployment
- ✅ Persistent database
- ✅ Scalable backend
- ✅ Better performance
