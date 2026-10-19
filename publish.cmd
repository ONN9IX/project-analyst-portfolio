@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Publishing Project Analyst Portfolio to ONN9IX/project-analyst-portfolio...
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish.ps1"
if errorlevel 1 (
  echo.
  echo Publication failed. Copy the error message and send it in ChatGPT.
  pause
  exit /b 1
)
echo.
echo Publication completed. Press any key to close.
pause >nul
