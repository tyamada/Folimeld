# Microsoft Store listing (English draft)

[日本語](windows-store-listing_ja.md) | [English](windows-store-listing.md)

Pre-publication draft based on the README and implementation on 2026-10-29. Verify features on the test PC and align with the actual Store candidate before copying. The intended name is Folimeld; MSIX registration/name transfer awaits a response. Initial scope is Windows 11 x64; no verified ARM64 or other-OS claims are included.

## Short description

<!-- store:short -->
Organize PDF pages visually: reorder, rotate, insert and delete pages, or create a PDF from an image folder.
<!-- /store:short -->

## Description

<!-- store:description -->
Folimeld is a desktop app for organizing PDF pages using thumbnail previews. Put pages in the right order, correct their orientation, or add pages from another PDF. Documents are processed on your device; PDF and image content is not sent to the developer's servers for editing.

Select multiple pages to move, rotate or delete them together. Undo and Redo let you step back and repeat changes, including after saving. Opening another PDF resets the history.

Create a new PDF from a folder of JPEG, PNG, BMP, TIFF or WebP images. Sort by name or date, exclude unwanted images, and choose image-sized or A4 pages. Multipage TIFF images are supported.

Document properties let you change the PDF version, page layout and binding direction. You can also set or remove a password required to open the PDF.

Before you start
Image-folder conversion excludes subfolders and animated WebP. Editing and cancellation are unavailable during saving. Undo and Redo history has storage limits. Large documents may require more temporary memory and processing time. Test important PDFs using copies and check their contents after saving.
<!-- /store:description -->

## Product features

Copy each feature's text into Partner Center without the Markdown bullet.

<!-- store:features -->
- Reorder PDF pages using thumbnail previews
- Move, rotate or delete multiple pages
- Insert pages from another PDF or add blank pages
- Undo and Redo remain available after saving
- Create a PDF from an image folder
- Support for multipage TIFF, image orientation and transparent images
- Change PDF version, page layout and binding direction
- Set or remove a PDF opening password
- Interface available in eight languages, including English and Japanese
<!-- /store:features -->

## Submission notes (not public listing text)

- Leave What's new blank for the first submission. Do not present GitHub release history as updates already published in the Store.
- App price, markets, category (candidate: Productivity) and age rating remain undecided. Answer rating questions according to the actual app declaration.
- If supporter purchases are included, verify product retrieval, purchase and restoration through the actual Store, then align product copy and displayed prices before adding purchase information. No price or purchase-availability promises are made here.
- Confirm publisher, support and policy URLs in the [decision register](windows-store-publication-decisions.md). Do not infer values from the name or automatically use the migration inquiry's sender address.

### Proposed runFullTrust justification

Folimeld is a Win32 desktop PDF editor using PySide6/Qt and PyMuPDF. It reads and writes local PDFs and images selected by the user and displays/edits pages through a Qt desktop interface. PDF saving and image conversion use separate native processes. The app declares runFullTrust for this desktop execution model. It does not implement features that request administrator elevation.

This restricted-capability declaration is a draft, not an approval. Verify against the final manifest and runtime behavior. Do not include development-certificate installation instructions in Store customer copy.

## Sources

- [README](../README.md), `folimeld/app.py`, `folimeld/model.py`, `folimeld/image_import.py`, `packaging/msix/AppxManifest.xml.in`
- [Microsoft listing fields](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/add-and-edit-store-listing-info): description up to 10,000 characters; up to 20 features of 200 characters each; What's new blank on first submission
- [Microsoft capability declarations](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations)
