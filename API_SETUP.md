# 🔑 Hugging Face API Setup

## Quick Setup

1. **Get your Hugging Face token:**
   - Go to https://huggingface.co/settings/tokens
   - Create a new token (read access is sufficient)
   - Copy the token

2. **Add token to backend/.env:**
   ```bash
   cd backend
   echo "HF_TOKEN=your_token_here" > .env
   ```

   Or manually create `backend/.env` with:
   ```
   HF_TOKEN=hf_your_token_here
   ```

## Current Configuration

Your token is already configured in `backend/.env`:
```
HF_TOKEN=your_huggingface_token_here
```

## API Models Used

- **Image Generation**: `black-forest-labs/FLUX.1-schnell`
- **Text Generation**: `google/gemma-2-2b-it`

## API Behavior

- **First Request**: May take 30-60 seconds if model is cold (returns 503)
- **Subsequent Requests**: Usually 10-30 seconds
- **Automatic Retry**: Code automatically retries after 30 seconds if model is loading

## Troubleshooting

**Error: "Missing HF_TOKEN"**
- Ensure `backend/.env` exists
- Check that `HF_TOKEN=...` is in the file
- Restart the backend server

**Error: "401 Unauthorized"**
- Token is invalid or expired
- Generate a new token at https://huggingface.co/settings/tokens

**Error: "503 Service Unavailable"**
- Model is loading (normal on first use)
- Code will automatically retry after 30 seconds
- Wait for the retry or try again later

**Error: "Timeout"**
- Model may be taking longer than expected
- Try again in a few moments
- Check Hugging Face status: https://status.huggingface.co/

## Benefits of API Approach

✅ No local model downloads (~15GB saved)  
✅ No GPU required  
✅ Always uses latest model versions  
✅ Faster setup (no model downloads)  
✅ Works on any machine with internet  

## API Costs

- **Free Tier**: Limited requests per day
- **Pro Tier**: More requests available
- Check your usage: https://huggingface.co/settings/billing

