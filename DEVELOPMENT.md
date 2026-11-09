# Folimeld Development Guide

[日本語](DEVELOPMENT_ja.md) | [English](DEVELOPMENT.md)

This document explains how to set up a development environment, run tests, build the application, and create release packages.

## Technology stack

- Python 3
- PySide6 / Qt Widgets
- PyMuPDF
- Pillow (icon generation)
- PyInstaller (executable generation)
- pytest (testing)

## Development environment setup

### Windows

The Windows edition supports both Intel/AMD (x64) and ARM (ARM64).

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

### macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

### Ubuntu

Ubuntu 22.04 or later is assumed.

```bash
sudo apt update
sudo apt install python3-venv libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 fonts-noto-cjk
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

`fonts-noto-cjk` is used to display Japanese, Chinese, and Korean text.

### NetBSD (verified configuration)

Source execution was verified on NetBSD 11.1 / amd64 with Python 3.12.14, PySide6 / Qt 6.11.2, and PyMuPDF / MuPDF 1.28.2. PySide6, PyMuPDF, and the build tools require NetBSD-specific changes. See the [verification record (Japanese)](documentation/netbsd-verification_ja.md) for setup instructions, patches, and the full test and GUI results. No NetBSD distribution package has been created.

After building the dependencies and `.venv-netbsd` as described in the record, launch from the repository root within an X11 session.

```sh
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
.venv-netbsd/bin/python main.py
```

## Public and private distribution policy

Windows and macOS binaries stay private and are built and verified locally. Linux deb/Snap packages are public. The [migration plan](documentation/linux-release-migration.md) groups Linux packages, SHA-256 checksums, corresponding source ZIPs and build records in one Release. Run the following offline asset check before publication; it does not upload files or create tags.

```bash
python -m tools.prepare_linux_release --version 0.3.3
```

CI uses Python 3.12. This macOS review verified dependency installation, tests and packaging with Python 3.14.6 and the constrained dependency versions. Start new environments with those constraints rather than installing unrestricted versions.

## Running from source

Windows:

```bat
.venv\Scripts\python main.py
```

macOS / Ubuntu:

```bash
. .venv/bin/activate
python main.py
```

## Tests

```bash
python -m pytest -q
```

To use the virtual environment directly on Windows:

```bat
.venv\Scripts\python -m pytest -q
```

## Quality checks and performance measurements

The GitHub Actions [Checks](.github/workflows/checks.yml) workflow runs Ruff, mypy, and pytest on Windows, Ubuntu 22.04, and macOS using Python 3.12. Ruff checks syntax errors, undefined names, unused code, and related issues; mypy checks the model and history layers. Distribution builds and CI use `constraints-release.txt` to constrain major dependency versions. These versions have been checked on Windows; the constraints do not guarantee OS-specific dependencies or distribution behavior. When updating dependencies, update the constraints and run CI on all three operating systems and the pre-release checks. Each job uploads test results and `pip freeze` as artifacts. Adding or changing CI does not itself verify success on each OS or the behavior of distribution packages.

```bash
python -m pip install -r requirements-dev.txt -c constraints-release.txt
python -m ruff check .
python -m mypy
python -m pytest -q -p no:cacheprovider
python -m tools.benchmark_pdf --pages 100 --output build/benchmarks/text-100.json
python -m tools.benchmark_pdf --pages 100 --image-size 256 --output build/benchmarks/images-100.json
python -m tools.benchmark_pdf --pages 1000 --output build/benchmarks/text-1000.json
```

Run each case in a fresh process. Use `--input path/to/document.pdf` for an existing PDF; saved PDFs go to a temporary directory. Encrypted PDFs are outside this tool's scope. Run each case at least three times with inputs that vary in page count, image content, and file size, then compare medians and variation. JSON reports record operation times, the longest thumbnail batch, process RSS sampled every 5 ms, and dependency versions. RSS includes native memory but sampling can miss short peaks. Fixture generation and window initialization are excluded from operation times.

See [Performance and release verification](documentation/performance-and-release_ja.md) (in Japanese) for initial measurements and pre-release checks.
See the [Windows load-test preflight record](documentation/windows-load-test_ja.md) (in Japanese); the load test itself was not performed at that time.

The measurement tool also scrolls through the document and records the maximum retained thumbnail count. Large PDFs render only the viewport and nearby pages, so `initial_thumbnails` does not measure rendering every page. Compare it together with `scroll_thumbnails` and memory usage. Normally up to 64 thumbnails are retained; if an exceptionally large screen shows more than 64 pages, all visible pages take priority.

## Saving, history, and diagnostics

Normal saving uses `garbage=3`, skipping stream deduplication. In the GUI, a separate process owns an independent document and writes temporary output; the model replaces the destination after success. Preparation and final switching remain synchronous; editing and cancellation are unavailable during saving. The benchmark tool measures the synchronous model API and excludes GUI process startup time.

History is bounded by 128 MiB in memory and 1 GiB in temporary files. `history_bytes` counts in-memory PDF data; `history_disk_bytes` counts encrypted-container bytes on disk, including authentication metadata. Snapshot creation and restoration process the whole PDF, so these limits do not bound temporary memory usage or edit latency. Spilled history, temporary save-process input, and intermediate image-conversion PDFs use AES-256-GCM in `folimeld/temporary_data.py`, which authenticates the entire input before returning plaintext. Each file gets a random key and nonce. Keys are not saved to files or settings: history keys remain in memory, and save/image-worker keys are passed through interprocess communication. Encryption processes large data in chunks, and decrypted results remain in memory until authenticated. Unused history is explicitly closed and key references released; save/image-conversion staging directories are removed when processing ends.

Automatic recovery of encrypted containers left by main-process termination or OS shutdown, and complete erasure from memory, pagefiles, or crash dumps are not guaranteed. Image conversion writes ciphertext directly, then the parent authenticates and opens the PDF from memory before replacing the current document. Serialization and decryption require memory for the complete PDF. Output PDFs use the encryption settings selected by the user. Do not conflate these scopes by claiming all temporary data is encrypted. Distribution notices also collect versions and licenses for `cryptography`, `cffi`, and `pycparser`.

Error tracebacks are recorded in `logs/folimeld.log` under Qt's `AppLocalDataLocation` (up to three files of 1 MiB each). On Windows this is normally `%LOCALAPPDATA%/Folimeld/Folimeld/logs/`. No code explicitly logs PDF contents or passwords, but exception messages may contain filenames and similar information. Failure to initialize logging does not prevent startup.

## Version management

The application's display version is managed by `__version__` in `folimeld/__init__.py`, and the App Store build number by `__build__`. Update either the display version or the build number for every new App Store submission. In particular, increment the build number when resubmitting the same display version.

Version information for the Windows executable is generated at build time by `tools/write_version_info.py`. Ubuntu packages and the macOS App Bundle also use the application's display version. Store-submission MSIX versions are managed separately in a dedicated configuration file.

License documents are bundled through calls to `tools/license_bundle.py` in each spec file.
Review [Licensing and distribution](documentation/license-distribution_ja.md) (in Japanese) before distributing the application.

## Icons

Run the following command to generate transparent PNG, ICO, ICNS, and MSIX images from `assets/Folimeld-icon-source.png`.

```bash
python tools/make_app_icon.py
```

Output locations:

- `assets/Folimeld-icon-master.png`
- `assets/Folimeld.iconset/`
- `assets/Folimeld.ico`
- `assets/Folimeld.icns`
- `packaging/msix/Assets/`

## Windows build

```bat
build_exe.bat
```

The output is `dist\Folimeld.exe`, a standalone executable that includes Python, PySide6, PyMuPDF, and translation data.

The unpackaged edition registers Folimeld in Windows **Open with** at startup. The MSIX edition uses file associations in the package manifest instead of registering them in the registry.

## MSIX for Microsoft Store

The user reports that the existing Folimeld registration is an EXE or MSI app. MSIX has been selected for publication, but migration/name handling and MSIX identity information await confirmation. The [release plan](documentation/windows-store-release-plan.md) records the status and requirements for each submission type.

### Intel/AMD (x64)

Unsigned development MSIX:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1
```

The output is `dist\Folimeld_<バージョン>_x64.msix`, where `<バージョン>` is the version.

For Store submissions, copy `packaging/msix/store-config.example.json` to `build/store-config.json` and configure the MSIX registration's identity, publisher, publisher display name, and submission version. Do not use the EXE/MSI application ID. Blank settings, the development identity, and invalid versions are rejected before rebuilding the EXE. Validate the configuration first.

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json -ValidateOnly

powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json
```

Omitting `-Store` selects development mode. The existing `-IdentityName`, `-Publisher`, and `-PublisherDisplayName` parameters remain available for development; Store mode uses only its configuration file. Generated MSIX packages are statically checked for identity, version, executable architecture, bundled images, and related settings, with results saved in `build/msix-preflight/`. For updates, `-PreviousPackage` checks that the version increases relative to the previous MSIX for the same Store product. Static checks do not replace WACK, installed-app tests, or Partner Center validation. To install outside the Store, sign it with a certificate that matches the Publisher in the manifest.

### ARM (ARM64)

Build the ARM64 edition on a physical Windows on ARM device or an ARM64 Windows virtual machine. PyInstaller does not cross-build from x64 to ARM64, so recreate the virtual environment with ARM64 Python and install ARM64-compatible packages for PySide6, PyMuPDF, Pillow, and PyInstaller.

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 -Architecture arm64 `
  -Store -StoreConfig .\build\store-config.json
```

The build script checks the architecture of the Python/PyInstaller environment and stops if it does not match the requested architecture.

## macOS build

```bash
./build_exe.sh
```

The output is `dist/Folimeld.app`. The script creates a virtual environment and installs dependencies as needed.

```bash
open dist/Folimeld.app
```

Ad-hoc signing is used for local verification. For official distribution, sign with an Apple Developer certificate and complete notarization.

### Mac App Store build

In Apple Developer, prepare an App Store application signing certificate, an installer signing certificate, and a provisioning profile with App Sandbox enabled for Bundle ID `com.folimeld.Folimeld`.

Replace the Japanese placeholders below with the Common Names of the application and installer signing certificates, respectively.

```bash
./build_appstore.sh \
  --application-identity "アプリ署名証明書のCommon Name" \
  --installer-identity "インストーラ署名証明書のCommon Name" \
  --provisioning-profile "/path/to/Folimeld.provisionprofile"
```

The output is `dist/Folimeld_<表示バージョン>.pkg`, where `<表示バージョン>` is the display version. The script applies App Sandbox entitlements and signs the application and installer. Before submission, it automatically verifies the application signature, Info.plist, Bundle ID, separation of the display version and build number, PDF document types, Sandbox entitlements, and installer signature. After testing with TestFlight, upload to App Store Connect using Transporter or Xcode.

Update the version in `folimeld/__init__.py` every time you upload to the App Store. The current entitlements do not include network access, as the application only reads and writes PDFs selected by the user through file dialogs.

## Ubuntu build

```bash
bash build_linux.sh
```

The following files are generated (`<バージョン>` means version and `<アーキテクチャ>` means architecture):

- `dist/folimeld`
- `releases/ubuntu/folimeld_<バージョン>_<アーキテクチャ>.deb`

Build distribution deb packages on Ubuntu 22.04 to support Ubuntu 22.04 and later. Building on a newer Ubuntu release may cause the bundled Python or shared libraries to require a newer glibc, preventing the application from starting on 22.04.

```bash
sudo apt install ./releases/ubuntu/folimeld_*.deb
```

The DEB package includes a desktop menu entry, icons, and PDF file associations.

A Linux-specific virtual environment, `.venv-linux`, is used. Set `FOLIMELD_LINUX_VENV` to change its location.
On WSL, using a path on the Linux side (for example, `/tmp/folimeld-build-venv`) speeds up builds.
The minimum `libc6` version for the deb package is determined from the build environment. Packages built on Ubuntu 22.04 target `libc6 >= 2.35`. Always build the executable itself on 22.04; do not merely lower the declared dependency version.

Example of building a distribution deb package from WSL (after installing the required dependencies):

```powershell
wsl -d Ubuntu-22.04 -- bash -lc 'cd /path/to/Folimeld && FOLIMELD_LINUX_VENV=~/.cache/folimeld-build-venv bash build_linux.sh'
```

Adjust the path for your environment. Before distribution, verify deb installation and PDF display, editing, and saving on Ubuntu 22.04, 24.04, and 26.04. When replacing packages, also update `releases/ubuntu/folimeld_<バージョン>_SHA256SUMS.txt`.

The same deb package is distributed for Debian 13 (amd64). Include Debian 13 in testing before distribution. Basic functionality of 0.3.2 has been verified on Debian 13.6 with WSL2 / WSLg (X11). See the [verification record](documentation/debian-wsl-verification_ja.md) (in Japanese) for the scope of testing and missing Fontconfig configuration on minimal installations.

### Snap package

After running `build_linux.sh` on Ubuntu 24.04, run:

```bash
sudo snap install snapcraft --classic
bash build_snap.sh
```

The output is `releases/ubuntu/folimeld_<バージョン>_<アーキテクチャ>.snap`.
Snapcraft's default isolated build environment is used. On a dedicated Ubuntu 24.04 build environment or WSL,
you can also build with `sudo bash build_snap.sh --destructive-mode` if installing build dependencies on the host is acceptable.
The package uses `core24` and the GNOME extension, and bundles Qt's X11 libraries, icons, and PDF file associations.

Install and launch the local package:

```bash
sudo snap install --dangerous ./releases/ubuntu/folimeld_0.3.2_amd64.snap
snap run folimeld
```

The Snap runs with strict confinement and can access regular files in the home folder.
To edit PDFs on external drives, run `sudo snap connect folimeld:removable-media`.
Publishing to the Snap Store is a separate procedure from this local build.

## Pre-release checks

1. Update the version in `folimeld/__init__.py`
2. Run all tests
3. Perform a clean build for each target operating system
4. Verify startup, opening files, editing, and saving in an environment without Python installed
5. Verify PDF file associations and uninstallation
6. Verify license and third-party license displays
7. Check MSIX packages with the Windows App Certification Kit

## License

Contributions to this project are provided under the same [GNU Affero General Public License v3.0](LICENSE) terms as the project itself.
