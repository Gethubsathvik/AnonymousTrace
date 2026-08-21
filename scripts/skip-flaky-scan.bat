@echo off
REM python -m anonymoustrace.main - Skip Flaky Sites Scan
REM Usage: scripts\skip-flaky-scan.bat <username> [sites...]

if "%~1"=="" (
    echo Usage: skip-flaky-scan.bat ^<username^> [site1] [site2] ...
    echo Skips known problematic sites with DNS/timeout issues
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %* --skip-flaky
pause

