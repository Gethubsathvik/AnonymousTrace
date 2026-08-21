@echo off
REM python -m anonymoustrace.main - Quick Scan Script
REM Usage: scripts\scan.bat <username> [site1] [site2] ...

if "%~1"=="" (
    echo Usage: scan.bat ^<username^> [site1] [site2] ...
    echo Example: scan.bat octocat github twitter
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %*
pause

