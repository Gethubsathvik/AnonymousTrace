@echo off
REM python -m anonymoustrace.main - Batch Scan from File
REM Usage: scripts\batch-scan.bat <input_file> [sites...]

if "%~1"=="" (
    echo Usage: batch-scan.bat ^<input_file^> [site1] [site2] ...
    echo Example: batch-scan.bat users.txt github twitter
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main --input-file %1 --timeout 15 --print-found
pause

