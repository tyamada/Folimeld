# Folimeld 0.3.5 — openSUSE Tumbleweed 20261110 amd64 preview

[日本語](linux-opensuse-tumbleweed-publication-body_ja.md)

This x86_64 RPM was verified in dedicated WSL2/WSLg Build/Test environments with VERSION_ID=20261110. The results do not cover all Tumbleweed snapshots, conventional desktops, ARM64, or other distributions. Existing Linux 0.3.4, AlmaLinux9, Fedora44/45, and Leap16.1 downloads remain available.

Download the RPM and SHA256SUMS.txt into the same directory, verify them, and install:

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo zypper install --allow-unsigned-rpm --no-recommends ./folimeld-0.3.5-1.tw20261110.x86_64.rpm
folimeld
```

The RPM is unsigned. This option permits only the specified local RPM while retaining standard repository signature checks.

409 tests and 67 subtests passed, with 9 skips. The new executable passed rotation, undo/redo, page movement, blank-page insertion/deletion, Japanese filename saving with spaces and GIO reopening, Mozc conversion/commit of にほんご to 日本語, and license-dialog display. Encrypted PDF authentication, rotation, saving, saved-file rejection of incorrect passwords, reauthentication and text preservation passed, as did image-PDF generation and saving.

The dedicated Test environment passed updating from 0.3.3 revision3 to 0.3.5 revision1, offscreen/xcb startup, removal/reinstallation, hash preservation of existing test PDFs/settings, and RPM/dependency consistency checks. A fresh minimal installroot passed offscreen startup as UID/GID1000 without development dependencies or recommended CJK fonts. This root was built from the regular rolling repositories using chroot; it does not verify independent WSL boot pinned to snapshot 20261110 or GUI/IME in the minimal environment.

The 206 distributed native entries match official wheels or OS-owned package files, with 35 matching signature-verified source RPMs. The PyInstaller bootloader also matches its official wheel. Attachments include the matching source ZIP, RPM-to-source record, third-party notices, dependency-source supplement, and verification records. The source commit and full input-byte comparison are recorded in the verification JSON. Frozen build-time documentation and preparation-time notice statements retain their historical state.

Conventional file-manager interaction, other snapshots, migration from public Ubuntu/Debian 0.3.4, broad input/settings coverage, and reconstruction of every historical wheel build setting remain unverified. The IBus switching command returned 1, but engine queries and actual conversion/commit confirmed operation. WSL systemd user-session warnings were retained without changing global settings. The RPM, checksums, and commit are unsigned. These checks are not a reproducible build or license-compliance certification. See the verification JSON and KNOWN-LIMITATIONS.txt.

The LZW implementation in LibTIFF includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice.
