@echo off
title GraphMindOS Cache Cleaner
echo ==================================================
echo   Czyszczenie __pycache__ oraz plikow .pyc
echo ==================================================
echo.
cd /d "%~dp0"

for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Usuwanie: "%%d"
        rd /s /q "%%d"
    )
)

del /s /q /f *.pyc >nul 2>&1
del /s /q /f *.pyo >nul 2>&1

echo.
echo [SUKCES] Czyszczenie pamieci podręcznej zakonczone!
pause
