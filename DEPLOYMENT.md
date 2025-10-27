# Deployment Guide for TestNeo E-Commerce Demo

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   VERCEL        │ ───────▶│   RAILWAY       │
│   (Frontend)    │  API    │   (Backend API) │
│   React UI     │  calls  │   FastAPI       │
│   - Static      │         │   SQLite DB     │
└─────────────────┘         └─────────────────┘
```

## Deployment Steps

### 1. Railway (Backend API)

#### Option A: GitHub Integration
1. Push to GitHub:
```bash
git remote add origin <your-github-repo-url>
git push -u origin master
```

2. In Railway Dashboard:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python

#### Option B: Manual Deployment
1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login:
```bash
railway login
```

3. Initialize:
```bash
cd testneo-ecommerce-demo
railway init
```

4. Set Environment Variables:
```bash
railway variables set DATABASE_URL=sqlite:///./ecommerce.db
```

5. Deploy:
```bash
railway up
```

### 2. Vercel (Frontend - Optional)

If you're building a React/Next.js frontend:

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

## Environment Variables

### Railway (.env or dashboard)

```env
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database

The API uses SQLite by default. The database is created automatically on first run with sample data.

To create sample data manually:
```bash
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
python create_test_data.py  # If you create this helper script
```

## Testing Locally Before Deployment

1. Start the API:
```bash
cd testneo-ecommerce-demo
python main.py
```

2. Test endpoints:
```bash
curl http://localhost:9000/health
```

## Post-Deployment

1. Get the Railway URL: `https://your-app.railway.app`
2. Update frontend API URL to point to Railway
3. Test all endpoints from Railway docs: `https://your-app.railway.app/docs`

## Monitoring

- Railway dashboard: Monitor logs, metrics, and deployments
- API Health: `/health` endpoint for uptime checks
- Swagger Docs: `/docs` for interactive API testing

## Scaling

Railway automatically handles:
- Restarts
- Logs
- Metrics
- SSL/HTTPS

## Costs

- Railway: Free tier includes $5 credit/month
- Vercel: Free tier for hobby projects
- Total: $0/month for small demos

## Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs

