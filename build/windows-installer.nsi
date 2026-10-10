Unicode true
!include "MUI2.nsh"
Name "Khavaran Desk"
OutFile "KhavaranDesk-Setup-x64.exe"
InstallDir "$PROGRAMFILES64\KhavaranDesk"
RequestExecutionLevel admin
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Farsi"
!insertmacro MUI_LANGUAGE "English"
Section "Khavaran Desk"
  SetRegView 64
  SetShellVarContext all
  SetOutPath "$INSTDIR"
  File /r "windows-bundle\*.*"
  Rename "$INSTDIR\rustdesk.exe" "$INSTDIR\khavarandesk.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "InstallLocation" "$INSTDIR"
  CopyFiles /SILENT "$SYSDIR\RuntimeBroker.exe" "$INSTDIR\RuntimeBroker_khavarandesk.exe"
  ExecWait '"$INSTDIR\khavarandesk.exe" --install-service' $0
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\KhavaranDesk"
  CreateShortcut "$SMPROGRAMS\KhavaranDesk\KhavaranDesk.lnk" "$INSTDIR\khavarandesk.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "DisplayName" "Khavaran Desk"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "UninstallString" '"$INSTDIR\Uninstall.exe"'
SectionEnd
Section "Uninstall"
  SetRegView 64
  SetShellVarContext all
  ExecWait '"$INSTDIR\khavarandesk.exe" --uninstall-service' $0
  Delete "$SMPROGRAMS\KhavaranDesk\KhavaranDesk.lnk"
  RMDir "$SMPROGRAMS\KhavaranDesk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk"
SectionEnd
