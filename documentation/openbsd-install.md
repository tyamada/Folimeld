# Installing and building on OpenBSD

[English](openbsd-install.md) | [日本語](openbsd-install_ja.md)

The commands and build instructions on this page target amd64. For arm64, use the [installation instructions](https://github.com/tyamada/Folimeld/releases/download/openbsd-aarch64-v0.3.3/INSTALL.txt) in the [dedicated Release](https://github.com/tyamada/Folimeld/releases/tag/openbsd-aarch64-v0.3.3), which also contains matching source, SHA-256 checksums, and verification records.

Targets OpenBSD 8.0 / amd64, Python 3.14, and an X11 desktop. This is a Folimeld preview, not an official OpenBSD package. Assets belong to the [OpenBSD Release](https://github.com/tyamada/Folimeld/releases/tag/openbsd-v0.3.3).

## Installing packages

Download `folimeld-0.3.3.tgz`, `folimeld-mupdf-1.28.2.tgz`, `folimeld-80-pkg.pub`, `SHA256SUMS.txt`, and `SHA256SUMS.txt.sig` into one directory. Compare the second line of the key with the [repository public key](../packaging/openbsd/folimeld-80-pkg.pub):

```text
RWSM2obNrKjUbNGU8itgBN/nGVFG95tTaBrcV9pO8dTLQvihQtAdPkIy
```

As a regular user, verify the signature and compare the `sha256 -r` results with the matching filenames in the signed list.

```sh
signify -V -p folimeld-80-pkg.pub -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
sha256 -r folimeld-0.3.3.tgz folimeld-mupdf-1.28.2.tgz
```

Configure an X11 desktop and `/etc/installurl` for official OpenBSD 8.0 packages. Run as root, using a root shell if `doas` is not configured:

```sh
install -m 644 folimeld-80-pkg.pub /etc/signify/folimeld-80-pkg.pub
pkg_add ./folimeld-mupdf-1.28.2.tgz ./folimeld-0.3.3.tgz
```

Use signed packages without options that allow unsigned packages. Python, PySide6/Qt, Pillow, cryptography, psutil, gettext-runtime, and Japanese fonts are official dependencies. Network access and free disk space are required.

Launch as a regular user within an X11 session:

```sh
folimeld
folimeld '/path/to/file.pdf'
```

To remove, run `pkg_delete folimeld` as root, followed by `pkg_delete folimeld-mupdf` if the private MuPDF dependency is no longer needed. No removal scripts delete user PDFs or settings. Shared official dependencies remain installed.

The application is installed in `/usr/local/share/folimeld/`, with `/usr/local/bin/folimeld` as its launcher. The private PyMuPDF/MuPDF 1.28.2 dependency lives in `share/folimeld/vendor/` and does not replace system PyMuPDF. Existing [source verification (Japanese)](openbsd-verification_ja.md) used a VirtualBox VM with 1 vCPU and 16 GiB RAM. Operation with 4 vCPUs, other OS versions, or other architectures is not guaranteed.

## Building from source

Download the hash-named `Folimeld-source-*.zip` and the two original PyMuPDF/MuPDF source archives from the Release. Check their hashes against the build record, extract the matching source ZIP, and work from its root. Use the archive associated with the packages rather than GitHub's automatically generated ZIP.

Install build dependencies as root. Base compiler, development, and X11 sets are also required.

```sh
pkg_add python py3-pip py3-virtualenv py3-llvm%22 swig gmake bash \
  pyside6 py3-Pillow py3-cryptography py3-psutil noto-cjk
```

As a regular user, use absolute paths without spaces or shell special characters:

```sh
sh tools/build_openbsd_native.sh /path/to/dependency-sources \
  /path/to/new-native-work /path/to/wheels
python3 -m venv --system-site-packages .venv-openbsd
.venv-openbsd/bin/python -m pip install --no-deps /path/to/wheels/pymupdf-1.28.2-*.whl
.venv-openbsd/bin/python main.py
```

The script verifies both upstream archive hashes, applies the LLVM 22 patch, and builds the wheel. Use a new work directory and allow time for native compilation.

To package, install the signature-verified OpenBSD 8.0 ports tree in `/usr/ports`. Run as root in a dedicated build VM. Existing `print/folimeld` and `print/folimeld-mupdf` ports are not overwritten.

```sh
python3 -m tools.build_openbsd_package \
  --source /path/to/Folimeld-source-SHA256.zip \
  --wheel /path/to/wheels/pymupdf-1.28.2-cp314-abi3-openbsd_8_0_amd64.whl \
  --wheel-sha256 RECORDED_WHEEL_SHA256 \
  --dependency-sources /path/to/dependency-sources \
  --output /path/to/output --work /path/to/new-package-work
```

The builder generates local ports and packing lists, then uses ports fake installation, shared-library checks, and packaging. `build-record.json` records hashes of the source archive, wheel, dependency sources, packages, and payload files. The publisher signs packages separately with `sh tools/sign_openbsd_packages.sh /path/to/secret.sec /path/to/output /path/to/new-signed-output`. Keep secret keys outside the source tree and release directory. Signing changes package hashes; the Release's signed checksum list records the final distributed hashes.

References: official OpenBSD [ports](https://www.openbsd.org/faq/ports/), [pkg_add(1)](https://man.openbsd.org/pkg_add), and [signify(1)](https://man.openbsd.org/signify).
