# Changelog

[日本語](CHANGELOG_ja.md) | [English](CHANGELOG.md)

## Unreleased

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
