@echo off

cd %~dp0
git checkout .
git pull origin main

@REM cd ../../../
@REM call run_nvidia_gpu.bat