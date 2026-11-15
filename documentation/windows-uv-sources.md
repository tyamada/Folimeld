# Windows source + uv edition: licenses and versioned source references

This guide applies to the Windows x64 / CPython 3.12.16 source + uv edition.
Keep it separate from Microsoft Store and Linux distribution records.

- [Complete uv-specific license notices](windows-uv-licenses/notices.txt)
- [Pinned artifacts, sources and verification scope](windows-uv-licenses/sources.json)
- [Installation and acceptance status](windows-uv-source.md)

## Distributed and downloaded material

Folimeld is distributed under AGPL-3.0-only. Its source ZIP includes application
source, installation/launch scripts, pinned inputs, license texts and notices;
it excludes Python, uv, wheels and installed environments. The installer downloads
pinned Python and uv from official GitHub Releases and wheels directly from PyPI,
checks their hashes and retains upstream notices.

A formal Release must link its commit, corresponding source ZIP, internal
manifest, SHA-256, this guide and notices. Preparation is currently unpublished.
Do not claim uncommitted changes belong to an existing tag or preview ZIP.

## Fourteen pinned packages and source locations

| Pinned package | Version | Principal license / source reference |
| --- | --- | --- |
| cffi | 2.1.1 | MIT-0; separate libffi terms. PyPI sdist in the ledger |
| cryptography | 50.0.2 | Apache-2.0 or BSD-3-Clause; separate OpenSSL/Rust terms. PyPI sdist |
| Pillow | 12.3.0 | MIT-CMU and embedded-component terms. PyPI sdist |
| pycparser | 3.12 | BSD-3-Clause. PyPI sdist |
| PyMuPDF | 1.28.2 | AGPLv3 option; observed MuPDF also 1.28.2. PyPI sdist and upstream MuPDF |
| PySide6 / Addons / Essentials / shiboken6 | 6.11.2 each | Qt community licenses; official QtForPython and Qt sources below |
| typing-extensions | 4.16.0 | PSF-2.0. PyPI sdist |
| winrt-runtime / Windows.Foundation / Windows.Foundation.Collections / Windows.Services.Store | 3.2.1 each | MIT. Individual PyPI sdists and PyWinRT v3.2.1 |

The ledger's `packages[].sdists` records exact filenames, URLs and published
hashes. Ten packages have PyPI sdists; the four Qt packages do not. All source
archives have not been downloaded/inspected or fully matched to wheel build patches.

- [Official QtForPython/PySide/Shiboken 6.11.2 sources](https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/)
- [Official Qt 6.11.2 sources](https://download.qt.io/archive/qt/6.11/6.11.2/single/)
- [MuPDF 1.28.2 source tag](https://github.com/ArtifexSoftware/mupdf/tree/1.28.2)
- [PyWinRT v3.2.1 sources](https://github.com/pywinrt/pywinrt/tree/v3.2.1)

Not all Qt modules are LGPL. Stock Addons include GPL modules such as Virtual
Keyboard. Do not transfer Linux's exclusions to this edition; distinguish
installed, used and redistributed components. No commercial Qt or Artifex
license is claimed.

## Python and uv

- [CPython v3.12.16](https://github.com/python/cpython/tree/v3.12.16): PSF and historical licenses.
- [python-build-standalone 20261110](https://github.com/astral-sh/python-build-standalone/tree/20261110):
  build scripts and patches for pinned Python. Its project license does not relicense Python.
- [uv 0.13.8](https://github.com/astral-sh/uv/tree/0.13.8): MIT or Apache-2.0. This guide selects MIT and preserves both texts.

The uv notices include the actual Python LICENSE.txt and pinned upstream uv and
PyWinRT licenses. Python's OpenSSL 3.5.9 and cryptography's OpenSSL 4.0.3 are
separate components. The PBS full archive's PYTHON.json, complete build inputs
and uv's complete Rust dependencies have not been fully verified.

## Modification, redistribution and limits

Under the LGPL route, preserve applicable rights to use modified libraries and
debug modifications. The launcher checks dependency version metadata, not actual
Qt DLL hashes at startup. Test ABI-compatible modified dependencies retaining
the required metadata version in a separate copy, preserving the old environment.
Modified-library acceptance and different ABIs remain unverified.

Do not reuse this direct-download arrangement unchanged when redistributing
runtimes, wheels, modified dependencies or offline environments. In addition to
copyright/permission texts and third-party notices, provide corresponding source,
required build/installation information and modification methods appropriate to
those artifacts under AGPL/LGPL and other applicable terms. Upstream links alone
are not assumed always sufficient. Parent-package licenses and runtime versions
do not establish all embedded-component terms or build provenance.

The existing `licenses/crypto-native-sources.json` records an earlier cp314
environment. The uv ledger separately records the matching cryptography binary
hash and different cp312 CFFI hash. Retain the earlier evidence; do not present it
as proof of the entire uv environment.

[日本語](windows-uv-sources_ja.md)
