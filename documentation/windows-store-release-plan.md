# Microsoft Store release plan

[日本語](windows-store-release-plan_ja.md) | [English](windows-store-release-plan.md)

## Registration type and current status

On 2026-10-29 (Japan time), Partner Center was checked in Chrome and Folimeld was confirmed to be registered as an EXE or MSI app, unpublished, with application setup in the draft stage. MSIX identity details have not been obtained.

MSIX has been selected as the publishing approach. On the same day, checking the availability of Folimeld under New product → MSIX or PWA app returned “This name is not available.” An inquiry was sent to the Microsoft contact provided on that screen, requesting the official procedure for moving from EXE/MSI to MSIX while retaining the existing registration and name reservation.

Microsoft replied at 21:19 on 2026-10-29 (Japan time) that the submission type cannot be changed once started and a new product registration is required. Support offered assistance releasing the name, but did not guarantee a transfer that preserves the reservation or prevents another developer from reserving it. At 07:37 on 2026-10-30 (Japan time), a reply confirmed the product name Folimeld and the intent to reserve it for a new MSIX product under the same existing developer account, requesting clarification of the exact procedure. That follow-up is now awaiting a response. The existing product has not been renamed/deleted, the name has not been released, no new name reservation has been created, and actual identity details remain unavailable.

EXE/MSI submissions require an offline installer with silent installation, code signing that chains to a trusted CA, and a versioned HTTPS URL whose binary remains unchanged after submission. Updates for existing users are also the application's responsibility. The standalone executable produced by `build_exe.bat` is not this installer.

MSIX submissions can use Store signing, hosting, and update delivery. Obtain the following values for the MSIX registration before filling in the Store configuration. Do not substitute the EXE/MSI application's application ID.

| Partner Center field | Store configuration key |
|---|---|
| `Package/Identity/Name` | `identity_name` |
| `Package/Identity/Publisher` | `publisher` |
| `Package/Properties/PublisherDisplayName` | `publisher_display_name` |

## Partner Center findings and next steps

1. On 2026-10-29 (Japan time), opened Apps and games → New product → MSIX or PWA app, entered Folimeld, and checked availability. Partner Center reported “This name is not available.”
2. On the same day, sent an English inquiry to Microsoft through Outlook and verified it in Sent Items. It asked whether the existing registration could be converted to MSIX, how to transfer or associate the reserved name if a separate MSIX registration was required, and whether Microsoft could assist while preserving the existing registration and name reservation.
3. The 21:19 reply confirmed that changing the submission type is unavailable and a new product registration is required. Microsoft requested confirmation of the product name and offered help releasing it. The reply also described a general rename/release/re-reservation approach and reference steps for deleting an unpublished EXE/MSI draft when deletion is unavailable. Applicability to the current draft is unverified; no rename, resubmission, certification cancellation or deletion has been performed.
4. At 07:37 on 2026-10-30, sent the user-reviewed reply to `reportap@microsoft.com`, verifying recipient, body and timestamp in Sent Items. It explicitly specifies the same existing developer account and asks the three questions below. It requests that the name not be released until the procedure is confirmed and agreed; this reply is not authorization to release it.
5. Review the follow-up response for the sequence, responsibilities and risks of securing the name, and agree on the procedure with the user before registration actions. Retain the existing product/name reservation meanwhile. Once the new MSIX registration and name reservation are ready, obtain the three identity values above from Product management → Product Identity.

The three follow-up questions:

- Can the name be transferred/associated directly with a new MSIX product under the same developer account without making it available to other developers?
- If release/re-reservation is necessary, what is the exact sequence, including when to create the new MSIX product, which steps Microsoft/developer handle, and how to avoid another developer reserving it?
- Must the unpublished EXE/MSI draft be renamed/deleted, and if so at what point?

Deleting a name reservation makes the name available for other developers to reserve, so do not assume deletion is a safe transfer mechanism even for an unpublished product. The existing registration and name reservation remain intact.

Inquiry record:

- Sent: 2026-10-29 (Japan time)
- From: takumayamada22@outlook.jp (Outlook)
- To: reportapp@microsoft.com
- Subject: Guidance requested: Moving Folimeld from EXE/MSI to MSIX while retaining its reserved name
- Initial inquiry status: Response received; changing submission type is unavailable and a new product registration is required
- Microsoft response: Received from Microsoft Store Report App Team at 21:19 on 2026-10-29 (Japan time)
- Follow-up reply: Sent to `reportap@microsoft.com` at 07:37 on 2026-10-30 (Japan time)
- Follow-up subject: Re: Guidance requested: Moving Folimeld from EXE/MSI to MSIX while retaining its reserved name
- Current status: Awaiting clarification of the same-account name-reservation procedure, responsibilities and risks. Name release is neither authorized nor performed

The initial recipient was `reportapp@microsoft.com`; the responding address and follow-up recipient are `reportap@microsoft.com`. These distinct addresses reflect the actual messages.

## Sequence and completion criteria

| Order | Work | Status / completion criteria |
|---|---|---|
| 1 | Registration type, name, and identity | Microsoft confirmed that changing submission type is unavailable and a new product registration is required. Follow-up sent on 2026-10-30 about securing Folimeld under the same developer account; response pending. Existing registration/name retained; release neither authorized nor performed; actual identity unavailable |
| 2 | Submission build and static checks | Development/Store modes and version, configuration, and generated-MSIX checks implemented; no build with actual Store identity yet |
| 3 | Privacy, support, and corresponding source | Drafted Japanese/English privacy policies and implemented encryption for history/save input and intermediate image PDFs. Publisher, support channel, public URLs, dependency sources, OS-shutdown residues and deletion tests for actual MSIX remain outstanding |
| 4 | Windows 11 x64 acceptance tests | Verify clean installation, PDF association, editing, saving, child processes, updates, and removal |
| 5 | WACK, listing materials, and limited distribution | Prepare WACK results, Japanese/English descriptions and screenshots, age ratings, and runFullTrust justification; retest the Store-delivered app |
| 6 | Supporter purchases and ARM64 | Test purchases, restoration, refunds, failures with a Store license, and physical ARM64 hardware; do not treat untested configurations as released |
| 7 | General availability and maintenance | Confirm release decisions, support handling, and delivery of corrective updates |

## Work while awaiting clarification of name reservation

On 2026-10-29, Japanese/English [listing drafts](windows-store-listing.md), [screenshot plans](windows-store-screenshot-plan.md), a [publication decision register](windows-store-publication-decisions.md) and [first-test instructions for the Dynabook](windows11-test-day.md) were prepared. Initial tests ran on 2026-10-30 on a Dynabook B65/DN (Core i5-8250U, Windows 11 Pro 25H2, 26200.9818, x64). Store screenshot capture and publication decisions remain pending.

The separate test PC used the [signed test-bundle preparation, installation and cleanup instructions](windows-store-test-bundle.md). The candidate was `Folimeld.Dev` 0.3.3.0 x64, with MSIX SHA-256 `b3025711dbb3bdfdee9728ef6790c801232570949ddc76302a658e34a4a44646`. Review of the test PC chat “Microsoft Storeテスト環境を設定” confirmed installation and launch, PDF opening with a Japanese path, rotation, movement, Undo/Redo, Save As and reopening, reopening after a password change, language persistence, license display, Explorer Open with, and completion of Inspect and Remove. Password changes and elevated operations include user-reported success. Cleanup state is `removed`, and the newly added certificate trust is absent. Direct post-removal package enumeration remains unverified because of execution-environment access restrictions. No trust registration or installation was performed on the build PC.

Image import verified four-page generation, sorting and exclusion, A4 selection, and cancellation from the setup dialog. Artifacts were collected onto the development PC on 2026-10-30, and all 31 checks independent of the application workflow passed. These covered edited page order, rotation and rendering, bookmark and internal-link targets and link geometry, annotations, canonical form references and values, attachment contents and metadata. The changed-password PDF accepts the new password and rejects the old one. All four image pages are A4-equivalent (within 1 pt per dimension); pixel comparisons matched EXIF correction, transparency composited onto white, and both TIFF frames. Inspection used PyMuPDF, the same PDF engine as the application, and Pillow; it does not establish compatibility with another engine. Records, hashes and a rendering review image are stored in `build/store-acceptance/dynabook-20261030/`. Received files are nested under `outputs/outputs/`. Original test-PC reports were not modified. Cancellation during active conversion, a clean OS installation, detailed memory/disk/display specifications, WACK, updates, real Store purchases, forced termination and the final Store package remain unverified.

The [native encryption dependency review](crypto-dependency-audit.md) verified sources for OpenSSL 4.0.3 and 32 Cargo.lock Rust dependencies, and collected OpenSSL, Rust dependency, and CFFI/libffi notices. Overall dependency review and wheel build provenance remain outstanding.

The [Windows 11 MSIX acceptance checklist](windows-store-acceptance.md) defines candidate records and installation, worker, update, deletion, and certification tests. Unexecuted tests remain pending.

A [privacy policy draft](privacy-policy.md) and [Japanese version](privacy-policy_ja.md) have been prepared. They describe the current implementation and must not yet be used as the published policy URL.

- Spilled history, save input, and intermediate image PDFs now use AES-256-GCM. Automated tests check rejection of tampering, wrong keys, and short writes; preservation of documents after encryption failures; cleanup of staged input after worker failures; and absence of plaintext/key files in an encrypted container left after abrupt process exit. This does not establish reliable erasure on OS shutdown or automatic recovery of residual files.
- Verify actual settings/log locations and manual deletion/uninstallation behavior with the submission candidate MSIX. Existing unit tests for normal saving/image conversion and worker failures do not establish deletion under all abnormal exits.
- Confirm the official publisher, support contact, support information retention/handling, and effective date. Do not automatically adopt the migration inquiry's sender address as the public support contact.
- Compare the final package with the documents, resolve outstanding items, and prepare a public policy URL. The existence of a privacy document alone does not establish Store policy compliance.

Reviewed implementations: settings/Store queries in `folimeld/app.py` and `folimeld/store_support.py`; history in `folimeld/model.py` and `folimeld/history.py`; save/image conversion temporary data in `folimeld/pdf_save.py` and `folimeld/image_import_dialog.py`; encrypted containers in `folimeld/temporary_data.py`; logs in `folimeld/diagnostics.py`. Pre-publication dependency-source work must also verify corresponding sources/notices for actual `cryptography`/CFFI binaries and bundled components such as OpenSSL.

## Preparing a Store build

Copy `packaging/msix/store-config.example.json` to `build/store-config.json` and enter verified MSIX registration values in the first three fields. The blanks are intentional: the unchanged example fails Store validation. Do not put credentials or private keys in this file.

`package_version` is the four-component MSIX version, managed separately from the application's display version, `__version__` in `folimeld/__init__.py`. Store mode requires a first component of at least 1, a final component of 0, and components no greater than 65535. The example `1.0.0.0` has not been submitted. An update must be greater than the previous MSIX version with the same Identity/Publisher. Do not pass a previous EXE/MSI product or development MSIX as `-PreviousPackage`.

The Store release targets Windows 11. The example uses `10.0.22000.0` for `minimum_windows_version` and `10.0.26100.0` for `maximum_tested_windows_version`. Example settings are not evidence of hardware testing; update them to reflect supported operating systems and actual test results. Development mode retains the previous default minimum OS.

```powershell
# Validate configuration and manifest only; do not rebuild the EXE, create MSIX, or install
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json -ValidateOnly

# Build a submission candidate after the configuration has been confirmed
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json
```

For updates, pass the previous MSIX using `-PreviousPackage`. For ARM64, add `-Architecture arm64` to the same command and build with ARM64 Python/PyInstaller. `-PythonExecutable` accepts an absolute Python path; the same Python is passed to the EXE build.

Configuration and manifest files are written to `build/msix-preflight/<channel>/<architecture>/`. Generated-MSIX inspection results are saved there as `preflight.json`. Checks cover identity, version, OS settings, executable architecture, PDF association, icons, the license file, and package SHA-256. Successful static checks do not establish matching Partner Center registration, WACK success, hardware acceptance, license compliance, or certification approval.

## Official references

- [Distribution path comparison](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path)
- [EXE/MSI package requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements)
- [EXE/MSI updates](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/publish-update-to-your-app-on-store)
- [MSIX package requirements and versioning](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Store policies](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIX name reservations](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)
- [EXE/MSI name reservation management](https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/msi/manage-app-name-reservations)
