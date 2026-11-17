# Ubuntu amd64 strict Snap 0.3.5 Verification

[日本語](linux-snap-amd64-035-validation_ja.md) | [English](linux-snap-amd64-035-validation.md)

November 17, 2026 (Japan time). Completed the build, installation, and runtime verification of the Folimeld 0.3.5 amd64 strict Snap package under Ubuntu 24.04.5 LTS amd64 (WSL2 / WSLg).

## Package Details

- **Package name**: `folimeld_0.3.5_amd64.snap`
- **File size**: 106,164,224 bytes
- **SHA-256**: `ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570`
- **Payload executable**: `dist/folimeld` (SHA-256: `65852198ae2282b8b49e52e4bd3583b0ee131e287a52aa73368f03c2817a47aa`)
- **Corresponding source snapshot**: `dist/source/Folimeld-source-a7683298b15e7326d100b54e0c1083e7fc12af3b5e3d19d329cfc417032ee545.zip` (SHA-256: `a7683298b15e7326d100b54e0c1083e7fc12af3b5e3d19d329cfc417032ee545`)
- **Association record**: `dist/source/folimeld_0.3.5_amd64.snap-ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570.json`

## Build Environment and Configuration

- **OS**: Ubuntu 24.04.5 LTS (Noble Numbat) amd64
- **Snapcraft**: 9.2.1
- **Base**: `core24`
- **Confinement**: `strict`
- **Grade**: `stable`
- **Extensions**: `gnome` (`gnome-46-2404`, `gtk-common-themes`, `mesa-2404`)

## Acceptance Verification Results

1. **Installation verification**:
   - Installed via `sudo snap install --dangerous releases/ubuntu/folimeld_0.3.5_amd64.snap`.
   - Confirmed version `0.3.5` (revision `x2`) via `snap list folimeld`.
2. **Interface connection verification**:
   - Verified active connections via `snap connections folimeld` for `desktop`, `desktop-legacy`, `wayland`, `x11`, `opengl`, `gsettings`, `home`, `gnome-46-2404`, `gpu-2404`, `gtk-3-themes`, `icon-themes`, and `sound-themes`.
3. **Offscreen GUI execution**:
   - Verified clean execution via `QT_QPA_PLATFORM=offscreen timeout 5s snap run folimeld`, confirming PySide6 Qt GUI initialization, PyMuPDF loading, window creation, and normal runtime.
