# ✅ Deployment Checklist

Use this checklist to track your deployment progress!

## 📝 Pre-Deployment

- [ ] Code is working locally (frontend + backend)
- [ ] MongoDB Atlas is connected and working
- [ ] Google OAuth works in development
- [ ] All sensitive data is in `.env` files (not in code)

## 🔐 Account Setup

- [ ] GitHub account created
- [ ] GitHub Student Pack activated: https://education.github.com/pack
- [ ] Railway account created: https://railway.app
- [ ] Vercel account created: https://vercel.com
- [ ] Have MongoDB Atlas credentials ready
- [ ] Have Google OAuth credentials ready

## 📦 Step 1: GitHub

- [ ] Run `./deploy-setup.sh` OR manually init git
- [ ] Create new repo on GitHub: https://github.com/new
- [ ] Repository name: `ai-memeforge`
- [ ] Set to Public (required for free hosting)
- [ ] Add remote: `git remote add origin YOUR_URL`
- [ ] Push code: `git push -u origin main`
- [ ] Verify code is on GitHub

## 🚂 Step 2: Railway (Backend)

- [ ] Sign up with GitHub: https://railway.app
- [ ] Link Student Pack in account settings
- [ ] Create new project → Deploy from GitHub
- [ ] Select `ai-memeforge` repository
- [ ] Set root directory to `backend` in Settings
- [ ] Add ALL environment variables from `.env`:
  - [ ] MONGODB_URI
  - [ ] MONGODB_DB_NAME
  - [ ] MONGODB_TIMEOUT_MS
  - [ ] HF_TOKEN
  - [ ] GOOGLE_CLIENT_ID
  - [ ] GOOGLE_CLIENT_SECRET
  - [ ] ALLOWED_ORIGINS (start with localhost)
  - [ ] BACKEND_PORT
  - [ ] ENABLE_ANALYTICS
  - [ ] API_KEY
- [ ] Wait for deployment to complete
- [ ] Copy your Railway URL: `___________________.up.railway.app`
- [ ] Test backend: Visit `YOUR_RAILWAY_URL/health`
- [ ] Check API docs: `YOUR_RAILWAY_URL/docs`

## ⚡ Step 3: Vercel (Frontend)

- [ ] Sign up with GitHub: https://vercel.com
- [ ] Import project → Select `ai-memeforge`
- [ ] Configure build settings:
  - [ ] Framework: Vite
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`
- [ ] Add environment variables:
  - [ ] VITE_API_BASE (your Railway URL)
  - [ ] VITE_GOOGLE_CLIENT_ID
- [ ] Deploy and wait for completion
- [ ] Copy your Vercel URL: `___________________.vercel.app`
- [ ] Visit your site - it should load!

## 🔄 Step 4: Connect Everything

### Update Railway CORS
- [ ] Go to Railway → Your project → Variables
- [ ] Update ALLOWED_ORIGINS:
  ```
  https://YOUR_VERCEL_URL.vercel.app,http://localhost:5173
  ```
- [ ] Save and redeploy

### Update Google OAuth
- [ ] Go to: https://console.cloud.google.com/apis/credentials
- [ ] Find your OAuth 2.0 Client
- [ ] Add to Authorized JavaScript origins:
  - [ ] `https://YOUR_VERCEL_URL.vercel.app`
- [ ] Add to Authorized redirect URIs:
  - [ ] `https://YOUR_VERCEL_URL.vercel.app`
  - [ ] `https://YOUR_VERCEL_URL.vercel.app/auth/callback`
- [ ] Save changes

## ✅ Step 5: Testing

- [ ] Visit your Vercel URL
- [ ] Homepage loads correctly
- [ ] Can browse without login
- [ ] Click "Generate Meme" → login modal appears
- [ ] Can close modal with X button
- [ ] Google login works (test it!)
- [ ] After login, can generate memes
- [ ] Check MongoDB Atlas → Users collection has new entry
- [ ] Dashboard shows user information
- [ ] Try generating a meme → check outputs
- [ ] Test on mobile device

## 🌐 Optional: Custom Domain

- [ ] Get free domain from Namecheap Student Pack: https://nc.me
- [ ] Choose domain name: `________________.me`
- [ ] Add domain to Vercel:
  - [ ] Vercel → Project → Settings → Domains
  - [ ] Add your domain
  - [ ] Copy DNS records from Vercel
- [ ] Configure Namecheap DNS:
  - [ ] Namecheap → Domain → Advanced DNS
  - [ ] Add CNAME: `@` → `cname.vercel-dns.com`
  - [ ] Wait 10-30 minutes for DNS propagation
- [ ] Update all URLs:
  - [ ] Update VITE_API_BASE in Vercel
  - [ ] Update ALLOWED_ORIGINS in Railway
  - [ ] Update Google OAuth origins
- [ ] Test with custom domain

## 📊 Post-Deployment

- [ ] Share your link on social media
- [ ] Add project to portfolio
- [ ] Monitor Railway dashboard for usage
- [ ] Check Vercel analytics
- [ ] Monitor MongoDB Atlas for users
- [ ] Get feedback from users
- [ ] Plan next features

## 🎉 Celebration

- [ ] Your app is LIVE! 🚀
- [ ] Take a screenshot
- [ ] Share with friends
- [ ] Add to resume/portfolio
- [ ] You're officially deployed! 🎊

---

## 📝 Notes

**Your URLs:**
- Frontend: https://_________________________.vercel.app
- Backend: https://_________________________.up.railway.app
- Custom Domain: https://_________________________.me

**Deployment Date:** _______________

**Issues Encountered:**
_________________________________________
_________________________________________
_________________________________________

**Solutions:**
_________________________________________
_________________________________________
_________________________________________

---

## 🆘 Help Resources

If stuck:
1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Check Railway logs for backend errors
3. Check Vercel logs for frontend errors
4. Check browser console for JavaScript errors
5. Verify all environment variables are set correctly

---

**You got this! 💪**
