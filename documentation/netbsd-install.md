# Installing and building on NetBSD

[English](netbsd-install.md) | [日本語](netbsd-install_ja.md)

The commands and build instructions on this page target amd64. For aarch64, use the [installation instructions](https://github.com/tyamada/Folimeld/releases/download/netbsd-aarch64-v0.3.3/INSTALL.txt) in the [dedicated Release](https://github.com/tyamada/Folimeld/releases/tag/netbsd-aarch64-v0.3.3), which also contains matching source, SHA-256 checksums, and verification records.

Targets NetBSD 11.1 / amd64, Python 3.12, and an X11 desktop. This is a Folimeld preview package, not an official NetBSD package. Obtain the package, matching source, dependency sources, and SHA-256 list from the [GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/netbsd-v0.3.3).

See the [package verification record](netbsd-package-verification_ja.md) for the tested scope.

## Installing the package

Release candidates are stored in `dist/netbsd/`. Keep the matching source ZIP, dependency sources, patches, build record, licenses, and `SHA256SUMS.txt` together. Compare `sha256 -r folimeld-0.3.3.tgz` with the entry for that file in the checksum list.

Run as root on NetBSD with X11 and a desktop configured. Use the tested pkgsrc repository for dependencies. Do not mix dependencies from different repository branches.

```sh
export PKG_PATH=https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/x86_64/11.0_2026Q3/All
/usr/pkg/sbin/pkg_add ./folimeld-0.3.3.tgz
```

Launch as a regular user.

```sh
/usr/pkg/bin/folimeld
/usr/pkg/bin/folimeld '/path/to/file.pdf'
```

Remove as root with `/usr/pkg/sbin/pkg_delete folimeld`. User PDFs and settings are preserved. Shared dependencies are not removed. Upgrades from future versions have not been tested.

Installs `/usr/pkg/bin/folimeld`, `/usr/pkg/share/folimeld/`, a desktop entry, and an icon. PySide6/shiboken6 6.11.2 (Core/Gui/Widgets) and PyMuPDF/MuPDF 1.28.2 are bundled privately. Python, Qt, Pillow, cryptography, psutil, and Japanese fonts use official packages. The dependency set is large and requires network access and disk space.

## Building from source

Extract the matching source ZIP and work in its directory. In addition to runtime dependencies, install Python pip, C/C++ compilers, LLVM/Clang, CMake, Ninja, Bash, GNU make, SWIG, pkg-config, and Qt development files. See the [verification record](netbsd-verification_ja.md) for tested versions and patches.

Install build dependencies as root.

```sh
/usr/pkg/sbin/pkg_add py312-pip llvm clang cmake ninja-build bash gmake swig4 pkgconf
/usr/pkg/sbin/pkg_add python312 qt6-qtbase qt6-qtsvg qt6-qtimageformats \
  qt6-qttranslations py312-Pillow py312-cryptography py312-psutil gettext-lib noto-cjk-fonts
```

Run as a regular user. Use absolute paths without spaces or shell metacharacters.

```sh
sh tools/build_netbsd_native.sh
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
.venv-netbsd/bin/python main.py
```

`NETBSD_BUILD_DIR` and `NETBSD_NATIVE_PREFIX` override the build directory and virtual environment. The script uses the preserved verification recipes and patches and checks the official Qt source hash. PyMuPDF/MuPDF downloads are also hash-checked. Native compilation takes considerable time.

Create the package on the same NetBSD environment. Pass the hash-named source ZIP for distribution to `--source`.

```sh
python3.12 -m tools.build_netbsd_package \
  --source /path/to/Folimeld-source-SHA256.zip \
  --native-prefix "$PWD/.venv-netbsd" \
  --dependency-sources /path/to/dependency-sources --output dist/netbsd
```

The builder validates the source manifest and invokes `pkg_create`. `build-record.json` records exact dependency versions and SHA-256 hashes for bundled native files and the package.

Place the three distributed original source archives for PySide6, PyMuPDF, and MuPDF in `--dependency-sources`. The builder checks their pinned SHA-256 hashes. The generalized build wrapper has passed shell syntax checks; recompiling all dependencies at a different path has not been tested. Also consult the original VM native build records.

References: official NetBSD [pkg_create(1)](https://man.netbsd.org/pkg_create.1) and [pkg_add(1)](https://man.netbsd.org/pkg_add.1).
