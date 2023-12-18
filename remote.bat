@echo off
for /f "skip=1 tokens=2" %%i in ('quser %USERNAME%') do (
    set "sessionid=%%i"
    goto :break
)
:break
tscon %sessionid% /dest:console 2> UnlockErrors.log