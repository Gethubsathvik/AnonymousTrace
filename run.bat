@echo off
REM Quick setup and run script for AnonymousTrace (Windows)
REM Usage: run.bat [username]

echo === AnonymousTrace ===
echo.

REM Check Python version
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q requests requests-futures certifi PySocks stem rich colorama pandas

REM Run scan if username provided
if "%~1"=="" (
    echo.
    echo Setup complete! Run a scan with:
    echo   python -m anonymoustrace.main ^<username^>
    echo.
    echo Or try:
    echo   python -m anonymoustrace.main --list-sites
    echo   python -m anonymoustrace.main --help
) else (
    echo.
    echo Running scan for: %*
    python -m anonymoustrace.main %*
)

pause