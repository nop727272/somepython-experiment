@echo off
title Monograph Updater
color 0A

echo.
echo ========================================
echo MONOGRAPH EDITOR - AUTO UPDATE
echo ========================================
echo.

echo [1/3] Downloading update...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/nop727272/somepython-experiment/archive/main.zip' -OutFile 'update.zip'"

echo.
echo [2/3] Extracting files...
powershell -Command "Expand-Archive -Path update.zip -DestinationPath . -Force"

echo.
echo [3/3] Copying files...
copy "somepython-experiment-main\*.py" . >nul 2>&1
copy "somepython-experiment-main\*.txt" . >nul 2>&1

echo.
echo Cleaning up...
del update.zip >nul 2>&1
rmdir /s /q "somepython-experiment-main" >nul 2>&1

echo.
echo ========================================
echo UPDATE COMPLETE!
echo ========================================
echo.
echo Run: py monograph-editor-gui.py
echo.
pause