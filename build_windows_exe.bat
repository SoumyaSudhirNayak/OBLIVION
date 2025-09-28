@echo off
setlocal enabledelayedexpansion

REM Build crash-proof OBLIVION.exe using clean venv and PyInstaller
set ROOT=%~dp0
set SRC=%ROOT%src
set VENV=%ROOT%venv

if not exist "%VENV%" (
  py -3 -m venv "%VENV%"
)
call "%VENV%\Scripts\activate"
python -m pip install --upgrade pip
python -m pip install pyinstaller pyjwt qrcode pillow cryptography

REM Ensure private key exists
if not exist "%ROOT%CP\python-scripts\output\private_key.pem" (
  echo Missing private_key.pem in CP\python-scripts\output\
  exit /b 1
)

pyinstaller --clean --noconfirm "%ROOT%\oblivion.spec"

REM Correct output path info
if exist "%ROOT%dist\OBLIVION\OBLIVION.exe" (
  echo Build complete. See dist\OBLIVION\OBLIVION.exe
) else (
  echo Build finished. Check dist\ for artifacts.
)