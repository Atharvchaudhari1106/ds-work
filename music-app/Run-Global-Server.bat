@echo off
title AesthetiCore Music - Global Public Launcher
echo ========================================================
echo   🚀 AesthetiCore Music - Global Public Server Launcher
echo ========================================================
echo.

:: Check Node.js installation
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is NOT installed!
    echo Please download and install Node.js from: https://nodejs.org/
    pause >nul
    exit
)

echo 📦 Starting backend music engine...
start /b node server/index.js

echo.
echo 🌐 Launching Global Cloudflare Tunnel...
echo (Access this link on ANY device, 4G/5G mobile data, or Wi-Fi worldwide!)
echo.
npx @cloudflare/cloudflared tunnel --url http://localhost:5000
