@echo off
REM python -m anonymoustrace.main - List All Sites
REM Usage: scripts\list-sites.bat

cd /d "%~dp0.."
python -m anonymoustrace.main --list-sites
pause

