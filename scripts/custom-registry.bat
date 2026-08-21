@echo off
REM python -m anonymoustrace.main - Custom Registry
REM Usage: scripts\custom-registry.bat <username> <registry.json> [sites...]

if "%~1"=="" (
    echo Usage: custom-registry.bat ^<username^> ^<registry.json^> [site1] [site2] ...
    echo Example: custom-registry.bat octocat my_sites.json github twitter
    exit /b 1
)

if "%~2"=="" (
    echo Error: registry file required
    exit /b 1
)

cd /d "%~dp0.."
python -m anonymoustrace.main %1 --data-file %2 --timeout 15 --print-all
pause

