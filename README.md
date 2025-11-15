# 🎨 AI MemeForge

**AI-Powered Meme & Marketing Generator** - Generate viral memes and marketing posts using AI models like Flux.1 Schnell, Gemma 2, and more.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Flux.1 Schnell for images and Gemma 2 for captions
- 🔥 **Trend Detection**: Automatically fetches trending topics from Google Trends
- 🎨 **Brand Personalization**: Upload your logo and extract brand colors
- 📊 **Analytics**: Track all generated memes with timestamps
- 💾 **Download & Share**: Easy download and sharing of generated content
- 🚀 **Local First**: Runs entirely on your MacBook (CPU) with modular GPU scaling support

## 🏗️ Architecture

```
aimemeforge/
├── backend/          # FastAPI Python backend
│   ├── main.py      # FastAPI app entry point
│   ├── routers/     # API route handlers
│   ├── services/    # AI engine & analytics
│   └── models/      # Data models
├── frontend/        # React + Tailwind + Framer Motion
│   └── src/         # React components
├── datasets/        # Brand data, logs, logos
└── outputs/         # Generated memes
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- pip and npm
- Hugging Face API token (get one at https://huggingface.co/settings/tokens)

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd aimemeforge
   ```

2. **Set up Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
   **Important**: Create a `.env` file in the `backend/` directory:
   ```bash
   echo "HF_TOKEN=your_huggingface_token_here" > backend/.env
   ```
   Get your token from: https://huggingface.co/settings/tokens

3. **Set up Frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start Backend (Terminal 1):**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```
   API will be available at: http://localhost:8000
   API Docs: http://localhost:8000/docs

2. **Start Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at: http://localhost:5173

## 📖 Usage

1. **Generate a Meme:**
   - Enter a prompt describing your meme idea
   - Optionally upload a brand logo
   - Click "Generate Meme"
   - Wait for AI to create your meme (may take 30-60 seconds on CPU)

2. **Use Trending Topics:**
   - Check the sidebar for trending topics
   - Click any trend to use it as your prompt

3. **Brand Personalization:**
   - Upload your logo via the file input
   - System extracts dominant colors
   - Logo and colors are applied to generated memes

4. **Download & Share:**
   - Click "Download" to save your meme
   - Share directly from the app

## 🔧 Configuration

Edit `.env` file to customize:
- Model settings
- Device (cpu/cuda/mps)
- Ports
- Analytics

## 🧠 AI Models

- **Image Generation**: Flux.1 Schnell (via Hugging Face Inference API)
- **Text Generation**: Gemma 2 2B IT (via Hugging Face Inference API)
- **Color Extraction**: ColorThief

**Note**: This project uses Hugging Face Inference API (no local model downloads needed!)

**Requirements**:
- Hugging Face API token (add to `backend/.env` as `HF_TOKEN`)
- Stable internet connection for API calls
- No local model storage needed (~15GB saved!)

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── routers/
│   ├── generate.py      # Meme generation endpoint
│   ├── trends.py        # Trending topics endpoint
│   └── brand.py         # Brand management endpoint
├── services/
│   ├── ai_engine.py     # Core AI generation logic
│   └── analytics.py     # Event logging & stats
└── requirements.txt     # Python dependencies

frontend/
├── src/
│   ├── App.jsx          # Main React component
│   ├── main.jsx         # React entry point
│   └── index.css        # Tailwind styles
├── package.json         # Node dependencies
└── vite.config.js       # Vite configuration
```

## 🎯 API Endpoints

- `POST /generate/` - Generate a meme
- `GET /trends/` - Get trending topics
- `POST /brand/upload` - Upload brand logo
- `GET /brand/` - Get brand settings
- `GET /outputs/{filename}` - Download generated meme

See full API docs at: http://localhost:8000/docs

## 🔮 Future Enhancements

- [ ] AnimateDiff integration for video memes
- [ ] Bark integration for voiceover memes
- [ ] MongoDB integration for user accounts
- [ ] Cron jobs for auto-generation from trends
- [ ] User authentication & plan limits
- [ ] GPU acceleration support
- [ ] Batch generation
- [ ] Template library

## 🐛 Troubleshooting

**API errors?**
- Verify your `HF_TOKEN` is set in `backend/.env`
- Check internet connection for API calls
- Some models may take 30-60 seconds to load on first use (503 status)
- Check Hugging Face API status: https://status.huggingface.co/

**Slow generation?**
- API-based generation: 10-30 seconds per meme (depends on model load)
- First request may take longer if model is cold (503 status)
- API automatically retries after 30 seconds if model is loading

**CORS errors?**
- Ensure backend is running on port 8000
- Check frontend proxy settings in `vite.config.js`

## 📝 License

Open-source project - feel free to contribute!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🙏 Acknowledgments

- Flux.1 Schnell by Black Forest Labs
- Gemma 2 by Google
- FastAPI, React, Tailwind CSS communities

---

**Made with ❤️ for viral content creators**

