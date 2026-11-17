# BSD and Linux (Debian/Ubuntu) 0.3.5 Package Update and Build Guide

[Japanese](bsd-035-release-plan_ja.md) | [English](bsd-035-release-plan.md)

> **Current Linux policy (2026-11-17):** all versions, including older releases, are prereleases (test distributions). New publication requires `prerelease=true` and not Latest; apply the [Linux publication checklist](linux-prerelease-policy.md). Historical records, snapshots and other OS classifications below remain unchanged.

Procedures for building, verifying, and publishing packages incorporating Folimeld 0.3.5 features (encrypted Undo/Redo disk offloading, accelerated large PDF saves, image folder batch import, virtualized thumbnails, and GitHub Sponsors guidance).

---

## 1. Upstream Source Snapshot

All platforms use the following captured source snapshot ZIP as their authoritative baseline:

- **File**: `dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`
- **SHA-256**: `E550BF65EC95B968DDCE59592F3EF4FD9E297A88B9E2B7364413592244A14E8A`
- **Commit**: `5d4ed15` (or later `main`)

---

## 2. FreeBSD 15.1 (amd64 / aarch64)

### Targets
- Package: `folimeld-0.3.5_1.pkg`
- Build record: `build-record.json`
- Source: `Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`

### Build procedure
Run on FreeBSD 15.1 (amd64 or aarch64).

```sh
# 1. Install build and runtime dependencies
pkg install git python312 py312-pip py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp gmake swig pkgconf llvm19

# 2. Build PyMuPDF 1.28.2 wheel (if not already prepared)
sh tools/build_freebsd_pymupdf.sh
# -> generates build/freebsd-pymupdf/wheels/pymupdf-1.28.2-*.whl

# 3. Build 0.3.5 package
python3.12 tools/build_freebsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --wheel build/freebsd-pymupdf/wheels/pymupdf-1.28.2-cp312-cp312-freebsd_*.whl \
  --output dist/freebsd
```

### Acceptance verification
```sh
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./dist/freebsd/folimeld-0.3.5_1.pkg

# Launch test
folimeld
```
- Confirm "Help → Sponsor Development..." menu appears and opens GitHub Sponsors.
- Verify PDF opening, rotation, large document saving, and image import.

### Build and acceptance verification (VirtualBox VM / FreeBSD 15.1-RELEASE-p5 amd64)
- Package: `dist/freebsd/folimeld-0.3.5_1.pkg` (26,168,773 bytes)
- SHA-256: `16d3d1801acae0f62bf99d89d53f8a679593e5896d1db60d46cc5b57c15946ae`
- Build record: `dist/freebsd/build-record.json` (SHA-256: `cf06b58c538bf6ba54cf1afa34bd8f7c3035ca1c0b0ce2190fd43b8361d462f9`)
- Verification results: Verified update installation with `pkg add -f` (MIME and icon cache triggers completed). Verified `0.3.5_1` via `pkg info folimeld`. Confirmed offscreen launch with `QT_QPA_PLATFORM=offscreen timeout 5s /usr/local/bin/folimeld` successfully initializing Qt GUI, loading PyMuPDF/fitz, creating window, and entering event loop.

---

## 3. NetBSD 11.1 (amd64 / aarch64)

### Targets
- Package: `folimeld-0.3.5.tgz`
- Build record: `build-record.json`

### Build procedure
Run on NetBSD 11.1.

```sh
# 1. Install pkgsrc dependencies
/usr/pkg/sbin/pkg_add py312-pip llvm clang cmake ninja-build bash gmake swig4 pkgconf
/usr/pkg/sbin/pkg_add python312 qt6-qtbase qt6-qtsvg qt6-qtimageformats \
  qt6-qttranslations py312-Pillow py312-cryptography py312-psutil gettext-lib noto-cjk-fonts

# 2. Prepare native prefix
sh tools/build_netbsd_native.sh

# 3. Build 0.3.5 package
python3.12 tools/build_netbsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --native-prefix .venv-netbsd \
  --dependency-sources /path/to/dependency_sources \
  --output dist/netbsd
```

### Acceptance verification
```sh
/usr/pkg/sbin/pkg_add ./dist/netbsd/folimeld-0.3.5.tgz
/usr/pkg/bin/folimeld
```

### Build and acceptance verification (VirtualBox VM / NetBSD 11.1 amd64)
- Package: `dist/netbsd/folimeld-0.3.5.tgz` (37,074,914 bytes)
- SHA-256: `7dc5c7d68e41b5120a9345fd679e5c99d46fcd7b7b50cf4f49e22d55ffec6e6a`
- Build record: `dist/netbsd/build-record.json` (SHA-256: `c1ce5d8574785b7f0af1aea20159a487349b45f7b5f2e04b633d43983f4124c4`)
- Verification results: Verified update installation via `/usr/pkg/sbin/pkg_add -u`. Confirmed `folimeld-0.3.5` via `/usr/pkg/sbin/pkg_info`. Verified offscreen launch with `QT_QPA_PLATFORM=offscreen timeout 5s /usr/pkg/bin/folimeld` successfully initializing Qt GUI, loading PyMuPDF/fitz, creating window, and entering event loop.

---

## 4. OpenBSD 8.0 (amd64 / arm64)

### Targets
- Package: `folimeld-0.3.5.tgz` (signed)
- Private dependency: `folimeld-mupdf-1.28.2.tgz`
- Signature: `SHA256SUMS.txt.sig`

### Build and signing procedure
Run on OpenBSD 8.0 with Python 3.14.

```sh
# 1. Build private MuPDF wheel (if not prepared)
sh tools/build_openbsd_native.sh /path/to/dependency_sources /tmp/work /tmp/out

# 2. Build 0.3.5 ports packages
python3.14 tools/build_openbsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --wheel /tmp/out/pymupdf-1.28.2-*.whl \
  --dependency-sources /path/to/dependency_sources \
  --output dist/openbsd \
  --work /tmp/pkgwork

# 3. Sign with signify
cd dist/openbsd
sha256 -r folimeld-0.3.5.tgz folimeld-mupdf-1.28.2.tgz > SHA256SUMS.txt
signify -S -s /etc/signify/folimeld-80-pkg.sec -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
```

### Acceptance verification
```sh
signify -V -p packaging/openbsd/folimeld-80-pkg.pub -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
pkg_add ./folimeld-mupdf-1.28.2.tgz ./folimeld-0.3.5.tgz
folimeld
```

### Build, signing, and acceptance verification (VirtualBox VM / OpenBSD 8.0 amd64)
- Main package (signed): `dist/openbsd/folimeld-0.3.5.tgz` (6,009,111 bytes)
  - SHA-256: `6d0b68373f380622dc1bbbe4bad4d132648f8974fa7246ca9af0c22db9028e63`
- Private MuPDF dependency (signed): `dist/openbsd/folimeld-mupdf-1.28.2.tgz` (26,822,825 bytes)
  - SHA-256: `1d537907faf92f11f2f701f967486c03643097e8dd5dff9199e6c6a6aa87bf8c`
- Signatures: `dist/openbsd/SHA256SUMS.txt`, `dist/openbsd/SHA256SUMS.txt.sig` (verified with `signify -V`)
- Build record: `dist/openbsd/build-record.json` (SHA-256: `b9a53586e99aa77f4e84f5633a73303a015a21ca7663a396cc001e9c83255bbc`)
- Verification results: Verified update installation via `pkg_add -r` with full signature verification passed. Confirmed `folimeld-0.3.5` and `folimeld-mupdf-1.28.2` via `pkg_info`. Verified offscreen launch with `QT_QPA_PLATFORM=offscreen /usr/local/bin/folimeld` successfully initializing Qt GUI, loading PyMuPDF/fitz, creating window, and running cleanly.

---

## 5. Ubuntu 24.04 / Debian 13 (amd64 / arm64)

### Targets
- DEB: `folimeld_0.3.5_amd64.deb`, `folimeld_0.3.5_arm64.deb`
- Snap: `folimeld_0.3.5_amd64.snap`, `folimeld_0.3.5_arm64.snap`

### Build procedure
Run on Ubuntu 24.04 / Debian 13 (or WSL2 / Docker).

```sh
# 1. Install dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-venv pyinstaller libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0

# 2. Build executable with PyInstaller
python3 -m venv .venv-linux
.venv-linux/bin/pip install -r requirements.txt -c constraints-release.txt pyinstaller
.venv-linux/bin/pyinstaller --noconfirm Folimeld-linux.spec

# 3. Assemble DEB package
dpkg-deb --build build/deb/folimeld_0.3.5_amd64 dist/folimeld_0.3.5_amd64.deb
```

### Build verification (WSL2 / Ubuntu 24.04)
Built via `./build_linux.sh deb` with verified package and association manifest generated:
- Package: `dist/ubuntu/folimeld_0.3.5_amd64.deb`
- Size: 105,690,904 bytes
- SHA-256: `5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174`
- Executable: `dist/folimeld` (SHA-256: `c799b852384f81839efcb79fa383a8ba3a6f8156d0d2b61501fb70803cd810b9`)
- Association record: `dist/source/folimeld_0.3.5_amd64.deb-5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174.json`

### Acceptance test results
- **Ubuntu 24.04.4 LTS / 24.04.5 LTS (WSL2)**:
  `QT_QPA_PLATFORM=offscreen timeout 4s /usr/bin/folimeld` verified successful Qt GUI initialization, PyMuPDF/fitz loading, window creation, and event loop entry (cleanly running).
- **Debian 13.6 / 13.7 Trixie (WSL2)**:
  Verified under Debian 13.6 and updated 13.7 fulfilling `libc6 (>= 2.39)` dependency (GLIBC 2.41), running successfully offscreen with Qt GUI window initialization and PyMuPDF/fitz loading.
