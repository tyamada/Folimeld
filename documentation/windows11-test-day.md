# First tests after the Dynabook arrives

[日本語](windows11-test-day_ja.md) | [English](windows11-test-day.md)

Planned for 2026-10-30 (Japan time). Verify the ordered Dynabook's actual model, CPU, RAM and Windows edition after delivery. Delivery/test outcomes are not yet confirmed. Start with direct installation and normal operation; do not set up VMs or perform forced-shutdown tests during this first run.

## 1. Arrival and baseline

- Check seller warranty, accessories and recovery/reinstallation instructions. Do not reset before checking faults and return conditions.
- Record model, CPU, RAM, SSD capacity, resolution, Windows edition/build/x64 and activation state. Do not record/share personal accounts or product keys.
- Ask the seller about BIOS management locks or previous organizational enrollment. Do not bypass them.
- If clean installation is needed, first confirm recovery/licensing. Refurbished does not itself establish a clean environment.
- Apply Windows Update and necessary manufacturer updates, finish required restarts and record the resulting OS build.
- Prepare a test user; do not add Python, Visual Studio or old Folimeld versions. Preserve a pre-installation image if possible and record known pre-existing runtimes/baseline conditions.

## 2. Prepare and install the bundle

Copy/extract the test ZIP into a local writable folder. Compare SHA-256 with the JSON beside the ZIP, for example:

```powershell
Get-FileHash .\Folimeld-Windows11-x64-test.zip -Algorithm SHA256
```

Check certificate expiry in `bundle.json`; the current bundle is valid for seven days. Stop to investigate expiry, hash mismatches or an existing `Folimeld.Dev` registration.

Follow the extracted instructions, using elevated Windows PowerShell as the same test user. Install changes certificate trust and app registration on the test PC.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Install
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Launch
```

## 3. Normal-operation checklist

Copy the [result template](windows11-test-result-template.json) into the test folder and fill in observed values/results. Use `not_run`, `pass`, `fail` or `partially_verified`, explicitly describing unverified parts. Preserve the original template.

Record pending/pass/fail, actual results and evidence filenames for each row. Preserve originals and work on copies/new destinations. Every row initially remains pending.

| ID | Action | Expected result |
| --- | --- | --- |
| T01 | Install and launch via registered identity | Launches without missing dependencies; version can be checked |
| T02 | Open sample PDF in a Japanese/spaced path | Three pages; metadata, TOC, annotation, form and attachment match the fixture |
| T03 | Multiple selection, rotate/move, Undo/Redo | Expected pages/order change and can be restored |
| T04 | Save a copy, close and reopen | Edits persist; compare links, annotations, forms, attachments and metadata with the original |
| T05 | Open password.pdf and change password on another copy | Opens with test password `folimeld-test-only`; saved copy follows the new password choice |
| T06 | Import fixture images, sort/exclude, choose A4, cancel | JPEG/PNG and TIFF frames behave as expected; cancelling retains the existing document |
| T07 | Switch Japanese/English, restart, open licenses | Language persists; OpenSSL, Rust and CFFI/libffi notices are readable |
| T08 | Choose Folimeld through Explorer Open with | Opens the right document without unwanted default-app changes |
| T09 | Run Inspect | installation-report.json identifies the expected version/registration |
| T10 | Remove test app and newly added trust | Test installation removed; pre-existing trust/fixtures retained; record actual settings/log residues |

If capturing listing images, do so after T09 and before uninstalling in T10.

Leave PDF elements that cannot be inspected in the UI unverified, and supplement with independent PDF inspection on the build PC or another tool. Successful launch alone does not establish complex-PDF save compatibility.

## 4. Evidence and cleanup

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Inspect
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Remove
```

Preserve bundle.json, artifact-source.json, test-state.json, installation-report.json, output PDFs and manual results under one run ID. Retain state and clean up even after failed installation. See [installation/cleanup details](windows-store-test-bundle.md).

After normal operation passes, follow the [capture plan](windows-store-screenshot-plan.md). Update, WACK, actual Store purchases, forced OS shutdown and final Store-package tests remain in the [acceptance checklist](windows-store-acceptance.md). Do not enter outcomes that have not been observed on the test PC.
