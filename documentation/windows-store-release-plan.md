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

## Submission 2 release plan (Folimeld 1.0.2.0: x64 + ARM64 dual architecture)

Plan for the next update (Submission 2) adding native Windows 11 ARM64 support (Copilot+ PCs such as Surface Pro 11 / Snapdragon X Elite) alongside Windows 11 x64.

- **Package version**: `1.0.2.0` (greater than previous published version `1.0.1.0`).
- **Target architectures**: `x64` and `arm64` (native PE Machine `0xAA64`).
- **Pricing & distribution**: 100% Free (remains a free app with in-app supporter add-ons kept disabled).
- **Included features**:
  - Native Windows 11 ARM64 support.
  - Large PDF saving acceleration (progress dialog, redundant stream check bypass, worker process writing, crash protection).
  - Undo/Redo history disk spooling (AES-256-GCM encrypted temp storage up to 1 GiB).
  - Virtualized thumbnail rendering (smooth scrolling for documents with 1,000+ pages).
  - Batch PDF creation from image folders (PNG, JPEG, TIFF, BMP, WebP).
- **Submission status**: Submitted both packages (x64 and ARM64) to Partner Center (Submission 2) on 2026-11-16; passed certification and published (updated 2026-11-21). Corresponding source published on GitHub Releases under tag [`windows-store-v1.0.2.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.2.0).
- **Package assets (built, preflight verified, and submitted)**:
  - `dist/Folimeld_1.0.2.0_x64.msix` (~76.4 MB, SHA-256: `86E1617340093A4F0BC2DDFBCCC15FA5A0B97E3DE5ED229A93415B54F391C421`, PE Machine `0x8664`, preflight passed)
  - `dist/Folimeld_1.0.2.0_arm64.msix` (~62.9 MB, SHA-256: `6BC0890A56E9AD028F91770167EBE7C3DDE2BD187CD0628BB9914D03B6A516CE`, PE Machine `0xAA64`, preflight passed)
  - Uploaded simultaneously in Partner Center Submission 2 Packages step for automatic architecture-specific distribution.
- **Build and preflight commands**:
  ```powershell
  # x64 package generation and preflight verification against previous version
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture x64 `
    -PreviousPackage .\dist\Folimeld_1.0.1.0_x64.msix

  # ARM64 package generation and preflight verification
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture arm64
  ```

## Submission 3 release plan (Folimeld 1.0.4.0: app 0.3.7 / x64 + ARM64)

Plan for the next update (Submission 3) bringing Folimeld 0.3.7 features (“Open sample PDF…”, PDF close action, and modeless empty-document prompt) to Microsoft Store. Because `1.0.3.0` (x64) was already used in an existing package flight (`Folimeld 1.0.3.0 x64 Thumbnail Fix`), the MSIX package version is incremented to `1.0.4.0` to satisfy Partner Center's unique package full name requirement.

- **Versions**: MSIX package version `1.0.4.0` (greater than `1.0.2.0` and prior flight `1.0.3.0`), application version `0.3.7`.
- **Target architectures**: `x64` (`0x8664`) and `arm64` (`0xAA64`).
- **Pricing & distribution**: 100% Free (in-app supporter add-ons and GitHub Sponsors menu remain disabled/hidden).
- **New 0.3.7 features**:
  - On-demand sample manga PDF downloads via “File -> Open sample PDF…” and the empty-document prompt (language filter, newest-first / episode-one-first order, CC BY 4.0 attribution, SHA-256 verification, offline reuse of verified originals, editable working copies).
  - “File -> Close” PDF close action and modeless empty-document guidance.
- **Privacy & certification alignment**:
  - User PDFs and images remain strictly local and are never uploaded.
  - Clarify in the privacy policy, Store listing, and submission notes that HTTPS requests occur only when the user explicitly opens “Open sample PDF…” to fetch the fixed public catalogue and selected sample PDF from GitHub Releases.
- **Screenshot fixture**:
  - Captured Japanese and English screenshots for documentation, the website, and Store listings using copies of `testdata/tameshibu_episode1_2_en.pdf` (CC BY 4.0, Komairo Hiyori) (`build/store-listing/screenshots/ja-JP/` and `en-US/` 01–06, plus `documentation/screenshots/`; see the [screenshot capture plan](windows-store-screenshot-plan.md)).
- **Build & preparation status (as of 2026-11-22)**:
  - Finalized release branch `release/windows-store-v1.0.4.0` (commit `8f6b47c`, app version `0.3.7`) and updated `docs/privacy/index.html` to document on-demand HTTPS sample PDF downloads.
  - Built and preflight-verified `dist/Folimeld_1.0.4.0_x64.msix` (78,990,624 bytes / ~75.3 MiB, SHA-256: `CD081C96BC0838BFE1B65E59814F29DFF31957D34119F3AF1BE51357A670B6A9`, PE Machine `0x8664`, static checks passed in `build/msix-preflight/store/x64/preflight.json`). Corresponding source ZIP: `dist/source/Folimeld-source-2fee6f48a3bc5c09ec6e80c142d593c6b2781abc0ad9794912749a80a847450e.zip`; association JSON: `dist/source/Folimeld_1.0.4.0_x64.msix-cd081c96bc0838bfe1b65e59814f29dff31957d34119f3af1be51357a670b6a9.json`.
  - Built and preflight-verified `dist/Folimeld_1.0.4.0_arm64.msix` (62,377,071 bytes / ~59.5 MiB, SHA-256: `9597D6F142A4520680BB1C943EC5ABA951549448CB8ADC30728A69379DAF7364`, PE Machine `0xAA64`, static checks passed in `build/msix-preflight/store/arm64/preflight.json`) on ARM64 hardware. Association JSON: `dist/source/Folimeld_1.0.4.0_arm64.msix-9597d6f142a4520680bb1c943ec5aba951549448cb8adc30728a69379daf7364.json`.
  - **Submission & publication status**: Submitted both `1.0.4.0` packages (x64 and ARM64), updated bilingual listings and 12 screenshots, and certification notes to Partner Center (Submission 3 / ID `1152921505702470707`) on 2026-11-22 with automatic publishing enabled. Passed certification and confirmed live (`1.0.4.0` x64 & ARM64) on Microsoft Store (verified 2026-11-24).
- **Build and preflight commands**:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture x64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_x64.msix

  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture arm64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_arm64.msix
  ```
- **Corresponding source publication**: Published matching source ZIP, `SHA256SUMS.txt`, and `source-association.json` on GitHub Releases under tag [`windows-store-v1.0.4.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.4.0).

## Submission 4 publication record (Folimeld 1.0.5.0: app 0.3.8 / Store update check + 3-tier Supporter Badge UI)

- **Versions**: MSIX package version `1.0.5.0`, application version `0.3.8` (branch `release/windows-store-v1.0.5.0`, commit `9ef9c1e44edac9d47a84b6386ee703304684fa29`).
- **Target architectures**: `x64` (`0x8664`) and `arm64` (`0xAA64`).
- **New Store-only features**:
  - Startup update check via Windows' built-in `StoreContext.get_app_and_optional_store_package_updates_async()`, displaying a status bar "Update" button that opens `ms-windows-store://pdp/?ProductId=9P5X2JFZRJC3` when a newer Store package is available.
  - 3-tier Supporter Badge UI (Bronze / Silver / Gold, bundling `assets/tip-icon/`).
- **Submission & publication status**: Submitted both x64 and ARM64 packages to Partner Center (Submission 4 / ID `1152921505702500801`) on 2026-11-25; passed certification and confirmed live on Microsoft Store the same day.
  - `Folimeld_1.0.5.0_x64.msix` (83,404,506 bytes, SHA-256: `B430CBBA5C144E8F1FBC99302BA0B8AE4C8F580E923942D1689EFEE0CCBF6FDF`)
  - `Folimeld_1.0.5.0_arm64.msix` (66,785,943 bytes, SHA-256: `C5E9C8F2394EC1600EE4B69A5762FC6582A62575E120D1D8CC4511C41297F0EE`)
- **Corresponding source publication**: Published matching source ZIP, `SHA256SUMS.txt`, and `source-association.json` on GitHub Releases under tag [`windows-store-v1.0.5.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.5.0).

## Submission 5 publication record (Folimeld 1.0.6.0: app 0.3.9 / East Asia expansion: Korea, Taiwan, Hong Kong, Macao)

- **Versions**: MSIX package version `1.0.6.0`, application version `0.3.9` (branch `release/windows-store-v1.0.6.0`, commit `c4a748c9ebbb08b0431626f2da17b065e14ccf19`).
- **Target architectures**: `x64` (`0x8664`) and `arm64` (`0xAA64`).
- **Markets (6 markets)**: Expanded distribution to South Korea, Taiwan, Hong Kong SAR, and Macao SAR alongside Japan and the United States.
- **Localization & Store listing updates**:
  - Added Traditional Chinese (`zh_TW` with automatic routing for `zh-TW` / `zh-HK` / `zh-MO` / `zh-Hant`) and completed Korean (`ko`) and Simplified Chinese (`zh`) translations.
  - Added Korean (`ko-KR`) and Traditional Chinese (`zh-Hant`) Store listings and screenshots (6 each).
- **Submission & publication status**: Submitted both x64 and ARM64 packages to Partner Center (Submission 5 / ID `1152921505702503922`) on 2026-11-25; passed certification and confirmed live across JP, KR, TW, HK, and MO on 2026-11-26.
  - `Folimeld_1.0.6.0_x64.msix` (83,410,681 bytes, SHA-256: `C872EAAADE28CF3329795DFD4902E47096A9CAE3EA3919373AA510227587AA1D`)
  - `Folimeld_1.0.6.0_arm64.msix` (66,791,132 bytes, SHA-256: `B60AAEB3D39DBB526A3DDAA337B4D66BA8F9CBE955794E9C8FC370602AED65BE`)
- **Corresponding source publication**: Published matching source ZIP, `SHA256SUMS.txt`, and `source-association.json` on GitHub Releases under tag [`windows-store-v1.0.6.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.6.0).

## Official references

- [Distribution path comparison](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path)
- [MSIX package requirements and versioning](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Store policies](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIX name reservations](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)

## Diagnostic follow-up (updated 2026-11-04)

The earlier local WACK checks on development builds 0.3.3.4 and 0.3.3.5 reported optional TEST88 FAIL and required TEST92 WARNING. The historical diagnostics identified an access-context hypothesis for the DPI warning. They did not directly trace the original WACK process or establish the cause. The TEST88 analysis identified API references and string matches. Those findings do not establish that a flagged external executable was launched during normal use.
