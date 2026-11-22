# Windows 11 MSIX Acceptance Tests

[Japanese](windows-store-acceptance_ja.md) | [English](windows-store-acceptance.md)

Use this checklist for specific packages, not just application versions. Save results in `build/store-acceptance/<run>/`; publish public records only after verifying contents. Check items without evidence as incomplete. Neither unit tests nor unsigned dev packages qualify a build for Store release.

## Candidate records

Record package name and SHA-256, executable SHA-256, source ZIP, hash, and matching JSON, package Identity, Publisher, version, and CPU, signature and distribution channel, OS build, Python and dependency versions, Windows SDK and WACK versions, test date, and tester. Keep matching records in `dist/source/` with the candidate. Do not include personal documents or test passwords in evidence.

```powershell
# Generate a development package. Do not install or change certificates.
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1
# Package hash. Replace with the actual generated filename.
Get-FileHash .\dist\Folimeld_0.3.3.0_x64.msix -Algorithm SHA256
```

Preflight records are stored at `build/msix-preflight/development/x64/preflight.json`. For Store builds, `development` becomes `store`. Verify the executable hash in the package matches the record. Build Store candidates only after verifying the actual Identity per the [release plan](windows-store-release-plan.md).

## Test matrix

Execute on clean Windows 11 x64 test systems without Python installed. Use disposable test copies; keep originals safe. Record procedure, expected behavior, observed results, evidence, and pass/fail/incomplete for each row. Do not test multiple candidates concurrently.

| Scope | Required behavior and evidence |
| --- | --- |
| Install & launch | Install signed test package and launch from Start menu. Display full licenses and build source info; no missing runtime dependencies or hard-coded developer paths |
| PDF association | Open correct document via Explorer, even with Japanese or space-separated paths. Respect user's choice of default handler |
| Edit & history | Rotate, move, delete, view properties, handle password-protected documents; undo and redo work after saving. Recover disk-spooled history |
| Save worker | Open saved new/overwritten files; verify text, images, links, annotations, forms, metadata, and passwords. On write failure, preserve destination file and pending edits |
| Image worker | PNG, JPEG, multi-page TIFF; order, orientation, transparency, A4 sizing. On cancellation or failure, preserve document and clean up encrypted intermediates |
| Temporary data | Observe actual temp directory and encrypted containers for history, saves, and image conversions. Clean exit and worker failure cleanups; record hard crashes using test documents |
| Settings & logs | Record actual storage paths for packaged application. Settings persist across restarts; log rotation leaves no test passwords or document contents. Separate manual clearing from uninstallation |
| Update & removal | Upgrade to higher-versioned signed package with same Identity and Publisher; verify settings, launch, and associations. Do not delete user PDFs; record behavior during uninstall and reinstall |
| In-app purchase | On actual Store candidates, verify purchase, restore, cancellation/refund, and service-unavailable states. Development Identity results do not validate purchase flows |
| Certification | Run latest Windows App Certification Kit against signed candidate; save all logs and investigate failures. Passing preflight does not mean passing WACK |

Configure certificates, installation, and WACK on the test system. ARM64 requires native builds and real-device testing. Re-test affected items after any code changes, and re-verify Store distribution packages before public release.

## Historical development verification

Previous development builds verified image conversion interruptions, write failures, disk-spooled history, and local WACK diagnostics. Those results are recorded separately from the Store distribution acceptance below. The test matrix above applies to future candidates.

## References

- [Microsoft: Debug and test packaged desktop apps (MSIX)](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-debug)
- [Microsoft: Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)

## Acceptance record for Store distribution 1.0.1.0 (2026-11-09)

Submission 1 passed Microsoft Store certification. Folimeld 1.0.1.0 was published in Japan and the US on November 9, 2026 (JST). Store-signed `TakumaYamada.Folimeld` 1.0.1.0 x64 was deployed to the test system.

| Check | Result |
| --- | --- |
| Install from Store, launch, normal termination | Pass |
| PDF display and Save As | Pass |
| PDF conversion and save from 2 images | Pass |
| PDF save, image conversion, and image-PDF save workers | Verified launch and termination for all 3 worker types |
| Supporter purchase | Confirmed menu is omitted in initial release |
| Main window DPI context | Verified Per-Monitor V2 |

The main window DPI context was inspected using `GetWindowDpiAwarenessContext` and compared via `AreDpiAwarenessContextsEqual`. Comparison with Per-Monitor V2 was true; Per-Monitor V1 was false. This check targeted the running main window. Scaling checks at 150% and 200% were not performed.

### Open certification items

| Item | Status |
| --- | --- |
| Legacy local WACK DPI warning | Root cause unverified. See [diagnostic history](windows-store-release-plan.md#diagnostic-tracking-status-updated-2026-11-04). |
| TEST92 and TEST88 | Individual Store certification findings were not reported. |
| `runFullTrust` | Full submission with declaration passed certification. Dedicated review comments were not provided. |

## Store candidate 1.0.2.0 preparation and acceptance plan (Submission 2: x64 & ARM64)

Acceptance plan for Submission 2 (package version `1.0.2.0`), adding native Windows 11 ARM64 support and large PDF optimizations. Both x64 and ARM64 packages were submitted to Partner Center on 2026-11-16 and are currently in Certification review. The acceptance checklist below will be executed using the actual Store-delivered packages upon approval.

### Candidate packages and preflight status

| Property | x64 candidate | ARM64 candidate |
| --- | --- | --- |
| Package file | `dist/Folimeld_1.0.2.0_x64.msix` | `dist/Folimeld_1.0.2.0_arm64.msix` |
| Package Identity | `TakumaYamada.Folimeld` | `TakumaYamada.Folimeld` |
| Package Publisher | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` |
| Package Family Name | `TakumaYamada.Folimeld_hn3600vb3j7rp` | `TakumaYamada.Folimeld_hn3600vb3j7rp` |
| Version | `1.0.2.0` | `1.0.2.0` |
| Target CPU (PE Machine) | `x64` (`0x8664`) | `arm64` (`0xAA64`) |
| Package SHA-256 | `86E1617340093A4F0BC2DDFBCCC15FA5A0B97E3DE5ED229A93415B54F391C421` | `6BC0890A56E9AD028F91770167EBE7C3DDE2BD187CD0628BB9914D03B6A516CE` |
| Preflight (`msix_preflight`) | Passed (`build/msix-preflight/store/x64/preflight.json`) | Passed (`build/msix-preflight/store/arm64/preflight.json`) |
| Source association | `dist/source/Folimeld_1.0.2.0_x64.msix-86e1617340093a4f0bc2ddfbccc15fa5a0b97e3de5ed229a93415b54f391c421.json` | `dist/source/Folimeld_1.0.2.0_arm64.msix-6bc0890a56e9ad028f91770167ebe7c3dde2bd187cd0628bb9914d03b6a516ce.json` |

### Submission 2 acceptance checklist

| Check | Scope | Required behavior and evidence | Status |
| --- | --- | --- | --- |
| Upgrade test from 1.0.1.0 | x64 | Install 1.0.2.0 over signed 1.0.1.0; verify settings, history, and PDF file associations are preserved | Pending |
| ARM64 hardware install & launch | ARM64 | Native launch, exit, and UI interaction on Copilot+ PC (Snapdragon X Elite, etc.) Windows 11 ARM64 | Pending |
| Large PDF save acceleration | Both | Separate worker process saving, progress dialog display, and original file preservation on failure | Unit tests passed, awaiting hardware |
| Encrypted Undo/Redo disk spooling | Both | Spool to AES-256-GCM encrypted temporary storage when memory exceeds 128 MiB; restore and secure wipe | Unit tests passed, awaiting hardware |
| Bulk image import | Both | PDF generation from image import dialog, reordering, rotation, and temp file cleanup | Unit tests passed, awaiting hardware |
| Free-app-only policy | Both | Supporter add-on menus are omitted; all functionality is available free of charge | Verified |

## Store candidate 1.0.3.0 preparation and acceptance plan (Submission 3: x64 & ARM64)

Acceptance plan for Submission 3 (package version `1.0.3.0`), incorporating Folimeld 0.3.7 features (on-demand sample PDF downloads, close action, etc.).

### Candidate packages and preflight status

| Property | x64 candidate | ARM64 candidate |
| --- | --- | --- |
| Package file | `dist/Folimeld_1.0.3.0_x64.msix` | `dist/Folimeld_1.0.3.0_arm64.msix` |
| Package Identity | `TakumaYamada.Folimeld` | `TakumaYamada.Folimeld` |
| Package Publisher | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` |
| Package Family Name | `TakumaYamada.Folimeld_hn3600vb3j7rp` | `TakumaYamada.Folimeld_hn3600vb3j7rp` |
| Version | `1.0.3.0` | `1.0.3.0` |
| Target CPU (PE Machine) | `x64` (`0x8664`) | `arm64` (`0xAA64`) |
| Package SHA-256 | Pending (build on x86 PC environment) | `2ECD780F5F075EEC9CE657C70A66A3A476A91B98986070F0BFB0936A65D60AD7` |
| Preflight (`msix_preflight`) | Pending | Passed (`build/msix-preflight/store/arm64/preflight.json`) |
| Source association | Generated upon package creation | `dist/source/Folimeld_1.0.3.0_arm64.msix-2ecd780f5f075eec9ce657c70a66a3a476a91b98986070f0bfb0936a65d60ad7.json` |

### Submission 3 acceptance checklist

| Check | Scope | Required behavior and evidence | Status |
| --- | --- | --- | --- |
| Upgrade test from 1.0.2.0 | Both | Install 1.0.3.0 over signed 1.0.2.0; verify settings, history, and PDF file associations are preserved | Pending |
| ARM64 hardware install & launch | ARM64 | Native launch, exit, and UI interaction on Copilot+ PC (Snapdragon X Elite, etc.) Windows 11 ARM64 | Pending |
| Sample PDF download | Both | Verify sample manga PDF fetch, display, and editing via "File -> Open sample PDF..." over HTTPS | Unit tests passed, awaiting hardware |
| Close PDF action | Both | Verify "File -> Close" safely closes active document and returns to modeless empty state | Unit tests passed, awaiting hardware |
| Free-app-only policy | Both | Supporter add-on menus are omitted; all functionality is available free of charge | Verified |
