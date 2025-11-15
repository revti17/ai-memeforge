# 🎯 Quick Start - Deploy AI MemeForge

## ✅ Deployment Files Created

All necessary deployment files have been created for you:

### Backend Files:
- ✅ `Procfile` - For Railway/Heroku deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `Dockerfile` - Container configuration
- ✅ `railway.json` - Railway-specific config
- ✅ `.gitignore` - Git ignore rules
- ✅ `.dockerignore` - Docker ignore rules
- ✅ Updated `main.py` - Dynamic CORS configuration

### Frontend Files:
- ✅ `vercel.json` - Vercel deployment config
- ✅ `VERCEL_DEPLOY.md` - Vercel setup instructions
- ✅ `.gitignore` - Git ignore rules

### Documentation:
- ✅ `DEPLOYMENT_GUIDE.md` - Complete step-by-step guide
- ✅ `deploy-setup.sh` - Automated git setup script

---

## 🚀 3-Step Deployment Process

### Step 1: Push to GitHub (5 minutes)

```bash
# Navigate to your project
cd "/Users/revtiramantripathi/Desktop/untitled folder 5/aimemeforge"

# Run the setup script
./deploy-setup.sh

# Or manually:
git init
git add .
git commit -m "Initial commit: AI MemeForge v1.0"

# Create repo on GitHub: https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/ai-memeforge.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Railway (10 minutes)

1. **Sign up**: https://railway.app (use GitHub login)
2. **Activate Student Pack**: https://railway.app/account
3. **New Project** → **Deploy from GitHub** → Select `ai-memeforge`
4. **Settings** → Set Root Directory: `backend`
5. **Variables** → Add environment variables (from .env)
6. **Deploy** → Wait 2-5 minutes
7. **Copy Railway URL** (e.g., `https://your-app.up.railway.app`)

### Step 3: Deploy Frontend to Vercel (10 minutes)

1. **Sign up**: https://vercel.com (use GitHub login)
2. **Import Project** → Select `ai-memeforge`
3. **Configure**:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Environment Variables**:
   ```
   VITE_API_BASE=https://your-railway-url.up.railway.app
   VITE_GOOGLE_CLIENT_ID=156698623566-iir6u01ubtmdhlcsgn56p7sig7s76g0r.apps.googleusercontent.com
   ```
5. **Deploy** → Wait 1-3 minutes
6. **Visit your site!** 🎉

---

## 🔧 Important Updates After Deployment

### 1. Update Railway CORS
In Railway → Variables → Update:
```
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
```

### 2. Update Google OAuth
Go to: https://console.cloud.google.com/apis/credentials

Add to **Authorized JavaScript origins**:
```
https://your-vercel-app.vercel.app
```

Add to **Authorized redirect URIs**:
```
https://your-vercel-app.vercel.app
https://your-vercel-app.vercel.app/auth/callback
```

---

## 🌐 Optional: Custom Domain (Namecheap)

### Get Free Domain:
1. Visit: https://nc.me (GitHub Student Pack)
2. Register free .me domain (e.g., `memeforge.me`)

### Configure Vercel:
1. Vercel → Settings → Domains
2. Add your domain
3. Copy DNS records

### Configure Namecheap:
1. Namecheap → Domain → Advanced DNS
2. Add CNAME record:
   - Host: `@`
   - Value: `cname.vercel-dns.com`

### Update URLs:
- Vercel env: `VITE_API_BASE=https://api.memeforge.me`
- Railway CORS: `ALLOWED_ORIGINS=https://memeforge.me`
- Google OAuth: Add `https://memeforge.me`

---

## 📊 What You Get FREE with Student Pack

| Service | Free Tier | Cost |
|---------|-----------|------|
| Railway | $5/month credit | $0 |
| Vercel | Unlimited deployments | $0 |
| MongoDB Atlas | 512MB storage | $0 |
| Namecheap | .me domain (1 year) | $0 |
| **Total** | **Enterprise features** | **$0/month** |

---

## ✅ Testing Your Deployment

Visit your Vercel URL and test:

- [ ] Homepage loads
- [ ] Can browse without login
- [ ] "Generate Meme" shows login modal
- [ ] Can close modal with X button
- [ ] Google login works
- [ ] Can generate memes
- [ ] Dashboard shows user info
- [ ] MongoDB saves data (check Atlas)

---

## 🆘 Troubleshooting

### Issue: CORS Error
**Fix**: Update `ALLOWED_ORIGINS` in Railway with your Vercel URL

### Issue: Google Login Fails
**Fix**: Add Vercel URL to Google OAuth authorized origins

### Issue: Build Fails on Railway
**Fix**: Check logs in Railway dashboard, verify all env vars are set

### Issue: Frontend Shows Wrong API URL
**Fix**: Verify `VITE_API_BASE` in Vercel, redeploy

---

## 📚 Resources

- **Full Guide**: See `DEPLOYMENT_GUIDE.md` for detailed instructions
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Student Pack**: https://education.github.com/pack

---

## 🎉 You're Ready!

Your deployment files are all set up. Just follow the 3 steps above and your app will be live in **~25 minutes**!

**Need help?** Open the `DEPLOYMENT_GUIDE.md` for detailed step-by-step instructions with screenshots and troubleshooting.

---

**Your Live URLs will be:**
- Frontend: `https://your-app.vercel.app` or `https://memeforge.me`
- Backend: `https://your-app.up.railway.app`
- API Docs: `https://your-app.up.railway.app/docs`

**Good luck! 🚀✨**
