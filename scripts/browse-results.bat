@echo off
REM python -m anonymoustrace.main - Browse Results
REM Usage: scripts\browse-results.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: browse-results.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --browse --print-found
pause

