@echo off
title Store Price Comparator - Live Public Server
echo ===================================================
echo Starting Local Server on http://127.0.0.1:8000 ...
echo ===================================================
start "" python server.py
timeout /t 3 /nobreak >nul
echo Starting Cloudflare Free Public Tunnel...
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
