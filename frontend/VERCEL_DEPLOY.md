# Vercel Configuration for AI MemeForge Frontend

## Build Configuration
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

## Environment Variables (Add these in Vercel Dashboard)

```
VITE_API_BASE=https://your-backend-url.railway.app
VITE_GOOGLE_CLIENT_ID=156698623566-iir6u01ubtmdhlcsgn56p7sig7s76g0r.apps.googleusercontent.com
```

## Post-Deployment
1. Update Google OAuth redirect URIs with your Vercel domain
2. Update backend CORS to allow your Vercel domain
3. Test the login flow end-to-end
