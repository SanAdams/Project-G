@echo off

title TestCMD
echo Starting chrome session...

:: Open chrome in debugging mode
start "" "..\BE\dependencies\chrome-win64\chrome.exe" --remote-debugging-port=9222

:: Check if Chrome is loaded
:checkChrome
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I "chrome.exe" >NUL
if %ERRORLEVEL% neq 0 (
    timeout /t 1 >nul
    goto checkChrome
)

:: Bring cmd back to foreground
"%systemroot%\System32\WindowsPowerShell\v1.0\powershell.exe" -command "(new-object -comobject wscript.shell).AppActivate('TestCMD') > $nul"

:: Open python script
python gotosite.py

pause