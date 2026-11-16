# Windows 11 MSIX acceptance tests

[日本語](windows-store-acceptance_ja.md) | [English](windows-store-acceptance.md)

Use this checklist for a specific package, not just an application version. Keep results under `build/store-acceptance/<run>/` and publish reviewed release evidence separately. A checklist entry is pending until supported by a result. Unit tests and unsigned development packages do not establish Store readiness.

## Record the candidate

Record the package name/SHA-256, executable SHA-256, source ZIP/hash and association JSON, package Identity/Publisher/version/architecture, signature/channel, OS build, Python/dependency versions, Windows SDK/WACK versions, test date and tester. Keep source records from `dist/source/` with that candidate. Exclude private documents and passwords from evidence.

```powershell
# Development package; no installation or certificate changes
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1
# Package digest: replace the filename with the actual generated package
Get-FileHash .\dist\Folimeld_0.3.3.0_x64.msix -Algorithm SHA256
```

`build/msix-preflight/development/x64/preflight.json` records static checks; Store builds use `store` instead of `development`. Inspect the package's executable hash against its association JSON. Build a Store candidate only after obtaining the verified identity described in the [release plan](windows-store-release-plan.md).

## Test matrix

Run on a clean Windows 11 x64 test environment without Python installed. Use copies of test fixtures and preserve originals. Record steps, expected/actual result, evidence and pass/fail/pending for every row. Test only one candidate at a time.

| Area | Required behavior and evidence |
| --- | --- |
| Installation and launch | Signed test package installs; Start menu launch works; license texts and source-build information open; no development-machine paths or missing runtime dependencies |
| PDF association | Opening via Explorer reaches the correct document, including Japanese/spaced paths; association selection respects the user's choice |
| Editing and history | Rotation, move, deletion, properties and passwords work; Undo/Redo survive saving; spilled history restores correctly |
| Save worker | New-file and overwrite saves reopen with expected content, images, links, annotations, forms, metadata and password behavior; failed writes preserve the destination and edits |
| Image worker | PNG/JPEG/multipage TIFF conversion, ordering, orientation, transparency and A4 work; cancel/failure preserves the existing document; encrypted intermediate files are removed after processing |
| Temporary data | Observe actual temporary paths and encrypted history/save/image containers; inspect normal cleanup and worker failure; separately record forced main-process termination and OS-shutdown residues using disposable documents |
| Settings and logs | Record actual packaged-app paths; settings persist across restart; logs rotate and contain no test passwords or document content; manual cleanup and uninstall outcomes are recorded separately |
| Updates and removal | Update from the previous signed package with the same Identity/Publisher and larger version; verify settings, launch and association; record uninstall/reinstall behavior without deleting user PDFs |
| Store purchases | On the actual Store-delivered candidate, test purchase, restoration, cancellation/refund and unavailable-service behavior; development identity results do not establish purchase readiness |
| Certification | Run the current Windows App Certification Kit on the actual signed candidate; retain its complete report and investigate failures; a static-check pass is not a WACK pass |

Certificate trust changes, installation and WACK belong in the test environment. ARM64 requires its own native build and hardware results. Repeat affected tests after fixes, and retest the Store-delivered package before general availability.

## Historical development checks

Earlier development builds were checked for conversion cancellation, write failures, disk-backed history and local WACK behavior. Keep their results separate from the Store-delivered checks below. The general test matrix remains a checklist for future candidates.

## References

- [Microsoft: run, debug and test an MSIX package](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-debug)
- [Microsoft: Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)

## Store-delivered 1.0.1.0 acceptance record (2026-11-09)

Submission 1 passed Microsoft Store certification. Folimeld 1.0.1.0 was published in Japan and the United States on 2026-11-09 (Japan time). The test PC received Store-signed `TakumaYamada.Folimeld` 1.0.1.0 x64.

| Check | Result |
| --- | --- |
| Store installation, startup and normal exit | Passed |
| PDF display and Save As | Passed |
| Convert two images to PDF and save | Passed |
| PDF save, image conversion and image PDF save workers | Startup and exit confirmed for all three |
| Support purchases | Menu absent in the initial release |
| Main-window DPI context | Per-Monitor V2 confirmed |

The DPI check used `GetWindowDpiAwarenessContext` on the main window and compared the result using `AreDpiAwarenessContextsEqual`. The Per-Monitor V2 comparison returned true and the Per-Monitor V1 comparison returned false. This records the main window’s runtime context. Visual scaling checks at 150% and 200% remain unperformed.

### Open certification questions

| Item | Status |
| --- | --- |
| Earlier local WACK DPI warning | Cause unconfirmed. See the [historical diagnostic summary](windows-store-release-plan.md#diagnostic-follow-up-updated-2026-11-04). |
| TEST92 and TEST88 | Individual Store certification outcomes unconfirmed. |
| `runFullTrust` | Declared in the submission that passed overall. A separate capability decision or review comment remains unconfirmed. |

## Store candidate 1.0.2.0 preparation and acceptance plan (Submission 2: x64 & ARM64)

Acceptance plan for Submission 2 (package version `1.0.2.0`), adding native Windows 11 ARM64 support and large PDF optimizations.

### Candidate packages and preflight status

| Property | x64 candidate | ARM64 candidate |
| --- | --- | --- |
| Package file | `dist/Folimeld_1.0.2.0_x64.msix` | `dist/Folimeld_1.0.2.0_arm64.msix` |
| Package Identity | `TakumaYamada.Folimeld` | `TakumaYamada.Folimeld` |
| Version | `1.0.2.0` | `1.0.2.0` |
| Target CPU (PE Machine) | `x64` (`0x8664`) | `arm64` (`0xAA64`) |
| Package SHA-256 | `E57D690DE5D07EE956DB25A1173F56ED36B81EFD951F1C42DB651252915B7853` | `3BBB94BC7E186533030933DC9F8E99258EACEDC5EBC23149CFF295AA454515AC` |
| Preflight (`msix_preflight`) | Passed (`build/msix-preflight/store/x64/preflight.json`) | Passed (`build/msix-preflight/store/arm64/preflight.json`) |
| Source association | `dist/source/Folimeld_1.0.2.0_x64.msix-e57d690de5d07ee956db25a1173f56ed36b81efd951f1c42db651252915b7853.json` | `dist/source/Folimeld_1.0.2.0_arm64.msix-3bbb94bc7e186533030933dc9f8e99258eacedc5ebc23149cff295aa454515ac.json` |

### Submission 2 acceptance checklist

| Check | Scope | Required behavior and evidence | Status |
| --- | --- | --- | --- |
| Upgrade test from 1.0.1.0 | x64 | Install 1.0.2.0 over signed 1.0.1.0; verify settings, history, and PDF file associations are preserved | Pending |
| ARM64 hardware install & launch | ARM64 | Native launch, exit, and UI interaction on Copilot+ PC (Snapdragon X Elite, etc.) Windows 11 ARM64 | Pending |
| Large PDF save acceleration | Both | Separate worker process saving, progress dialog display, and original file preservation on failure | Unit tests passed, awaiting hardware |
| Encrypted Undo/Redo disk spooling | Both | Spool to AES-256-GCM encrypted temporary storage when memory exceeds 128 MiB; restore and secure wipe | Unit tests passed, awaiting hardware |
| Bulk image import | Both | PDF generation from image import dialog, reordering, rotation, and temp file cleanup | Unit tests passed, awaiting hardware |
| 100% Free app policy | Both | Supporter purchase menu absent; all features available freely | Confirmed |

