# Windows x64 Desktop: implementation before building

[譌･譛ｬ隱枉(windows-desktop-build_ja.md)

Unbuilt, unpublished candidate configuration, separate from Store and uv editions.
PyInstaller onedir plus Inno Setup requires no user-installed Python, uv or PowerShell.

## Implementation

- launch_desktop.py retains freeze_support and requires a frozen, unpackaged Windows x64 process.
- Settings: %LOCALAPPDATA%/Folimeld-Desktop/settings/settings.ini, with no INI fallbacks.
- Logs: %LOCALAPPDATA%/Folimeld-Desktop/logs/<version>/<session>. Initialization failure stops startup.
- Reject simultaneous uv/Desktop profiles. No automatic settings migration, default-PDF changes or Open With registration.
- Sponsors guidance requires an active Desktop profile; Store remains excluded.
- Hold Local\Folimeld-Desktop mutex during regular launch. Inno checks the same mutex to prevent updating/removing a running app, without forcibly terminating workers.

## onedir prerequisites

Use a dedicated CPython3.12.16 environment. Validate the fourteen runtime versions from packaging/windows/desktop-runtime.json; uv itself is not used for installation or runtime.
Validate PyInstaller6.22.2 and hooks-contrib2026.7. Restrict native collection to private Python/Windows roots. Disable UPX and retain the DPI manifest.
Explicitly sort collection inputs; cross-environment byte reproducibility remains unverified. Leave the Store Folimeld.spec unchanged.

Before building, prepare dedicated numeric file-version information and reviewed legal inputs.
legal/reviewed-files.json must contain distribution=windows-desktop-x64 and a files mapping from relative paths to SHA256, including Installed-packages.txt, THIRD-PARTY-NOTICES.txt and DEPENDENCY-SOURCES.json.
This pins hashes; it does not perform or replace license review. Do not reuse old cp314 records or uv documentation assuming dependencies are not redistributed without matching them to the actual binaries.
Do not fabricate records merely to pass this gate before Qt/dependency source, patch and payload review.

After approval, use python -m tools.desktop_build --output <new absolute directory> --legal-root <reviewed records> --version-info <dedicated version info>.
Existing output stops the build. Validate restricted PATH, dependency versions and legal hashes; retain build-inputs.json and pyinstaller.log.
At build time, separately finalize matching application source ZIP, Git commit, complete inputs/payload ledger and final setup association; verify them before release.

## Inno Setup candidate

Inno Setup7.1.1 is the proposed pinned official compiler. Actual compiler version and downloaded signature/hash verification are pending.
Compile packaging/windows/Folimeld-desktop.iss with DesktopVersion (numeric), PayloadRoot (verified onedir), OutputRoot (new dedicated output) and PayloadReviewed=1.
Finalize release numbering, all input hashes and executable/setup/uninstaller signing before building.

- Per-user, Windows11 x64 only; reject ARM64.
- Fixed Desktop AppId; install under %LOCALAPPDATA%/Programs/Folimeld-Desktop/versions/<version>.
- Create Folimeld Desktop Start-menu shortcut; no automatic launch after installation.
- Reject an existing same-version directory. Retain previous versions; point the shortcut to the new version on upgrade.
- Remove only Inno-owned application files/shortcuts. Do not target documents/settings/logs under %LOCALAPPDATA%/Folimeld-Desktop or Store/uv data. No recursive cleanup directive.

Settings backup/migration and complete failure recovery/rollback are not implemented or tested. Verify them with partial-install failure behavior before release.
This candidate is not yet ready for general distribution.

## Checks and remaining work

Automated checks cover profile isolation, invalid environments, Sponsors eligibility, existing Store/uv paths and legal hashes.
Simulated Qt platform conditions do not replace real installer/frozen-process acceptance.
No ISCC compilation, compiler validation of the Inno script or executable generation is performed yet.
Startup timing, PDF/image operations, three workers, Per-Monitor V2, visible support-link behavior, coexistence, update/removal/recovery, legal records and signing remain acceptance tasks.
No test-PC update, WACK or Hosted API comparison.


## Desktop fixed inputs / Qt policy

Desktop uses packaging/windows/desktop-runtime.json independently: Python archive hash, fourteen runtime versions and wheel URLs/SHA256, PyInstaller/hooks versions. No uv configuration is read. The Desktop input hash is recorded in build-inputs.json.
Only the Desktop spec uses tools/desktop_qt.py. Core/Gui/Widgets and optional SVG/OpenGL support are allowed. Unused modules (VirtualKeyboard, Charts, Graphs, QML/Quick, WebEngine, Pdf, Multimedia, etc.), native plugins and QML data are excluded. Retained code requiring excluded/unresolved Qt dependencies stops collection. Missing Core/Gui/Widgets/qwindows also stops collection. Exclusions are recorded in future workpath/desktop-qt-exclusions.json.
Dynamic loading, Japanese IME, GPU behavior and actual payload acceptance remain unverified. Store/uv specs and launchers remain unchanged. No dependency download/environment creation is performed. Tool archive hashes, Inno confirmation and independent environment setup/download hash verification remain pending. Wheel hashes do not establish redistribution rights or installed-file correspondence. The reviewed-legal-input gate remains mandatory.
