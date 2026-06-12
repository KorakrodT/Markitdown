; MarkItDown GUI - Inno Setup Installer Script
; Download Inno Setup: https://jrsoftware.org/isdl.php
; Usage: Open this file in Inno Setup -> Build -> Compile

#define MyAppName      "MarkItDown"
#define MyAppVersion   "1.0.0"
#define MyAppPublisher "Your Organization"
#define MyAppURL       "https://github.com/microsoft/markitdown"
#define MyAppExeName   "MarkItDown.exe"
#define MyAppSourceDir "..\release\dist\MarkItDown"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=..\release\installer
OutputBaseFilename=MarkItDown_Setup_v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern
WizardResizable=no
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; ThaiIslPath is passed by build_all.bat as /dThaiIslPath=<full path>
; Fallback: "Thai.isl" relative to this script if not passed
#ifndef ThaiIslPath
  #define ThaiIslPath "Thai.isl"
#endif

[Languages]
Name: "thai";    MessagesFile: "{#ThaiIslPath}"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#MyAppSourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}";           Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}";     Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName} now"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
