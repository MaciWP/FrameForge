@echo off
@echo Extracting Bios Settings...
pushd "%~dp0"
SCEWIN_64.exe /O /S BIOSSettings.txt /SD Dupes.txt
popd 
timeout 2 >nul
exit