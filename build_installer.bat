@echo off
setlocal
set ROOT=%~dp0

if not exist "%ROOT%\dist\OBLIVION\OBLIVION.exe" (
  echo OBLIVION.exe not found. Run build_windows_exe.bat first.
  exit /b 1
)

if not exist "%ROOT%\oblivion_os.iso" (
  echo oblivion_os.iso not found at project root. Build it on Linux with build_iso.sh and copy the ISO here.
  echo Proceeding without ISO: the installer will still be created but won't include the bootable ISO.
)

makensis "%ROOT%\OBLIVION_Installer.nsi"

echo Installer build complete.