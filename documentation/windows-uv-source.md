# Windows x64 and ARM64 source + uv preview

Use the instructions below for the published preview. Later records about earlier test ZIPs and pre-publication status are historical and use different archive hashes.

Microsoft Store remains the standard distribution. This additional route is for
advanced users on Windows 11 x64 and Windows 11 ARM64 (such as Copilot+ PCs / Surface Pro 11). The developer PC has passed regular-launcher, document-operation, three-worker
and settings-persistence checks. Production Store coexistence, cross-version
updates and rollback remain unverified.

## Pinned inputs

### Windows 11 x64
- CPython 3.12.16, python-build-standalone build 20261110.
- uv 0.13.8. URLs and published SHA-256 values: `../windows-uv-runtime.json`.
- Fourteen runtime dependencies: `../requirements-windows-uv.in`.
- `../requirements-windows-uv.lock` permits only the inspected Windows x64 /
  CPython 3.12 wheel hashes, narrowed from the original uv resolution. Do not use
  this lock on other platforms or Python versions.

### Windows 11 ARM64
- CPython 3.12.10, official Python Software Foundation signed ARM64 NuGet package (`pythonarm64.3.12.10.nupkg`). All binaries carry valid Authenticode signatures and do not trigger block notifications on Windows 11 systems with Smart App Control enabled.
- uv 0.13.8 (ARM64 Windows native binary). URLs and published SHA-256 values: `../windows-arm64-uv-runtime.json`.
- `../requirements-windows-arm64-uv.lock` permits only the inspected Windows ARM64 / CPython 3.12 wheel hashes.
- At installation, verify the actual Python archive hash and extract it into a
  private, versioned runtime. The Python version number alone does not establish
  the distribution build. Record downloaded hashes in the installation ledger.
- The source commit, ZIP hash and source association record will be finalized
  when a distribution candidate is prepared. This JSON is not an authenticity
  signature for the complete source ZIP.

## Installation and launch contract

PowerShell 7.2 or later and the Windows-provided tar are required. Isolated
developer-PC installation checks are recorded separately from GUI acceptance.
Verify the source ZIP SHA-256 against the published ledger and extract it into a
fresh dedicated directory before running:

```powershell
pwsh -NoProfile -File .\install_uv.ps1
```

#### Verify the published ZIP and unblock the unsigned installer

These instructions apply only to the published x64 preview `windows-uv-v0.3.5-preview.1`. Do not reuse this expected hash for another ZIP.
Run in non-elevated PowerShell 7.2 or later. The example assumes the ZIP is in Downloads; change `$zip` if needed.
Set `$destination` to a dedicated directory that does not exist. Do not reuse an installation directory.

```powershell
$ErrorActionPreference = 'Stop'
$zip = Join-Path $HOME 'Downloads\Folimeld-0.3.5-windows-x64-uv-source-1475b48-candidate1.zip'
$expected = '8B651224221505B4CA6F0F48ECC13989C33573DE4501ACE3A9BA960C2EBB86BA'
if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne $expected) {
    throw 'ZIP SHA-256 mismatch. Stop without extracting or running it.'
}

$destination = Join-Path $HOME 'Folimeld-uv-0.3.5'
if (Test-Path -LiteralPath $destination) {
    throw 'Destination already exists. Choose a new dedicated folder.'
}
Expand-Archive -LiteralPath $zip -DestinationPath $destination

$scripts = @(Get-ChildItem -LiteralPath $destination -Recurse -File -Filter 'install_uv.ps1')
if ($scripts.Count -ne 1) {
    throw 'Expected exactly one install_uv.ps1. Stop without running it.'
}
$installer = $scripts[0].FullName
Unblock-File -LiteralPath $installer
Push-Location -LiteralPath $scripts[0].DirectoryName
try {
    pwsh -NoProfile -File $installer
    if ($LASTEXITCODE -ne 0) { throw 'Installation failed. Retain the error and installation records.' }
}
finally {
    Pop-Location
}
```

A hash mismatch stops before extraction or execution. The verified ZIP is extracted into a new directory, and the script requires exactly one `install_uv.ps1` before unblocking only that file with `Unblock-File`. It does not unblock the ZIP or a directory recursively.

Unblocking removes the downloaded-file restriction; it does not digitally sign the script. This addresses an unsigned downloaded script blocked under `RemoteSigned`. `AllSigned`, `Restricted` or organizational policy may still prevent execution. If blocked, retain the full error and the output of `Get-ExecutionPolicy -List` for review. Do not use `Set-ExecutionPolicy` or `-ExecutionPolicy Bypass`; machine, user and process execution policies remain unchanged.

After installation, launch the generated **Folimeld UV** shortcut beside `install_uv.ps1`. Do not run `main.py` directly or move/rename the installation directory afterward.

`install_uv.ps1` downloads uv and Python from pinned URLs, verifies archive
hashes, and installs only into `.uv-runtime` and `.venv` under the source folder.
After `uv pip check` and launcher validation, it creates normal and diagnostic
shortcuts in that same folder without launching the application. Existing
runtime/environment directories or shortcut names cause it to stop; nothing is
overwritten or automatically removed. Failed attempts retain records and files
for inspection. No elevation, PATH or execution-policy changes, or Store
registration changes are performed.

Records default to
`%LOCALAPPDATA%\Folimeld-UV\install-records\<version>\<run-id>\`.
Isolated checks can use `-RecordRoot <absolute-path>`. Records contain archive
hashes/sizes, step results, installed versions and shortcut paths, not credentials
or a dump of environment variables.

Create `.venv` directly under the release directory using an
absolute path to the pinned Python. Disable automatic Python downloads; do not
reuse system or shared environments. Use the exact uv executable without PATH
or global-setting changes. Run `uv pip sync` with the dedicated interpreter,
`--require-hashes`, `--only-binary :all:` and `--no-config`. Stop when a compatible
wheel is unavailable rather than building from source.

Launch `.venv\Scripts\pythonw.exe` with the absolute path to `launch_uv.py`.
Use the same environment's `python.exe` for diagnostics. Shortcuts belong to the
later installation stage. Do not synchronize or upgrade on launch, register
file associations, or use the legacy `main.py` directly for the uv edition.

The launcher checks Windows x64, CPython 3.12.16, the release-local `.venv`,
absence of MSIX identity, non-frozen execution, the lock hash and all fourteen
installed dependency versions. Mismatches produce an error and exit without
automatic repair or installation. It retains `freeze_support()` and the
`__main__` guard so spawned children do not create another GUI. All three
workers use the same Python. Developer-PC acceptance confirmed their parent
PID, executable path, startup and termination.

## Storage and Store separation

- Settings: `%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini`
- Logs: `%LOCALAPPDATA%\Folimeld-UV\logs\<app-version>\<session-id>\`
- Installation ledger:
  `%LOCALAPPDATA%\Folimeld-UV\install-records\<version>\`

The uv entry calls `run(source_uv=True)` and selects its profile before I18n and
MainWindow read settings. All application settings use a shared factory. The
uv profile explicitly selects an INI and disables Qt fallback. Normal Store
launches retain the existing QSettings and log locations. Failure to initialize
the dedicated storage or logs does not fall back to Store storage; uv startup
fails instead.

Logs retain the existing 1 MiB, three-file rotation per session. Old session
directories are not automatically removed. No Store settings migration, default
PDF app change, registry association or Store purchase is performed. Documents
stay in user-selected locations and are not moved into release directories.

## License notices and corresponding source

The uv profile's license view shows dedicated notices for fourteen runtime
dependencies, Python and uv, observed installed versions and the versioned source
ledger. It includes typing-extensions and does not count PyInstaller as a runtime
dependency. Store builds retain their existing bundled-notice route.

[Versioned sources and limits](windows-uv-sources.md) / [Full notices](windows-uv-licenses/notices.txt) /
[Provenance ledger](windows-uv-licenses/sources.json)

## Updates and remaining checks

Install each new release into a separate directory and `.venv`. Preserve the
shared uv INI and the previous source/environment; switch the shortcut only
after acceptance. A future settings-schema change requires backup and tested
rollback. No schema migration is implemented here.

### Fresh installation and acceptance from the preview ZIP (2026-11-15)

The developer PC was tested using a preview ZIP containing the uncommitted 0.3.5
source plus uv implementation. This was neither a formal release nor a
cross-version update test.

- ZIP: `Folimeld-0.3.5-windows-uv-source-preview.zip`, 26,569,868 bytes.
- SHA-256: `EB48FF341C90AA9323CBB32EC0D98A16CB94442B3C2BB4D037964B6FC6336924`.
- All 1031 source files in the internal manifest were checked by size and SHA-256
  before and after extraction into a new dedicated directory with Japanese
  characters and spaces. They remained unchanged after acceptance.
- The ZIP's `install_uv.ps1` freshly installed the pinned uv, Python and fourteen
  dependencies. Archive/wheel hashes, installed versions, dependency consistency
  and launcher preflight checks passed.
- The regular entry point used the dedicated `.venv` Python's `pythonw.exe` and
  `launch_uv.py`. Checks covered displaying a three-page synthetic PDF, save-as,
  converting and saving two images as a PDF, and reopening both PDFs after restart.
- Parent PID, executable path, startup and termination were observed for all three
  workers: PDF saving, image conversion and image-PDF saving.
- Thumbnail size was changed from 144px to 288px. The 288px selection and previous
  PDF directory persisted after restart. Both normal exits returned code 0, and
  all observed target processes terminated.
- The three synthetic inputs' hashes, existing development-package registration,
  settings and default PDF association were unchanged.

Only the source, runtime and dependency location was new; the shared uv settings
INI was retained. The additional checks below were performed separately.
Production Store coexistence, cross-version updates and rollback remain
unverified. This single
ordinary acceptance flow does not establish effectiveness against the
image-conversion shutdown crash. The hash above identifies the existing tested
ZIP. An archive rebuilt after this documentation update or a commit needs a
distinct identifier, manifest, SHA-256 and appropriate verification.

### Additional empty-settings, DPI, error-recovery and target-Python checks (2026-11-15)

- The existing uv INI was temporarily set aside after hash verification. The
  regular launcher started successfully with no INI present and exited with
  code 0. The generated INI was saved separately and the original restored with
  the same SHA-256. Logs and installation history were retained; this was not a
  completely new Windows-user test.
- The main window's `GetWindowDpiAwarenessContext` matched
  `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2` (-4) using
  `AreDpiAwarenessContextsEqual`. Process awareness value 2 alone was not used to
  identify V2. Current `GetDpiForWindow` was 144 (150% equivalent). Scale changes
  and multi-monitor movement were not tested. The old WACK warning's cause and
  individual certification determinations remain unconfirmed.
- Dismissing the conversion warning for a dedicated invalid PNG redisplayed the
  image-import dialog. Cancel returned to the main window, which could then open
  a synthetic three-page PDF. This tested an expected read error, not crash
  reproduction.
- A separate test environment used the same CPython 3.12.16 and fourteen pinned
  dependencies, plus pytest 9.1.1, without changing the application environment.
  Qt settings were isolated to a test-only INI. All 61 tests and 16 subtests in
  ten relevant modules passed; this was not the full repository suite.
- The initial run had 54 passes and three failures caused by stale mocks of
  `folimeld.app.QSettings` from before settings were centralized. Five mock
  targets in `tests/test_file_dialog.py` and `tests/test_button_display.py` were
  aligned with `folimeld.app.application_settings`. Expectations, assertions and
  cases were retained. The original failures were preserved; application code
  was unchanged.
- The fourteen runtime dependency pins, existing Folimeld registration/settings
  and default PDF association remained unchanged. Static and diff checks for
  the two test files also passed.

The GUI checks used the existing verified ZIP installation; automated checks
used the working tree. The two test fixes and these documentation additions
are uncommitted and absent from that ZIP. Its hash must not be reused for an
updated artifact.

### Remaining work before GitHub publication

- Verify production Store coexistence, cross-version updates/rollback, rendering
  at multiple scales and movement between monitors. Confirm
  the environment and scope beforehand; test-PC updates require separate approval.
- Dedicated uv notices, a ledger and versioned source references are prepared.
  Distinguish remaining embedded-component build/source checks and verify notices
  for the final distribution. Bundling runtimes or wheels requires another review.
- Preserve the verified scope of the relevant target-Python checks, run any
  additional checks needed for final changes, and review the bilingual diff.
- After commit approval, finalize an archive tied to that commit, its internal
  manifest and SHA-256, with acceptance appropriate to any content changes. Present
  bilingual README download links and the Release file list and description
  before publication.

Effectiveness against the image-conversion shutdown crash remains unverified and
must be stated separately in any pre-publication assessment.
Publication, test-PC updates, WACK and Hosted API comparisons are out of scope.

[日本語](windows-uv-source_ja.md)
