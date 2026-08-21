@echo off
REM python -m anonymoustrace.main - TXT Export
REM Usage: scripts\export-txt.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: export-txt.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --txt --output results.txt
echo TXT exported to results.txt
pause

