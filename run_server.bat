@echo off
:: UTF-8 지원을 위한 설정
chcp 65001 > nul
cd /d "%~dp0"

echo [INFO] Media Extractor 서버를 시작합니다...
echo.

:: 가상 환경의 파이썬 실행
set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] 가상 환경(venv)을 찾을 수 없습니다.
    echo [FIX] python -m venv venv 를 먼저 실행해 주세요.
    pause
    exit /b
)

:: 브라우저 자동 실행
start http://127.0.0.1:8000

:: 서버 실행 (uvicorn)
"%PYTHON_EXE%" -m uvicorn main:app --host 127.0.0.1 --port 8000

pause
