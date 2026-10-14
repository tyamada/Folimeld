# Changelog

[日本語](CHANGELOG.md) | [English](CHANGELOG_en.md)

## Unreleased

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
