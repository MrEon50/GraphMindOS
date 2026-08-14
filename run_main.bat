@echo off
title GraphMindOS v1.4 Launcher
echo ==================================================
echo   GraphMindOS v1.4 - Multi-Provider Launcher
echo ==================================================
echo.
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Aplikacja zakroczyla z bledem %ERRORLEVEL%.
    pause
)
