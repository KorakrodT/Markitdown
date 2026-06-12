@echo off
title MarkItDown - Build
color 0A

echo.
echo  ==========================================
echo   MarkItDown GUI - Build All-in-One
echo  ==========================================
echo.

:: Move to src directory (where this bat file lives)
cd /d "%~dp0"

:: Find Python
set PY=
where py >nul 2>&1 && set PY=py
if "%PY%"=="" (where python >nul 2>&1 && set PY=python)
if "%PY%"=="" (
    echo [ERROR] Python not found. Install Python 3.9+ from python.org
    pause & exit /b 1
)
echo [OK] Python: %PY%
%PY% --version

echo.
echo [1/5] Installing dependencies...
%PY% -m pip install -r requirements.txt -q --no-warn-script-location
if errorlevel 1 (echo [ERROR] pip install failed & pause & exit /b 1)
echo [OK] Done

echo.
echo [2/5] Cleaning old build...
if exist "..\release\dist"  rmdir /s /q "..\release\dist"
if exist "..\release\build" rmdir /s /q "..\release\build"
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist
echo [OK] Cleaned

echo.
echo [3/5] Building .exe with PyInstaller (2-5 min)...
%PY% -m PyInstaller markitdown_gui.spec --clean --noconfirm --distpath "..\release\dist" --workpath "..\release\build"
if errorlevel 1 (echo [ERROR] PyInstaller failed & pause & exit /b 1)
if not exist "..\release\dist\MarkItDown\MarkItDown.exe" (
    echo [ERROR] MarkItDown.exe not found
    pause & exit /b 1
)
echo [OK] .exe created: release\dist\MarkItDown\MarkItDown.exe

echo.
echo [4/5] Looking for Inno Setup...
set ISCC=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe"       set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

if "%ISCC%"=="" (
    echo [WARN] Inno Setup not found.
    echo        Download: https://jrsoftware.org/isdl.php
    echo        Then run this script again to build the installer.
    echo.
    echo [OK] .exe is ready at: release\dist\MarkItDown\
    start explorer "..\release\dist\MarkItDown"
    pause & exit /b 0
)
echo [OK] Inno Setup: %ISCC%

echo.
echo [5/5] Building installer...
if not exist "..\release\installer" mkdir "..\release\installer"
:: Use Python (CreateProcessW) instead of cmd.exe to call ISCC.
:: This handles Unicode directory names reliably.
%PY% build_installer.py
if errorlevel 1 (echo [ERROR] build_installer.py failed & pause & exit /b 1)
echo [OK] Installer created in release\installer\

echo.
echo  ==========================================
echo   BUILD COMPLETE!
echo   .exe      : release\dist\MarkItDown\
echo   Installer : release\installer\
echo  ==========================================
echo.
start explorer "..\release\installer"
pause
