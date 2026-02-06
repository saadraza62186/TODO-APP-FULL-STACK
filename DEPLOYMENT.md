# Vercel Deployment Guide

## Backend Deployment to Vercel

### Prerequisites
- Vercel account
- PostgreSQL database (Neon recommended)
- GitHub repository with your code

### Step 1: Prepare Your Backend

The following files are already configured for Vercel:
- ✅ `index.py` - Vercel handler
- ✅ `vercel.json` - Vercel configuration
- ✅ CORS configured to allow all origins

### Step 2: Push Code to GitHub

```bash
git add .
git commit -m "Configure backend for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. **Root Directory**: Select `backend` folder
5. Click "Deploy"

### Step 4: Configure Environment Variables

After deployment, go to your project settings:

1. Navigate to **Settings** → **Environment Variables**
2. Add the following variables:

| Variable | Value | Example |
|----------|-------|---------|
| `DATABASE_URL` | Your PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | Secret key (min 32 chars) | `your-secret-key-here-min-32-chars` |
| `CORS_ORIGINS` | `*` (or specific origins) | `*` |
| `DEBUG` | `False` | `False` |

3. Click "Save"
4. **Redeploy** your application (Deployments tab → Redeploy)

### Step 5: Test Your Backend

After redeployment, test your backend:

```bash
# Test health endpoint
curl https://your-backend-url.vercel.app/health

# Test root endpoint
curl https://your-backend-url.vercel.app/
```

You should see successful responses with no CORS errors.

### Step 6: Update Frontend Configuration

Create or update `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

Then restart your frontend development server:

```bash
cd frontend
npm run dev
```

## Troubleshooting

### CORS Errors
- Make sure `CORS_ORIGINS` is set to `*` in Vercel environment variables
- Redeploy after changing environment variables
- Clear browser cache and restart dev server

### Function Invocation Failed
- Check if all environment variables are set correctly
- Verify `DATABASE_URL` is accessible from Vercel
- Check deployment logs in Vercel dashboard

### Database Connection Errors
- Ensure database allows connections from Vercel IPs
- For Neon: Enable "Pooled connection" in connection string
- Verify connection string format includes `?sslmode=require`

### Import Errors
- Make sure all dependencies are in `requirements.txt`
- Check Python version compatibility (Vercel uses Python 3.9 by default)
- Add `runtime.txt` with `python-3.11` if needed

## Common Issues

**Issue**: "Module not found" errors
**Solution**: Ensure all imports in `index.py` and `main.py` are correct

**Issue**: Database tables not created
**Solution**: Run migration script or manually create tables in your database

**Issue**: JWT token errors
**Solution**: Verify `BETTER_AUTH_SECRET` matches between frontend and backend

## Production Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Database**: Use connection pooling for better performance
3. **CORS**: In production, replace `*` with specific frontend URLs
4. **Monitoring**: Enable Vercel Analytics and Error Tracking
5. **Logs**: Check Vercel logs regularly for errors

## Links

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Neon Serverless Postgres](https://neon.tech/docs)
