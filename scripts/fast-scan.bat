@echo off
REM python -m anonymoustrace.main - Fast Scan Mode
REM Usage: scripts\fast-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: fast-scan.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --fast
pause

