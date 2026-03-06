import os
import yt_dlp
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InfoRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    is_audio_only: bool = False
    format_id: str = None

# 정보 분석 API (URL 정규화 및 추출 강화)
@app.post("/api/info")
async def info_endpoint(req: InfoRequest):
    # URL에서 재생목록 파라미터 제거 (단일 영상 정보만 가져오기 위해)
    clean_url = req.url.split('&list=')[0].split('?list=')[0]
    print(f"\n--- [분석 요청 받음] URL: {clean_url} ---")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        def extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(clean_url, download=False)
        
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, extract)
        
        formats = []
        seen = set()
        
        all_formats = info.get('formats', [])
        print(f"1. 전체 포맷 분석 중... (개수: {len(all_formats)})")
        
        for f in all_formats:
            # 해상도가 있고, 비디오 코덱이 'none'이 아닌 것
            # mp4 혹은 best quality 위주로 필터링
            if f.get('vcodec') != 'none' and f.get('height'):
                res = f"{f.get('height')}p"
                if res not in seen:
                    formats.append({
                        'format_id': f.get('format_id'),
                        'resolution': res,
                        'note': f.get('format_note') or ""
                    })
                    seen.add(res)
        
        # 만약 포맷이 하나도 없다면? (일부 사이트 대응)
        if not formats and info.get('url'):
            formats.append({'format_id': 'best', 'resolution': '기본 화질'})

        # 해상도 높은 순 정렬
        formats.sort(key=lambda x: int(''.join(filter(str.isdigit, x['resolution'])) if any(c.isdigit() for c in x['resolution']) else 0), reverse=True)
        
        print(f"2. 분석 완료: 화질 {len(formats)}개 발견")
        return {
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration'),
            'formats': formats[:10]
        }
    except Exception as e:
        print(f"❌ 분석 실패 상세: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/download")
async def download_endpoint(req: DownloadRequest):
    clean_url = req.url.split('&list=')[0].split('?list=')[0]
    print(f"\n--- [다운로드 시작] URL: {clean_url} ---")
    save_dir = './downloads'
    os.makedirs(save_dir, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{save_dir}/%(title)s.%(ext)s',
        'quiet': False,
    }
    
    if req.is_audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}],
        })
    else:
        # 특정 화질이 선택된 경우
        if req.format_id and req.format_id != 'best':
            ydl_opts['format'] = f"{req.format_id}+bestaudio/best"
        else:
            ydl_opts['format'] = "bestvideo+bestaudio/best"
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                return ydl.prepare_filename(info)
        
        loop = asyncio.get_event_loop()
        path = await loop.run_in_executor(None, download)
        
        if req.is_audio_only: path = os.path.splitext(path)[0] + ".mp3"
        elif not os.path.exists(path): path = os.path.splitext(path)[0] + ".mp4"
        
        return FileResponse(path=path, filename=os.path.basename(path))
    except Exception as e:
        print(f"❌ 다운로드 실패: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/", StaticFiles(directory="."), name="static")
