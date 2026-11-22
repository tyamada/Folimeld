# Changelog

[日本語](CHANGELOG_ja.md) | [English](CHANGELOG.md)

## Unreleased

- For the upcoming Microsoft Store release (Submission 3 / package version 1.0.3.0, app version 0.3.7), built native Store MSIX packages on x64 and ARM64 hardware (`Folimeld_1.0.3.0_x64.msix`, `Folimeld_1.0.3.0_arm64.msix`), passed static checks (`msix_preflight`), completed source bundle association, recorded both candidate package hashes in the release plan (`windows-store-release-plan.md`) and acceptance checklist (`windows-store-acceptance.md`), and updated bilingual screenshots and the privacy policy (`docs/privacy/index.html`).

- Publish 0.3.5 amd64 packages for FreeBSD 15.1, NetBSD 11.1, and OpenBSD 8.0: Published preview Releases for `folimeld-0.3.5_1.pkg` (FreeBSD 15.1 amd64), `folimeld-0.3.5.tgz` (NetBSD 11.1 amd64), and `folimeld-0.3.5.tgz` with `folimeld-mupdf-1.28.2.tgz` (OpenBSD 8.0 amd64, signed with Signify). Synchronized English and Japanese installation guides (`documentation/freebsd-install*.md`, `netbsd-install*.md`, `openbsd-install*.md`) and README download tables.

- Publish Ubuntu amd64 strict Snap 0.3.5 package: Built core24-based `folimeld_0.3.5_amd64.snap` (SHA-256: `ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570`) on Ubuntu 24.04.5 LTS amd64, verifying `snap install --dangerous` update installation, active interface plug connections (GNOME extensions, Wayland, X11, OpenGL, Home), and offscreen GUI execution. Provided bilingual verification records (`documentation/linux-snap-amd64-035-validation_ja.md`, `linux-snap-amd64-035-validation.md`) and JSON verification record.

- Cleaned up superseded Ubuntu and Debian 0.3.4 entries from the README downloads table in favor of 0.3.5 release rows.

- Update macOS Homebrew formula to 0.3.5: Support Python 3.14 environment, add `launch_homebrew.py` launcher passing distribution identifier (`homebrew`) to enable the "Help -> Support Development..." action, generate lean 5.7 MB source archive, and complete verification for `brew install --build-from-source tyamada/tap/folimeld`, `brew test tyamada/tap/folimeld`, and clean uninstallation.

- Update FreeBSD 15.1 aarch64 package to 0.3.5_1: Update ARM64 packaging tools, build `folimeld-0.3.5_1.pkg`, and verify `pkg add` installation, offscreen GUI execution, and active "Support Development..." menu action.

- Update OpenBSD 8.0 arm64 packages to 0.3.5: Extend `tools/build_openbsd_package.py` to support arm64/aarch64 alongside amd64, build `folimeld-0.3.5.tgz` with Python 3.14 and LLVM 22, apply Signify signatures (embedded gzip signature and `SHA256.sig`), and verify `pkg_add` installation, offscreen execution, and active "Support Development..." action.

- Update NetBSD 11.1 aarch64 package to 0.3.5: Extend `tools/build_netbsd_package.py` to support evbarm/aarch64 alongside amd64, build `folimeld-0.3.5.tgz` with Python 3.12, Qt6, and PySide6 6.11.2, and verify `/usr/pkg/sbin/pkg_add` installation, offscreen execution, and active "Support Development..." action.

- Consolidate Ubuntu / Debian / Kali Linux 0.3.5 packaging: Stage verified 0.3.5 DEB (amd64 / arm64) and strict Snap (arm64) packages for release.

- Formulated and executed an update plan to upgrade Debian, Ubuntu, and BSD (FreeBSD, NetBSD, OpenBSD) packages to the Folimeld 0.3.5 baseline. Captured and associated the deterministic source code snapshot ZIP (`Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`), added test suites for BSD version resolution (FreeBSD `0.3.5_1`, NetBSD `0.3.5`, OpenBSD `0.3.5`) and dependency source integrity (`tests/test_bsd_packages.py`, `tests/test_freebsd_package.py`), and verified all 18 tests passed.
  - **Linux (amd64)**: Built Ubuntu 24.04 amd64 DEB package (`folimeld_0.3.5_amd64.deb`, SHA-256: `5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174`) via WSL2, and verified offscreen GUI initialization, PyMuPDF loading, and standalone binary integrity under both Ubuntu 24.04.4/24.04.5 LTS and Debian 13.6/13.7 (Trixie). Updated and synchronized the README download table to reflect verified latest point releases (Ubuntu 24.04.5 / Debian 13.7).
  - **FreeBSD 15.1 (amd64)**: Built `folimeld-0.3.5_1.pkg` (SHA-256: `16d3d1801acae0f62bf99d89d53f8a679593e5896d1db60d46cc5b57c15946ae`) in the FreeBSD VirtualBox VM, verifying `pkg add -f` update installation and offscreen execution.
  - **NetBSD 11.1 (amd64)**: Built `folimeld-0.3.5.tgz` (SHA-256: `7dc5c7d68e41b5120a9345fd679e5c99d46fcd7b7b50cf4f49e22d55ffec6e6a`) in the NetBSD VirtualBox VM, verifying `pkg_add -u` update installation and offscreen execution.
  - **OpenBSD 8.0 (amd64)**: Built ports packages `folimeld-0.3.5.tgz` (SHA-256: `6d0b68373f380622dc1bbbe4bad4d132648f8974fa7246ca9af0c22db9028e63`) and private dependency `folimeld-mupdf-1.28.2.tgz` (SHA-256: `1d537907faf92f11f2f701f967486c03643097e8dd5dff9199e6c6a6aa87bf8c`) in the OpenBSD VirtualBox VM. Completed signing with `pkg_sign` and `signify` (`SHA256SUMS.txt.sig`), and verified signature-checked `pkg_add -r` update installation and offscreen execution.
  - Recorded verified package information and acceptance results in bilingual guides (`documentation/bsd-035-release-plan_ja.md`, `bsd-035-release-plan.md`).

- Prepared next Microsoft Store release plan (Submission 2 / package version 1.0.2.0) with native Windows 11 ARM64 support, disabled UPX in `Folimeld.spec`, and updated bilingual Store listing copy (What's new) and release planning documentation. Built native Store MSIX packages on x64 and ARM64 hardware (`Folimeld_1.0.2.0_x64.msix`, `Folimeld_1.0.2.0_arm64.msix`), passed static checks (`msix_preflight`), completed source bundle association, and recorded verified package information in the release plan (`windows-store-release-plan.md`) and MSIX acceptance documentation (`windows-store-acceptance.md`). Completed submission to Partner Center (Submission 2) on 2026-11-16 for Certification review. Maintained free-app-only policy with in-app supporter add-ons kept disabled.

- Consolidated and unified the prerequisites, download, installation, and execution guides for all three Windows 11 preview packages (source + uv, `uv tool install`, and Desktop installer) across x86_64 and ARM64 in bilingual READMEs and documentation, with architecture-specific SHA-256 verification and Smart App Control guidance.

- Add three preview packages for Windows 11 ARM64 (such as Copilot+ PCs / Snapdragon X Elite): source + uv edition, `uv tool install` edition, and PyInstaller onedir + Inno Setup Desktop installer edition.
  - Adopt official Python Software Foundation (PSF) signed CPython 3.12.10 ARM64 (`pythonarm64.3.12.10.nupkg`) and native ARM64 uv 0.13.8, establishing an environment setup that prevents unsigned binary block notifications under Windows 11 Smart App Control (SAC).
  - Add native ARM64 support across `install_uv.ps1`, `launch_uv.py`, `folimeld.uv_tool_launcher`, `folimeld.desktop_profile`, `folimeld.uv_tool_profile`, `pyproject.toml`, `Folimeld-desktop.spec`, `tools.desktop_build`, `tools.desktop_compile`, and `tools.uv_tool_build` (PE Machine `0xAA64`, ARM64 CRT 14.52.37029.0).
  - Expand test suite to accept ARM64 environments and safely handle Smart App Control restrictions during testing.

- Add the Windows 11 x86_64 `uv tool install` edition (Pure Python Wheel / GitHub Releases distribution): add `pyproject.toml`, deterministic Wheel and corresponding-source ZIP builder/verifier (`tools.uv_tool_build`), packaged `_resources` resolution (`folimeld.resources`), isolated `%LOCALAPPDATA%\Folimeld-UV-Tool` profile, dedicated `folimeld` / `folimeld-console` entry points validating CPython 3.12.x minor version match plus 14 pinned dependencies with the `Local\Folimeld-UV-Tool` mutex, bilingual documentation, and unit/isolated-install verification.

- Publish the Linux ARM64 strict Snap 0.3.4+fix1 preview after dedicated conversion/save/exit, same-candidate reinstall, confinement and outer-library provenance checks. Record the automatic-update Xorg interruption separately and verify the post-update retry.

- Publish the Linux ARM64 DEB 0.3.4+fix1 preview: image-conversion exit fix, byte-identical rebuild, Ubuntu ARM64 GUI/removal-reinstallation checks, and matching sources for all 210 native files. Debian acceptance uses saved records of the same DEB and was not rerun today. Preserve existing downloads.

- Integrate Linux RPM builds for Fedora, Leap 16.1, Tumbleweed, and AlmaLinux 9, package overwrite refusal, the asynchronous rotated-thumbnail layout fix, and full PyInstaller/LibTIFF LZW notices into main. Synchronize the source version to 0.3.5; existing other-OS downloads remain unchanged.
- Additionally verify the public DEB 0.3.5 on Ubuntu 24.04.4: Mozc conversion, GIO, encrypted-PDF editing/saving and reauthentication, and image import/saving. These additional features were not retested on Debian/Kali.

- Add signed application and private MuPDF dependency packages, matching source, build tools, and bilingual installation instructions for OpenBSD 8.0 / amd64

- Restrict the Windows build DLL search path to required Python, Windows and Git locations; validate native binary provenance and stop builds that collect binaries from unrelated tools
- Embed a Per-Monitor V2 DPI-awareness manifest in the Windows executable; subsequent hardware tests still report a WACK DPI warning, which remains under investigation
- Add Japanese/English Store listing drafts, screenshot plans, publication decisions, and arrival-day Dynabook test instructions with a result template
- Add short-lived signed development MSIX test bundles with source/payload hash verification and separate-PC installation, reporting and scoped cleanup scripts
- Collect checksum-verified OpenSSL/Rust sources and native dependency notices for Windows x64 encryption; add a reproducible collector, integrity tests, and review records
- Encrypt intermediate image-conversion PDFs directly and authenticate them before opening from memory; preserve the current document on authentication or conversion failure and verify temporary-file cleanup
- Encrypt spilled history and temporary save input with AES-256-GCM, keep keys out of files/settings, and release plaintext to PDF processing only after authentication. Test tampering, short writes, abnormal termination, and save-failure recovery; account for encryption metadata in history budgets and update dependency notices
- Add implementation-based Japanese/English privacy policy drafts and pre-publication temporary-data/log checks as work to proceed with while awaiting Microsoft's migration response
- Record MSIX as the Microsoft Store publishing approach; separate development/Store builds and add identity/version preflight validation and static checks of generated MSIX packages. Migration/name handling for the existing EXE/MSI registration and actual MSIX identity details await confirmation
- Move supplementary documentation, verification records, and README images from `docs/` to `documentation/`, updating document links and source ZIP collection
- Standardize documentation filenames as `<base>.md` for English and `<base>_ja.md` for Japanese, updating cross-document links and translation synchronization rules
- Speed up saving large image PDFs by skipping stream deduplication; add a progress dialog and a separate writing process, verifying preservation of edits and history on failure and protection of existing destinations on write failure
- Spill Undo/Redo history exceeding the 128 MiB memory budget to local temporary files up to 1 GiB, enabling history for large documents; release unused temporary history on document close and history branching
- Separate thumbnail management into a dedicated class and optimize viewport searches and movement of contiguous page selections
- Add dependency version constraints for distribution builds and CI, unused-code checks, type checks for the model and history layers, and bounded local error logs
- Detect broken pipes when image conversion exits without returning a result on Windows, avoiding an indefinite wait

- Add File → Exit; show all file types in the image folder picker and add shortcuts to configured OneDrive folders on Windows

- Import image folders as new PDFs with ascending or descending name, creation-time, or modification-time sorting, exclusions, page sizes, progress, and cancellation

- Record whether Undo/Redo actually ran in performance measurements, and document three runs each for three image PDFs and successful CI on all three operating systems
- Limit thumbnails for large PDFs to the viewport and nearby pages, releasing off-screen images and rendering them again when scrolling; normally retain up to 64 thumbnails and retain all pages for documents with 64 pages or fewer
- Resynchronize thumbnails with the replacement PDF after saving, edit rollback, or closing Document Properties
- Add document scrolling and retained thumbnail counts to performance measurements, comparing a 1,000-page PDF before and after the changes with three runs each
- Strengthen PDF operation validation and edit error reporting, and verify history and save-state preservation after failures
- Reorder a single page with one move and yield between thumbnail renders after approximately 16 ms
- Add test CI for Windows, Linux, and macOS, static checks, a PDF performance measurement tool, and pre-release verification instructions
- Preserve edits and Undo/Redo history after save failures so saving can be retried; prevent temporary filename collisions and clean up temporary files on failure
- Fix inconsistencies between Document Properties and saved cover settings for continuous two-column layouts
- Reuse thumbnails and render them in small batches, prioritizing the visible area; rerender only affected pages after rotation
- Limit PDF data in Undo and Redo history to a combined 128 MiB, removing older history first

## 0.3.7 Linux / BSD amd64 previews (all 10 targets) - 2026-11-22

- Publish all 10 Linux and BSD amd64 (`x86_64`) targets from commit `01501d7125419007420f2adb1cd503969684dacb` (`release/linux-bsd-amd64-0.3.7`) as Pre-releases while preserving `latest` (`macos-source-v0.3.5`) and existing 0.3.5 / ARM64 downloads. Redownload all 42 assets across all 10 Releases over unauthenticated HTTPS and verify exact byte sizes and SHA-256 hashes.
  - **Linux DEB / strict Snap**: [`linux-deb-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.7) (verified upgrade install and offscreen launch on Ubuntu 24.04.5, Debian 13.7, and Kali Rolling 2026.3 WSL2), [`linux-snap-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/linux-snap-amd64-v0.3.7) (verified `snap install --dangerous` and offscreen launch on Ubuntu 24.04.5).
  - **Linux RPM**: [`opensuse-tumbleweed20261110-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.7), [`opensuse-leap161-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.7), [`fedora44-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/fedora44-amd64-v0.3.7), [`fedora45-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.7), [`almalinux9-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.7) (verified install and offscreen launch in each distribution's Test WSL2).
  - **BSD**: [`freebsd-v0.3.7_1`](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.7_1) (verified `pkg add -f` and offscreen launch in FreeBSD 15.1 VM), [`netbsd-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/netbsd-v0.3.7) (verified `pkg_add -u` and offscreen launch in NetBSD 11.1 VM), [`openbsd-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/openbsd-v0.3.7) (verified Signify signing, `signify -V`, `pkg_add -r`, and offscreen launch in OpenBSD 8.0 VM).

## 0.3.7.0 Windows x64 Desktop installer preview / 0.3.7 source + uv preview - 2026-11-22

- Publish the [Windows 11 x64 Desktop installer preview 0.3.7.0](https://github.com/tyamada/Folimeld/releases/tag/windows-desktop-v0.3.7.0-preview.1) (12 assets) and [Windows 11 x64 source + uv preview 0.3.7](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-v0.3.7-preview.1) (4 assets) from commit `6841276fa3de03b039076c91cf947c8198c757df` (`release/windows-x64-0.3.7-preview.1`) as Pre-releases while preserving `latest` (`macos-source-v0.3.5`) and existing 0.3.5 downloads. Redownload all 16 public assets over unauthenticated HTTPS and verify exact byte sizes and SHA-256 hashes.
- Bring post-0.3.5 changes to both distribution channels, including the PDF close action, modeless empty-document prompt, and on-demand sample manga PDF downloads (“Open sample PDF…”) with SHA-256 verification and editable working copies.
- For Desktop installer 0.3.7.0, verify installer blocking while `Local\Folimeld-Desktop` mutex is held (exit code 1), non-elevated fresh install with all 201 payload files matching `payload-review.json` SHA-256, same-version overwrite refusal (exit code 7), frozen `FolimeldDesktop.exe` launch / duplicate-launch rejection (exit code 1) / clean exit (exit code 0), and `unins000.exe` removal preserving `%LOCALAPPDATA%\Folimeld-Desktop`.
- For source + uv 0.3.7, verify ZIP SHA-256 check, fresh extraction, `install_uv.ps1` setup with pinned CPython 3.12.16 / uv 0.13.8 / 14 dependencies and `uv pip check`, online sample catalogue retrieval and verified Japanese manga PDF download/save/reopen, GUI launch via `launch_uv.py`, and isolated logging.
- Live three-worker PID observation, upgrade/rollback from 0.3.5 / 0.3.5.0, coexistence with production Microsoft Store install, multi-DPI/multi-monitor scaling, and ARM64 remain unverified. This is not an update to Microsoft Store 1.0.1.0.

## 0.3.7 preview.1 Windows x64 uv tool install preview - 2026-11-21

- Publish the [Windows 11 x64 uv tool install edition 0.3.7 preview.1](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.7-preview.1) as a Pre-release, preserving Latest and existing 0.3.5/0.3.6 downloads. Redownload all ten public assets, including the Wheel, corresponding source, manifests, dependency lock and notices, and verify their sizes and SHA-256.
- Add one-book-at-a-time sample manga PDF downloads through “Open sample PDF…” in the File menu or empty-document prompt. Include a language filter defaulting to the app/system language, newest-first (default)/episode-one-first ordering, and copyright/CC BY 4.0 attribution. Verify downloaded PDFs with SHA-256 and open separate working copies. PDFs are not bundled; the first download requires internet access. Verified originals can be reused offline.
- Verify installation into a fresh isolated uv tool environment, GUI launch, online catalogue retrieval, one Japanese manga download/verification, eight-page display, Save As, reopen and exit. Fresh three-worker PID observation, upgrade/rollback, Store coexistence, mixed DPI and ARM64 remain unverified for this candidate.
- Continue recommending Microsoft Store for everyday use. Store version 1.0.1.0 does not include this download feature; this is not a Store update. ARM64 uv tool install guidance remains on the existing 0.3.5 release.

## 0.3.5.0 Windows x64 Desktop installer preview - 2026-11-16

- Publish the [Windows 11 x64 Desktop installer preview](https://github.com/tyamada/Folimeld/releases/tag/windows-desktop-v0.3.5.0-preview.1) (PyInstaller onedir + Inno Setup 7.1.1) as a Pre-release while preserving `latest`. Distribute 12 assets (Setup EXE, matching source ZIP, payload review ledger, internal source manifest, commit association, Installed-packages, third-party notices, dependency sources ledger, English/Japanese CRT user notices, compile result, and SHA256SUMS) and verify public redownload sizes and SHA-256 hashes for all 12 files.
- Verify the Microsoft Runtime-scoped consent page and original RTF hash guard, unused Qt module exclusion, canonical 7-file CRT normalization, `Local\Folimeld-Desktop` mutex protection, and isolated `%LOCALAPPDATA%\Folimeld-Desktop` settings/logs. Verify installer blocking while mutex is held, non-elevated fresh install with all 201 installed files matching `payload-review.json` SHA-256, same-version overwrite refusal, frozen `FolimeldDesktop.exe` CLI PDF launch, Per-Monitor V2 DPI, duplicate-launch rejection, clean exit, and `unins000.exe` removal preserving user settings.

## 0.3.5 Windows x64 uv tool install preview - 2026-11-16

- Publish the [Windows 11 x86_64 uv tool install preview](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.5-preview.1) (Pure Python Wheel / GitHub Releases distribution) as a Pre-release while preserving `latest`. Distribute 10 assets (Wheel, dependency lock, runtime profile, matching source ZIP, internal manifest, commit association, third-party notices, dependency sources ledger, SHA256SUMS, and release manifest) and verify public redownload sizes and SHA-256 hashes for all 10 files.
- Implement `pyproject.toml`, deterministic Wheel and corresponding-source ZIP builder/verifier (`tools.uv_tool_build`), packaged `_resources` resolution (`folimeld.resources`), isolated `%LOCALAPPDATA%\Folimeld-UV-Tool` profile, and dedicated `folimeld` / `folimeld-console` entry points validating CPython 3.12.x minor version match plus 14 pinned dependencies with the `Local\Folimeld-UV-Tool` mutex. Verify isolated `uv tool install`, real GUI PDF editing, image conversion, all 3 spawned workers, Per-Monitor V2 DPI, settings persistence across restart, mutex duplicate-launch rejection, and non-interference with other editions and registry entries.

## 0.3.5 Windows x64 uv preview - 2026-11-15

- Publish the [Windows 11 x64 source + uv preview](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-v0.3.5-preview.1) as a Pre-release, with a source ZIP, internal manifest, source commit association and SHA-256 checksums. Microsoft Store remains the standard Windows distribution channel.
- Pin CPython 3.12.16, uv 0.13.8 and fourteen dependencies, with dedicated settings and log storage. Verify fresh installation from the release candidate ZIP, regular launch, PDF display/Save As/reopening, image conversion/saving, start/end of all three workers and settings persistence after restart. All four files downloaded from the published Release match their expected sizes and SHA-256 hashes.
- Production Store coexistence, cross-version updates/rollback, multiple display scales/monitor transitions and effectiveness against the known crash remain unverified.

## 0.3.5 Kali ARM64 preview - 2026-11-14

- Publish [Kali2026.3 ARM64 DEB0.3.5](https://github.com/tyamada/Folimeld/releases/tag/kali-arm64-v0.3.5). Fresh ARM64 checks cover PDF editing/image conversion/save,purge/reinstall preserving documents/settings,and minimum-dependency startup. Normal-user Xorg/IceWM,all3GUI exits0.
- 410tests/69subtests pass,9skip;ruff passes. Verify1011inputs,173AArch64 members,30corresponding source packages and all16public redownloads. CFFI built from official source with dynamic Kali libffi;219upstream tests pass. ELF/DEB match across two output roots. Unsigned GitHub preview,glibc>=2.43. Other versions/current rolling,physical ARM,full desktops/Wayland/IME/upgrades untested. Preserve prior releases/latest.

## 0.3.5 openSUSE Tumbleweed ARM64 preview - 2026-11-14

- Publish [Tumbleweed20261111 ARM64 RPM0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed-arm64-v0.3.5). Normal-user Xorg/IceWM with SELinux Enforcing;all3GUI exits0. Verify PDF editing/image conversion/save,full removal/reinstall preserving documents/settings,and minimum-dependency startup.
- 410tests/69subtests pass,9skips;ruff passes;ELF matches across two output roots. Verify1001inputs,201AArch64 members,32signed SRPMs and all16public redownloads. Unsigned GitHub preview,glibc>=2.44. Other snapshots/physical ARM/Wayland/IME/cross-version updates untested. Minimal desktop requires added fonts for CJK glyphs. Preserve previous releases/latest.

## 0.3.5 openSUSE Leap 16.1 ARM64 preview - 2026-11-13

- Publish [Leap16.1 ARM64 RPM0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-arm64-v0.3.5). Fresh ARM64 checks cover installation, PDF editing/image conversion/save, full removal/reinstall with document/settings preservation and minimum-dependency startup. SELinux Enforcing; all 3 GUI runs exited 0.
- Verify 410 passed/9 skipped/69 subtests, identical ELF across two output roots,999inputs, 202AArch64 native members (105 official-wheel / 95 signed OS payload / 2 source-built fixed Brotli), 32 exact signed SRPMs and all 16 public redownloads. Unsigned GitHub preview, glibc>=2.40. Physical ARM/Wayland/IME/cross-version updates untested. Preserve prior releases/latest.

## 0.3.5 AlmaLinux 9 ARM64 preview - 2026-11-13

- Publish [AlmaLinux9.8 ARM64 RPM0.3.5-2](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-arm64-v0.3.5). Source-build Qt/PySide6.11.2 on glibc2.34 with required modules only; omit Qt standard translation catalogs, include app translations. Revision2 fixes the minimum-root OpenGL dependency.
- Verify editing/save, image PDF, full removal/reinstall with document/settings preservation,3normal GUI exits and minimum dependency startup on an ARM64 execution VM.410passed/9skipped/69subtests;994inputs,163native members,39signed SRPMs and public redownloads of all16attachments matched. Two app roots sharing one Qt SDK yield identical ELF; RPM times differ. Unsigned preview accepted on9.8 only; physical ARM/Wayland/IME/cross-version updates untested. Preserve prior releases/latest.

## 0.3.5 Fedora 45 ARM64 preview - 2026-11-13

- Publish [Fedora45 ARM64 RPM 0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/fedora45-arm64-v0.3.5). Fresh ARM64 checks cover installation, editing/save, image PDF, full removal/reinstall with document/settings preservation and minimum-dependency startup. SELinux remained Enforcing; all 3 GUI runs exited normally.
- Verify 409 passing Fedora ARM64 tests/9 skipped/67 subtests, identical ELF from two output roots on one VM, 981 inputs/200 AArch64 native members, 34 signed source RPMs and public redownloads of all 16 attachments. RPM header times differ. Unsigned GitHub preview; physical ARM/Wayland/IME/cross-version upgrade remain untested. Preserve existing downloads and latest.

## 0.3.5 Fedora 44 ARM64 preview - 2026-11-13

- Publish [Fedora44 ARM64 RPM 0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/fedora44-arm64-v0.3.5). Fresh ARM64 checks cover installation, editing/save, image PDF, full removal/reinstall with document/settings preservation and minimum-dependency startup. SELinux remained Enforcing; all 3 GUI runs exited normally.
- Verify 409 passing Fedora ARM64 tests/9 skipped/67 subtests, identical ELF from two output roots on one VM, 974 inputs/200 AArch64 native members, 34 signed source RPMs and public redownloads of all 16 attachments. RPM header times differ. Unsigned GitHub preview; physical ARM/Wayland/IME/cross-version upgrade remain untested. Preserve existing downloads and latest.

## 0.3.5 Linux strict Snap ARM64 preview - 2026-11-13

- Publish [ARM64 strict Snap 0.3.5 for Ubuntu24.04](https://github.com/tyamada/Folimeld/releases/tag/linux-snap-arm64-v0.3.5). Fresh Snap-specific checks cover editing, image conversion/save, clean exits, old-version update, same-candidate reinstall and document/settings preservation. Record AppArmor enforce, Seccomp2 and limited allow/deny probes.
- Verify 409 passing ARM64 tests/9 skipped, byte-identical Snaps from separate build roots on one VM, matching materials for 968 inputs/210 internal and 11 outer native files, and public redownload checks of all 16 assets. Full removal/reinstallation, IME/Wayland/physical hardware remain untested. Publish as a GitHub asset without a Snap Store assertion; preserve existing downloads and latest.

## 0.3.5 Linux DEB ARM64 preview - 2026-11-13

- Publish [ARM64 DEB 0.3.5 for Ubuntu 24.04 / Debian 13](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-arm64-v0.3.5). Fresh checks on both OSes cover major PDF editing, image conversion, clean exits, removal/reinstallation and document/settings preservation; verify saved page order, rotation and image pixels.
- Record 409 passing ARM64 tests/9 skipped, minimal-Ubuntu startup, byte-identical DEBs from separate build roots on the same VM, matching materials for 961 inputs/210 AArch64 files, and post-publication redownload checks of all 16 assets. IME/Wayland/physical hardware/encryption and forms GUI were not retested. Preserve existing downloads and latest.

## 0.3.5 Linux DEB amd64 preview - 2026-11-13

- Publish an [amd64 DEB preview](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5) verified for updates, removal/reinstallation, startup, and Japanese PDF rotation/undo in dedicated Ubuntu 24.04.4, Debian 13.6, and Kali Rolling 2026.3 WSL2/WSLg environments. Ubuntu additionally passed editing, saving/reopening, and minimal-chroot startup.
- Verify 870 source inputs, 214 native entries, 61 matching Ubuntu sources, 53 signed Sources indexes, and 12 public attachments. State that IME/GIO/encrypted-PDF/image GUI tests were not repeated; preserve existing 0.3.4, ARM64, Snap, and latest.

## 0.3.5 openSUSE Tumbleweed 20261110 amd64 preview - 2026-11-13

- Publish the amd64 RPM 0.3.5-1.tw20261110 verified in dedicated WSL2/WSLg environments as a [GitHub preview release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.5). Verify major GUI workflows, Japanese filename saving/GIO, Mozc input, encrypted PDFs, image PDFs, updates, removal/reinstallation, and fresh minimal-installroot startup.
- Fix 864 matching inputs in a dedicated source commit; verify 206 distributed native entries, 35 signature-verified source RPMs and 11 attachments. The minimal root uses regular rolling repositories with chroot, not an independent boot of a pinned 20261110 environment. Other snapshots, conventional desktops, ARM64, and migration from public 0.3.4 remain unverified. Preserve existing Releases and latest.

## 0.3.5 openSUSE Leap 16.1 amd64 preview - 2026-11-13

- Publish the amd64 RPM (0.3.5-1) verified in dedicated WSL2/WSLg environments as a [GitHub preview release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.5). Verify PDF editing, Japanese filename saving/GIO reopening, encrypted PDFs, image PDFs, Mozc Japanese input, updates, removal/reinstallation, and fresh minimal-installroot startup.
- Fix 858 matching source inputs in a dedicated commit. Verify 209 distributed native entries, 36 signature-verified source RPMs and 11 attachments. Conventional desktops, ARM64, Tumbleweed, and migration from public Ubuntu/Debian 0.3.4 are outside the verified scope. Document synthetic-input failures/retests and provenance limits; preserve existing downloads and latest.

## 0.3.5 Fedora 44 amd64 preview - 2026-11-13

- Publish the amd64 RPM (0.3.5-2), verified in dedicated Fedora 44 WSL2/WSLg environments, as a [GitHub preview release](https://github.com/tyamada/Folimeld/releases/tag/fedora44-amd64-v0.3.5). Verify PDF editing, Japanese filename saving/reopening, encrypted PDFs, image PDFs, Japanese input, GIO, updates, removal/reinstallation, and fresh minimal-installroot startup.
- Verify 822 matching source inputs, 207 distributed native entries, 37 signature-verified source RPMs and 11 attachments. Conventional desktops, ARM64, and migration from public Ubuntu/Debian 0.3.4 remain unverified. Preserve existing downloads and latest.

## 0.3.5 Fedora 45 amd64 preview - 2026-11-13

- Publish an amd64 RPM (0.3.5-2) verified on Fedora 45 WSL2/WSLg as a [GitHub preview release](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.5) (Japan time).
- Verify PDF editing, Japanese filename saving and reopening, password-protected PDFs, image PDFs, Japanese input, GIO, updates, removal/reinstallation, and offscreen startup in a fresh minimal-dependency installroot. Conventional desktops, Fedora 44, ARM64, and migration from public Ubuntu/Debian 0.3.4 remain untested.
- Freeze 785 matching source inputs in a dedicated commit and attach 11 files including dependency sources, third-party notices, verification records, known limitations, and SHA-256 checksums. The RPM and checksums are unsigned. Preserve existing downloads and the latest release.

## 0.3.5 AlmaLinux 9 amd64 preview - 2026-11-12

- Publish the amd64 RPM (0.3.5-5), verified on AlmaLinux 9.8 under WSL2/WSLg, as a preview in the [GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.5).
- Verify PDF editing, Save As with Japanese filenames, reopening, Japanese input, upgrades between candidates, removal/reinstallation, and minimal-dependency startup. Conventional desktops, ARM64, AlmaLinux 10, and migration from public Ubuntu/Debian 0.3.4 remain untested.
- Include the thumbnail layout fix and supplemental PyInstaller, LibTIFF LZW, ICU, and Qt/MuPDF notices. Attach matching source, dependency-source materials, verification records, known limitations, and SHA-256 checksums. Retain existing Ubuntu/Debian 0.3.4 distributions and releases for other operating systems.

## 0.3.4 - 2026-11-10

- Released Folimeld 0.3.4 for Linux on November 10, 2026.
- Published amd64 and ARM64 DEB packages for Ubuntu 24.04 and Debian 13, and amd64 and ARM64 Snap packages for Ubuntu 24.04.
- Matching source archives and SHA-256 checksums are available in the [Linux 0.3.4 GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.4).

## 0.3.3_1 FreeBSD ARM64 preview - 2026-11-10

- Published the Folimeld 0.3.3 package revision 1 preview for FreeBSD 15.1 ARM64 (aarch64).
- Verified installation and operation in an Xorg desktop session on a MacBook Air M5 using QEMU with HVF.
- The package, matching source, and installation instructions are available in the [FreeBSD ARM64 GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-aarch64-v0.3.3_1).

## 1.0.1.0 - 2026-11-09

- Released Folimeld 1.0.1.0 for Windows 11 (x64) on November 9, 2026. It is available for free on the Microsoft Store in Japan and the United States. [Microsoft Store (Japan)](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=ja-JP&gl=JP) · [Microsoft Store (United States)](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=en-US&gl=US)

## 0.3.3 - 2026-09-09

- Build distribution deb packages on Ubuntu 22.04 to support Ubuntu 22.04 and later, and complete the X11 dependency declarations
- Move full license texts and third-party notices from the About dialog to a dedicated dialog, and add Licenses to the Help menu
- Verify Windows EXE / MSIX and Linux deb / Snap builds on ARM64
- Fix line endings in Linux scripts, the Snap output location, and the font configuration dependency on minimal Debian installations
- Add build-time source snapshots and records linking distribution artifacts to their sources, and fix the recorded source ZIP filename

## 0.3.2 - 2026-09-07

- Fix the About dialog so it works during normal startup even when package metadata for WinRT or other dependencies is unavailable
- Add copyright information, full license texts, third-party notices, and a source code link to the About dialog
- Bundle license documents and dependency notices in builds for all operating systems

## 0.3.1 - 2026-09-06

- Immediately update the page display description and layout change guidance when the cover page checkbox changes
- Add Page display to the Details tab in Document Properties and display a live explanation of the selected page layout
- Align the page display description to the top and fix a translation error when selecting a cover page

## 0.3.0 - 2026-09-04

- Change the project license to GNU Affero General Public License v3.0
- Centralize the application version and automatically apply it to metadata for each package format
- Add a new Folimeld application icon and images for each operating system and Microsoft Store
- Move PDF file associations to the MSIX manifest
- Support building x64 MSIX packages for Microsoft Store
- Add ARM64 MSIX build instructions and detection of architecture mismatches
- Reorganize the README for publication on GitHub and move development instructions and the changelog into separate documents

## 0.2.5 - 2026-09-03

- Improve scrolling behavior

## 0.2.4 - 2026-08-31

- Add Ubuntu support

## 0.2.3 - 2026-08-31

- Support automatic PDF version changes

## 0.2.2 - 2026-08-30

- Set up macOS build instructions, icons, and signing

## 0.2.1 - 2026-08-30

- Safely disable Windows-specific operations on macOS

## 0.2.0 - 2026-08-30

- Rename the application to Folimeld

## 0.1.0 - 2026-08-29

- Initial release
