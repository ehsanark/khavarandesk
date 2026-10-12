Unicode true
!include "MUI2.nsh"
Name "Khavaran Desk"
OutFile "KhavaranDesk-Setup-x64.exe"
InstallDir "$PROGRAMFILES64\KhavaranDesk"
RequestExecutionLevel admin
!define MUI_WELCOMEPAGE_TITLE "Welcome to Khavaran Desk"
!define MUI_WELCOMEPAGE_TEXT "Install or update Khavaran Desk for your team.$\r$\n$\r$\nActive Khavaran Desk sessions will close during setup."
!define MUI_HEADER_TEXT "Khavaran Desk"
!define MUI_HEADER_SUBTEXT "Secure remote access for your team"
!define MUI_FINISHPAGE_TITLE "Khavaran Desk is ready"
!define MUI_FINISHPAGE_RUN "$INSTDIR\khavarandesk.exe"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
Section "Khavaran Desk"
  SetRegView 64
  SetShellVarContext all
  SetOutPath "$INSTDIR"
  ; Stop only this product before replacing in-use executables and DLLs.
  nsExec::ExecToLog '"$SYSDIR\sc.exe" stop KhavaranDesk'
  Pop $0
  nsExec::ExecToLog '"$SYSDIR\taskkill.exe" /F /T /IM khavarandesk.exe'
  Pop $0
  nsExec::ExecToLog '"$SYSDIR\taskkill.exe" /F /T /IM RuntimeBroker_khavarandesk.exe'
  Pop $0
  Sleep 1500
  ClearErrors
  Delete "$INSTDIR\khavarandesk.exe"
  IfErrors install_failed
  SetOverwrite on
  File /r "windows-bundle\*.*"
  IfErrors install_failed
  Rename "$INSTDIR\rustdesk.exe" "$INSTDIR\khavarandesk.exe"
  IfErrors install_failed
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "InstallLocation" "$INSTDIR"
  CopyFiles /SILENT "$SYSDIR\RuntimeBroker.exe" "$INSTDIR\RuntimeBroker_khavarandesk.exe"
  ExecWait '"$INSTDIR\khavarandesk.exe" --install-service' $0
  ; Check the registered service after the native installer returns.
  nsExec::ExecToLog '"$SYSDIR\sc.exe" start KhavaranDesk'
  Pop $0
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\KhavaranDesk"
  CreateShortcut "$SMPROGRAMS\KhavaranDesk\KhavaranDesk.lnk" "$INSTDIR\khavarandesk.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "DisplayName" "Khavaran Desk"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\KhavaranDesk" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  Goto install_done
install_failed:
  MessageBox MB_ICONSTOP "Setup could not replace the previous version. Close Khavaran Desk and run setup again."
  SetErrorLevel 1
  Abort
install_done:
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
