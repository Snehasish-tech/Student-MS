# Vercel Deployment Guide - StudentMS

## ⚠️ Important Setup Required

This Django project requires specific environment variables to be set in Vercel before deployment will work.

### Step 1: Set Environment Variables in Vercel

Go to **Settings → Environment Variables** in your Vercel project dashboard and add:

```
SECRET_KEY = <generate-a-random-secure-key>
DEBUG = False
DATABASE_URL = <your-postgresql-database-url>
ALLOWED_HOSTS = yourdomain.vercel.app,yourdomain.com
```

### Step 2: Set Up a Database

Since Vercel doesn't support persistent SQLite databases, you **MUST** use a cloud database like:

**Option A: PostgreSQL (Recommended)**
- **Neon** (Free tier available): https://neon.tech
- **ElephantSQL** (Free tier available): https://www.elephantsql.com
- **Railway** (Free tier): https://railway.app
- **Heroku PostgreSQL** (paid): https://www.heroku.com

**Option B: Other Databases**
- **MongoDB**: https://www.mongodb.com/cloud/atlas
- **MySQL**: https://www.planetscale.com (Free tier)

### Step 3: Get Your DATABASE_URL

1. Create a PostgreSQL instance on one of the providers above
2. Copy the connection string (DATABASE_URL)
3. Add it to Vercel Environment Variables

Example PostgreSQL URL format:
```
postgresql://user:password@host:5432/dbname
```

### Step 4: Deploy

```bash
git push origin main
```

Your project will automatically build and deploy! Vercel will:
1. Install dependencies from requirements.txt
2. Collect static files
3. Run database migrations (if DATABASE_URL is set)

### Step 5: Verify Deployment

1. Check build logs in Vercel dashboard
2. Visit your deployed URL
3. If you see errors, check the "Logs" tab in Vercel

---

## Troubleshooting

### Error: "django.db.utils.OperationalError: FATAL: Ident authentication failed"
- Database URL might be incorrect
- Check the database provider's connection string format

### Error: "No module named 'student_management_app'"
- Ensure all Python files are committed to git
- Check that `__init__.py` files exist in all directories

### Error: "ALLOWED_HOSTS error"
- Add your exact Vercel domain to ALLOWED_HOSTS environment variable
- Format: `yourdomain.vercel.app` (without https://)

### Static Files Not Loading (404 errors)
- Vercel automatically collects static files during build
- Check `staticfiles/` directory exists
- Verify WhiteNoise middleware is configured (it is by default)

---

## For Production (Custom Domain)

Once you add a custom domain in Vercel:
1. Add it to ALLOWED_HOSTS: `yourdomain.com,www.yourdomain.com`
2. Update any hardcoded URLs in templates
3. Ensure SECURE_SSL_REDIRECT = True if needed

## Support

For Vercel-specific issues: https://vercel.com/docs/frameworks/django
For Django deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
