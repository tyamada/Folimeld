# Folimeld 0.3.5 — AlmaLinux 9 amd64 preview

This x86_64 RPM was verified on AlmaLinux 9.8 under WSL2/WSLg. Existing Linux 0.3.4 distributions for Ubuntu/Debian and distributions for other operating systems are retained.

Download the RPM and SHA256SUMS.txt into the same folder, verify the files, and install:

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo dnf install ./folimeld-0.3.5-5.alma9_8.x86_64.rpm
folimeld
```

Verified operations include Japanese PDF display, rotation, Undo/Redo, page moves, blank-page insertion and deletion, Save As with Japanese filenames and reopening, encrypted PDFs, PNG import, and IBus/Mozc input. Upgrades between candidates, preservation of three settings, and GIO opening with isolated XDG/D-Bus settings were also tested. Final revision5 passed upgrade, removal/reinstallation, preservation of test PDFs/settings, non-root startup, and offscreen startup and integrity checks in a fresh minimal-dependency installroot.

Conventional desktops, ARM64, AlmaLinux 10, migration from public Ubuntu/Debian 0.3.4, and arbitrary existing settings remain untested. The minimal-dependency test does not establish independent WSL boot or Japanese GUI/IME operation.

Attachments include the matching Folimeld source ZIP, package-to-source records, third-party notices, and collected dependency-source materials. The locally fixed source commit is `03b14ec8c4410fbc7510aa9bedb27950e78cfc6e`; its 686 candidate inputs were verified. See the attached verification JSON and KNOWN-LIMITATIONS.txt for details.

The RPM, checksums, and source commit are unsigned. Matching the distributed wheels does not independently reconstruct every historical build setting and patch or certify compliance with all license conditions.

The LibTIFF LZW implementation includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice for details.
