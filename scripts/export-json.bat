@echo off
REM python -m anonymoustrace.main - JSON Export
REM Usage: scripts\export-json.bat <username> [sites...] [output.json]

if "%~1"=="" (
    echo Usage: export-json.bat ^<username^> [site1] [site2] ... [output.json]
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --json results.json
echo JSON exported to results.json
pause

