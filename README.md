# 🎧 Voice-Based AI IT Support Agent

A real-time voice conversational AI agent built specifically to act as an IT Support professional. The system continuously listens, processes intent via LangChain & Groq (llama3-8b-8192), and natively converts replies to human-like voice.

## 🌟 Features

- **Continuous Conversation Loop**: Fully mimics a real phone call where you take turns speaking
- **Speech-to-Text**: Powered by `faster-whisper` for fast local inference
- **Agentic Brain**: LangChain powered logic, hooked up to the blazing fast **Groq API**
- **Text-to-Speech**: `edge-tts` handles audio feedback directly inside your environment
- **Streamlit UI**: A clean, accessible UI that holds conversation state and live transcriptions
- **No GPU Required**: Runs efficiently on CPU

---

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Speech-to-Text** | faster-whisper |
| **LLM Provider** | Groq (Llama 3 - 8B) |
| **Text-to-Speech** | edge-tts |
| **Audio Recording** | sounddevice |
| **Audio Playback** | pygame |
| **Business Logic** | LangChain |
| **Language** | Python 3.9+ |

---

## 📁 Project Structure

```
voice-ai-agent/
├── app.py                      # Main Streamlit UI frontend
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # This file
├── models/                    # Pre-downloaded models
│   └── models--Systran--faster-whisper-base.en/
└── utils/
    ├── __init__.py
    ├── audio_recorder.py      # Microphone input handler
    ├── speech_to_text.py      # faster-whisper wrapper
    ├── llm_handler.py         # LangChain & Groq integration
    └── text_to_speech.py      # edge-tts & pygame wrapper
```

---

## ⚙️ Prerequisites

- **Python 3.9+**
- **Microphone**: Connected and working
- **Groq API Key**: Free account at [console.groq.com](https://console.groq.com/)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB+ recommended
- **Internet**: Required for Groq API calls

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/voice-ai-agent.git
cd voice-ai-agent
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get Groq API Key
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up or log in with your email
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the key (format: `gsk_xxx...`)

### Step 5: Configure Environment
Create a `.env` file in the project root:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

Or add `.env.example` reference:
```bash
cp .env.example .env
# Then edit .env and add your actual key
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will automatically open at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push your latest code to GitHub (already done for this repo).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **Create app**.
4. Select:
   - **Repository**: `Nahid305/voice-ai-agent`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Open **Advanced settings → Secrets** and add:

```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

6. Click **Deploy**.

### Important for Cloud
- In the app sidebar, use **Audio Mode** = **Browser Live Call (auto voice detect, Streamlit Cloud)**.
- This mode records voice in the browser and plays responses in the browser (no server microphone/speaker required).

---

## 💬 How to Use

### Quick Start
1. Run `streamlit run app.py`
2. Open browser to `http://localhost:8501`
3. Add Groq API Key (if not in .env):
   - Look in the sidebar under **⚙️ Settings**
   - Paste your Groq API key
4. Set **Audio Mode**:
   - **Browser Live Call (auto voice detect, Streamlit Cloud)** for hands-free cloud call behavior
   - **Browser Push-to-Talk (manual send)** if your browser blocks live capture
   - **Desktop (local mic + speaker)** for local machine use
5. Click **Start Call** button

### Step-by-Step Usage
1. **Listening Phase**: Click "Start Call" - UI shows "🎤 Listening"
2. **Speak Your Issue**: You have ~5 seconds to explain your problem
   - Examples:
     - *"My WiFi keeps dropping out"*
     - *"How do I reset my password?"*
     - *"My computer is running slow"*
3. **AI Responds**: Agent processes your request and speaks back
4. **Continue Chat**: Speak the follow-up and agent responds
5. **End Call**: Click "End Call" to finish the conversation

### Features During Call
- **Live Transcript**: See exactly what was transcribed
- **Chat History**: View conversation history in sidebar
- **Audio Feedback**: Hear responses in natural voice
- **Real-time Status**: Know when agent is listening/processing

---

## 🔄 How It Works

```
┌─────────────────┐
│  User Speaks    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ audio_recorder.py           │
│ (Records audio via mic)     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ speech_to_text.py           │
│ (faster-whisper converts    │
│  speech to text)            │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ llm_handler.py              │
│ (LangChain + Groq API       │
│  generates intelligent      │
│  IT support response)       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ text_to_speech.py           │
│ (edge-tts converts response │
│  to natural human voice)    │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│ User Hears Reply│
└─────────────────┘
```

### Detailed Processing
1. **Audio Recording**: Captures microphone input using `sounddevice`
2. **Speech Recognition**: Transcribes audio to text using `faster-whisper` model
3. **LLM Processing**: Sends transcribed text to Groq API via LangChain
   - Model: Llama 3 (8B parameters)
   - System Prompt: Acts as helpful IT Support professional
4. **Voice Synthesis**: Converts AI response to speech using `edge-tts`
5. **Audio Playback**: Plays generated audio using `pygame`
6. **Loop**: Returns to listening for next user input

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "No audio device found"
**Solution**:
- Check microphone is connected to your computer
- Test microphone in Windows Sound Settings
- Try different USB port if using USB mic
- Restart the Streamlit app

#### ❌ "GROQ_API_KEY not found"
**Solution**:
- Verify `.env` file exists in project root directory
- Check API key is correctly formatted (starts with `gsk_`)
- Make sure you're not using quotes around the key in `.env`
- Try pasting key directly in Streamlit sidebar instead
```env
# ✅ Correct
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxx

# ❌ Wrong (don't use quotes)
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxx"
```

#### ❌ "Failed to transcribe audio"
**Solution**:
- Ensure audio input is clear (minimize background noise)
- Speak clearly and directly into microphone
- Check microphone volume levels
- Verify faster-whisper is installed: `pip install faster-whisper --upgrade`

#### ❌ "Text-to-speech not working"
**Solution**:
- Check speaker/headphone volume is turned up
- Verify pygame is installed: `pip list | grep pygame`
- Update pygame: `pip install pygame --upgrade`
- On Linux, install audio libraries: `sudo apt-get install libsdl2-mixer-2.0`
- On macOS, ensure audio output is not muted

#### ❌ "Streamlit app won't start"
**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with explicit port
streamlit run app.py --server.port 8501

# Check Python version
python --version
```

#### ❌ "Permission denied on Linux/macOS"
**Solution**:
```bash
# Grant microphone permissions
# The app will request permissions on first run
# Check system preferences > Security & Privacy
```

---

## 📦 Dependencies Explained

```
streamlit              # Modern Python UI framework for data apps
faster-whisper         # Fast, CPU-friendly speech recognition model
groq                   # Official Groq API Python client
langchain              # LLM chain orchestration and management
edge-tts               # Neural text-to-speech synthesis
sounddevice            # Cross-platform audio input/output
pygame                 # Audio playback and multimedia
python-dotenv          # Load environment variables from .env file
numpy                  # Numerical and scientific computing
scipy                  # Advanced scientific computing
requests               # HTTP library for API calls
```

---

## 🔐 Security Best Practices

- ✅ **Never commit `.env` file** - Add to `.gitignore`
- ✅ **Keep API key secret** - Don't share or post online
- ✅ **Use environment variables** in production
- ✅ **Rotate API keys regularly** for security
- ✅ **Validate user inputs** if extending the app
- ✅ **Monitor API usage** at console.groq.com

### `.gitignore` Setup
```
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Streamlit
.streamlit/

# Audio files
*.wav
temp_recording.wav
```

---

## 📝 Example Environment File

Create `.env.example` for documentation:
```env
# Groq API Configuration
# Get free API key at: https://console.groq.com/
GROQ_API_KEY=gsk_your_actual_key_here

# Optional: Configure LLM model
# Default is llama3-8b-8192
# LLM_MODEL=llama3-8b-8192

# Optional: Debugging
# DEBUG=true
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Getting Started
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test locally
4. Commit: `git commit -m 'Add: your feature description'`
5. Push: `git push origin feature/your-feature`
6. Open Pull Request

### Contribution Ideas
- 🎨 UI/UX improvements
- 🚀 Performance optimizations
- 🌍 Multi-language support
- 📚 Documentation improvements
- 🐛 Bug fixes and testing
- ✨ New features and functionality

### Development Tips
```bash
# Install dev dependencies
pip install -r requirements.txt pytest black flake8

# Run code quality checks
black utils/ app.py
flake8 utils/ app.py

# Test locally
streamlit run app.py
```

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

MIT License means:
- ✅ Free for commercial use
- ✅ Free for private use
- ✅ Modification allowed
- ✅ Distribution allowed
- ⚠️ Include license and copyright notice
- ⚠️ No liability or warranty

---

## 🙋 Support & Questions

### Getting Help
- **🐛 Bug Reports**: Open [GitHub Issues](https://github.com/yourusername/voice-ai-agent/issues)
- **💡 Feature Requests**: Use GitHub Discussions
- **📖 Documentation**: Check existing documentation
- **🆘 Emergency Help**: Check troubleshooting section above

### Useful Links
- [Streamlit Docs](https://docs.streamlit.io/)
- [Groq API Docs](https://console.groq.com/docs)
- [LangChain Docs](https://python.langchain.com/)
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [edge-tts GitHub](https://github.com/rany2/edge-tts)

---

## 🎯 Roadmap

### Current Version (v1.0)
- ✅ Real-time voice conversation
- ✅ Speech-to-text recognition
- ✅ Text-to-speech responses
- ✅ Streamlit web interface

### Planned Features
- [ ] Multi-language support
- [ ] Conversation history export (PDF/JSON)
- [ ] Custom system prompts
- [ ] Audio file processing
- [ ] Integration with ticketing systems
- [ ] Performance metrics dashboard
- [ ] Docker containerization
- [ ] API backend deployment
- [ ] Mobile app version
- [ ] Sentiment analysis during calls

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Speech Recognition Latency** | ~1-2 seconds |
| **LLM Response Time** | ~2-3 seconds (Groq API) |
| **Text-to-Speech Generation** | ~1-2 seconds |
| **Total Response Time** | ~4-7 seconds |
| **Memory Usage** | ~500MB base |
| **GPU Required** | No (CPU only) |

---

## 🎓 Learning Resources

### For Beginners
- Introduction to Streamlit: [Official Tutorial](https://docs.streamlit.io/library/get-started)
- Python Virtual Environments: [Guide](https://docs.python.org/3/tutorial/venv.html)
- Git & GitHub Basics: [GitHub Guides](https://guides.github.com/)

### For Advanced Users
- LangChain Architecture: [Deep Dive](https://python.langchain.com/docs/modules/)
- Groq API Optimization: [Performance Tips](https://console.groq.com/docs)
- faster-whisper Model Tuning: [Repository](https://github.com/SYSTRAN/faster-whisper)

---

## 💡 Tips & Tricks

### Performance Tips
- Keep microphone away from fans/AC for better audio quality
- Use headphones to avoid audio feedback loops
- Speak clearly and at normal pace
- Minimize background noise for better transcription

### Configuration Tips
- Store API key in `.env` for security
- Use virtual environment to avoid package conflicts
- Clear Streamlit cache if seeing old responses
- Monitor API usage at console.groq.com

### Debugging Tips
```bash
# Enable verbose logging
streamlit run app.py --logger.level=debug

# Check API connection
python -c "from groq import Groq; print('Groq available')"

# Test microphone
python -c "import sounddevice; print(sounddevice.query_devices())"
```

---

## 👨‍💻 About This Project

Created with ❤️ as an intelligent IT support solution combining:
- **Fast Speech Recognition** (faster-whisper)
- **Powerful LLM** (Groq's Llama 3)
- **Natural Voice Synthesis** (edge-tts)
- **Clean Web UI** (Streamlit)

Perfect for:
- IT help desk automation
- Customer support chatbots
- Educational projects
- Voice assistant development

---

## ⭐ Show Your Support

If you found this project helpful, please:
- ⭐ **Star this repository**
- 🍴 **Fork** for your own use
- 👥 **Share** with others
- 📝 **Contribute** improvements

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/voice-ai-agent?style=social)](https://github.com/yourusername/voice-ai-agent)

---

## 🤖 Similar Projects

Check out these related projects:
- [LangChain](https://github.com/langchain-ai/langchain) - LLM orchestration
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [Streamlit](https://github.com/streamlit/streamlit) - Web UI framework
- [Groq API](https://console.groq.com/) - Fast LLM API

---

## 📮 Contact

- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Email**: your.email@example.com
- **LinkedIn**: [Your Name](https://linkedin.com/)

---

**Last Updated**: March 2026  
**Status**: ✅ Active Development  
**Version**: 1.0.0

---

*Made with ❤️ for the open-source community*
