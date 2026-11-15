; Candidate configuration only. Compile after payload/legal/acceptance review.
#ifndef DesktopVersion
  #error DesktopVersion must be supplied as a numeric release version
#endif
#ifndef PayloadRoot
  #error PayloadRoot must reference the verified onedir payload
#endif
#ifndef OutputRoot
  #error OutputRoot must reference a new dedicated output directory
#endif
#ifndef PayloadReviewed
  #error Supply PayloadReviewed=1 only after payload and source/license review
#endif
#if PayloadReviewed != 1
  #error Payload is not reviewed
#endif

[Setup]
AppId={{9F76A89B-64DC-45C9-95F1-7A353DBBAE12}
AppName=Folimeld Desktop
AppVersion={#DesktopVersion}
VersionInfoVersion={#DesktopVersion}
DefaultDirName={localappdata}\Programs\Folimeld-Desktop
DisableDirPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
MinVersion=10.0.22000
OutputDir={#OutputRoot}
OutputBaseFilename=Folimeld-Desktop-{#DesktopVersion}-x64-setup
Compression=lzma2
SolidCompression=yes
DiskSpanning=no
UninstallDisplayName=Folimeld Desktop
UninstallDisplayIcon={app}\versions\{#DesktopVersion}\FolimeldDesktop.exe
CloseApplications=no
RestartApplications=no
SetupLogging=yes
AppMutex=Local\Folimeld-Desktop
DisableProgramGroupPage=yes
; No association/Store/uv entries, recursive cleanup, or post-install auto-launch.

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Files]
Source: "{#PayloadRoot}\*"; DestDir: "{app}\versions\{#DesktopVersion}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{userprograms}\Folimeld Desktop"; Filename: "{app}\versions\{#DesktopVersion}\FolimeldDesktop.exe"; WorkingDir: "{app}\versions\{#DesktopVersion}"

[Code]
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  if DirExists(ExpandConstant('{app}\versions\{#DesktopVersion}')) then
    Result := 'This version directory already exists. Do not overwrite it; use a new candidate version.';
end;
