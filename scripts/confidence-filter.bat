@echo off
REM python -m anonymoustrace.main - Confidence Filter
REM Usage: scripts\confidence-filter.bat <username> <confidence_level> [sites...]
REM Levels: found, likely, unknown

if "%~1"=="" (
    echo Usage: confidence-filter.bat ^<username^> ^<confidence^> [site1] [site2] ...
    echo Levels: found, likely, unknown
    echo Example: confidence-filter.bat octocat likely github twitter
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --min-confidence %2 --print-found
pause

