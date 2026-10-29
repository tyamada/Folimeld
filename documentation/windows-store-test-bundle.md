# Separate Windows 11 test PC/VM

[日本語](windows-store-test-bundle_ja.md) | [English](windows-store-test-bundle.md)

Use the development package on the separate Windows 11 x64 test PC/VM selected for acceptance testing. Installation and WACK remain pending until executed there. The build computer's signing preparation does not establish installed-app behavior.

## Prepare on the build computer

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/prepare_msix_test.ps1 `
  -Package dist/Folimeld_0.3.3.0_x64.msix `
  -OutputDirectory build/store-test-bundles/new-run
```

Requires Windows SDK SignTool and the package's existing source association under `dist/source/`. Uses a seven-day, self-signed development certificate, deletes the temporary PFX in cleanup, and does not add certificate-store entries or install the app on the build computer. Existing output directories and other package identities are rejected. The signed executable payload is checked against the original source association. CMS signature verification checks the signature without adding trust; the build machine's Authenticode trust status may therefore be unsuccessful. This certificate/package is for local testing, not Store submission.

Transfer the complete generated directory: signed MSIX, public certificate, `bundle.json`, `artifact-source.json`, corresponding source ZIP and `test_msix_on_vm.ps1`. Keep the input package/source records; signing changes the package hash. Extra fixtures/instructions supplied with a test run should travel with the directory. Do not transfer private keys. If the certificate has expired, create a fresh bundle.

## Run on the test PC/VM

Copy the directory to a local, writable folder. Use elevated Windows PowerShell as the same test user for installation and cleanup. No Python or Windows SDK is needed for these scripts on the test PC. Start from a clean VM snapshot if available; the installer refuses to replace an existing `Folimeld.Dev` registration.

```powershell
# Verify hashes, trust the public certificate in LocalMachine/TrustedPeople,
# install for this user, and record the result
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Install
# Launch from the registered application identity
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Launch
# Refresh the installation report
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Inspect
```

Follow the [acceptance checklist](windows-store-acceptance.md) and record actual results/screenshots. Installation alone does not mark GUI, update, deletion or WACK tests as passed. SDK/WACK installation is separate if certification tests are to be run. Preserve `bundle.json`, `artifact-source.json`, `test-state.json`, `installation-report.json` and manual results; remove private document paths or contents before sharing evidence.

```powershell
# Elevated, same user and machine: remove only this installation and any
# certificate trust added by this run; keep reports
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Remove
```

Cleanup also supports an installation attempt that stopped after adding trust. If installation failed, retain the error and state file and run cleanup before retrying with a new copy. Do not change the bundle or delete its state file between installation and cleanup. Pre-existing certificate trust is retained; a different installed version is not removed automatically. The script does not explicitly delete user PDFs or manually purge settings/logs. Record actual uninstall residues separately.

Reference: [Microsoft package-signing certificate creation and test-machine trust](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing).
