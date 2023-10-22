@echo off
setlocal enabledelayedexpansion

set "ZielDatei=main.py"
set "Datei=%~dp0%ZielDatei%"

cd accepted
set "path_accepted=%cd%"
cd ..


echo python %Datei% --path %path_accepted%> run.bat


set "Datei=.\run.bat"


set "AutostartOrdner=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

copy "%Datei%" "%AutostartOrdner%\\"
echo Datei erfolgreich in den Autostart-Ordner verschoben.

del %Datei%
endlocal