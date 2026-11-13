# Proposed Folimeld 0.3.5 release for AlmaLinux 9 amd64

Unpublished preparation draft. Do not publish until the attachments have been reviewed and the version finalized.

This x86_64 RPM candidate was tested on AlmaLinux 9.8 under WSL2/WSLg. ARM64, AlmaLinux 10, and a conventional desktop environment are outside this verification scope.

Installation example (using the files distributed after publication):

```sh
sha256sum -c SHA256SUMS.txt
sudo dnf install ./folimeld-0.3.5-5.alma9_8.x86_64.rpm
folimeld
```

Verified operations include displaying Japanese PDFs, rotation, Undo/Redo, page moves, blank-page insertion and deletion, Save As with Japanese filenames and reopening, encrypted PDFs, PNG import, and IBus/Mozc input. Upgrading from a private 0.3.3 candidate, preserving three settings, removing and reinstalling, and opening through GIO with isolated XDG/D-Bus settings also passed. Offscreen startup as a non-root numeric user was checked in a minimal-dependency installroot.

Migration from public Ubuntu/Debian 0.3.4, conventional file-manager operations, booting an independent minimal WSL instance, and arbitrary existing settings remain untested. The minimal-dependency test without the recommended Japanese font does not verify Japanese GUI rendering.

Planned attachments include the RPM, matching Folimeld source ZIP, package-to-source records, third-party notices, collected dependency-source materials, and checksums. Dependency-source coverage and wheel build provenance remain under review. This draft does not claim complete attachments or publication readiness.

The RPM is unsigned. SHA256SUMS.txt checks file consistency; it is not a signature authenticating the publisher.

The LibTIFF LZW implementation includes software developed by the University of California, Berkeley. See the bundled LibTIFF-LZW notice for details.
