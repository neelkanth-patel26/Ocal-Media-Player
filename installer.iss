; ============================================================
;  Ocal Media Player - Inno Setup 6 Installer
;  Version  : 1.0.1
;  Builder  : Ocal Software under Gaming Network Studio
;  Compiler : Inno Setup 6
; ============================================================

[Setup]
AppId={{C72A0D45-B8E3-4E8A-9BF7-9A1D8DF12A74}
AppName=Ocal Media Player
AppVersion=1.0.1
AppVerName=Ocal Media Player 1.0.1
AppPublisher=Ocal Software under Gaming Network Studio
AppPublisherURL=https://github.com/neelkanth-patel26/Ocal-Media-Player
AppSupportURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/issues
AppUpdatesURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/releases
AppCopyright=Copyright (C) 2026 Ocal Software under Gaming Network Studio
DefaultDirName={autopf}\Ocal Media Player
DefaultGroupName=Ocal Media Player
OutputDir=dist-installer
OutputBaseFilename=Ocal-Media-Player-1.0.1-Setup
SetupIconFile=assets\app-icon.ico
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
VersionInfoVersion=1.0.1.0
VersionInfoCompany=Ocal Software under Gaming Network Studio
VersionInfoDescription=Ocal Media Player Installer
VersionInfoProductName=Ocal Media Player
VersionInfoProductVersion=1.0.1
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
procedure SHChangeNotify(wEventId: Integer; uFlags: Cardinal; dwItem1, dwItem2: Integer);
  external 'SHChangeNotify@shell32.dll stdcall';

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Notify Windows Explorer that file associations and default apps changed
    SHChangeNotify($08000000, 0, 0, 0);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    SHChangeNotify($08000000, 0, 0, 0);
  end;
end;
