# YouTube Agent

A lightweight Python agent that **searches YouTube**, **downloads the audio**, **transcribes** the content and **generates a concise summary** using Google's Gemini model.

---

## ✨ Features
- Search YouTube videos by keyword (YouTube Data API v3).
- Download audio only (via `pytube`).
- Transcribe audio locally with OpenAI **Whisper**.
- Summarize the transcript using **Gemini‑1.5‑flash** (or any Gemini model). 
- Simple CLI for quick experimentation.

---

## 🚀 Quick Start
```bash
# 1. Clone the repo (once we push it) or copy this folder locally
git clone <your‑github‑url>
cd youtube-agent

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the example env and fill in your keys
cp .env.example .env
# edit .env with your YOUTUBE_API_KEY and GEMINI_API_KEY

# 5. Run the agent
python youtube_agent.py "come guadagnare online"  # esempio di query
```

---

## 📄 Configuration (`.env`)
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```
> **Tip:** Keep the `.env` file out of version control – it’s listed in `.gitignore`.

---

## 🛠️ How it works
1. **Search** – `search_youtube(query)` uses the YouTube Data API to fetch the top‑most relevant video ID.
2. **Download** – `download_audio(video_id)` pulls the audio stream with `pytube` and stores it as `audio.mp4`.
3. **Transcribe** – `transcribe(audio_path)` runs `whisper` locally and returns the raw transcript.
4. **Summarize** – `summarize(transcript)` sends the text to Gemini (`gemini-1.5-flash`) and receives a concise summary (≈3‑4 sentences).

---

## 📦 Dependencies (`requirements.txt`)
```
python-dotenv==1.0.1
google-generativeai==0.4.0
pytube==15.0.0
openai-whisper==20231117
```

---

## 🧭 Roadmap
- [ ] Add support for batch processing multiple video IDs.
- [ ] Cache transcripts to avoid re‑transcribing the same video.
- [ ] Optional language detection for multi‑language videos.

---

## 🤝 Contributing
Feel free to open issues or submit PRs. Follow the standard GitHub flow:
1. Fork the repository.
2. Create a feature branch.
3. Open a Pull Request.

---

## 📜 License
MIT – see `LICENSE` file.

---

*Built with 🛠️ passion for automation and the **Protocollo Nuova Identità** mindset.*
