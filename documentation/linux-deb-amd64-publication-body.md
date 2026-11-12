# Folimeld 0.3.5 — Linux DEB amd64 preview

[日本語](linux-deb-amd64-publication-body_ja.md)

This x86_64 DEB was built on Ubuntu 24.04 and verified in dedicated Ubuntu 24.04.4, Debian 13.6, and Kali Rolling 2026.3 WSL2/WSLg environments. Existing Linux 0.3.4 and published RPM downloads remain available. glibc 2.39 or newer is required.

Download the DEB and SHA256SUMS.txt into the same directory, verify them, and install. Ubuntu also requires its official universe repository.

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo apt install --no-install-recommends ./folimeld_0.3.5_amd64.deb
folimeld
```

409 tests and 67 subtests passed, with 9 skips; ruff passed. All three environments passed updating from their existing versions (Ubuntu/Debian 0.3.4, Kali 0.3.3), offscreen/xcb startup as a regular user, removal/reinstallation, hash preservation of existing test PDFs/settings, dpkg integrity checks, and APT dependency checks. Japanese PDF display, immediate thumbnail rotation, and undo were verified in each GUI.

Ubuntu additionally passed redo, page movement, blank-page insertion/deletion, and saving/reopening a filename containing Japanese characters and a space. The saved PDF retained text, three pages in original order [2,1,3], and rotations [0,90,0]. A minimal chroot created solely from official Ubuntu noble main/universe repositories passed offscreen startup as UID/GID1000 without development dependencies, Python, or recommended CJK fonts. This does not verify independent WSL boot or GUI operation in that minimal environment.

All 870 source inputs match the source ZIP and Git commit byte for byte. The 214 shipped native entries (105 official-wheel files and 109 Ubuntu OS files) were matched, and 61 corresponding Ubuntu source packages were obtained. Older versions unavailable in current official indexes were obtained using signed official Ubuntu Snapshot indexes. InRelease signatures, Sources SHA-256 hashes, and source-file SHA-256 hashes were verified. The PyInstaller bootloader matches its official wheel. Attachments include matching source, third-party notices, two dependency-source supplements, and verification records.

Conventional Linux desktops, ARM64, other distributions, future rolling updates, and broad PDF/image/encryption settings remain unverified. IME conversion, GIO association, image import, and encrypted-PDF GUI tests were not repeated with this new DEB; RPM results do not establish a pass for this DEB. Frozen preparation-time statements about pending audits remain historical records; completed results are in the external verification JSON. The package, checksums, and commit are unsigned. These checks are not a reproducible build or license-compliance certification.

The LZW implementation in LibTIFF includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice.
