@echo off
REM python -m anonymoustrace.main - Plain Text Output
REM Usage: scripts\plain.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: plain.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --plain
pause

