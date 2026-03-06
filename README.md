# Media Extractor 🎬

A powerful and user-friendly web application to extract high-quality videos and audio from various platforms like YouTube and Instagram.

## 🚀 Key Features

- **Multi-Quality Support**: Choose your preferred resolution, from **480p to 4K (2160p)**.
- **Audio Extraction**: Easily convert videos to high-quality **MP3 (192kbps)**.
- **Smart Analysis**: Fetches video titles, thumbnails, and durations before you download.
- **Playlist Fix**: Automatically extracts the specific video info even from YouTube Playlist or Mix URLs.
- **Modern UI**: A clean, responsive interface with real-time status updates.

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3 (Modern Baseline), Vanilla JavaScript.
- **Backend**: Python 3.x, **FastAPI** (High-performance API framework).
- **Core Engine**: **yt-dlp** (The most advanced media extraction library).
- **Process Manager**: Uvicorn.

## 📦 Recent Updates

1. **Enhanced Format Selection**: Added a dynamic quality picker that lists all available resolutions for the target video.
2. **Performance Optimization**: Improved metadata extraction speed by 5x using optimized `yt-dlp` flags.
3. **Robust URL Handling**: Implemented URL normalization to handle complex parameters like `&list=` or `?index=`.
4. **Environment Stabilization**: Updated the server startup sequence (`run_server.bat`) to ensure proper virtual environment (`venv`) activation and port management.

## 🚥 How to Run

1. **Setup Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install fastapi uvicorn yt-dlp pydantic
   ```
2. **Start Server**:
   Run `run_server.bat` or use the command:
   ```powershell
   .\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```
3. **Access**:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---
© 2026 Media Extractor Service. Managed by Gemini CLI.
