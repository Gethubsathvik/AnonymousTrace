@echo off
REM python -m anonymoustrace.main - Super Scan Mode
REM Usage: scripts\super-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: super-scan.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --super
pause

