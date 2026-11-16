# Windows 11 x86_64 and ARM64 `uv tool install` Edition (Pure Python Wheel) Specification and Guide

[日本語](windows-uv-tool_ja.md)

This document describes the specification and installation procedure for the Pure Python Wheel (`folimeld-<version>-py3-none-any.whl`) distributed via GitHub Releases for Windows 11 x86_64 and Windows 11 ARM64 (such as Copilot+ PCs / Surface Pro 11) and installed with `uv tool install`. The Microsoft Store edition remains the standard Windows distribution, and this edition keeps its settings, logs, and entry points strictly isolated from the Store, Desktop, and source+uv editions.

## 1. Distinction Across Windows Editions

| Aspect | 1. Microsoft Store Edition | 2. Desktop Edition (PyInstaller + Inno Setup) | 3. Source + uv Edition (`install_uv.ps1`) | 4. `uv tool install` Edition (Pure Python Wheel) |
| --- | --- | --- | --- | --- |
| **Entry Point** | `main.py` → `run()` | `launch_desktop.py` → `run(distribution="desktop")` | `launch_uv.py` → `run(source_uv=True)` | `folimeld` / `folimeld-console` → `folimeld.uv_tool_launcher:main` → `run(distribution="uv-tool")` |
| **Settings Path** | MSIX virtualized registry (`QSettings()`) | `%LOCALAPPDATA%\Folimeld-Desktop\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` |
| **Logs Path** | `AppLocalDataLocation/logs/folimeld.log` (`strict=False`) | `%LOCALAPPDATA%\Folimeld-Desktop\logs\<ver>\<session>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV\logs\<ver>\<session>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV-Tool\logs\<ver>\<session>\folimeld.log` (`strict=True`) |
| **Mutex** | None | `Local\Folimeld-Desktop` | None | `Local\Folimeld-UV-Tool` |
| **Environment Check** | `is_packaged() == True` | `win32` / `x64` or `ARM64` / `frozen` / not MSIX | `win32` / `x64` or `ARM64` / CPython 3.12 (patch match) / unfrozen / not MSIX / dedicated `.venv` / lock SHA-256 & 14 exact deps | `win32` / `x64` or `ARM64` / **CPython 3.12.x (minor match)** / unfrozen / not MSIX / virtual environment (`sys.prefix != sys.base_prefix`) / **14 exact deps** |
| **Sponsors / Store Support** | `StoreSupport` enabled, Sponsors hidden | `StoreSupport` disabled, Sponsors enabled | `StoreSupport` disabled, Sponsors enabled | `StoreSupport` disabled, Sponsors enabled |
| **Open With Registration** | MSIX manifest | Skipped | Skipped | Skipped |
| **Resource Resolution** | `sys._MEIPASS` | `sys._MEIPASS` (`_internal/`) | Repository root | Packaged `folimeld/_resources/` |

## 2. Building and Staging Release Artifacts

`tools/uv_tool_build.py` verifies consistency across `pyproject.toml`, `folimeld/__init__.py`, runtime profile (`windows-uv-runtime.json` or `windows-arm64-uv-runtime.json`), and lock file (`requirements-windows-uv.lock` or `requirements-windows-arm64-uv.lock`), then builds a deterministic Pure Python Wheel and stages companion files into a new output directory.

```powershell
# x64 staging
python -m tools.uv_tool_build --output .\dist\uv-tool-release --arch x64

# ARM64 staging
python -m tools.uv_tool_build --output .\dist\uv-tool-arm64-release --arch arm64
```

Staged and published artifacts ([GitHub Release `windows-uv-tool-v0.3.5-preview.1`](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.5-preview.1) / commit `7aee32a74fe51cf20657f8ff9fd2726790db43a9`):
- `folimeld-0.3.5-py3-none-any.whl` (2,176,864 bytes, SHA-256: `759b2fe0052f1741427194e40104db0af65184041ad5bad8bb5d2003874dbdaf`, Pure Python Wheel bundling locales, icons, and license notices under `folimeld/_resources/`)
- `Folimeld-0.3.5-windows-x64-uv-tool-source.zip` (26,715,550 bytes, SHA-256: `7cf388af261a8f9a47a49d1453d87f98d39430bc9cbdf4f2692dd0a0b4756ad7`)
- `source-manifest.json` (138,318 bytes, SHA-256: `9752f792e2f5bf4bcad90b00d1347dddab8d8ce627c7b3b98d1778838a8ad3d3`)
- `SOURCE-ASSOCIATION.txt` (506 bytes, SHA-256: `530bd105a65d8725e8847f1c5a2e54274f57b377fbaa470718684e90c5cd8d17`)
- `requirements-windows-uv.lock` (2,316 bytes, SHA-256: `7e994b4c231536fb5c53d79959761bc426bd9ff9585b578165f1fd67ec19077f`, Windows x64 / CPython 3.12 wheel SHA-256 lockfile)
- `windows-uv-runtime.json` (1,239 bytes, SHA-256: `49ca2dea68fcc253574d867b9d5ff29524aa50e3b214d7c4687cd441dbdaa1dd`, pinned runtime dependency definitions)
- `THIRD-PARTY-NOTICES.txt` (622,989 bytes, SHA-256: `21929c232ddf95e158a808561a5cdf21b9cbb9798b2d55f6c577975d5393fd3c`)
- `DEPENDENCY-SOURCES.json` (24,583 bytes, SHA-256: `5ef42613490d2f807cbd0cca13b51e96e1f73716d880db2a5fc8dce844291609`)
- `SHA256SUMS.txt` (759 bytes, SHA-256: `099dad4c384a4c520fc2047ac52213c5147906e772496adee4c3efc215cada7f`)
- `uv-tool-release-manifest.json` (1,381 bytes, SHA-256: `883cd08d59fff23949608cbf133542a880266f7c0adb799947b4d4ec45786ad1`)

## 3. Installation and Launch Procedure

### 1. Prerequisites

Requires Windows 11 x64 (x86_64) and uv. Run `uv --version` in a non-administrator PowerShell session. If uv is not installed, install it below and reopen PowerShell. This preview was tested with uv 0.13.8; ARM64 is not supported.

```powershell
winget install --id=Astral.uv -e
uv --version
```

**You do not need to install Python 3.12 manually beforehand.** With uv's default settings, `--python 3.12` downloads CPython 3.12.x if no suitable Python is available. Disabled automatic downloads or network restrictions require separate preparation. This option does not pin the Python patch version.

### 2. Files to download from GitHub

Save these **two files in the same folder**, such as Downloads:

1. [**folimeld-0.3.5-py3-none-any.whl**](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-v0.3.5-preview.1/folimeld-0.3.5-py3-none-any.whl) — the application Wheel.
2. [**requirements-windows-uv.lock**](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-v0.3.5-preview.1/requirements-windows-uv.lock) — pinned versions and distribution-wheel SHA-256 hashes for 14 dependencies.

### 3. Working directory and installed locations

Run commands **in the folder containing both downloads**, normally `C:\Users\<username>\Downloads`. Adjust the location below if Downloads has been relocated or you saved the files elsewhere.

Unlike the source + uv edition's `install_uv.ps1`, this does not create a `.venv` in the current folder.

- **Tool environment**: the `folimeld` subfolder of `uv tool dir`; a default example is `%APPDATA%\uv\data\tools\folimeld\`.
- **Launch commands**: `folimeld.exe` (GUI) and `folimeld-console.exe` (diagnostics) in `uv tool dir --bin`; a default example is `%USERPROFILE%\.local\bin\`.
- **Settings and logs**: `%LOCALAPPDATA%\Folimeld-UV-Tool\`, isolated from the Store, Desktop, and source + uv editions.

Environment variables can override these locations. Check the actual directories:

```powershell
uv tool dir
uv tool dir --bin
```

**After successful installation, moving or deleting the downloaded Wheel and lock does not prevent the installed app from running.** Keep both files and their hashes for reinstallation. Do not delete the uv-managed environment or the Python it uses.

### 4. SHA-256 verification and installation

```powershell
$ErrorActionPreference = 'Stop'

# Adjust this if you saved the files elsewhere
Set-Location -LiteralPath (Join-Path $HOME 'Downloads')

# Stop if either SHA-256 does not match
if ((Get-FileHash -LiteralPath .\folimeld-0.3.5-py3-none-any.whl -Algorithm SHA256).Hash -ne '759B2FE0052F1741427194E40104DB0AF65184041AD5BAD8BB5D2003874DBDAF') {
    throw 'Wheel SHA-256 mismatch.'
}
if ((Get-FileHash -LiteralPath .\requirements-windows-uv.lock -Algorithm SHA256).Hash -ne '7E994B4C231536FB5C53D79959761BC426BD9FF9585B578165F1FD67EC19077F') {
    throw 'Lock SHA-256 mismatch.'
}

uv tool install --python 3.12 --with-requirements .\requirements-windows-uv.lock --no-build .\folimeld-0.3.5-py3-none-any.whl
if ($LASTEXITCODE -ne 0) { throw 'uv tool install failed.' }
```

### 5. Launch

Once the executable directory is on PATH, launch from **any folder**:

```powershell
# Standard GUI launch without a console
folimeld

# Diagnostic launch with console output
folimeld-console
```

> [!TIP]
> If you see `warning: ... is not on your PATH`, run `uv tool update-shell` once and reopen PowerShell. This updates your user shell/PATH settings; no machine-wide execution-policy change is needed.

Uninstall with `uv tool uninstall folimeld` (settings and logs are preserved).

Storage and Python download details: [uv storage](https://docs.astral.sh/uv/reference/storage/) / [Installing Python](https://docs.astral.sh/uv/guides/install-python/).

## 4. Isolated Installation, Real GUI, and 3-Worker Verification Record (2026-11-16)

- Executed the `uv tool install` command above using CPython 3.12.16 (`python-build-standalone` 20261110) and `uv 0.13.8` into isolated `UV_TOOL_DIR`, `UV_TOOL_BIN_DIR`, and `LOCALAPPDATA` directories.
- Verified installation of `folimeld==0.3.5` plus all 14 pinned runtime dependencies (15 packages total) and generation of both `folimeld.exe` (GUI) and `folimeld-console.exe` (console) entry points.
- Verified resolution of `resource_root()` to `site-packages/folimeld/_resources`, loading of locales, icons, and all 4 license tabs (`Folimeld`, `Windows uv notices`, `Windows uv installed packages`, `Windows uv sources`).
- Verified real GUI operations: opening a synthetic 3-page PDF, rotating, moving pages, saving via Worker 1 (PDF save worker), importing and converting 2 PNG images via Worker 2 (image conversion worker), saving the converted PDF via Worker 3 (image PDF save worker), and reopening both saved PDFs with matching page counts and rotation.
- Verified `GetWindowDpiAwarenessContext` on the main window matches `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2` (-4) (`GetDpiForWindow` = 144), Sponsors action enabled, and `StoreSupport` disabled.
- Verified settings persistence (`thumbnail_size=144`, `button_display=icon_text`) in `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` across restarts and per-session log directory creation.
- Verified duplicate-launch rejection when `Local\Folimeld-UV-Tool` is held: launching `folimeld-console.exe` displays the `Folimeld uv tool` error dialog, writes the error to `stderr`, and exits with code `1`.
- Verified existing `Folimeld-UV` and `Folimeld-Desktop` settings files and `HKCU\Software\Classes\Applications\Folimeld.exe` registry entries remained unchanged before and after testing.
- Verified unauthenticated HTTPS redownload of all 10 assets from the published GitHub Release (`windows-uv-tool-v0.3.5-preview.1`) with matching byte sizes and SHA-256 checksums, plus `uv tool install` from the redownloaded `.whl` and `requirements-windows-uv.lock` and `uv tool uninstall folimeld` removing the tool executables while preserving `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini`.
