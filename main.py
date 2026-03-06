import os
import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Media Extractor API")

# 1. CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 클라이언트 데이터 형식
class DownloadRequest(BaseModel):
    url: str
    is_audio_only: bool = False

# 3. 핵심 로직
def download_media_logic(url: str, is_audio_only: bool) -> str:
    save_dir = './downloads'
    os.makedirs(save_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{save_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,
    }

    if is_audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            downloaded_file_path = ydl.prepare_filename(info_dict)
            if is_audio_only:
                base, _ = os.path.splitext(downloaded_file_path)
                downloaded_file_path = f"{base}.mp3"
            return downloaded_file_path
    except Exception as e:
        raise Exception(str(e))

# 4. API 엔드포인트
@app.post("/api/download")
async def download_endpoint(req: DownloadRequest):
    try:
        file_path = download_media_logic(req.url, req.is_audio_only)
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            return FileResponse(
                path=file_path, 
                filename=filename, 
                media_type='application/octet-stream'
            )
        else:
            raise HTTPException(status_code=500, detail="파일 저장에 실패했습니다.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"다운로드 중 오류 발생: {str(e)}")

# 5. 정적 파일 서빙
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# CSS, JS 파일을 위해 StaticFiles 등록
app.mount("/", StaticFiles(directory=".", html=True), name="static")
