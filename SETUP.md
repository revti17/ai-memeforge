# 🚀 AI MemeForge Setup Guide

## Quick Start

### Option 1: Using Startup Scripts (Recommended)

1. **Start Backend:**
   ```bash
   ./start_backend.sh
   ```

2. **Start Frontend (in a new terminal):**
   ```bash
   ./start_frontend.sh
   ```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## ⚠️ Important Notes

### Model Downloads

On first run, the application will download AI models:
- **Flux.1 Schnell**: ~10GB (image generation)
- **Gemma 2 2B**: ~5GB (text generation)

**Requirements:**
- Stable internet connection (initial download)
- ~15GB free disk space
- 16GB+ RAM recommended for CPU inference

### Performance Expectations

- **CPU (MacBook)**: 30-60 seconds per meme generation
- **GPU**: 5-10 seconds per meme generation

### Troubleshooting

**Out of Memory Errors:**
- Reduce `num_inference_steps` in `backend/services/ai_engine.py` (default: 4)
- Close other applications
- Consider using a smaller image model

**Model Download Fails:**
- Check internet connection
- Verify Hugging Face access (some models may require login)
- Check disk space

**CORS Errors:**
- Ensure backend is running on port 8000
- Check frontend proxy settings

## 🧪 Testing

1. Open http://localhost:5173
2. Enter a prompt like: "A cat wearing sunglasses"
3. Click "Generate Meme"
4. Wait for generation (30-60s on CPU)
5. Download your meme!

## 📚 Next Steps

- Upload a brand logo for personalization
- Check trending topics in the sidebar
- View analytics in `backend/datasets/logs.json`

