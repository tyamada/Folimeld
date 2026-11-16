# Windows 11 x86_64 `uv tool install` Edition (Pure Python Wheel) Specification and Guide

[日本語](windows-uv-tool_ja.md)

This document describes the specification and installation procedure for the Pure Python Wheel (`folimeld-<version>-py3-none-any.whl`) distributed via GitHub Releases for Windows 11 x86_64 and installed with `uv tool install`. The Microsoft Store edition remains the standard Windows distribution, and this edition keeps its settings, logs, and entry points strictly isolated from the Store, Desktop, and source+uv editions.

## 1. Distinction Across Windows Editions

| Aspect | 1. Microsoft Store Edition | 2. Desktop Edition (PyInstaller + Inno Setup) | 3. Source + uv Edition (`install_uv.ps1`) | 4. `uv tool install` Edition (Pure Python Wheel) |
| --- | --- | --- | --- | --- |
| **Entry Point** | `main.py` → `run()` | `launch_desktop.py` → `run(distribution="desktop")` | `launch_uv.py` → `run(source_uv=True)` | `folimeld` / `folimeld-console` → `folimeld.uv_tool_launcher:main` → `run(distribution="uv-tool")` |
| **Settings Path** | MSIX virtualized registry (`QSettings()`) | `%LOCALAPPDATA%\Folimeld-Desktop\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` |
| **Logs Path** | `AppLocalDataLocation/logs/folimeld.log` (`strict=False`) | `%LOCALAPPDATA%\Folimeld-Desktop\logs\<ver>\<session>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV\logs\<ver>\<session>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV-Tool\logs\<ver>\<session>\folimeld.log` (`strict=True`) |
| **Mutex** | None | `Local\Folimeld-Desktop` | None | `Local\Folimeld-UV-Tool` |
| **Environment Check** | `is_packaged() == True` | `win32` / `x64` / `frozen` / not MSIX | `win32` / `x64` / CPython 3.12.16 (exact patch) / unfrozen / not MSIX / dedicated `.venv` / lock SHA-256 & 14 exact deps | `win32` / `x64` / **CPython 3.12.x (minor match)** / unfrozen / not MSIX / virtual environment (`sys.prefix != sys.base_prefix`) / **14 exact deps** |
| **Sponsors / Store Support** | `StoreSupport` enabled, Sponsors hidden | `StoreSupport` disabled, Sponsors enabled | `StoreSupport` disabled, Sponsors enabled | `StoreSupport` disabled, Sponsors enabled |
| **Open With Registration** | MSIX manifest | Skipped | Skipped | Skipped |
| **Resource Resolution** | `sys._MEIPASS` | `sys._MEIPASS` (`_internal/`) | Repository root | Packaged `folimeld/_resources/` |

## 2. Building and Staging Release Artifacts

`tools/uv_tool_build.py` verifies consistency across `pyproject.toml`, `folimeld/__init__.py`, `windows-uv-runtime.json`, and `requirements-windows-uv.lock`, then builds a deterministic Pure Python Wheel and stages companion files into a new output directory.

```powershell
python -m tools.uv_tool_build --output .\dist\uv-tool-release
```

Staged artifacts (`dist/windows-uv-tool-0.3.5`):
- `folimeld-0.3.5-py3-none-any.whl` (2,176,881 bytes, SHA-256: `86aa152ca386f857861b4598258ff95ad14f0bd4485d9024f9c6ef28fb517cdc`, Pure Python Wheel bundling locales, icons, and license notices under `folimeld/_resources/`)
- `Folimeld-0.3.5-windows-x64-uv-tool-source.zip` / `source-manifest.json` (corresponding source archive and internal manifest; see `SHA256SUMS.txt` for SHA-256)
- `requirements-windows-uv.lock` (2,316 bytes, SHA-256: `7e994b4c231536fb5c53d79959761bc426bd9ff9585b578165f1fd67ec19077f`, Windows x64 / CPython 3.12 wheel SHA-256 lockfile)
- `windows-uv-runtime.json` (1,239 bytes, SHA-256: `49ca2dea68fcc253574d867b9d5ff29524aa50e3b214d7c4687cd441dbdaa1dd`, pinned runtime dependency definitions)
- `THIRD-PARTY-NOTICES.txt` (622,989 bytes, SHA-256: `21929c232ddf95e158a808561a5cdf21b9cbb9798b2d55f6c577975d5393fd3c`)
- `DEPENDENCY-SOURCES.json` (24,583 bytes, SHA-256: `5ef42613490d2f807cbd0cca13b51e96e1f73716d880db2a5fc8dce844291609`)
- `SHA256SUMS.txt` / `uv-tool-release-manifest.json`

## 3. Installation and Launch Procedure

Download the `.whl`, `requirements-windows-uv.lock`, and `SHA256SUMS.txt` from the GitHub Release, verify their SHA-256 hashes, and install with `uv tool install`:

```powershell
$ErrorActionPreference = 'Stop'
# 1. Verify SHA-256 checksums
Get-FileHash .\folimeld-0.3.5-py3-none-any.whl, .\requirements-windows-uv.lock -Algorithm SHA256

# 2. Install into an isolated uv tool environment (CPython 3.12.x, hash-locked requirements, no source builds)
uv tool install --python 3.12 --with-requirements .\requirements-windows-uv.lock --no-build .\folimeld-0.3.5-py3-none-any.whl
```

- **Standard launch (GUI without console)**: `folimeld`
- **Diagnostic launch (console with stderr output)**: `folimeld-console`
- **Uninstall**: `uv tool uninstall folimeld` (settings and logs under `%LOCALAPPDATA%\Folimeld-UV-Tool` are preserved)

## 4. Isolated Installation, Real GUI, and 3-Worker Verification Record (2026-11-16)

- Executed the `uv tool install` command above using CPython 3.12.16 (`python-build-standalone` 20261110) and `uv 0.13.8` into isolated `UV_TOOL_DIR`, `UV_TOOL_BIN_DIR`, and `LOCALAPPDATA` directories.
- Verified installation of `folimeld==0.3.5` plus all 14 pinned runtime dependencies (15 packages total) and generation of both `folimeld.exe` (GUI) and `folimeld-console.exe` (console) entry points.
- Verified resolution of `resource_root()` to `site-packages/folimeld/_resources`, loading of locales, icons, and all 4 license tabs (`Folimeld`, `Windows uv notices`, `Windows uv installed packages`, `Windows uv sources`).
- Verified real GUI operations: opening a synthetic 3-page PDF, rotating, moving pages, saving via Worker 1 (PDF save worker), importing and converting 2 PNG images via Worker 2 (image conversion worker), saving the converted PDF via Worker 3 (image PDF save worker), and reopening both saved PDFs with matching page counts and rotation.
- Verified `GetWindowDpiAwarenessContext` on the main window matches `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2` (-4) (`GetDpiForWindow` = 144), Sponsors action enabled, and `StoreSupport` disabled.
- Verified settings persistence (`thumbnail_size=144`, `button_display=icon_text`) in `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` across restarts and per-session log directory creation.
- Verified duplicate-launch rejection when `Local\Folimeld-UV-Tool` is held: launching `folimeld-console.exe` displays the `Folimeld uv tool` error dialog, writes the error to `stderr`, and exits with code `1`.
- Verified existing `Folimeld-UV` and `Folimeld-Desktop` settings files and `HKCU\Software\Classes\Applications\Folimeld.exe` registry entries remained unchanged before and after testing.
