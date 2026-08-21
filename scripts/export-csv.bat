@echo off
REM python -m anonymoustrace.main - CSV Export
REM Usage: scripts\export-csv.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: export-csv.bat ^<username^> [site1] [site2] ...
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --csv --output results.csv
echo CSV exported to results.csv
pause

