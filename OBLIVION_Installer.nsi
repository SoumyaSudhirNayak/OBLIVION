; NSIS installer for OBLIVION
!include "MUI2.nsh"

!define APPNAME "OBLIVION"
!define COMPANY "OBLIVION"
!define VERSION "1.0.0"
!define EXE_NAME "OBLIVION.exe"
!define ISO_NAME "oblivion_os.iso"

Name "${APPNAME} ${VERSION}"
OutFile "OBLIVION-Setup.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"
RequestExecutionLevel admin
SetCompressor /SOLID lzma

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  ; Copy executable
  File /oname=${EXE_NAME} "dist\OBLIVION\OBLIVION.exe"
  ; Copy ISO if available at project root
  File /nonfatal /oname=${ISO_NAME} "oblivion_os.iso"

  ; Create shortcut
  CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXE_NAME}"
SectionEnd

Section "Run"
  Exec "$INSTDIR\${EXE_NAME}"
SectionEnd