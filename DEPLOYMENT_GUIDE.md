# 🚀 AI MemeForge - Complete Deployment Guide

## 📦 What You'll Need (All FREE with GitHub Student Pack!)

1. **GitHub Account** (with Student Pack activated)
2. **Railway Account** (Free $5/month credit with Student Pack)
3. **Vercel Account** (Unlimited free deployments)
4. **Namecheap** (Free .me domain for 1 year)
5. **MongoDB Atlas** (Already configured! ✅)

---

## 🎯 Deployment Architecture

```
Frontend (Vercel) ──────> Backend (Railway) ──────> MongoDB Atlas
     ↓                          ↓
Your Domain              API Endpoint
```

---

## 📋 Step 1: Push to GitHub

### 1.1 Initialize Git Repository

```bash
cd "/Users/revtiramantripathi/Desktop/untitled folder 5/aimemeforge"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI MemeForge v1.0"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-memeforge`
3. Description: `AI-powered meme generator with Google OAuth`
4. Keep it **Public** (required for free hosting)
5. **Don't** initialize with README (we already have code)
6. Click "Create repository"

### 1.3 Push Code to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/ai-memeforge.git

# Push code
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy Backend to Railway

### 2.1 Sign Up for Railway
1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway
4. Go to https://railway.app/account to link Student Pack

### 2.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `ai-memeforge` repository
4. Railway will auto-detect the Dockerfile

### 2.3 Configure Environment Variables
Click on your deployment → "Variables" tab → Add these:

```
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=aimemeforge
MONGODB_TIMEOUT_MS=10000
HF_TOKEN=your_huggingface_token
BACKEND_PORT=8000
ENABLE_ANALYTICS=true
API_KEY=your_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 2.4 Set Root Directory
1. Go to "Settings" tab
2. Under "Build & Deploy"
3. Set "Root Directory" to: `backend`
4. Save changes

### 2.5 Deploy
1. Railway will automatically deploy
2. Wait for build to complete (2-5 minutes)
3. Copy your Railway URL (e.g., `https://your-app.up.railway.app`)

---

## ⚡ Step 3: Deploy Frontend to Vercel

### 3.1 Sign Up for Vercel
1. Go to https://vercel.com/signup
2. Click "Continue with GitHub"
3. Authorize Vercel

### 3.2 Import Project
1. Click "Add New..." → "Project"
2. Select `ai-memeforge` repository
3. Click "Import"

### 3.3 Configure Build Settings
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 3.4 Add Environment Variables
Click "Environment Variables" → Add these:

```
VITE_API_BASE=https://your-railway-url.up.railway.app
VITE_GOOGLE_CLIENT_ID=your_google_client_id
```

⚠️ **Important**: Replace `your-railway-url.up.railway.app` with your actual Railway URL from Step 2.5!

### 3.5 Deploy
1. Click "Deploy"
2. Wait for deployment (1-3 minutes)
3. You'll get a URL like: `https://ai-memeforge.vercel.app`

---

## 🔐 Step 4: Update Google OAuth Settings

### 4.1 Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/apis/credentials
2. Find your OAuth 2.0 Client ID
3. Click "Edit"

### 4.2 Add Authorized Origins
Add these to "Authorized JavaScript origins":
```
https://your-vercel-app.vercel.app
https://your-custom-domain.me (if using custom domain)
```

### 4.3 Add Redirect URIs
Add these to "Authorized redirect URIs":
```
https://your-vercel-app.vercel.app
https://your-vercel-app.vercel.app/auth/callback
```

### 4.4 Save Changes
Click "Save" at the bottom

---

## 🔄 Step 5: Update CORS in Backend

### 5.1 Update Railway Environment Variables
Go back to Railway → Your project → Variables tab

Update `ALLOWED_ORIGINS`:
```
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173,http://localhost:5174
```

### 5.2 Redeploy
Railway will automatically redeploy with new settings

---

## 🌐 Step 6: Set Up Custom Domain (Optional but Recommended!)

### 6.1 Get Free Domain from Namecheap
1. Go to https://nc.me (Namecheap Student Pack)
2. Register for free .me domain
3. Choose your domain (e.g., `memeforge.me`)

### 6.2 Add Domain to Vercel (Frontend)
1. In Vercel, go to your project
2. Click "Settings" → "Domains"
3. Add your domain: `memeforge.me`
4. Vercel will give you DNS records

### 6.3 Configure Namecheap DNS
1. Go to Namecheap dashboard
2. Find your domain → "Manage"
3. Go to "Advanced DNS"
4. Add the DNS records Vercel provided:
   - Type: `CNAME`
   - Host: `@`
   - Value: `cname.vercel-dns.com`
   - TTL: `Automatic`

### 6.4 Add Domain to Railway (Backend)
1. In Railway, go to your project → "Settings"
2. Scroll to "Domains"
3. Click "Generate Domain" for a Railway subdomain
4. Or add custom subdomain: `api.memeforge.me`

### 6.5 Update Environment Variables
Update everywhere:
- Vercel: `VITE_API_BASE=https://api.memeforge.me`
- Railway: `ALLOWED_ORIGINS=https://memeforge.me`
- Google OAuth: Add `https://memeforge.me` to origins

---

## ✅ Step 7: Test Your Deployment

### 7.1 Visit Your Site
Go to: `https://your-vercel-url.vercel.app` or `https://memeforge.me`

### 7.2 Test These Features
- ✅ Homepage loads correctly
- ✅ Can browse without login
- ✅ Click "Generate Meme" → Login modal appears
- ✅ Google login works
- ✅ Can generate memes after login
- ✅ Dashboard shows user info
- ✅ MongoDB saves user data

---

## 🐛 Troubleshooting

### Issue: CORS Error
**Solution**: Make sure `ALLOWED_ORIGINS` in Railway includes your Vercel URL

### Issue: Google Login Fails
**Solution**: Check that Vercel URL is added to Google OAuth authorized origins

### Issue: Backend Not Responding
**Solution**: Check Railway logs → Click on deployment → "View Logs"

### Issue: MongoDB Connection Error
**Solution**: Check that `MONGODB_URI` is correctly set in Railway environment variables

### Issue: Frontend Shows Wrong API URL
**Solution**: Make sure `VITE_API_BASE` is set correctly in Vercel environment variables, then redeploy

---

## 💰 Costs

| Service | Cost with Student Pack |
|---------|----------------------|
| Railway | $5/month credit (FREE) |
| Vercel | Unlimited (FREE) |
| MongoDB Atlas | 512MB free tier (FREE) |
| Namecheap Domain | First year (FREE) |
| **Total** | **$0/month** 🎉 |

---

## 📊 Monitoring

### Railway (Backend)
- Dashboard: https://railway.app/dashboard
- View logs, metrics, and deployments
- Auto-scaling included

### Vercel (Frontend)
- Dashboard: https://vercel.com/dashboard
- View deployments, analytics
- Automatic HTTPS, CDN included

### MongoDB Atlas
- Dashboard: https://cloud.mongodb.com
- View users, collections, performance

---

## 🚀 Next Steps After Deployment

1. **Share Your Link** on social media!
2. **Monitor Usage** in Railway/Vercel dashboards
3. **Add Analytics** (Google Analytics, Plausible)
4. **Set Up Error Tracking** (Sentry)
5. **Add More Features** based on user feedback

---

## 🆘 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review Railway/Vercel logs
3. Test locally first to isolate the issue
4. Check MongoDB Atlas connection

---

## 📝 Important Notes

- **Never commit .env files** to GitHub
- **Always use environment variables** for sensitive data
- **Keep your MongoDB credentials secure**
- **Regularly check Railway credits** (free tier limits)
- **Enable 2FA** on all accounts

---

**Good luck with your deployment! 🚀**

Your app will be live at:
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-app.railway.app
- **API Docs**: https://your-app.railway.app/docs

Enjoy! 🎨✨
