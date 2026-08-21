@echo off
REM python -m anonymoustrace.main - Proxy Scan
REM Usage: scripts\proxy-scan.bat <username> <proxy_url> [sites...]

if "%~1"=="" (
    echo Usage: proxy-scan.bat ^<username^> ^<proxy_url^> [site1] [site2] ...
    echo Example: proxy-scan.bat octocat socks5://127.0.0.1:1080 github twitter
    exit /b 1
)

if "%~2"=="" (
    echo Error: proxy URL required
    echo Example: proxy-scan.bat octocat socks5://127.0.0.1:1080 github
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %1 --proxy %2 --timeout 15 --print-all
pause

