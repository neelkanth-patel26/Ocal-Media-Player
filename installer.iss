; ============================================================
;  Ocal Media Player - Inno Setup 6 Installer
;  Version  : 1.0.0
;  Builder  : Ocal Software under Gaming Network Studio
;  Compiler : Inno Setup 6
; ============================================================

[Setup]
AppId={{C72A0D45-B8E3-4E8A-9BF7-9A1D8DF12A74}
AppName=Ocal Media Player
AppVersion=1.0.0
AppVerName=Ocal Media Player 1.0.0
AppPublisher=Ocal Software under Gaming Network Studio
AppPublisherURL=https://github.com/neelkanth-patel26/Ocal-Media-Player
AppSupportURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/issues
AppUpdatesURL=https://github.com/neelkanth-patel26/Ocal-Media-Player/releases
AppCopyright=Copyright (C) 2026 Ocal Software under Gaming Network Studio
DefaultDirName={autopf}\Ocal Media Player
DefaultGroupName=Ocal Media Player
OutputDir=dist-installer
OutputBaseFilename=Ocal-Media-Player-1.0.0-Setup
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
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Ocal Software under Gaming Network Studio
VersionInfoDescription=Ocal Media Player Installer
VersionInfoProductName=Ocal Media Player
VersionInfoProductVersion=1.0.0
WizardStyle=modern
ShowLanguageDialog=no
CloseApplications=no
RestartIfNeededByRun=no
UsedUserAreasWarning=no

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "fileassoc";   Description: "Associate audio & video file types with Ocal Media Player"; GroupDescription: "File Associations:"; Flags: checkedonce

[Files]
Source: "dist\Ocal Media Player\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\app-icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Ocal Media Player"; Filename: "{app}\Ocal Media Player.exe"; IconFilename: "{app}\assets\app-icon.ico"; AppUserModelID: "OcalSoftware.OcalMediaPlayer"
Name: "{group}\Uninstall Ocal Media Player"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Ocal Media Player"; Filename: "{app}\Ocal Media Player.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\app-icon.ico"; AppUserModelID: "OcalSoftware.OcalMediaPlayer"

[Registry]
; File type association handler
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.AssocFile"; ValueType: string; ValueData: "Media File"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.AssocFile\DefaultIcon"; ValueType: string; ValueData: "{app}\assets\app-icon.ico,0"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\OcalMediaPlayer.AssocFile\shell\open\command"; ValueType: string; ValueData: """{app}\Ocal Media Player.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc

; Audio extensions
Root: HKCU; Subkey: "Software\Classes\.mp3\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.flac\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wav\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.m4a\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.aac\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.ogg\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.opus\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wma\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc

; Video extensions
Root: HKCU; Subkey: "Software\Classes\.mp4\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mkv\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.avi\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.mov\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.wmv\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKCU; Subkey: "Software\Classes\.webm\OpenWithProgids"; ValueType: string; ValueName: "OcalMediaPlayer.AssocFile"; Flags: uninsdeletevalue; Tasks: fileassoc

[Run]
Filename: "{app}\Ocal Media Player.exe"; Description: "{cm:LaunchProgram,Ocal Media Player}"; Flags: nowait postinstall skipifsilent
