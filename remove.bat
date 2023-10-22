@echo off

set "AutostartOrdner=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

echo %AutostartOrdner%
cd /d %AutostartOrdner% 
del run.bat
del data.pt