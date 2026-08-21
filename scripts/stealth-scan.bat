@echo off
REM python -m anonymoustrace.main - Stealth Scan Mode
REM Usage: scripts\stealth-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: stealth-scan.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --stealth --tor
pause

