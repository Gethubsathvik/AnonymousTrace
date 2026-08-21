@echo off
REM python -m anonymoustrace.main - Custom Workers Scan
REM Usage: scripts\workers-scan.bat <username> <worker_count> [sites...]

if "%~1"=="" (
    echo Usage: workers-scan.bat ^<username^> ^<worker_count^> [site1] [site2] ...
    echo Example: workers-scan.bat octocat 50 github twitter
    exit /b 1
)

if "%~2"=="" (
    echo Error: worker count required
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %1 --workers %2 --timeout 15 %3 %4 %5 %6 %7 %8 %9
pause

