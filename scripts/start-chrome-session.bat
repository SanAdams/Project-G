@echo off

title Testing-CMD-Window
echo Starting chrome session...

:: Open chrome in debugging mode
start "" "%CHROME_PATH%" --remote-debugging-port=9222

:: Wait a bit to allow Chrome to start
timeout /t 2 >nul

:: Bring cmd back to foreground
powershell -command "(new-object -comobject wscript.shell).AppActivate('Testing-CMD-Window') > $nul"

:: Open python script
python gotosite.py

pause