@echo off
title Push to GitHub
cd /d "%~dp0"

where git >nul 2>&1 || (echo [ERROR] git not found & pause & exit /b 1)

if not exist ".git" git init
git config user.name >nul 2>&1 || git config user.name "KorakrodT"
git config user.email >nul 2>&1 || git config user.email "korakrod.fifa@gmail.com"

git add -A
git commit -m "MarkItDown GUI v1.0.0 - Thai-friendly Markdown converter (Tkinter + Microsoft MarkItDown)"
git branch -M main

git remote get-url origin >nul 2>&1 || git remote add origin https://github.com/KorakrodT/Markitdown.git

echo.
echo Fetching remote and merging (keeping local files on conflict)...
git fetch origin
git merge origin/main --allow-unrelated-histories -X ours -m "Merge remote initial commit"

echo.
echo Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo [ERROR] Push failed - check credentials / network
    pause & exit /b 1
)
echo.
echo [OK] Pushed to https://github.com/KorakrodT/Markitdown
pause
