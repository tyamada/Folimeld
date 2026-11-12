#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

FORMAT="${1:-deb}"
case "$FORMAT" in
  deb|binary|rpm|suse-rpm|tumbleweed-rpm|alma-rpm) ;;
  --help|-h)
    echo "Usage: $0 [deb|binary|rpm|suse-rpm|tumbleweed-rpm|alma-rpm]"
    echo "Default: deb. binary builds the standalone executable without DEB packaging."
    echo "rpm builds a Fedora-specific RPM on Fedora."
    echo "suse-rpm builds an openSUSE Leap 16.1 RPM on that distribution."
    echo "tumbleweed-rpm builds an RPM for the current Tumbleweed snapshot."
    echo "alma-rpm builds an AlmaLinux 9 RPM on that distribution."
    exit 0 ;;
  *) echo "Unknown build format: $FORMAT (use deb, binary, rpm, suse-rpm, tumbleweed-rpm or alma-rpm)" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [deb|binary|rpm|suse-rpm|tumbleweed-rpm|alma-rpm]" >&2
  exit 2
fi

if [ "$(uname -s)" != "Linux" ]; then
  echo "This build script must be run on Linux." >&2
  exit 1
fi
BUILD_PYTHON="${FOLIMELD_LINUX_PYTHON:-python3}"

if [ "$FORMAT" = deb ]; then
  for tool in dpkg dpkg-deb getconf; do
    command -v "$tool" >/dev/null 2>&1 || {
      echo "DEB packaging requires $tool; use binary for other distributions." >&2
      exit 1
    }
  done
  VERSION="$("$BUILD_PYTHON" -c 'from folimeld import __version__; print(__version__)')"
  ARCH="$(dpkg --print-architecture)"
  OUTPUT_DIR="${FOLIMELD_LINUX_OUTPUT:-$SCRIPT_DIR/releases/ubuntu}"
  mkdir -p "$OUTPUT_DIR"
  OUTPUT_DIR="$(CDPATH= cd -- "$OUTPUT_DIR" && pwd)"
  PACKAGE="$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.deb"
  if [ -e "$PACKAGE" ]; then
    echo "Refusing to overwrite existing package: $PACKAGE" >&2
    echo "Set FOLIMELD_LINUX_OUTPUT to a new candidate directory." >&2
    exit 1
  fi
fi

if [ "$FORMAT" = rpm ]; then
  "$BUILD_PYTHON" "$SCRIPT_DIR/tools/package_linux_rpm.py" --check
fi
if [ "$FORMAT" = suse-rpm ]; then
  "$BUILD_PYTHON" "$SCRIPT_DIR/tools/package_linux_suse_rpm.py" --check
fi
if [ "$FORMAT" = tumbleweed-rpm ]; then
  "$BUILD_PYTHON" "$SCRIPT_DIR/tools/package_linux_tumbleweed_rpm.py" --check
fi
if [ "$FORMAT" = alma-rpm ]; then
  "$BUILD_PYTHON" "$SCRIPT_DIR/tools/package_linux_alma_rpm.py" --check
fi

VENV_DIR="${FOLIMELD_LINUX_VENV:-$SCRIPT_DIR/.venv-linux}"
PYTHON_EXE="$VENV_DIR/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
  echo "Creating Python virtual environment..."
  "$BUILD_PYTHON" -m venv "$VENV_DIR"
fi

"$PYTHON_EXE" -m pip install --upgrade pip
"$PYTHON_EXE" -m pip install -r requirements.txt -c constraints-release.txt pyinstaller
# Import native modules before freezing: PyInstaller can otherwise finish while
# host libraries needed by Qt are missing, leaving incomplete plugin discovery.
"$PYTHON_EXE" -c 'from PySide6 import QtCore, QtGui, QtWidgets; import pymupdf'
"$PYTHON_EXE" "$SCRIPT_DIR/tools/make_app_icon.py"
"$PYTHON_EXE" -m PyInstaller --noconfirm --clean Folimeld-linux.spec

if [ "$FORMAT" = binary ]; then
  echo "Built standalone executable: dist/folimeld"
  echo "Matching source and build records: dist/source/"
  exit 0
fi

if [ "$FORMAT" = rpm ]; then
  "$PYTHON_EXE" "$SCRIPT_DIR/tools/package_linux_rpm.py"
  exit 0
fi
if [ "$FORMAT" = suse-rpm ]; then
  "$PYTHON_EXE" "$SCRIPT_DIR/tools/package_linux_suse_rpm.py"
  exit 0
fi
if [ "$FORMAT" = tumbleweed-rpm ]; then
  "$PYTHON_EXE" "$SCRIPT_DIR/tools/package_linux_tumbleweed_rpm.py"
  exit 0
fi
if [ "$FORMAT" = alma-rpm ]; then
  "$PYTHON_EXE" "$SCRIPT_DIR/tools/package_linux_alma_rpm.py"
  exit 0
fi

VERSION="$("$PYTHON_EXE" -c 'from folimeld import __version__; print(__version__)')"

PACKAGE_ROOT="$(mktemp -d)"
trap 'rm -rf -- "$PACKAGE_ROOT"' EXIT
chmod 755 "$PACKAGE_ROOT"
install -Dm755 "$SCRIPT_DIR/dist/folimeld" "$PACKAGE_ROOT/usr/bin/folimeld"
install -Dm644 "$SCRIPT_DIR/packaging/linux/folimeld.desktop" \
  "$PACKAGE_ROOT/usr/share/applications/folimeld.desktop"
install -Dm644 "$SCRIPT_DIR/assets/Folimeld.iconset/icon_256x256.png" \
  "$PACKAGE_ROOT/usr/share/icons/hicolor/256x256/apps/folimeld.png"
mkdir -p "$PACKAGE_ROOT/DEBIAN"
LIBC_VERSION="$(getconf GNU_LIBC_VERSION | cut -d ' ' -f 2)"
sed -e "s/@VERSION@/$VERSION/" -e "s/@ARCH@/$ARCH/" \
  -e "s/@LIBC_VERSION@/$LIBC_VERSION/" \
  "$SCRIPT_DIR/packaging/linux/control.in" > "$PACKAGE_ROOT/DEBIAN/control"

dpkg-deb --root-owner-group --build "$PACKAGE_ROOT" "$PACKAGE"
"$PYTHON_EXE" tools/source_bundle.py --executable dist/folimeld --artifact "$PACKAGE"

echo
echo "Built standalone executable: dist/folimeld"
echo "Built DEB package: $PACKAGE"
