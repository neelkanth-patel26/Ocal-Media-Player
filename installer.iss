; ============================================================
;  Ocal Media Player - Inno Setup 6 Installer
;  Version  : 1.0.2
;  Builder  : Ocal Software under Gaming Network Studio
;  Compiler : Inno Setup 6
; ============================================================

[Setup]
AppId={{C72A0D45-B8E3-4E8A-9BF7-9A1D8DF12A74}
AppName=Ocal Media Player
AppVersion=1.0.2
AppVerName=Ocal Media Player 1.0.2
AppPublisher=Ocal Software under Gaming Network Studio
AppPublisherURL=https://github.com/neelkanth-patel26/Ocal-Media-Player
AppSupportURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/issues
AppUpdatesURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/releases
AppCopyright=Copyright (C) 2026 Ocal Software under Gaming Network Studio
DefaultDirName={autopf}\Ocal Media Player
DefaultGroupName=Ocal Media Player
OutputDir=dist-installer
OutputBaseFilename=Ocal-Media-Player-1.0.2-Setup
SetupIconFile=assets\app-icon.ico
LicenseFile=LICENSE
Compression=lzma2/ultra64
LZMAUseSeparateProcess=yes
SolidCompression=yes
DiskSpanning=no
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
ArchitecturesAllowed=x64compatible x64
ArchitecturesInstallIn64BitMode=x64compatible x64
MinVersion=10.0.17763
UninstallDisplayIcon={app}\Ocal Media Player.exe
UninstallDisplayName=Ocal Media Player
VersionInfoVersion=1.0.2.0
VersionInfoCompany=Ocal Software under Gaming Network Studio
VersionInfoDescription=Ocal Media Player Installer
VersionInfoProductName=Ocal Media Player
VersionInfoProductVersion=1.0.2
WizardStyle=modern
ShowLanguageDialog=no
CloseApplications=no
RestartIfNeededByRun=no
UsedUserAreasWarning=no

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "fileassoc";   Description: "Register Ocal Media Player in Windows Default Apps & associate media file types"; GroupDescription: "Windows Integration:"; Flags: checkedonce

[Files]
Source: "dist\Ocal Media Player\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\app-icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\installer_logo.bmp"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\installer_update_logo.bmp"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\installer_logo.bmp"; Flags: dontcopy
Source: "assets\installer_update_logo.bmp"; Flags: dontcopy
Source: "LICENSE"; Flags: dontcopy

[Icons]
Name: "{autoprograms}\Ocal Media Player"; Filename: "{app}\Ocal Media Player.exe"; IconFilename: "{app}\assets\app-icon.ico"; AppUserModelID: "OcalSoftware.OcalMediaPlayer"
Name: "{group}\Uninstall Ocal Media Player"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Ocal Media Player"; Filename: "{app}\Ocal Media Player.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\app-icon.ico"; AppUserModelID: "OcalSoftware.OcalMediaPlayer"

[Registry]
; -------------------------------------------------------------
; 1. Windows RegisteredApplications Registration (Visible in Windows Default Apps)
; -------------------------------------------------------------
Root: HKCU; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "Ocal Media Player"; ValueData: "Software\Clients\Media\Ocal Media Player\Capabilities"; Flags: uninsdeletevalue; Tasks: fileassoc

; -------------------------------------------------------------
; 2. Media Client Registration & Capabilities
; -------------------------------------------------------------
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player"; ValueType: string; ValueData: "Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "Fluent Design Audio & Video Media Player for Windows 11"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities"; ValueType: string; ValueName: "ApplicationIcon"; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc

; Capabilities FileAssociations
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mp3"; ValueData: "OcalMediaPlayer.mp3"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".flac"; ValueData: "OcalMediaPlayer.flac"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".wav"; ValueData: "OcalMediaPlayer.wav"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".m4a"; ValueData: "OcalMediaPlayer.m4a"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".aac"; ValueData: "OcalMediaPlayer.aac"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".ogg"; ValueData: "OcalMediaPlayer.ogg"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".opus"; ValueData: "OcalMediaPlayer.opus"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".wma"; ValueData: "OcalMediaPlayer.wma"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mp4"; ValueData: "OcalMediaPlayer.mp4"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mkv"; ValueData: "OcalMediaPlayer.mkv"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".avi"; ValueData: "OcalMediaPlayer.avi"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mov"; ValueData: "OcalMediaPlayer.mov"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".wmv"; ValueData: "OcalMediaPlayer.wmv"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Clients\Media\Ocal Media Player\Capabilities\FileAssociations"; ValueType: string; ValueName: ".webm"; ValueData: "OcalMediaPlayer.webm"; Flags: uninsdeletekey; Tasks: fileassoc

; -------------------------------------------------------------
; 3. Applications\Ocal Media Player.exe Registration
; -------------------------------------------------------------
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe"; ValueType: string; ValueName: "ApplicationCompany"; ValueData: "Ocal Software under Gaming Network Studio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".mp3"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".flac"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".wav"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".m4a"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".aac"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".ogg"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".opus"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".wma"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".mp4"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".mkv"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".avi"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".mov"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".wmv"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\Applications\Ocal Media Player.exe\SupportedTypes"; ValueType: string; ValueName: ".webm"; ValueData: ""; Flags: uninsdeletekey; Tasks: fileassoc

; -------------------------------------------------------------
; 4. Audio ProgIDs (Displays app icon in File Explorer)
; -------------------------------------------------------------
; .mp3
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3"; ValueType: string; ValueData: "MP3 Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp3\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .flac
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac"; ValueType: string; ValueData: "FLAC Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.flac\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .wav
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav"; ValueType: string; ValueData: "WAV Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wav\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .m4a
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a"; ValueType: string; ValueData: "M4A Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.m4a\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .aac
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.aac"; ValueType: string; ValueData: "AAC Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.aac"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.aac\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.aac\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .ogg
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.ogg"; ValueType: string; ValueData: "OGG Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.ogg"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.ogg\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.ogg\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .opus
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.opus"; ValueType: string; ValueData: "Opus Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.opus"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.opus\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.opus\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .wma
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wma"; ValueType: string; ValueData: "WMA Audio File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wma"; ValueType: string; ValueName: "PerceivedType"; ValueData: "audio"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wma\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wma\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; -------------------------------------------------------------
; 5. Video ProgIDs (Preserves Windows video thumbnail preview with app badge overlay)
; -------------------------------------------------------------
; .mp4
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4"; ValueType: string; ValueData: "MP4 Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mp4\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .mkv
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv"; ValueType: string; ValueData: "MKV Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\shell\Play"; ValueType: string; ValueData: "Play with Ocal Media Player"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\shell\Play"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\assets\app-icon.ico"""; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mkv\shell\Play\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .avi
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi"; ValueType: string; ValueData: "AVI Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.avi\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .mov
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov"; ValueType: string; ValueData: "QuickTime Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.mov\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .wmv
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv"; ValueType: string; ValueData: "WMV Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.wmv\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; .webm
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm"; ValueType: string; ValueData: "WebM Video File (Ocal Media Player)"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm"; ValueType: dword; ValueName: "Treatment"; ValueData: 3; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm"; ValueType: dword; ValueName: "ThumbnailCutoff"; ValueData: 1; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.webm\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; -------------------------------------------------------------
; 6. Extension OpenWithProgids & ShellEx Wireup
; -------------------------------------------------------------
; Audio
Root: HKCU; Subkey: "Software\Classes\.mp3\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.mp3"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.flac\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.flac"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wav\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.wav"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.m4a\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.m4a"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.aac\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.aac"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.ogg\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.ogg"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.opus\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.opus"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wma\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.wma"; Flags: uninsdeletevalue; Tasks: fileassoc

; Video - with ShellEx and PerceivedType
Root: HKCU; Subkey: "Software\Classes\.mp4"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mp4\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.mp4"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mp4\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mp4\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

Root: HKCU; Subkey: "Software\Classes\.mkv"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mkv\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.mkv"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mkv\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mkv\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

Root: HKCU; Subkey: "Software\Classes\.avi"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.avi\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.avi"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.avi\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.avi\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

Root: HKCU; Subkey: "Software\Classes\.mov"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mov\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.mov"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mov\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mov\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

Root: HKCU; Subkey: "Software\Classes\.wmv"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wmv\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.wmv"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wmv\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wmv\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

Root: HKCU; Subkey: "Software\Classes\.webm"; ValueType: string; ValueName: "PerceivedType"; ValueData: "video"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.webm\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.webm"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.webm\ShellEx\{{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.webm\ShellEx\{{e357fccd-a995-4576-b01f-234630154e96}"; ValueType: string; ValueData: "{{9DBD2C50-62AD-11D0-B806-00C04FD706EC}"; Flags: uninsdeletevalue; Tasks: fileassoc

[Run]
Filename: "{app}\Ocal Media Player.exe"; Description: "{cm:LaunchProgram,Ocal Media Player}"; Flags: nowait postinstall skipifsilent

[Code]
function DwmSetWindowAttribute(hWnd: HWND; dwAttribute: DWORD; var pvAttribute: DWORD; cbAttribute: DWORD): HRESULT;
  external 'DwmSetWindowAttribute@dwmapi.dll stdcall delayload';

procedure SHChangeNotify(wEventId: LongInt; uFlags: Cardinal; dwItem1: Cardinal; dwItem2: Cardinal);
  external 'SHChangeNotify@shell32.dll stdcall';

const
  SHCNE_ASSOCCHANGED = $08000000;
  SHCNF_FLUSH        = $1000;

  DWMWA_WINDOW_CORNER_PREFERENCE = 33;
  DWMWCP_ROUND                   = 2;
  DWMWA_CAPTION_COLOR            = 35;
  DWMWA_TEXT_COLOR               = 36;

  COLOR_TEXT          = $2A170F; // #0F172A (Deep slate typography)
  COLOR_MUTED         = $8B7464; // #64748B (Slate muted)
  COLOR_HINT          = $B8A394; // #94A3B8 (Light slate hint)
  COLOR_ACCENT_INSTALL= $596FFF; // #FF6F59 (Ocal Coral)
  COLOR_ACCENT_UPDATE = $78B400; // #00B478 (Emerald Green)
  COLOR_BOX_BG        = $FCFAF8; // #F8FAFC (Soft modern panel surface)
  COLOR_HEADER        = $695547; // #475569 (Label text)

var
  IsUpdateMode: Boolean;
  CurrentAccent: TColor;

  PnlMain: TPanel;
  PnlWelcome: TPanel;
  PnlOptionsBorder: TPanel;
  PnlOptions: TPanel;
  PnlInstalling: TPanel;
  PnlFinished: TPanel;
  PnlTerms: TPanel;

  ImgLogo: TBitmapImage;
  LblBrandTitle: TLabel;
  LblBrandSub: TLabel;
  LblVersion: TLabel;
  BtnInstall: TNewButton;
  LblLegal: TLabel;
  LblLegal2: TLabel;
  BtnToggleOptions: TLabel;
  BtnViewTermsTopLink: TLabel;

  LblTermsTitle: TLabel;
  LblTermsSub: TLabel;
  BtnTabHighlights: TNewButton;
  BtnTabPrivacy: TNewButton;
  BtnTabFullEula: TNewButton;
  PnlViewHighlights: TPanel;
  PnlViewPrivacy: TPanel;
  PnlViewFullEula: TPanel;
  PnlTermsBorder: TPanel;
  ChkAcceptTerms: TNewCheckBox;
  BtnBackFromTerms: TNewButton;
  BtnAcceptFromTerms: TNewButton;
  BtnOpenLicenseExternal: TLabel;

  // Fresh install options
  LblPathTitle: TLabel;
  EditPath: TNewEdit;
  BtnBrowse: TNewButton;
  Sep1: TBevel;
  ChkDefaultMedia: TNewCheckBox;
  LblDefMediaSub: TLabel;
  ChkDesktopIcon: TNewCheckBox;
  LblDesktopSub: TLabel;
  ChkShellThumbnails: TNewCheckBox;
  LblShellThumbSub: TLabel;
  ChkAllUsers: TNewCheckBox;
  LblAllUsersSub: TLabel;

  // Update mode options widgets
  PnlUpdateCard: TPanel;
  LblUpdateCardTitle: TLabel;
  LblUpdatePathVal: TLabel;
  LblUpdateSafe1: TLabel;
  LblUpdateSafe2: TLabel;
  LblUpdateSafe3: TLabel;

  ImgInstallLogo: TBitmapImage;
  LblInstallTitle: TLabel;
  LblInstallStatus: TLabel;
  LblProgressPct: TLabel;
  PnlProgressTrack: TPanel;
  PnlProgressFill: TPanel;

  ImgFinishLogo: TBitmapImage;
  LblFinishedTitle: TLabel;
  LblFinishedSub: TLabel;
  BtnFinishLaunch: TNewButton;

  OptionsVisible: Boolean;

function DetectIsUpdateMode(): Boolean;
var
  InstalledExe: string;
begin
  if Pos('/UPDATE', UpperCase(GetCmdTail)) > 0 then
  begin
    Result := True;
    Exit;
  end;
  if RegKeyExists(HKCU, 'Software\Clients\Media\Ocal Media Player') or
     RegKeyExists(HKLM, 'Software\Clients\Media\Ocal Media Player') or
     RegValueExists(HKCU, 'Software\RegisteredApplications', 'Ocal Media Player') then
  begin
    Result := True;
    Exit;
  end;
  InstalledExe := ExpandConstant('{autopf}\Ocal Media Player\Ocal Media Player.exe');
  if FileExists(InstalledExe) then
  begin
    Result := True;
    Exit;
  end;
  Result := False;
end;

procedure ApplyModernTitleBar(FormHandle: HWND);
var
  CaptionColor, TextColor, CornerPref: DWORD;
begin
  CaptionColor := $00FFFFFF;
  DwmSetWindowAttribute(FormHandle, DWMWA_CAPTION_COLOR, CaptionColor, 4);

  TextColor := $002A170F;
  DwmSetWindowAttribute(FormHandle, DWMWA_TEXT_COLOR, TextColor, 4);

  CornerPref := DWMWCP_ROUND;
  DwmSetWindowAttribute(FormHandle, DWMWA_WINDOW_CORNER_PREFERENCE, CornerPref, 4);
end;

procedure ChkAllUsersClick(Sender: TObject);
begin
  if ChkAllUsers.Checked then
    EditPath.Text := ExpandConstant('{commonpf}\Ocal Media Player')
  else
    EditPath.Text := ExpandConstant('{autopf}\Ocal Media Player');
end;

procedure BtnToggleOptionsClick(Sender: TObject);
begin
  OptionsVisible := not OptionsVisible;
  PnlOptionsBorder.Visible := OptionsVisible;
  if OptionsVisible then
  begin
    if IsUpdateMode then
      BtnToggleOptions.Caption := 'Hide details ▲'
    else
      BtnToggleOptions.Caption := 'Hide options ▲';
    WizardForm.ClientHeight := ScaleY(464);
    PnlMain.Height := WizardForm.ClientHeight;
    PnlWelcome.Height := WizardForm.ClientHeight;
  end
  else
  begin
    if IsUpdateMode then
      BtnToggleOptions.Caption := 'Update details & options ▾'
    else
      BtnToggleOptions.Caption := 'Installation options ▾';
    WizardForm.ClientHeight := ScaleY(256);
    PnlMain.Height := WizardForm.ClientHeight;
    PnlWelcome.Height := WizardForm.ClientHeight;
  end;
end;

procedure BtnBrowseClick(Sender: TObject);
var
  NewDir: string;
begin
  NewDir := EditPath.Text;
  if BrowseForFolder('Select Installation Folder', NewDir, True) then
  begin
    EditPath.Text := NewDir;
  end;
end;

procedure SetTermsTabState(TabIdx: Integer);
begin
  if TabIdx = 0 then
  begin
    BtnTabHighlights.Caption := '✓  Key Highlights';
    BtnTabHighlights.Font.Style := [fsBold];
  end
  else
  begin
    BtnTabHighlights.Caption := 'Key Highlights';
    BtnTabHighlights.Font.Style := [];
  end;

  if TabIdx = 1 then
  begin
    BtnTabPrivacy.Caption := '✓  Codecs & Privacy';
    BtnTabPrivacy.Font.Style := [fsBold];
  end
  else
  begin
    BtnTabPrivacy.Caption := 'Codecs & Privacy';
    BtnTabPrivacy.Font.Style := [];
  end;

  if TabIdx = 2 then
  begin
    BtnTabFullEula.Caption := '✓  Full Legal Text';
    BtnTabFullEula.Font.Style := [fsBold];
  end
  else
  begin
    BtnTabFullEula.Caption := 'Full Legal Text';
    BtnTabFullEula.Font.Style := [];
  end;

  PnlViewHighlights.Visible := (TabIdx = 0);
  PnlViewPrivacy.Visible    := (TabIdx = 1);
  PnlViewFullEula.Visible   := (TabIdx = 2);

  if TabIdx = 0 then
    LblTermsSub.Caption := 'Hardware acceleration, zero-telemetry local privacy, and permissive MIT license.'
  else if TabIdx = 1 then
    LblTermsSub.Caption := 'Native LibVLC 4 engine, multi-ratio video detection, and Shell thumbnails.'
  else
  begin
    LblTermsSub.Caption := 'Official binding MIT License agreement and third-party notices.';
    WizardForm.LicenseMemo.Show;
  end;
end;

procedure TabHighlightsClick(Sender: TObject);
begin
  SetTermsTabState(0);
end;

procedure TabPrivacyClick(Sender: TObject);
begin
  SetTermsTabState(1);
end;

procedure TabFullEulaClick(Sender: TObject);
begin
  SetTermsTabState(2);
end;

procedure ChkAcceptTermsClick(Sender: TObject);
begin
  BtnAcceptFromTerms.Enabled := ChkAcceptTerms.Checked;
end;

procedure CreateFeatureCard(ParentPnl: TPanel; LeftPx, TopPx, WidthPx, HeightPx: Integer; BadgeTxt, TitleTxt, DescTxt: string; BadgeColor: TColor);
var
  BorderPnl, InnerPnl: TPanel;
  LblBadge, LblTitle, LblDesc: TLabel;
begin
  BorderPnl := TPanel.Create(WizardForm);
  BorderPnl.Parent := ParentPnl;
  BorderPnl.SetBounds(LeftPx, TopPx, WidthPx, HeightPx);
  BorderPnl.Color := $E2E8F0;
  BorderPnl.BevelOuter := bvNone;

  InnerPnl := TPanel.Create(WizardForm);
  InnerPnl.Parent := BorderPnl;
  InnerPnl.SetBounds(ScaleX(1), ScaleY(1), BorderPnl.Width - ScaleX(2), BorderPnl.Height - ScaleY(2));
  InnerPnl.Color := COLOR_BOX_BG;
  InnerPnl.BevelOuter := bvNone;

  LblBadge := TLabel.Create(WizardForm);
  LblBadge.Parent := InnerPnl;
  LblBadge.ShowAccelChar := False;
  LblBadge.Caption := BadgeTxt;
  LblBadge.Font.Name := 'Segoe UI';
  LblBadge.Font.Size := 7;
  LblBadge.Font.Style := [fsBold];
  LblBadge.Font.Color := BadgeColor;
  LblBadge.Left := ScaleX(12);
  LblBadge.Top := ScaleY(9);

  LblTitle := TLabel.Create(WizardForm);
  LblTitle.Parent := InnerPnl;
  LblTitle.ShowAccelChar := False;
  LblTitle.Caption := TitleTxt;
  LblTitle.Font.Name := 'Segoe UI';
  LblTitle.Font.Size := 9;
  LblTitle.Font.Style := [fsBold];
  LblTitle.Font.Color := COLOR_TEXT;
  LblTitle.Left := ScaleX(12);
  LblTitle.Top := ScaleY(25);

  LblDesc := TLabel.Create(WizardForm);
  LblDesc.Parent := InnerPnl;
  LblDesc.ShowAccelChar := False;
  LblDesc.Caption := DescTxt;
  LblDesc.Font.Name := 'Segoe UI';
  LblDesc.Font.Size := 8;
  LblDesc.Font.Color := COLOR_MUTED;
  LblDesc.WordWrap := True;
  LblDesc.Left := ScaleX(12);
  LblDesc.Top := ScaleY(45);
  LblDesc.Width := InnerPnl.Width - ScaleX(24);
end;

procedure BtnViewTermsClick(Sender: TObject);
begin
  PnlWelcome.Hide;
  PnlTerms.Show;
  WizardForm.ClientHeight := ScaleY(500);
  PnlMain.Height := WizardForm.ClientHeight;
  PnlTerms.Height := WizardForm.ClientHeight;
  SetTermsTabState(0);
end;

procedure BtnBackFromTermsClick(Sender: TObject);
begin
  PnlTerms.Hide;
  PnlWelcome.Show;
  if OptionsVisible then
    WizardForm.ClientHeight := ScaleY(464)
  else
    WizardForm.ClientHeight := ScaleY(256);
  PnlMain.Height := WizardForm.ClientHeight;
  PnlWelcome.Height := WizardForm.ClientHeight;
end;

procedure BtnOpenLicenseExternalClick(Sender: TObject);
var
  LicenseFile: string;
  ErrorCode: Integer;
begin
  LicenseFile := ExpandConstant('{tmp}\LICENSE');
  if not FileExists(LicenseFile) then
    ExtractTemporaryFile('LICENSE');
  ShellExec('open', LicenseFile, '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
end;

procedure BtnInstallClick(Sender: TObject);
var
  Tasks: string;
begin
  if not IsUpdateMode then
  begin
    WizardForm.DirEdit.Text := EditPath.Text;
    Tasks := '';
    if ChkDesktopIcon.Checked then
      Tasks := Tasks + 'desktopicon';
    if ChkDefaultMedia.Checked then
    begin
      if Tasks <> '' then Tasks := Tasks + ',';
      Tasks := Tasks + 'fileassoc';
    end;
    WizardSelectTasks(Tasks);
  end
  else
  begin
    Tasks := 'fileassoc,desktopicon';
    WizardSelectTasks(Tasks);
  end;

  WizardForm.NextButton.OnClick(WizardForm.NextButton);
end;

procedure BtnFinishLaunchClick(Sender: TObject);
begin
  WizardForm.NextButton.OnClick(WizardForm.NextButton);
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  if (PageID = wpLicense) or 
     (PageID = wpSelectDir) or 
     (PageID = wpSelectComponents) or 
     (PageID = wpSelectProgramGroup) or 
     (PageID = wpSelectTasks) or 
     (PageID = wpReady) then
  begin
    Result := True;
  end
  else
    Result := False;
end;

procedure CurInstallProgressChanged(CurProgress, MaxProgress: Integer);
var
  Pct: Integer;
  NewW: Integer;
begin
  if MaxProgress > 0 then
  begin
    Pct := (CurProgress * 100) div MaxProgress;
    NewW := (PnlProgressTrack.Width * CurProgress) div MaxProgress;
    if NewW > PnlProgressTrack.Width then
      NewW := PnlProgressTrack.Width;
    PnlProgressFill.Width := NewW;
    if IsUpdateMode then
      LblInstallStatus.Caption := 'Upgrading player engine, LibVLC 4 codecs, and assets...'
    else
      LblInstallStatus.Caption := 'Extracting player engine, LibVLC 4 codecs, and assets...';
    LblProgressPct.Caption := Format('%d%%', [Pct]);
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    PnlWelcome.Show;
    PnlInstalling.Hide;
    PnlFinished.Hide;
  end
  else if CurPageID = wpInstalling then
  begin
    PnlWelcome.Hide;
    PnlOptionsBorder.Hide;
    PnlInstalling.Show;
    PnlFinished.Hide;
    WizardForm.ClientHeight := ScaleY(140);
    PnlMain.Height := WizardForm.ClientHeight;
    PnlInstalling.Height := WizardForm.ClientHeight;
  end
  else if CurPageID = wpFinished then
  begin
    PnlWelcome.Hide;
    PnlOptionsBorder.Hide;
    PnlInstalling.Hide;
    PnlFinished.Show;
    WizardForm.ClientHeight := ScaleY(160);
    PnlMain.Height := WizardForm.ClientHeight;
    PnlFinished.Height := WizardForm.ClientHeight;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_FLUSH, 0, 0);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_FLUSH, 0, 0);
  end;
end;

procedure InitializeWizard();
var
  LogoPath: string;
  PnlSeparator: TPanel;
  BannerBorder, BannerInner: TPanel;
  LblBanner: TLabel;
begin
  OptionsVisible := False;
  IsUpdateMode := DetectIsUpdateMode();

  if IsUpdateMode then
  begin
    CurrentAccent := COLOR_ACCENT_UPDATE;
    WizardForm.Caption := 'Ocal Media Player Updater';
  end
  else
  begin
    CurrentAccent := COLOR_ACCENT_INSTALL;
    WizardForm.Caption := 'Ocal Media Player Setup';
  end;

  WizardForm.ClientWidth := ScaleX(560);
  WizardForm.ClientHeight := ScaleY(256);
  WizardForm.Position := poScreenCenter;
  WizardForm.Color := clWhite;

  ApplyModernTitleBar(WizardForm.Handle);

  // Hide default wizard chrome
  WizardForm.OuterNotebook.Hide;
  WizardForm.InnerNotebook.Hide;
  WizardForm.Bevel.Hide;
  WizardForm.BeveledLabel.Hide;
  WizardForm.BackButton.Hide;
  WizardForm.NextButton.Hide;
  WizardForm.CancelButton.Hide;

  // Root canvas panel
  PnlMain := TPanel.Create(WizardForm);
  PnlMain.Parent := WizardForm;
  PnlMain.SetBounds(0, 0, WizardForm.ClientWidth, WizardForm.ClientHeight);
  PnlMain.Color := clWhite;
  PnlMain.BevelOuter := bvNone;

  // 1. WELCOME / UPDATE HERO SCREEN
  PnlWelcome := TPanel.Create(WizardForm);
  PnlWelcome.Parent := PnlMain;
  PnlWelcome.SetBounds(0, 0, PnlMain.Width, PnlMain.Height);
  PnlWelcome.Color := clWhite;
  PnlWelcome.BevelOuter := bvNone;

  ExtractTemporaryFile('installer_logo.bmp');
  ExtractTemporaryFile('installer_update_logo.bmp');
  if IsUpdateMode then
    LogoPath := ExpandConstant('{tmp}\installer_update_logo.bmp')
  else
    LogoPath := ExpandConstant('{tmp}\installer_logo.bmp');

  if FileExists(LogoPath) then
  begin
    ImgLogo := TBitmapImage.Create(WizardForm);
    ImgLogo.Parent := PnlWelcome;
    ImgLogo.SetBounds(ScaleX(32), ScaleY(24), ScaleX(56), ScaleY(56));
    ImgLogo.Stretch := True;
    ImgLogo.Bitmap.LoadFromFile(LogoPath);
  end;

  LblBrandTitle := TLabel.Create(WizardForm);
  LblBrandTitle.Parent := PnlWelcome;
  if IsUpdateMode then
    LblBrandTitle.Caption := 'Updating Ocal Media Player'
  else
    LblBrandTitle.Caption := 'Ocal Media Player';
  LblBrandTitle.Font.Name := 'Segoe UI';
  LblBrandTitle.Font.Size := 20;
  LblBrandTitle.Font.Color := COLOR_TEXT;
  LblBrandTitle.Font.Style := [fsBold];
  LblBrandTitle.Left := ScaleX(104);
  LblBrandTitle.Top := ScaleY(18);

  LblBrandSub := TLabel.Create(WizardForm);
  LblBrandSub.Parent := PnlWelcome;
  if IsUpdateMode then
    LblBrandSub.Caption := 'Preserving your playlists, audio profiles, favorites, and settings'
  else
    LblBrandSub.Caption := 'Ultra-responsive Windows 11 Fluent Media Player & LibVLC 4 Engine';
  LblBrandSub.Font.Name := 'Segoe UI';
  LblBrandSub.Font.Size := 10;
  LblBrandSub.Font.Color := COLOR_MUTED;
  LblBrandSub.Left := ScaleX(106);
  LblBrandSub.Top := ScaleY(50);

  LblVersion := TLabel.Create(WizardForm);
  LblVersion.Parent := PnlWelcome;
  if IsUpdateMode then
    LblVersion.Caption := '⚡  Update Detected  •  Upgrading to v1.0.2'
  else
    LblVersion.Caption := '✦  New Installation  •  Version 1.0.2';
  LblVersion.Font.Name := 'Segoe UI';
  LblVersion.Font.Size := 8;
  LblVersion.Font.Color := CurrentAccent;
  LblVersion.Font.Style := [fsBold];
  LblVersion.Left := ScaleX(106);
  LblVersion.Top := ScaleY(72);

  PnlSeparator := TPanel.Create(WizardForm);
  PnlSeparator.Parent := PnlWelcome;
  PnlSeparator.SetBounds(ScaleX(32), ScaleY(98), ScaleX(496), ScaleY(1));
  PnlSeparator.Color := $E2E8F0;
  PnlSeparator.BevelOuter := bvNone;

  BtnInstall := TNewButton.Create(WizardForm);
  BtnInstall.Parent := PnlWelcome;
  if IsUpdateMode then
    BtnInstall.Caption := 'Install Update Now'
  else
    BtnInstall.Caption := 'Accept and Install';
  BtnInstall.Font.Name := 'Segoe UI';
  BtnInstall.Font.Size := 11;
  BtnInstall.Font.Style := [fsBold];
  BtnInstall.SetBounds(ScaleX(32), ScaleY(114), ScaleX(496), ScaleY(42));
  BtnInstall.OnClick := @BtnInstallClick;

  LblLegal := TLabel.Create(WizardForm);
  LblLegal.Parent := PnlWelcome;
  if IsUpdateMode then
    LblLegal.Caption := 'By clicking "Install Update Now", you agree to update Ocal Media Player to v1.0.2.'
  else
    LblLegal.Caption := 'By clicking "Accept and Install", you agree to the Ocal Media Player Terms of Service,';
  LblLegal.Font.Name := 'Segoe UI';
  LblLegal.Font.Size := 8;
  LblLegal.Font.Color := COLOR_MUTED;
  LblLegal.Left := ScaleX(32);
  LblLegal.Top := ScaleY(166);
  LblLegal.AutoSize := True;
  LblLegal.Cursor := crHand;
  LblLegal.OnClick := @BtnViewTermsClick;

  LblLegal2 := TLabel.Create(WizardForm);
  LblLegal2.Parent := PnlWelcome;
  if IsUpdateMode then
    LblLegal2.Caption := 'All your existing playlists, equalizer profiles, and bookmarks are safely kept.'
  else
    LblLegal2.Caption := 'End User License Agreement (EULA), and Zero-Telemetry Privacy Policy.';
  LblLegal2.Font.Name := 'Segoe UI';
  LblLegal2.Font.Size := 8;
  LblLegal2.Font.Color := COLOR_MUTED;
  LblLegal2.Left := ScaleX(32);
  LblLegal2.Top := ScaleY(184);
  LblLegal2.AutoSize := True;
  LblLegal2.Cursor := crHand;
  LblLegal2.OnClick := @BtnViewTermsClick;

  BtnToggleOptions := TLabel.Create(WizardForm);
  BtnToggleOptions.Parent := PnlWelcome;
  if IsUpdateMode then
    BtnToggleOptions.Caption := 'Update details & options ▾'
  else
    BtnToggleOptions.Caption := 'Installation options ▾';
  BtnToggleOptions.Font.Name := 'Segoe UI';
  BtnToggleOptions.Font.Size := 8;
  BtnToggleOptions.Font.Color := CurrentAccent;
  BtnToggleOptions.Font.Style := [fsBold];
  BtnToggleOptions.Cursor := crHand;
  BtnToggleOptions.Left := ScaleX(32);
  BtnToggleOptions.Top := ScaleY(208);
  BtnToggleOptions.OnClick := @BtnToggleOptionsClick;

  BtnViewTermsTopLink := TLabel.Create(WizardForm);
  BtnViewTermsTopLink.Parent := PnlWelcome;
  BtnViewTermsTopLink.ShowAccelChar := False;
  if IsUpdateMode then
    BtnViewTermsTopLink.Caption := 'Read What''s New & License Terms ↗'
  else
    BtnViewTermsTopLink.Caption := 'Read Full License & Audio Codecs Terms ↗';
  BtnViewTermsTopLink.Font.Name := 'Segoe UI';
  BtnViewTermsTopLink.Font.Size := 8;
  BtnViewTermsTopLink.Font.Color := CurrentAccent;
  BtnViewTermsTopLink.Font.Style := [fsBold, fsUnderline];
  BtnViewTermsTopLink.Cursor := crHand;
  BtnViewTermsTopLink.Left := ScaleX(308);
  BtnViewTermsTopLink.Top := ScaleY(208);
  BtnViewTermsTopLink.OnClick := @BtnViewTermsClick;

  // OPTIONS PANEL (Expandable Card)
  PnlOptionsBorder := TPanel.Create(WizardForm);
  PnlOptionsBorder.Parent := PnlWelcome;
  PnlOptionsBorder.SetBounds(ScaleX(24), ScaleY(234), ScaleX(512), ScaleY(210));
  PnlOptionsBorder.Color := $E2E8F0;
  PnlOptionsBorder.BevelOuter := bvNone;
  PnlOptionsBorder.Visible := False;

  PnlOptions := TPanel.Create(WizardForm);
  PnlOptions.Parent := PnlOptionsBorder;
  PnlOptions.SetBounds(ScaleX(1), ScaleY(1), PnlOptionsBorder.Width - ScaleX(2), PnlOptionsBorder.Height - ScaleY(2));
  PnlOptions.Color := COLOR_BOX_BG;
  PnlOptions.BevelOuter := bvNone;

  if not IsUpdateMode then
  begin
    LblPathTitle := TLabel.Create(WizardForm);
    LblPathTitle.Parent := PnlOptions;
    LblPathTitle.Caption := 'INSTALLATION LOCATION';
    LblPathTitle.Font.Name := 'Segoe UI';
    LblPathTitle.Font.Color := COLOR_HEADER;
    LblPathTitle.Font.Size := 8;
    LblPathTitle.Font.Style := [fsBold];
    LblPathTitle.Left := ScaleX(16);
    LblPathTitle.Top := ScaleY(14);

    EditPath := TNewEdit.Create(WizardForm);
    EditPath.Parent := PnlOptions;
    EditPath.Text := ExpandConstant('{autopf}\Ocal Media Player');
    EditPath.Font.Name := 'Segoe UI';
    EditPath.Font.Size := 9;
    EditPath.SetBounds(ScaleX(16), ScaleY(34), ScaleX(388), ScaleY(26));

    BtnBrowse := TNewButton.Create(WizardForm);
    BtnBrowse.Parent := PnlOptions;
    BtnBrowse.Caption := 'Browse...';
    BtnBrowse.Font.Name := 'Segoe UI';
    BtnBrowse.Font.Size := 8;
    BtnBrowse.Font.Style := [fsBold];
    BtnBrowse.SetBounds(ScaleX(414), ScaleY(33), ScaleX(86), ScaleY(28));
    BtnBrowse.OnClick := @BtnBrowseClick;

    Sep1 := TBevel.Create(WizardForm);
    Sep1.Parent := PnlOptions;
    Sep1.Shape := bsTopLine;
    Sep1.SetBounds(ScaleX(16), ScaleY(72), PnlOptions.Width - ScaleX(32), ScaleY(2));

    ChkDefaultMedia := TNewCheckBox.Create(WizardForm);
    ChkDefaultMedia.Parent := PnlOptions;
    ChkDefaultMedia.Caption := 'Set as default media player';
    ChkDefaultMedia.Checked := True;
    ChkDefaultMedia.Font.Name := 'Segoe UI';
    ChkDefaultMedia.Font.Size := 9;
    ChkDefaultMedia.Font.Style := [fsBold];
    ChkDefaultMedia.Left := ScaleX(16);
    ChkDefaultMedia.Top := ScaleY(84);
    ChkDefaultMedia.Width := ScaleX(240);

    LblDefMediaSub := TLabel.Create(WizardForm);
    LblDefMediaSub.Parent := PnlOptions;
    LblDefMediaSub.Caption := 'Associate 14 audio & video formats with Ocal';
    LblDefMediaSub.Font.Name := 'Segoe UI';
    LblDefMediaSub.Font.Size := 8;
    LblDefMediaSub.Font.Color := COLOR_HINT;
    LblDefMediaSub.Left := ScaleX(36);
    LblDefMediaSub.Top := ScaleY(104);

    ChkDesktopIcon := TNewCheckBox.Create(WizardForm);
    ChkDesktopIcon.Parent := PnlOptions;
    ChkDesktopIcon.Caption := 'Create desktop shortcut';
    ChkDesktopIcon.Checked := True;
    ChkDesktopIcon.Font.Name := 'Segoe UI';
    ChkDesktopIcon.Font.Size := 9;
    ChkDesktopIcon.Font.Style := [fsBold];
    ChkDesktopIcon.Left := ScaleX(264);
    ChkDesktopIcon.Top := ScaleY(84);
    ChkDesktopIcon.Width := ScaleX(240);

    LblDesktopSub := TLabel.Create(WizardForm);
    LblDesktopSub.Parent := PnlOptions;
    LblDesktopSub.Caption := 'Quick access from your desktop';
    LblDesktopSub.Font.Name := 'Segoe UI';
    LblDesktopSub.Font.Size := 8;
    LblDesktopSub.Font.Color := COLOR_HINT;
    LblDesktopSub.Left := ScaleX(284);
    LblDesktopSub.Top := ScaleY(104);

    ChkShellThumbnails := TNewCheckBox.Create(WizardForm);
    ChkShellThumbnails.Parent := PnlOptions;
    ChkShellThumbnails.Caption := 'File Explorer thumbnail badges';
    ChkShellThumbnails.Checked := True;
    ChkShellThumbnails.Font.Name := 'Segoe UI';
    ChkShellThumbnails.Font.Size := 9;
    ChkShellThumbnails.Font.Style := [fsBold];
    ChkShellThumbnails.Left := ScaleX(16);
    ChkShellThumbnails.Top := ScaleY(134);
    ChkShellThumbnails.Width := ScaleX(240);

    LblShellThumbSub := TLabel.Create(WizardForm);
    LblShellThumbSub.Parent := PnlOptions;
    LblShellThumbSub.Caption := 'Video previews with custom player badges';
    LblShellThumbSub.Font.Name := 'Segoe UI';
    LblShellThumbSub.Font.Size := 8;
    LblShellThumbSub.Font.Color := COLOR_HINT;
    LblShellThumbSub.Left := ScaleX(36);
    LblShellThumbSub.Top := ScaleY(154);

    ChkAllUsers := TNewCheckBox.Create(WizardForm);
    ChkAllUsers.Parent := PnlOptions;
    ChkAllUsers.Caption := 'Install for all users';
    ChkAllUsers.Checked := False;
    ChkAllUsers.Font.Name := 'Segoe UI';
    ChkAllUsers.Font.Size := 9;
    ChkAllUsers.Font.Style := [fsBold];
    ChkAllUsers.Left := ScaleX(264);
    ChkAllUsers.Top := ScaleY(134);
    ChkAllUsers.Width := ScaleX(240);
    ChkAllUsers.OnClick := @ChkAllUsersClick;

    LblAllUsersSub := TLabel.Create(WizardForm);
    LblAllUsersSub.Parent := PnlOptions;
    LblAllUsersSub.Caption := 'System-wide install (Program Files)';
    LblAllUsersSub.Font.Name := 'Segoe UI';
    LblAllUsersSub.Font.Size := 8;
    LblAllUsersSub.Font.Color := COLOR_HINT;
    LblAllUsersSub.Left := ScaleX(284);
    LblAllUsersSub.Top := ScaleY(154);
  end
  else
  begin
    PnlUpdateCard := TPanel.Create(WizardForm);
    PnlUpdateCard.Parent := PnlOptions;
    PnlUpdateCard.SetBounds(ScaleX(16), ScaleY(14), PnlOptions.Width - ScaleX(32), ScaleY(44));
    PnlUpdateCard.Color := $ECFDF5;
    PnlUpdateCard.BevelOuter := bvNone;

    LblUpdateCardTitle := TLabel.Create(WizardForm);
    LblUpdateCardTitle.Parent := PnlUpdateCard;
    LblUpdateCardTitle.Caption := 'CURRENT INSTALLATION DETECTED';
    LblUpdateCardTitle.Font.Name := 'Segoe UI';
    LblUpdateCardTitle.Font.Size := 8;
    LblUpdateCardTitle.Font.Style := [fsBold];
    LblUpdateCardTitle.Font.Color := $047857;
    LblUpdateCardTitle.Left := ScaleX(12);
    LblUpdateCardTitle.Top := ScaleY(8);

    LblUpdatePathVal := TLabel.Create(WizardForm);
    LblUpdatePathVal.Parent := PnlUpdateCard;
    LblUpdatePathVal.Caption := ExpandConstant('{autopf}\Ocal Media Player');
    LblUpdatePathVal.Font.Name := 'Segoe UI';
    LblUpdatePathVal.Font.Size := 8;
    LblUpdatePathVal.Font.Color := COLOR_TEXT;
    LblUpdatePathVal.Left := ScaleX(12);
    LblUpdatePathVal.Top := ScaleY(24);

    LblUpdateSafe1 := TLabel.Create(WizardForm);
    LblUpdateSafe1.Parent := PnlOptions;
    LblUpdateSafe1.Caption := '✓  Playlists, favorites, acoustic equalizer profiles & bookmarks will be safely preserved';
    LblUpdateSafe1.Font.Name := 'Segoe UI';
    LblUpdateSafe1.Font.Size := 8;
    LblUpdateSafe1.Font.Style := [fsBold];
    LblUpdateSafe1.Font.Color := $065F46;
    LblUpdateSafe1.Left := ScaleX(16);
    LblUpdateSafe1.Top := ScaleY(74);

    LblUpdateSafe2 := TLabel.Create(WizardForm);
    LblUpdateSafe2.Parent := PnlOptions;
    LblUpdateSafe2.Caption := '✓  Upgrades LibVLC 4 engine, multi-aspect ratio & vertical video anti-stretch support';
    LblUpdateSafe2.Font.Name := 'Segoe UI';
    LblUpdateSafe2.Font.Size := 8;
    LblUpdateSafe2.Font.Style := [fsBold];
    LblUpdateSafe2.Font.Color := $065F46;
    LblUpdateSafe2.Left := ScaleX(16);
    LblUpdateSafe2.Top := ScaleY(104);

    LblUpdateSafe3 := TLabel.Create(WizardForm);
    LblUpdateSafe3.Parent := PnlOptions;
    LblUpdateSafe3.Caption := '✓  Refreshes Windows 11 Shell thumbnails, Default Apps registration & desktop icons';
    LblUpdateSafe3.Font.Name := 'Segoe UI';
    LblUpdateSafe3.Font.Size := 8;
    LblUpdateSafe3.Font.Style := [fsBold];
    LblUpdateSafe3.Font.Color := $065F46;
    LblUpdateSafe3.Left := ScaleX(16);
    LblUpdateSafe3.Top := ScaleY(134);
  end;

  // 2. TERMS & CONDITIONS / LICENSE SCREEN
  PnlTerms := TPanel.Create(WizardForm);
  PnlTerms.Parent := PnlMain;
  PnlTerms.SetBounds(0, 0, PnlMain.Width, ScaleY(496));
  PnlTerms.Color := clWhite;
  PnlTerms.BevelOuter := bvNone;
  PnlTerms.Visible := False;

  LblTermsTitle := TLabel.Create(WizardForm);
  LblTermsTitle.Parent := PnlTerms;
  LblTermsTitle.ShowAccelChar := False;
  LblTermsTitle.Caption := 'Terms of Service & License Agreement';
  LblTermsTitle.Font.Name := 'Segoe UI';
  LblTermsTitle.Font.Size := 13;
  LblTermsTitle.Font.Style := [fsBold];
  LblTermsTitle.Font.Color := COLOR_TEXT;
  LblTermsTitle.Left := ScaleX(28);
  LblTermsTitle.Top := ScaleY(14);

  LblTermsSub := TLabel.Create(WizardForm);
  LblTermsSub.Parent := PnlTerms;
  LblTermsSub.Caption := 'Hardware acceleration, zero-telemetry local privacy, and permissive MIT license.';
  LblTermsSub.Font.Name := 'Segoe UI';
  LblTermsSub.Font.Size := 8;
  LblTermsSub.Font.Color := COLOR_MUTED;
  LblTermsSub.Left := ScaleX(28);
  LblTermsSub.Top := ScaleY(38);

  BtnOpenLicenseExternal := TLabel.Create(WizardForm);
  BtnOpenLicenseExternal.Parent := PnlTerms;
  BtnOpenLicenseExternal.ShowAccelChar := False;
  BtnOpenLicenseExternal.Caption := 'Open in editor ↗';
  BtnOpenLicenseExternal.Font.Name := 'Segoe UI';
  BtnOpenLicenseExternal.Font.Size := 8;
  BtnOpenLicenseExternal.Font.Color := CurrentAccent;
  BtnOpenLicenseExternal.Font.Style := [fsBold, fsUnderline];
  BtnOpenLicenseExternal.Cursor := crHand;
  BtnOpenLicenseExternal.Left := ScaleX(420);
  BtnOpenLicenseExternal.Top := ScaleY(16);
  BtnOpenLicenseExternal.OnClick := @BtnOpenLicenseExternalClick;

  BtnTabHighlights := TNewButton.Create(WizardForm);
  BtnTabHighlights.Parent := PnlTerms;
  BtnTabHighlights.Caption := 'Key Highlights';
  BtnTabHighlights.Font.Name := 'Segoe UI';
  BtnTabHighlights.Font.Size := 9;
  BtnTabHighlights.SetBounds(ScaleX(28), ScaleY(56), ScaleX(160), ScaleY(32));
  BtnTabHighlights.OnClick := @TabHighlightsClick;

  BtnTabPrivacy := TNewButton.Create(WizardForm);
  BtnTabPrivacy.Parent := PnlTerms;
  BtnTabPrivacy.Caption := 'Codecs & Privacy';
  BtnTabPrivacy.Font.Name := 'Segoe UI';
  BtnTabPrivacy.Font.Size := 9;
  BtnTabPrivacy.SetBounds(ScaleX(200), ScaleY(56), ScaleX(160), ScaleY(32));
  BtnTabPrivacy.OnClick := @TabPrivacyClick;

  BtnTabFullEula := TNewButton.Create(WizardForm);
  BtnTabFullEula.Parent := PnlTerms;
  BtnTabFullEula.Caption := 'Full Legal Text';
  BtnTabFullEula.Font.Name := 'Segoe UI';
  BtnTabFullEula.Font.Size := 9;
  BtnTabFullEula.SetBounds(ScaleX(372), ScaleY(56), ScaleX(160), ScaleY(32));
  BtnTabFullEula.OnClick := @TabFullEulaClick;

  // View 1: Highlights (Bento Grid)
  PnlViewHighlights := TPanel.Create(WizardForm);
  PnlViewHighlights.Parent := PnlTerms;
  PnlViewHighlights.SetBounds(ScaleX(28), ScaleY(96), ScaleX(504), ScaleY(310));
  PnlViewHighlights.Color := clWhite;
  PnlViewHighlights.BevelOuter := bvNone;

  CreateFeatureCard(PnlViewHighlights, 0, 0, ScaleX(247), ScaleY(120),
    'HARDWARE ACCELERATION', 'Ultra-Smooth 4K/60fps',
    'GPU hardware decoding for ultra-smooth 4K/60fps video playback with near-zero CPU overhead.', CurrentAccent);

  CreateFeatureCard(PnlViewHighlights, ScaleX(257), 0, ScaleX(247), ScaleY(120),
    'ZERO-CLOUD PRIVACY', '100% On-Device Vault',
    'Playlists, bookmarks, and playback history are stored strictly on your local PC. No remote profiling or data harvesting.', CurrentAccent);

  CreateFeatureCard(PnlViewHighlights, 0, ScaleY(128), ScaleX(247), ScaleY(120),
    '14+ NATIVE CODECS', 'LibVLC 4 Acoustic Engine',
    'Built-in playback for MP3, FLAC, M4A, WAV, AAC, OGG, OPUS, MP4, MKV, AVI, MOV, and WebM without codec packs.', CurrentAccent);

  CreateFeatureCard(PnlViewHighlights, ScaleX(257), ScaleY(128), ScaleX(247), ScaleY(120),
    'PERMISSIVE LICENSE', 'Personal & Business',
    'Free to use across personal and productivity workstations under standard open-source MIT terms.', CurrentAccent);

  BannerBorder := TPanel.Create(WizardForm);
  BannerBorder.Parent := PnlViewHighlights;
  BannerBorder.SetBounds(0, ScaleY(258), ScaleX(504), ScaleY(44));
  BannerBorder.Color := $E2E8F0;
  BannerBorder.BevelOuter := bvNone;

  BannerInner := TPanel.Create(WizardForm);
  BannerInner.Parent := BannerBorder;
  BannerInner.SetBounds(ScaleX(1), ScaleY(1), BannerBorder.Width - ScaleX(2), BannerBorder.Height - ScaleY(2));
  BannerInner.Color := $ECFDF5;
  BannerInner.BevelOuter := bvNone;

  LblBanner := TLabel.Create(WizardForm);
  LblBanner.Parent := BannerInner;
  LblBanner.ShowAccelChar := False;
  LblBanner.Caption := 'LibVLC 4.0 Engine Foundation  •  Zero Telemetry  •  Clean Uninstall Anytime';
  LblBanner.Font.Name := 'Segoe UI';
  LblBanner.Font.Size := 8;
  LblBanner.Font.Style := [fsBold];
  LblBanner.Font.Color := $047857;
  LblBanner.Left := ScaleX(12);
  LblBanner.Top := ScaleY(13);

  // View 2: Codecs & Privacy
  PnlViewPrivacy := TPanel.Create(WizardForm);
  PnlViewPrivacy.Parent := PnlTerms;
  PnlViewPrivacy.SetBounds(ScaleX(28), ScaleY(96), ScaleX(504), ScaleY(310));
  PnlViewPrivacy.Color := clWhite;
  PnlViewPrivacy.BevelOuter := bvNone;
  PnlViewPrivacy.Visible := False;

  CreateFeatureCard(PnlViewPrivacy, 0, 0, ScaleX(504), ScaleY(96),
    '13 HARDWARE EQUALIZER PRESETS', 'Acoustic Frequency Tuning',
    'Hardware-tuned presets including Flat, Full Bass, Headphones, Rock, Pop, Classical, Techno, Dance, and Live concert immersion.', CurrentAccent);

  CreateFeatureCard(PnlViewPrivacy, 0, ScaleY(104), ScaleX(504), ScaleY(96),
    'MULTI-RATIO & PORTRAIT ANTI-STRETCH', 'Automatic Orientation Detection',
    'Phone vertical videos (9:16, 3:4, 4:5, 1:1) are automatically pillarboxed with zero horizontal distortion or stretching.', CurrentAccent);

  CreateFeatureCard(PnlViewPrivacy, 0, ScaleY(208), ScaleX(504), ScaleY(96),
    'SHELL THUMBNAILS & BADGES', 'Windows File Explorer Integration',
    'Extracts high-resolution video thumbnails with custom application badges in File Explorer for instant recognition.', CurrentAccent);

  // View 3: Full Legal Text
  PnlViewFullEula := TPanel.Create(WizardForm);
  PnlViewFullEula.Parent := PnlTerms;
  PnlViewFullEula.SetBounds(ScaleX(28), ScaleY(96), ScaleX(504), ScaleY(310));
  PnlViewFullEula.Color := clWhite;
  PnlViewFullEula.BevelOuter := bvNone;
  PnlViewFullEula.Visible := False;

  PnlTermsBorder := TPanel.Create(WizardForm);
  PnlTermsBorder.Parent := PnlViewFullEula;
  PnlTermsBorder.SetBounds(0, 0, ScaleX(504), ScaleY(310));
  PnlTermsBorder.Color := $E2E8F0;
  PnlTermsBorder.BevelOuter := bvNone;

  WizardForm.LicenseMemo.Parent := PnlTermsBorder;
  WizardForm.LicenseMemo.SetBounds(ScaleX(1), ScaleY(1), PnlTermsBorder.Width - ScaleX(2), PnlTermsBorder.Height - ScaleY(2));
  WizardForm.LicenseMemo.Color := COLOR_BOX_BG;
  WizardForm.LicenseMemo.Font.Name := 'Consolas';
  WizardForm.LicenseMemo.Font.Size := 9;

  ChkAcceptTerms := TNewCheckBox.Create(WizardForm);
  ChkAcceptTerms.Parent := PnlTerms;
  ChkAcceptTerms.Caption := 'I have read and accept the license terms & privacy commitments';
  ChkAcceptTerms.Font.Name := 'Segoe UI';
  ChkAcceptTerms.Font.Size := 9;
  ChkAcceptTerms.Font.Style := [fsBold];
  ChkAcceptTerms.SetBounds(ScaleX(28), ScaleY(416), ScaleX(504), ScaleY(20));
  ChkAcceptTerms.Checked := True;
  ChkAcceptTerms.OnClick := @ChkAcceptTermsClick;

  BtnBackFromTerms := TNewButton.Create(WizardForm);
  BtnBackFromTerms.Parent := PnlTerms;
  BtnBackFromTerms.Caption := 'Back';
  BtnBackFromTerms.Font.Name := 'Segoe UI';
  BtnBackFromTerms.Font.Size := 9;
  BtnBackFromTerms.SetBounds(ScaleX(28), ScaleY(444), ScaleX(120), ScaleY(38));
  BtnBackFromTerms.OnClick := @BtnBackFromTermsClick;

  BtnAcceptFromTerms := TNewButton.Create(WizardForm);
  BtnAcceptFromTerms.Parent := PnlTerms;
  if IsUpdateMode then
    BtnAcceptFromTerms.Caption := 'Install Update Now'
  else
    BtnAcceptFromTerms.Caption := 'Accept and Install';
  BtnAcceptFromTerms.Font.Name := 'Segoe UI';
  BtnAcceptFromTerms.Font.Size := 10;
  BtnAcceptFromTerms.Font.Style := [fsBold];
  BtnAcceptFromTerms.SetBounds(ScaleX(372), ScaleY(444), ScaleX(160), ScaleY(38));
  BtnAcceptFromTerms.OnClick := @BtnInstallClick;

  // 3. INSTALLING SCREEN
  PnlInstalling := TPanel.Create(WizardForm);
  PnlInstalling.Parent := PnlMain;
  PnlInstalling.SetBounds(0, 0, PnlMain.Width, PnlMain.Height);
  PnlInstalling.Color := clWhite;
  PnlInstalling.BevelOuter := bvNone;
  PnlInstalling.Visible := False;

  if FileExists(LogoPath) then
  begin
    ImgInstallLogo := TBitmapImage.Create(WizardForm);
    ImgInstallLogo.Parent := PnlInstalling;
    ImgInstallLogo.SetBounds(ScaleX(32), ScaleY(28), ScaleX(48), ScaleY(48));
    ImgInstallLogo.Stretch := True;
    ImgInstallLogo.Bitmap.LoadFromFile(LogoPath);
  end;

  LblInstallTitle := TLabel.Create(WizardForm);
  LblInstallTitle.Parent := PnlInstalling;
  if IsUpdateMode then
    LblInstallTitle.Caption := 'Updating Ocal Media Player...'
  else
    LblInstallTitle.Caption := 'Installing Ocal Media Player...';
  LblInstallTitle.Font.Name := 'Segoe UI';
  LblInstallTitle.Font.Size := 16;
  LblInstallTitle.Font.Color := COLOR_TEXT;
  LblInstallTitle.Font.Style := [fsBold];
  LblInstallTitle.Left := ScaleX(96);
  LblInstallTitle.Top := ScaleY(26);

  LblInstallStatus := TLabel.Create(WizardForm);
  LblInstallStatus.Parent := PnlInstalling;
  if IsUpdateMode then
    LblInstallStatus.Caption := 'Upgrading player engine, LibVLC 4 codecs, and assets...'
  else
    LblInstallStatus.Caption := 'Extracting player engine, LibVLC 4 codecs, and assets...';
  LblInstallStatus.Font.Name := 'Segoe UI';
  LblInstallStatus.Font.Color := COLOR_MUTED;
  LblInstallStatus.Font.Size := 9;
  LblInstallStatus.Left := ScaleX(98);
  LblInstallStatus.Top := ScaleY(54);
  LblInstallStatus.Width := ScaleX(360);

  LblProgressPct := TLabel.Create(WizardForm);
  LblProgressPct.Parent := PnlInstalling;
  LblProgressPct.Caption := '0%';
  LblProgressPct.Font.Name := 'Segoe UI';
  LblProgressPct.Font.Color := CurrentAccent;
  LblProgressPct.Font.Size := 9;
  LblProgressPct.Font.Style := [fsBold];
  LblProgressPct.Alignment := taRightJustify;
  LblProgressPct.SetBounds(ScaleX(468), ScaleY(54), ScaleX(60), ScaleY(18));

  PnlProgressTrack := TPanel.Create(WizardForm);
  PnlProgressTrack.Parent := PnlInstalling;
  PnlProgressTrack.SetBounds(ScaleX(32), ScaleY(92), ScaleX(496), ScaleY(6));
  PnlProgressTrack.Color := $E2E8F0;
  PnlProgressTrack.BevelOuter := bvNone;

  PnlProgressFill := TPanel.Create(WizardForm);
  PnlProgressFill.Parent := PnlProgressTrack;
  PnlProgressFill.SetBounds(0, 0, 0, PnlProgressTrack.Height);
  PnlProgressFill.Color := CurrentAccent;
  PnlProgressFill.BevelOuter := bvNone;

  // 4. FINISHED SCREEN
  PnlFinished := TPanel.Create(WizardForm);
  PnlFinished.Parent := PnlMain;
  PnlFinished.SetBounds(0, 0, PnlMain.Width, PnlMain.Height);
  PnlFinished.Color := clWhite;
  PnlFinished.BevelOuter := bvNone;
  PnlFinished.Visible := False;

  if FileExists(LogoPath) then
  begin
    ImgFinishLogo := TBitmapImage.Create(WizardForm);
    ImgFinishLogo.Parent := PnlFinished;
    ImgFinishLogo.SetBounds(ScaleX(32), ScaleY(24), ScaleX(52), ScaleY(52));
    ImgFinishLogo.Stretch := True;
    ImgFinishLogo.Bitmap.LoadFromFile(LogoPath);
  end;

  LblFinishedTitle := TLabel.Create(WizardForm);
  LblFinishedTitle.Parent := PnlFinished;
  if IsUpdateMode then
    LblFinishedTitle.Caption := 'Update Complete!'
  else
    LblFinishedTitle.Caption := 'Installation Complete!';
  LblFinishedTitle.Font.Name := 'Segoe UI';
  LblFinishedTitle.Font.Size := 18;
  LblFinishedTitle.Font.Color := COLOR_TEXT;
  LblFinishedTitle.Font.Style := [fsBold];
  LblFinishedTitle.Left := ScaleX(100);
  LblFinishedTitle.Top := ScaleY(22);

  LblFinishedSub := TLabel.Create(WizardForm);
  LblFinishedSub.Parent := PnlFinished;
  if IsUpdateMode then
    LblFinishedSub.Caption := 'Ocal Media Player has been upgraded to version 1.0.2.'
  else
    LblFinishedSub.Caption := 'Ocal Media Player is installed and ready for your music & videos.';
  LblFinishedSub.Font.Name := 'Segoe UI';
  LblFinishedSub.Font.Color := COLOR_MUTED;
  LblFinishedSub.Font.Size := 9;
  LblFinishedSub.Left := ScaleX(100);
  LblFinishedSub.Top := ScaleY(52);

  BtnFinishLaunch := TNewButton.Create(WizardForm);
  BtnFinishLaunch.Parent := PnlFinished;
  if IsUpdateMode then
    BtnFinishLaunch.Caption := 'Restart Ocal Media Player'
  else
    BtnFinishLaunch.Caption := 'Launch Ocal Media Player';
  BtnFinishLaunch.Font.Name := 'Segoe UI';
  BtnFinishLaunch.Font.Size := 11;
  BtnFinishLaunch.Font.Style := [fsBold];
  BtnFinishLaunch.SetBounds(ScaleX(100), ScaleY(88), ScaleX(240), ScaleY(40));
  BtnFinishLaunch.OnClick := @BtnFinishLaunchClick;
end;
