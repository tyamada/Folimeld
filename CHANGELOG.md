# Changelog

[日本語](CHANGELOG_ja.md) | [English](CHANGELOG.md)

## Unreleased

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
