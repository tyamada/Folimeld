#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$(uname -s)" != "Linux" ]; then
  echo "This build script must be run on Linux." >&2
  exit 1
fi

VENV_DIR="${FOLIMELD_LINUX_VENV:-$SCRIPT_DIR/.venv-linux}"
PYTHON_EXE="$VENV_DIR/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

"$PYTHON_EXE" -m pip install --upgrade pip
"$PYTHON_EXE" -m pip install -r requirements.txt pyinstaller
"$PYTHON_EXE" "$SCRIPT_DIR/tools/make_app_icon.py"
"$PYTHON_EXE" -m PyInstaller --noconfirm --clean Folimeld-linux.spec

VERSION="$($PYTHON_EXE -c 'from folimeld import __version__; print(__version__)')"
if command -v dpkg >/dev/null 2>&1; then
  ARCH="$(dpkg --print-architecture)"
else
  case "$(uname -m)" in
    x86_64) ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $(uname -m)" >&2; exit 1 ;;
  esac
fi

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

OUTPUT_DIR="$SCRIPT_DIR/releases/ubuntu"
mkdir -p "$OUTPUT_DIR"
PACKAGE="$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.deb"
dpkg-deb --root-owner-group --build "$PACKAGE_ROOT" "$PACKAGE"

echo
echo "Built standalone executable: dist/folimeld"
echo "Built Ubuntu package: releases/ubuntu/$(basename "$PACKAGE")"
