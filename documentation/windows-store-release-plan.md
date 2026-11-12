# Microsoft Store release plan

[日本語](windows-store-release-plan_ja.md) | [English](windows-store-release-plan.md)

## Folimeld 1.0.1.0 publication

The initial Windows 11 x64 MSIX release, Submission 1, passed Microsoft Store certification and was published on 2026-11-09 (Japan time). The free listing is live in [Japan](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=ja-JP&gl=JP) and the [United States](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=en-US&gl=US) under Store product ID `9P5X2JFZRJC3`. The first release ships with support purchases disabled.

The Store-delivered package passed the recorded installation and normal-use checks. Its main window was confirmed to use Per-Monitor V2. See the [Windows 11 MSIX acceptance record](windows-store-acceptance.md) for the checks performed and their scope.

The cause of the earlier local WACK DPI warning remains unconfirmed. The Store submission passed overall with `runFullTrust` declared. The individual Store certification outcomes for TEST92 (DPI awareness), TEST88 (blocked executables) and `runFullTrust` remain unconfirmed.

## Registration and update checklist

Use the published MSIX product registration for updates. Verify these values in Partner Center before configuring a build.

| Partner Center field | Store configuration key |
| --- | --- |
| `Package/Identity/Name` | `identity_name` |
| `Package/Identity/Publisher` | `publisher` |
| `Package/Properties/PublisherDisplayName` | `publisher_display_name` |

1. Verify the package version, signing and source association for the candidate.
2. Review the [listing](windows-store-listing.md), [screenshots](windows-store-screenshot-plan.md) and the [published privacy policy](https://tyamada.github.io/Folimeld/privacy/).
3. Record the certification result and confirm publication in the intended markets. Verify the Store-delivered version and affected workflows separately from development builds.

## Preparing a Store build

Copy `packaging/msix/store-config.example.json` to `build/store-config.json` and enter verified MSIX registration values in the first three fields. The blanks are intentional: the unchanged example fails Store validation. Do not put credentials or private keys in this file.

`package_version` is the four-component MSIX version, managed separately from the application's display version, `__version__` in `folimeld/__init__.py`. Store mode requires a first component of at least 1, a final component of 0, and components no greater than 65535. An update must be greater than the previous MSIX version with the same Identity/Publisher. Do not pass a previous EXE/MSI product or development MSIX as `-PreviousPackage`.

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
- [MSIX package requirements and versioning](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Store policies](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIX name reservations](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)

## Diagnostic follow-up (updated 2026-11-04)

The earlier local WACK checks on development builds 0.3.3.4 and 0.3.3.5 reported optional TEST88 FAIL and required TEST92 WARNING. The historical diagnostics identified an access-context hypothesis for the DPI warning. They did not directly trace the original WACK process or establish the cause. The TEST88 analysis identified API references and string matches. Those findings do not establish that a flagged external executable was launched during normal use.
