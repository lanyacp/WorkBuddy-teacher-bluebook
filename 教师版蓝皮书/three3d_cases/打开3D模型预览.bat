@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  ========================================
echo   3D Model Viewer - Local Server
echo  ========================================
echo.
echo  Starting local server on port 8801...
echo  Browser will open automatically.
echo.
echo  Press Ctrl+C to stop the server.
echo.

start "" /b cmd /c "timeout /t 2 >nul & start http://127.0.0.1:8801/index.html"
python -m http.server 8801 --bind 127.0.0.1
