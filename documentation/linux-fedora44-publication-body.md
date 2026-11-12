# Folimeld 0.3.5 — Fedora 44 amd64 preview

[日本語](linux-fedora44-publication-body_ja.md)

This x86_64 RPM was verified in dedicated Fedora 44 WSL2/WSLg environments. These results do not cover conventional desktops, ARM64, or other distributions. Existing Linux 0.3.4, Fedora 45 preview, and AlmaLinux preview downloads will remain available.

Download the RPM and SHA256SUMS.txt into the same folder, verify them, and install:

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo dnf install ./folimeld-0.3.5-2.fc44.x86_64.rpm
folimeld
```

409 tests and 67 subtests passed, with 9 skips. Verification covered PDF display, rotation, undo/redo, page movement, blank-page insertion/deletion, saving under a Japanese filename and reopening, password-protected PDF reauthentication, PDF creation from PNG, and Japanese conversion and commit through IBus/Mozc. GIO opening of paths containing Japanese characters and spaces in isolated XDG/D-Bus sessions, and the additional notices in the license dialog, also passed.

Updating to revision2, removal/reinstallation, preservation of six test PDF/configuration files, and startup as a regular user after reinstallation passed. A fresh minimal-dependency installroot passed offscreen startup and consistency checks without Python or build tools. This chroot test does not verify independent WSL boot or Japanese GUI/IME operation in the minimal environment. Migration from public Ubuntu/Debian 0.3.4 packages and arbitrary existing settings remain untested.

Attachments include the matching Folimeld source ZIP, package-to-source record, third-party notices, dependency-source supplement, and verification records. Source commit `293da8abe0459eba5d2a95609a6c3d630c986033` matches all 822 build-time inputs. Frozen build-time sources, including README and CHANGELOG, retain their historical preparation status rather than being rewritten at publication.

The 207 native entries match 105 entries from official wheels and 102 Fedora OS entries mapped to 37 signature-verified source RPMs. The PyInstaller bootloader also matches its official wheel. The RPM, checksums, and source commit are unsigned. These checks do not constitute independent reconstruction of every historical compiler setting and patch, a reproducible build, or license-compliance certification. See the attached verification JSON and KNOWN-LIMITATIONS.txt for details.

The LZW implementation in LibTIFF includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice for details.
