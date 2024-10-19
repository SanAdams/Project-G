start-chrome-session
@echo off

title TestCMD
echo Starting chrome session...

:: Open chrome in debugging mode
start "" "..\BE\dependencies\chrome-win64\chrome-win64\chrome.exe" --remote-debugging-port=9222

:: Wait for chrome to start up
"%systemroot%\System32\timeout.exe" /t 1 >nul

:: Bring cmd back to foreground
"%systemroot%\System32\WindowsPowerShell\v1.0\powershell.exe" -command "(new-object -comobject wscript.shell).AppActivate('TestCMD') > $nul"

:: Open python script
python gotosite.py

pause