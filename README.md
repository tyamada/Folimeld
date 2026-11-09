# Folimeld

[English](README.md) | [日本語](README_ja.md)

![Folimeld icon](assets/Folimeld.iconset/icon_128x128.png)

Folimeld is a desktop application for visually rearranging, rotating, inserting, and deleting PDF pages. It supports Windows, macOS, Ubuntu, and Debian, and processes files locally without sending them to external services.

![Folimeld main window](documentation/screenshots/main-window.png)

### Create a PDF from an image folder

Choose “File → Create PDF from image folder…” to list JPEG, PNG, BMP, TIFF, and WebP files directly in a folder. Sort by name, creation time, or modification time in ascending or descending order; the default is natural name order, ascending. Exclude unwanted images. Images are not decoded until you press Load. Each image becomes one page (each multipage TIFF frame becomes a page) in a new unsaved PDF for editing and saving. Choose image-sized pages or A4. Image orientation is applied and transparency is flattened onto white. Image-sized pages use image DPI, falling back to 300 DPI for missing or invalid values. Subfolders and animated WebP are excluded. Unavailable creation times sort last; equal timestamps use ascending name order. Conversion can be cancelled, and failures preserve the current document.


Choose File → Exit to close the app, with a save prompt for unsaved changes. On Windows, the image folder picker provides sidebar shortcuts to configured personal and work OneDrive folders. The initial folder picker displays all file types while accepting folders only.

## Features

- Multi-step Undo and Redo from the Edit menu or toolbar for page operations, properties, and viewing password changes. History remains available after saving and resets when another PDF is opened. PDF data in Undo and Redo history is kept in memory up to a combined 128 MiB; overflow is stored in local temporary files up to a combined 1 GiB. Older history is removed when both limits are exceeded or spilling fails; a single entry larger than the disk limit is not retained. Temporary history is released when the document is closed. Temporary data used during editing and saving, and thumbnails, are outside these limits, and whole-document processing can temporarily increase memory usage.
- Saving shows a progress dialog and compresses and writes the PDF in a separate process. Editing and cancellation are unavailable during saving. Preparing the document for the worker and switching documents after saving remain synchronous.
- Spilled history, temporary save-process input, and intermediate image-conversion PDFs are encrypted, with keys kept out of files and settings. User-selected output PDFs use the selected password settings.
- Rearrange PDF pages using thumbnail previews
- Select, move, rotate, or delete multiple pages at once
- Insert another PDF or a blank page of the same size
- Edit the PDF version, page layout, and binding direction
- Set or remove a password required to open a PDF
- Available in Japanese, English, German, Spanish, French, Korean, Portuguese, and Chinese
- Runs on Windows (both Intel/AMD (x64) and ARM (arm64) editions), macOS, Ubuntu, and Debian

Source execution has been verified on OpenBSD 8.0 / amd64 in a VirtualBox VM with 1 vCPU and 16 GiB RAM. Building the dependencies requires a patch. No distribution package has been created. See the [OpenBSD verification record (Japanese)](documentation/openbsd-verification_ja.md) for setup instructions and the scope of verification.

## Downloads

Only Linux packages are publicly distributed. Windows and macOS binaries remain private for local development and verification. Linux 0.3.3 packages, matching source ZIPs, checksums and build records are available in the [GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3). The download links below now point to that Release. See the [migration plan and implementation record](documentation/linux-release-migration.md). Existing repository download URLs remain available for compatibility.

| OS | Package formats |
| --- | --- |
| Windows 10 / 11 (Intel/AMD (x64) / ARM (arm64)) | EXE / MSIX (binaries private) |
| macOS | `.app` (binaries private) |
| Ubuntu | `.deb` / `.snap` / standalone executable (see each release for supported versions) |
| Debian 13 | `.deb` (amd64 / arm64; basic functionality verified on WSL2) |
| FreeBSD 15.1 / amd64 | Native `.pkg` and matching source (publication pending) |

> [!NOTE]
> Windows and macOS verification artifacts are not added to this public repository or GitHub Releases.

### Direct downloads for Ubuntu / Debian

Version **0.3.3 / x86_64 (amd64)**:

- [Download the x86_64 deb package](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.deb) (Ubuntu 22.04 or later / Debian 13)
- [Download the x86_64 Snap package](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.snap) (requires snapd)
- [SHA-256 checksums](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_SHA256SUMS.txt)
- [Build source snapshots and artifact records](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)

Run the installation command for your chosen package from the download folder.

```bash
# deb package
sudo apt install ./folimeld_0.3.3_amd64.deb

# Snap package
sudo snap install --dangerous ./folimeld_0.3.3_amd64.snap
```

Version **0.3.3 / arm64 (AArch64)**:

- [Download the arm64 deb package](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_arm64.deb) (Ubuntu 22.04 or later / Debian 13)
- [Download the arm64 Snap package](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_arm64.snap) (requires snapd)
- [SHA-256 checksums](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_SHA256SUMS.txt)
- [Build source snapshots and artifact records](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)

```bash
# arm64 deb package
sudo apt install ./folimeld_0.3.3_arm64.deb

# arm64 Snap package
sudo snap install --dangerous ./folimeld_0.3.3_arm64.snap
```

Debian 13 uses the same deb package as Ubuntu. If a minimal installation displays `Fontconfig error: Cannot load default config file`, run `sudo apt install fontconfig-config`. PDF display, page movement, rotation, saving, and reopening have been verified on Debian 13.6 amd64 (WSL2 / WSLg, X11). See the [Debian verification record](documentation/debian-wsl-verification_ja.md) (in Japanese) for details. Installation of the deb package and startup with a PDF have also been verified on arm64 (WSL2).

### FreeBSD source, package, and installation

A native `folimeld-0.3.3_1.pkg` package and matching source have been created for FreeBSD 15.1 / amd64. Installation, GUI launch, saving, removal, and reinstallation have been verified. **Downloads have not been published yet.** Current artifacts are stored locally in `dist/freebsd/`. Follow the [FreeBSD installation and build instructions](documentation/freebsd-install.md) to run from source or build a package. A matching source ZIP, PyMuPDF/MuPDF sources, SHA-256 checksums, and build records are also ready. See the [package verification record (Japanese)](documentation/freebsd-package-verification_ja.md).

On FreeBSD with a configured graphical desktop, run the following as root after obtaining the package. Python, Qt, and other dependencies are installed from the official repository.

```sh
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./folimeld-0.3.3_1.pkg
```

Run `folimeld` or `folimeld /path/to/file.pdf` as a regular user. To uninstall, run `pkg delete folimeld` as root. PyMuPDF/MuPDF 1.28.2, which fixes the form-loading crash, is bundled in the application's private directory without replacing system PyMuPDF. Other FreeBSD versions and CPUs are unverified. See the [GUI verification](documentation/freebsd-gui-verification_ja.md) and [image import, save failure, and load tests](documentation/freebsd-extended-verification_ja.md) (Japanese).

## Basic usage

Open **Help → User guide** or press F1 to view basic operations, settings, and keyboard shortcuts. You can keep the guide open while working on a PDF.

1. Launch Folimeld and select a PDF using **File → Open**.
2. Click a page to select it. Use Ctrl or Shift to select multiple pages.
3. Edit pages using the toolbar, menus, or drag and drop.
4. Export the PDF using **Save** or **Save As**.

Opening a password-protected PDF displays a prompt for the password required to open it.

![Password dialog](documentation/screenshots/password-dialog.png)

### Document settings

The **Details** tab in **Document Properties** lets you change the PDF version and page layout. Selecting `TwoPageLeft` or `TwoPageRight` raises the PDF version to 1.5 if necessary.

### Saved preferences

Under **Settings → Image Size**, choose a thumbnail size of 144, 288, or 432 px for the longer edge (default: 288 px). Changes take effect immediately.

The display language, image size, and last opened folder are saved on your device. PDFs are processed locally. Support purchases in the Windows MSIX edition use Microsoft Store to retrieve product information, check purchase status, and process payments. PDFs are never sent to the Store.

In the Windows MSIX edition, **Help → Support Development…** lets you make a one-time purchase with a supporter icon (once the product is published in the Store). Purchasing adds a supporter icon to the Help menu. PDF editing features are the same whether or not you make a purchase. For developer setup instructions, see [Windows support purchases](documentation/windows-store-purchases_ja.md) (in Japanese).

In the Linux edition, **Help → Support development…** displays information about [GitHub Sponsors](https://github.com/sponsors/tyamada). The button in the dialog opens the support page in your browser. Support is optional, and all features remain available whether or not you contribute.

## Development and contributions

See [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on running from source, testing, and building packages for each operating system. Report bugs and suggest improvements through [Issues](https://github.com/tyamada/Folimeld/issues).

Release history is available in [CHANGELOG.md](CHANGELOG.md).

## License

Folimeld is released under the [GNU Affero General Public License v3.0](LICENSE).

Third-party libraries, including PySide6 and PyMuPDF, are covered by their respective licenses.

The full license texts and third-party notices are available under **Help → Licenses**.
See [Licensing and distribution](documentation/license-distribution_ja.md) (in Japanese) for distribution requirements.
