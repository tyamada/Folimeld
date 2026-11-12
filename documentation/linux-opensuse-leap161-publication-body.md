# Folimeld 0.3.5 — openSUSE Leap 16.1 amd64 preview

[日本語](linux-opensuse-leap161-publication-body_ja.md)

This x86_64 RPM was verified in dedicated openSUSE Leap 16.1 WSL2/WSLg environments. These results do not cover conventional desktops, ARM64, or other distributions. Existing Linux 0.3.4, AlmaLinux9, and Fedora44/45 downloads remain available.

Download the RPM and SHA256SUMS.txt into the same directory, verify them, and install:

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo zypper install --allow-unsigned-rpm --no-recommends ./folimeld-0.3.5-1.lp161.x86_64.rpm
folimeld
```

The specified local RPM is unsigned. This option permits that local RPM without disabling signature verification for standard repositories.

409 tests and 67 subtests passed, with 9 skips. The new executable passed PDF rotation, undo/redo, page movement, blank-page insertion/deletion, saving with a Japanese filename containing spaces and reopening through GIO, IBus/Mozc conversion and commit of にほんご to 日本語, and license-dialog display. Password-protected PDF authentication, rotation, saving, saved-file reauthentication and text preservation passed, as did PNG-to-PDF creation, saving, and image-pixel verification.

The dedicated Test environment passed updating from 0.3.3 revision3 to 0.3.5 revision1, offscreen/xcb startup, removal/reinstallation, hash preservation of existing test PDFs and settings, RPM integrity and dependency checks. A fresh minimal installroot passed offscreen startup as UID/GID1000 without development dependencies or recommended CJK fonts. This chroot test does not cover independent WSL boot or IME in the minimal environment.

The matching source commit is `44f76e77c05c0c097be9dc1e8f1de9f8449e6aaa`, verified against all 858 build inputs. The attached source ZIP, RPM-to-source record, third-party notices, dependency-source supplement, and verification records identify this build. Build-time README, CHANGELOG, and preparation-time notice records retain their historical state.

The distributed executable's 209 native entries match 105 entries from official wheels and 104 OS entries mapped to 36 signature-verified source RPMs. Its PyInstaller bootloader also matches the official wheel. Three Virtual Keyboard entries present during analysis are excluded from the distributed executable.

Conventional file-manager interaction, migration from public Ubuntu/Debian 0.3.4, broad input/settings coverage, and reconstruction of every historical wheel build setting remain unverified. The RPM, checksums, and commit are unsigned. These checks are not a reproducible build or license-compliance certification. Synthetic GUI inputs initially produced repeated characters/dialogs and an overlong-filename save error; image import/save passed when retested in a standalone GUI using mouse confirmations. See the verification JSON and KNOWN-LIMITATIONS.txt.

The LZW implementation in LibTIFF includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice.
