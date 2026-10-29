# Native encryption dependency review

[日本語](crypto-dependency-audit_ja.md) | [English](crypto-dependency-audit.md)

This review covers the Windows x64 encryption additions, not the complete Folimeld dependency tree. The [machine-readable record](../licenses/crypto-native-sources.json) identifies exact native binaries, source archive hashes, Cargo.lock hash, upstream URLs and notice hashes. Recheck after dependency updates or a change of wheel/platform. It is not a certification of license compliance or proof that an upstream wheel was compiled from unmodified sources.

| Component | Observed version | Collected evidence |
| --- | --- | --- |
| cryptography | 50.0.2 | PyPI sdist and checksum; packaged Apache/BSD licenses; installed native binding SHA-256 |
| OpenSSL in cryptography | 4.0.3 (backend reports 29 Sep 2026) | Official release archive matched to upstream SHA-256; legal files in `licenses/OpenSSL.txt` |
| Rust dependencies | 32 Cargo.lock registry entries | Each `.crate` checked against its lockfile checksum; legal documents in `licenses/Cryptography-Rust.txt` |
| CFFI | 2.1.1 | PyPI sdist and checksum; installed native binding SHA-256; bundled x86/x64 libffi copyright headers in `licenses/CFFI-libffi-x64.txt` |
| pycparser | 3.12 | PyPI sdist and checksum; wheel license collected by the existing package-notice mechanism |

The Rust set includes build-time and platform-specific dependencies. It is a conservative source/notice set, not an inventory of only the code linked into the Windows executable. The OpenSSL version was queried from cryptography's backend, independently of Python's `ssl` module. CFFI's package license alone does not replace the separately retained copyright notices in its bundled libffi sources.

## Reproduce collection

Use the release build's environment and exact installed versions. Download code is not executed and archive paths are not extracted into the filesystem.

```powershell
.venv\Scripts\python.exe tools/fetch_dependency_sources.py cryptography==50.0.2 cffi==2.1.1 pycparser==3.12
.venv\Scripts\python.exe tools/fetch_crypto_sources.py --cryptography-version 50.0.2 --cffi-version 2.1.1 --openssl-version 4.0.3
```

Archives remain under `dist/source/dependencies/`; generated notices and their manifest go to `build/legal/crypto-native/`. Review them before copying the three `.txt` files and `crypto-native-sources.json` into `licenses/`. The existing packaging specs and license dialog include the text files. Build a new executable/MSIX after changing notices; previous artifacts do not acquire the new documents retroactively. Preserve and publish the reviewed dependency archives alongside the final application's corresponding source.

## Outstanding review

- Upstream wheel build provenance, compiler/Rust standard-library notices, build flags, patches, and precise linked-code inventory remain unverified. Source-version equality and checksums alone do not establish binary/source equivalence.
- OpenSSL source legal files and CFFI x86/x64 headers were retained; completeness of notices for compiled configurations and other native components needs final review. ARM64, Linux and macOS require separate evidence.
- Qt/PySide/Shiboken, PyMuPDF/MuPDF, Pillow's native image libraries, Python and PyInstaller remain part of the overall release review described in [license and distribution](license-distribution_ja.md). This encryption review does not complete that work or the Store-distribution review.

## Primary sources

- [OpenSSL official source downloads and checksums](https://www.openssl-library.org/source/)
- [cryptography installation and static OpenSSL wheels](https://cryptography.io/en/latest/installation/)
- Package source archives and their legal documents are identified by URL and SHA-256 in the machine-readable record.
