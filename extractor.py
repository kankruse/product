import os
import sys

# 가상 환경의 라이브러리를 자동으로 불러오기 위한 설정
venv_path = os.path.join(os.path.dirname(__file__), 'venv', 'lib', 'python3.11', 'site-packages')
if os.path.exists(venv_path):
    sys.path.append(venv_path)

try:
    import yt_dlp
except ImportError:
    print("❌ 에러: yt-dlp 라이브러리가 설치되지 않았습니다.")
    print("💡 해결 방법: 터미널에 'source venv/bin/activate && pip install yt-dlp'를 입력하세요.")
    sys.exit(1)

def download_media(url, is_audio_only=False):
    save_dir = './downloads'
    os.makedirs(save_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{save_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    if is_audio_only:
        print("\n🎧 음원(MP3) 추출 모드로 시작합니다...")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        print("\n🎬 동영상(MP4) 추출 모드로 시작합니다...")
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 [{url}] 다운로드 중...")
            ydl.download([url])
            print("\n✅ 모든 작업이 완료되었습니다! (./downloads 폴더 확인)")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("      🎥 미디어 추출기 (YouTube / Instagram) 🎬")
    print("="*50)

    # 1. URL 입력 받기 (가장 먼저 실행)
    test_url = input("\n🔗 다운로드할 URL을 입력하세요: ").strip()

    if not test_url:
        print("⚠️ URL이 입력되지 않았습니다. 프로그램을 종료합니다.")
        sys.exit(0)

    # 2. 모드 선택 받기
    print("\n[모드 선택]")
    print(" 1: 동영상 (MP4)")
    print(" 2: 음원 추출 (MP3)")
    mode = input("\n👉 선택 (기본 1): ").strip()

    if mode == '2':
        download_media(test_url, is_audio_only=True)
    else:
        download_media(test_url, is_audio_only=False)