@echo off
REM Azure OpenAI Tokenization Demo - Windows Batch Script
REM Run this to execute the demonstration

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     Azure OpenAI - Tokenization Visualization Demo                ║
echo ║                                                                    ║
echo ║  This demo shows how text is converted into tokens (numbers)      ║
echo ║  that language models understand.                                 ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

:menu
echo.
echo Select a demonstration:
echo.
echo   1) Run Basic Tokenization Demo (Recommended - No Azure needed)
echo   2) Verify Project Setup
echo   3) Run Azure OpenAI Demo (Requires .env setup)
echo   4) Open README Documentation
echo   5) Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto demo1
if "%choice%"=="2" goto demo2
if "%choice%"=="3" goto demo3
if "%choice%"=="4" goto demo4
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
goto menu

:demo1
echo.
echo Running Basic Tokenization Demo...
echo.
C:/Demo/.venv/Scripts/python.exe main_demo.py
pause
goto menu

:demo2
echo.
echo Verifying Project Setup...
echo.
C:/Demo/.venv/Scripts/python.exe quickstart.py
pause
goto menu

:demo3
echo.
echo Running Azure OpenAI Demo...
echo.
echo Note: This requires Azure credentials set up in .env file
echo.
C:/Demo/.venv/Scripts/python.exe azure_demo.py
pause
goto menu

:demo4
echo.
echo Opening README.md...
echo.
if exist README.md (
    start notepad README.md
) else (
    echo README.md not found
    pause
)
goto menu

:end
echo.
echo Thank you for using the Tokenization Demo!
echo.
pause
