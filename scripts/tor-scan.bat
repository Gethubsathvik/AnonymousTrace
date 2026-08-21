@echo off
REM python -m anonymoustrace.main - Tor Scan
REM Usage: scripts\tor-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: tor-scan.bat ^<username^> [site1] [site2] ...
    echo Note: Tor service must be running on 127.0.0.1:9050
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --tor --stealth --print-all
pause

