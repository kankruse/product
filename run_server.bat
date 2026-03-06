@echo off
chcp 65001 > nul
:: 현재 배치 파일이 있는 폴더로 이동
cd /d "%~dp0"

echo [INFO] 가상환경(venv)을 활성화합니다...
call venv\Scripts\activate

echo.
echo [INFO] Media Extractor 서버를 시작합니다...
echo [INFO] 서버 중지: Ctrl + C
echo.

echo [INFO] 현재 컴퓨터의 로컬 IP 주소:
for /f "tokens=1,2 delims=:" %%a in ('ipconfig^|find "IPv4"') do for /f "tokens=*" %%c in ("%%b") do echo    - %%c:8000

echo.
echo [INFO] 같은 네트워크의 다른 기기에서 위 주소로 접속할 수 있습니다.
echo [INFO] 외부 인터넷에서 접속하려면 공유기/라우터에서 포트포워딩(8000번) 설정이 필요합니다.
echo.

echo [INFO] 브라우저를 자동으로 실행합니다...
start http://127.0.0.1:8000

uvicorn main:app --reload --host 0.0.0.0

pause
