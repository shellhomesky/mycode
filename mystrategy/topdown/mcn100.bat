cd /d %~dp0



for /L %%i in (0,1,17) do ( 
    start mcn010.bat %%i 
    @ping -n 5 127.1>nul
)
