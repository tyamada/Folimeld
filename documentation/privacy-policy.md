# Folimeld privacy policy (pre-publication draft)

[日本語](privacy-policy_ja.md) | [English](privacy-policy.md)

Prepared: 2026-10-29 (Japan time)

This draft was prepared by reviewing the current Windows MSIX implementation. Confirm the publisher, contact details, effective date, public URL, and behavior of the package actually distributed before publication. This is not a published policy.

## Scope and publisher

Scope: Folimeld for Windows, packaged as MSIX for Microsoft Store.

- Publisher: [Enter the official publisher name before publication]
- Contact: [Enter the support URL or email address before publication]
- Effective date: [To be confirmed before publication]

## PDF and image processing

Folimeld processes PDFs you open, images you select, PDF properties, and viewing passwords you enter on your device to display, edit, and save documents. Image folder sorting uses filenames and creation/modification times. No feature is implemented to send PDF or image contents to a developer-operated server.

Viewing passwords are used to open documents and encrypt saved PDFs, and remain in memory as part of the open document and history state. No code saves them in application settings. The protection applied to a saved password-protected PDF differs from that of temporary editing data.

## Data retained on your device

| Data | Purpose and location | Retention and deletion |
|---|---|---|
| Language, thumbnail size, button display, and last-used PDF/image folder paths | Restore preferences using local Qt settings storage | Retained until changed; no automatic expiry based on time |
| PDF data for Undo/Redo | Restore edits using memory and the OS temporary-file area | Memory budget of 128 MiB and temporary-file budget of 1 GiB; older or unused history is released, including when the document closes |
| Intermediate PDF data for saving and image conversion | Separate-process writing and image conversion using the OS temporary-file area and destination folder | Removed on normal processing completion; temporary files are also used to replace the destination |
| Thumbnails | Page previews in memory | Released as the viewport or document changes; no code persistently saves separate thumbnail files |
| Error logs | Troubleshooting in `logs/folimeld.log` under Windows application-local data storage | Rotation at approximately 1 MiB, retaining up to three files including two backups; no automatic expiry based on age |

History spilled to temporary files, temporary input passed to the separate save process, and intermediate image-conversion PDFs are encrypted with AES-256-GCM. Each file gets a random key, kept out of files and settings and handled in application and necessary save/image-conversion process memory. Decrypted contents are used for PDF processing only after authentication succeeds; key references are also released when history is released.

User-selected output PDFs are encrypted according to the selected password settings. Forced process termination, OS shutdown, or deletion failures may leave temporary files behind. Automatic recovery of residual files and complete erasure from memory, OS pagefiles, or crash dumps are not guaranteed. This does not guarantee encryption of all temporary data or reliable erasure after abnormal termination.

The history budgets above apply to retained PDF history data; they do not limit total process memory or the total amount of temporary data during processing.

Logs record exception messages and tracebacks. No code explicitly passes PDF contents or passwords to logging, but exceptions may include filenames, folder paths, or information produced by libraries. No code automatically sends logs to the developer.

Saved PDFs and original images remain in the locations you select. Files in synchronization folders such as OneDrive may be synchronized according to the service's settings.

## Microsoft Store communication

The Windows MSIX edition queries Microsoft Store APIs for license and product information at startup, when the supporter purchase dialog opens, after a purchase, and when purchase status is refreshed. It uses information such as product identifiers, displayed prices, purchase results, and entitlement status. No code passes PDF or image contents as arguments to these APIs.

Purchase processing and Store account authentication use Microsoft's systems. Folimeld's code does not retrieve or store payment card numbers or Microsoft account passwords. Microsoft's privacy information also applies to data processed by Microsoft Store and Windows.

Application-specific user registration, advertising, custom usage analytics, and automatic crash reporting are not implemented. This does not disable independent processing performed by Microsoft Store or Windows.

## External links and support inquiries

When you open an external link, the website and browser's data practices apply. Separately from automatic application transmission, messages, contact details, and attachments you choose to send for support reach the support recipient. Do not include confidential documents or passwords in inquiries.

Support information purposes, retention, and contact-channel operation: [Confirm the actual support process before publication].

## Your controls and changes

Closing a document releases its editing history. Public instructions for removing settings and logs, and whether data remains after MSIX uninstallation, will be finalized after testing the submission candidate. The application does not delete existing input PDFs or PDFs you saved when it exits.

When features or data practices change, this policy will be updated at its public URL. Resolve the outstanding items above before Microsoft Store submission.
