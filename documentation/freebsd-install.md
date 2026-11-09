# FreeBSD installation and build

[English](freebsd-install.md) | [日本語](freebsd-install_ja.md)

Target: FreeBSD 15.1 / amd64, Python 3.12, and a graphical desktop. A preview is available in the [GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.3). This is not an official FreeBSD Ports package.

Package creation, installation in a clean chroot, GUI launch, image conversion, saving, removal, and reinstallation have been verified. See the [verification record (Japanese)](freebsd-package-verification_ja.md).

## Installing the package

Download the [package](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/folimeld-0.3.3_1.pkg) and [checksums](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/SHA256SUMS.txt) from the Release. The [matching source ZIP](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/Folimeld-source-9ceb5ec75dcd3ddb60bb66f0b6996da5e700cf4400bd89b31808f5250b19f23b.zip), `build-record.json`, and PyMuPDF/MuPDF source archives are attached to the same Release. Compare `sha256 -r folimeld-0.3.3_1.pkg` with the entry for that file in the checksum list. Check the other distribution files in the same way. Local build outputs remain in `dist/freebsd/`; files organized for publication are retained in `build/freebsd-release/`.

Install dependencies first as root. Do not rely on `pkg add` for a local file to fetch missing dependencies from the official repository.

```sh
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./folimeld-0.3.3_1.pkg
```

Launch as a regular user:

```sh
folimeld
folimeld /path/to/file.pdf
```

Install an update with `pkg add ./new-package-name.pkg`. Updates from future versions have not been tested. Uninstall as root with `pkg delete folimeld`; do not automatically remove dependencies shared by other applications. User PDFs and settings are retained.

The package installs `/usr/local/bin/folimeld`, `/usr/local/share/folimeld/`, a desktop entry, and an icon. Python, Qt, Pillow, cryptography, and psutil use official packages. Only PyMuPDF/MuPDF 1.28.2 is bundled in a private `vendor/` directory. No development virtual environment is referenced. Qt dependencies are large and require network access and sufficient disk space.

## Running from source

Install runtime and build dependencies as root:

```sh
pkg install git python312 py312-pip py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp gmake swig pkgconf llvm19
```

Use the matching source ZIP attached to this Release. Extract it into a new directory as a regular user. Replace the filename below with the actual hash-based filename.

```sh
python3.12 -m zipfile -e /path/to/Folimeld-source-SHA256.zip Folimeld
cd Folimeld
sh tools/build_freebsd_pymupdf.sh
python3.12 -m venv --system-site-packages .venv-freebsd
.venv-freebsd/bin/python -m pip install --no-deps \
  build/freebsd-pymupdf/wheels/pymupdf-1.28.2-*.whl
.venv-freebsd/bin/python main.py
```

System PyMuPDF 1.27.2.2 crashes when reading forms. See the [cause and fix (Japanese)](freebsd-forms-fix_ja.md). Use the virtual environment's Python.

## Building the package

Supply the matching source ZIP and a wheel built on the target FreeBSD environment. `source_datas()` in `tools/source_bundle.py` creates a hashed source ZIP from the Git working tree and records any uncommitted changes in its manifest.

```sh
python3.12 -c "from tools.source_bundle import source_datas; source_datas('.', 'freebsd-amd64')"
python3.12 tools/build_freebsd_package.py \
  --source dist/source/Folimeld-source-ACTUAL_SHA256.zip \
  --wheel build/freebsd-pymupdf/wheels/ACTUAL_WHEEL_NAME.whl \
  --output dist/freebsd
```

Building the package does not require root. The builder verifies the source manifest and records dependency names, versions, and origins, plus SHA-256 hashes of the source ZIP, wheel, and package. Installed files are owned by root:wheel. The package version appends `_1` to the application version as the FreeBSD package revision.

Corresponding sources for bundled native code are [PyMuPDF 1.28.2](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/pymupdf-1.28.2.tar.gz), [MuPDF 1.28.2](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/mupdf-1.28.2-source.tar.gz), and `packaging/freebsd/pymupdf-1.28.2-freebsd.patch` in the matching source ZIP. They have been verified against the fixed hashes in the build script. External official dependency packages are not bundled.

References: official FreeBSD pkg [pkg-create(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-create.8) and [pkg-add(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-add.8).
