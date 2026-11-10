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

## Remaining test priorities (2026-10-30)

Initial hardware tests and inspection of returned PDFs are recorded in the [release plan](windows-store-release-plan.md). Twenty additional cross-engine checks passed. Continue in this order:

| Priority | Test | Prerequisites and current state |
| --- | --- | --- |
| 1 | Active-conversion cancellation and document/destination protection on failure | Completed: cancellation at 31% of 72-image conversion retained the document. Invalid-image failure and a busy save destination also preserved the document and existing destination |
| 2 | Disk-backed history, temporary data, settings and logs | Verified disk-backed Undo/Redo, encrypted headers, actual storage paths and cleanup after normal exit, failure and removal. History-limit pruning, log rotation and app forced termination remain untested; do not force an OS shutdown |
| 3 | WACK precertification | WACK 10.0.28000.2957 tested 0.3.3.0: 22 PASS, one optional FAIL, one required DPI WARNING; overall WARNING. 0.3.3.2 failed to launch QtCore, so WACK was deferred. Verify startup first with DLL-isolated version 0.3.3.3, then repeat WACK and high-DPI checks. Distinguish development-candidate results from final Store-candidate results |
| 4 | Update, reinstallation and removal | The 0.3.3.0→0.3.3.2 update preserved originals and the default app, but startup failure prevented GUI settings verification. DLL-isolated version 0.3.3.3 is prepared; transfer/update/startup checks remain pending. Preserve previous ownership records. Finalize trust handling for the different test certificate and cleanup targeting the updated version before execution |
| 5 | Final Store package, purchases/restoration/refunds, ARM64 | Run after actual Identity, Store candidate, purchase configuration and target hardware are established |

Preserve the previous test directory and original reports; use a separate directory and state file for the next run. Baseline records established about 16 GiB RAM, a 237 GiB SSD, 176 GiB free and a 1366×768 display. A clean OS installation remains unverified. Distinguish user reports of manual certificate/elevated operations from directly obtained state evidence.

## References

- [Microsoft: run, debug and test an MSIX package](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-debug)
- [Microsoft: Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)

## Current diagnostic status (2026-11-04)

The October 30 priorities above are historical. See the [diagnostic follow-up](windows-store-release-plan.md#diagnostic-follow-up-updated-2026-11-04) for completed 0.3.3.3–0.3.3.13 trials and the unresolved DPI/TEST88 findings. WACK remains WARNING; no rerun or Hosted API comparison is authorized by this document. High-DPI 150%/200%, the final Store package and other outstanding acceptance work remain unverified.
