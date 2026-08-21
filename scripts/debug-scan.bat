@echo off
REM python -m anonymoustrace.main - Debug/Dump Response
REM Usage: scripts\debug-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: debug-scan.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --dump-response --verbose --print-all
pause

