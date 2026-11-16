# Windows x64 Desktop: implementation before building

[日本語](windows-desktop-build_ja.md)

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

After approval, use python -m tools.desktop_build --output <new absolute directory> --legal-root <reviewed records> --version-info <dedicated version info> --input-root <verified download directory> --crt-root <dedicated verified CRT directory> --inno-root <dedicated pinned Inno directory>.
Existing output stops the build. Validate restricted PATH, dependency versions and legal hashes; retain build-inputs.json and pyinstaller.log.
At build time, separately finalize matching application source ZIP, Git commit, complete inputs/payload ledger and final setup association; verify them before release.

## Inno Setup candidate

The official Inno Setup7.1.1 x64 installer archive is hash-pinned and its signature was verified. A dedicated non-administrative portable copy was prepared and all 133 files were hashed. ISCC --version reports7.1.1; PE tool version fields are0.0.0.0 and stub resource placeholders do not identify a release. No script has been compiled.
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
Dynamic loading, Japanese IME, GPU behavior and actual payload acceptance remain unverified. Store/uv specs and launchers remain unchanged. The build helper does not download dependencies or create environments. Seven build-tool wheels and the Inno distribution archive now have fixed hashes. A dedicated environment was prepared and installed files were matched to the fixed wheels. Reproducible environment recreation and application/installer acceptance remain pending. Wheel hashes do not establish redistribution rights or installed-file correspondence. The reviewed-legal-input gate remains mandatory.


## Verified archive inputs (2026-11-15)

The fixed manifest now includes seven build-tool versions/wheels and the Inno7.1.1 x64 installer. The read-only preflight requires --input-root and hashes all 23 local archives (Python, fourteen runtime wheels, seven tool wheels, Inno) before creating build output. Missing, changed or escaping paths stop the procedure. Verification does not install or execute inputs.
The separate desktop-runtime-requirements.txt and desktop-tools-requirements.txt use direct wheel URLs, --require-hashes and --only-binary=:all:. These HTTPS requirement files were not passed directly to pip; a local-file derivation with the same fixed hashes was used for offline environment preparation. Wheel metadata confirms nineteen active dependency requirements are satisfied for Windows x64/Python3.12.16 without optional extras. Inputs were downloaded and verified, and a dedicated environment was prepared with wheel/RECORD correspondence checks. The prepared Inno file tree is pinned below; its third-party conditions and final installer acceptance remain pending. Hashes do not approve redistribution. Source/license review remains incomplete. In particular, finalize third-party notices and corresponding source, CRT redistribution terms, and the installed Inno compiler/stub correspondence before approving legal inputs. Archive hashes alone do not complete these checks.


## Desktop CRT collection

`packaging/windows/desktop-crt.json` pins exactly seven official Desktop x64 CRT files at 14.44.35211.0 by SHA256 and size. `--crt-root` must contain exactly those files. Preflight verifies containment, contents and x64 PE headers without installing or running them. The same checks run again in the spec before collection.
The existing Python/Windows source guard stays in place for Analysis inputs. Only individually verified CRT paths are added afterward; no general Program Files or workspace allowance is introduced. Approved-name CRT duplicates from binaries and data TOCs are replaced with one canonical set. Unknown CRT, system UCRT/API-set copies and renamed CRT files stop collection. Input files are never deleted or modified.
The Desktop spec explicitly uses `_internal`. After COLLECT, a read-only audit requires the seven exact files there and rejects nested/root duplicates, extra CRT, missing/changed files and escaping paths. The build work directory records desktop-crt-inputs.json and desktop-crt-collected.json. A failed audit fails the build; any partial output is not an accepted candidate.
Source input and synthetic-TOC/unit checks do not verify real frozen-app DLL loading, worker behavior or runtime compatibility. Redistribution/notice/source review and reviewed-files.json remain separate prerequisites. No legal approval is inferred from the CRT hashes. Store/uv specs and data remain unchanged.


## Fixed-input format and requirements synchronization

The manifest loader validates both runtime and tool wheels with the same rules: exactly 64 lowercase hexadecimal SHA-256 characters; HTTPS on the exact files.pythonhosted.org host; no credentials, port, query, fragment, whitespace or traversal; and a safe .whl filename matching the decoded URL basename.
Both requirements files must have exactly one --require-hashes and --only-binary=:all: flag and only direct-wheel entries. Names, URLs and SHA-256 values must match the corresponding JSON section; missing/extra/duplicate entries, additional pip options and version-only requirements fail before build output creation. Blank/comment lines are allowed. Distribution names are normalized using Python package name rules. The hashes of both requirements files are also recorded in build-inputs.json.
This validation reads local files only. It does not install packages, query an index, run uv or establish legal approval. Dedicated-environment file correspondence was checked locally. Final installer acceptance and license/source review remain pending.


## Inno tool and stub preflight

`packaging/windows/desktop-inno.json` pins the entire prepared 133-file Inno7.1.1 x64 tool tree, including nine primary compiler/stub files, language inputs and compression support. `--inno-root` is mandatory. Before creating build output, check the exact file set, containment, sizes and SHA256. Only after all hashes pass, query ISCC.exe --version and require7.1.1. Record the manifest, script and file hashes in build-inputs.json. This guard does not compile or install anything.
The setup script now explicitly preserves Inno7's defaults: SetupArchitecture=x86, UseSetupLdr=x86, WizardStyle=classic light. The selected stubs are Setup.e32 and SetupLdr.e32; the application payload and allowed target OS remain x64. The x64 compiler does not imply an x64 setup bootstrap. Alternate architecture, loader/style policy, duplicate directives or includes require a new review and stop the fixed-script guard. This is not a general Inno preprocessor. The current helper still creates only onedir when later authorized; it does not invoke ISCC compilation. The separate compile entry below reruns this check immediately before compilation and fixes command-line overrides.

## Reviewed installer compile entry

`python -m tools.desktop_compile` is a separate entry from onedir collection. Its default is verification only: it creates no output directory and does not compile. It can query the already hash-verified ISCC version. Required arguments are `--payload-root`, `--payload-review`, `--legal-root`, `--inno-root`, `--output` (a new directory with an existing parent), and a four-part numeric `--version`. Only an explicitly authorized future invocation with `--compile` runs ISCC; this change has not built an installer.

The independently reviewed payload ledger must contain `schema_version: 1`, `distribution: windows-desktop-x64`, `status: reviewed-for-desktop-compile`, the matching `version`, and `files` mapping every payload-relative POSIX path to its lowercase SHA-256. It also binds `legal_manifest_sha256` (legal-root/reviewed-files.json), `inno_manifest_sha256`, `crt_manifest_sha256`, `runtime_manifest_sha256`, and `setup_script_sha256` to the current files. The latter four refer to the existing packaging/windows Desktop manifests and Folimeld-desktop.iss. There is no approval-ledger generator. A status string is a review record, not a digital signature or proof of redistribution rights. Confirm the payload's actual application version during that review; the entry binds the review's version to exact payload bytes, not a separate PE-version-resource comparison.

The guard requires the exact payload file set, an x64 FolimeldDesktop.exe, python312.dll, the unchanged application LICENSE, the seven canonical CRT files, and an exact packaged copy of the reviewed legal file set under _internal/licenses. Missing, extra, changed, linked or escaping payload entries fail. Legal source files and the complete pinned Inno tree are checked again. Input trees must be separate; output must be separate from inputs and the repository, and cannot be reused. The fixed compiler command selects the reviewed version/paths and PayloadReviewed=1, disables IDE signing-tool inheritance, and accepts no arbitrary compiler arguments. PATH is restricted to the prepared Inno directory and Windows directories.

A full verification runs before creating output, immediately before compiler invocation, and after it returns. A changed snapshot, nonzero compiler result, missing/unexpected output, or unexpected installer PE architecture fails acceptance. This is a recheck, not an atomic filesystem lock; do not modify inputs concurrently. Logs and input hashes are retained; failures are marked failed-not-approved and are never automatically retried in the same directory. A successful future compile records installer size/SHA-256 and compiled-not-release-approved: runtime acceptance, signing, license approval and publication remain separate. Unit tests use synthetic fixtures and a mock compiler only. Production reviewed license/payload ledgers and real installer acceptance remain pending. uv development remains discontinued; Store behavior is unchanged.

## Microsoft Runtime-only consent and original-text guard

The installer candidate now displays the pinned original English Microsoft Runtime RTF before installation. English/Japanese labels explicitly scope acceptance to the Microsoft Runtime and preserve the separate licences of Folimeld and other OSS. The page offers acceptance and refusal; it does not turn the app's AGPL licence into Microsoft terms. Actual page layout and unattended-install behaviour require future installer acceptance.

`tools/desktop_runtime_terms.py` pins the original 9235-byte RTF (SHA256 8099dc3cf9502c335da829e5c755948a12e3e6de490eb492a99deb673d883d8b) at `microsoft-runtime/MICROSOFT-VC-RUNTIME-14.44-EN.original.rtf`. Before onedir work, the helper and spec require the original bytes and its entry in the Desktop reviewed legal ledger. After COLLECT, the original packaged bytes are checked again without fabricating a review record. The compile entry repeats the source/legal check in every full verification pass. The Inno fixed-directive manifest additionally pins LicenseFile to the corresponding _internal/licenses path.

This change does not create reviewed-files.json or establish that all redistribution/end-user protection requirements are satisfied. Individual development and an unsigned initial test candidate were confirmed by the user; no paid certificate is acquired. Store/uv behaviour remains unchanged and uv development remains discontinued. Build/publication still require completion of the remaining material review and actual acceptance; no compiler was invoked for this change.

## Initial Candidate 0.3.5.0 onedir Build, Inno Setup Compilation, and Acceptance Verification (2026-11-16)

- Fixed three issues surfaced during actual execution: PyInstaller `workpath` binding in `Folimeld-Desktop.spec`, collected-TOC Qt DLL resolution in `tools/desktop_qt.py`, and ISPP string comparison (`#if PayloadReviewed != "1"`) in `packaging/windows/Folimeld-Desktop.iss`.
- Ran `tools.desktop_build` in the dedicated CPython 3.12.16 environment, passing all 23 archive checks, 7 canonical CRT checks, 133 Inno tool checks, and 10 reviewed legal file checks to produce the 201-file onedir payload (`FolimeldDesktop.exe`, 4,709,397 bytes).
- Created `payload-review.json` binding all 201 payload file SHA-256 hashes and the 5 manifests, then ran `tools.desktop_compile --compile` with Inno Setup 7.1.1 (`ISCC.exe`) to build `Folimeld-Desktop-0.3.5.0-x64-setup.exe` (49,919,431 bytes, SHA-256: `adbe1b0e983f1dfa9bd62d5782ee173ae47e5f625f3babd24b55cc0b5e6386c3`).
- Completed installer and frozen-application acceptance verification:
  - Verified `AppMutex` (`Local\Folimeld-Desktop`) blocks installer execution when held (exit code 1, no install directory created).
  - Verified non-elevated fresh installation (exit code 0, all 201 installed files under `%LOCALAPPDATA%\Programs\Folimeld-Desktop\versions\0.3.5.0` match `payload-review.json` SHA-256, and Start menu shortcut `Folimeld Desktop.lnk` created).
  - Verified `PrepareToInstall` refuses same-version overwrite (exit code 7).
  - Verified installed `FolimeldDesktop.exe` opens a 3-page PDF passed via CLI, matches `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2` (-4, DPI=144), rejects duplicate launch via `Local\Folimeld-Desktop` mutex with dialog and exit code 1, and exits cleanly with code 0.
  - Verified `unins000.exe` cleanly removes `versions\0.3.5.0` and the Start menu shortcut (exit code 0) while preserving user settings under `%LOCALAPPDATA%\Folimeld-Desktop`.
