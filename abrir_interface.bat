@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Primeira execucao: preparando o ambiente Python...
    call instalar.bat
    if errorlevel 1 exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" interface.py
endlocal
