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
#if PayloadReviewed != "1"
  #error Payload is not reviewed
#endif

[Setup]
; Preserve Inno 7 defaults explicitly: x86 bootstrap, x64 application payload.
SetupArchitecture=x86
UseSetupLdr=x86
WizardStyle=classic light
; Original terms apply only to the Microsoft Runtime, not all application code.
LicenseFile={#PayloadRoot}\_internal\licenses\microsoft-runtime\MICROSOFT-VC-RUNTIME-14.44-EN.original.rtf
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

[Messages]
english.LicenseLabel=These terms apply only to the bundled Microsoft Visual C++ Runtime.
english.LicenseLabel3=Read the original English Microsoft terms below. Folimeld and other open-source components retain their own licences. Accept these Runtime terms to continue.
english.LicenseAccepted=I &accept the Microsoft Runtime terms
english.LicenseNotAccepted=I &do not accept the Microsoft Runtime terms
japanese.LicenseLabel=この条件は同梱のMicrosoft Visual C++ Runtimeだけに適用されます。
japanese.LicenseLabel3=以下はMicrosoftの英語原文です。Folimeldと他のOSSにはそれぞれのライセンスが適用されます。続行するにはRuntime条件に同意してください。
japanese.LicenseAccepted=Microsoft Runtimeの条件に同意する(&A)
japanese.LicenseNotAccepted=Microsoft Runtimeの条件に同意しない(&D)

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
