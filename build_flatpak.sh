#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$(uname -s)" != "Linux" ]; then
  echo "This build script must be run on Linux." >&2
  exit 1
fi

for tool in flatpak flatpak-builder python3; do
  command -v "$tool" >/dev/null 2>&1 || {
    echo "Flatpak packaging requires $tool." >&2
    exit 1
  }
done

FLATPAK_DIR="$SCRIPT_DIR/packaging/linux/flatpak"
APP_ID="io.github.tyamada.Folimeld"

if command -v appstreamcli >/dev/null 2>&1; then
  appstreamcli validate --no-net "$FLATPAK_DIR/${APP_ID}.metainfo.xml"
fi
if command -v desktop-file-validate >/dev/null 2>&1; then
  desktop-file-validate "$FLATPAK_DIR/${APP_ID}.desktop"
fi

BUILD_PYTHON="${FOLIMELD_LINUX_PYTHON:-python3}"
VERSION="${FOLIMELD_FLATPAK_VERSION:-$("$BUILD_PYTHON" -c 'from folimeld import __version__; print(__version__)')}"
RAW_ARCH="$(uname -m)"
case "$RAW_ARCH" in
  x86_64) ARCH="amd64"; FLATPAK_ARCH="x86_64" ;;
  aarch64|arm64) ARCH="arm64"; FLATPAK_ARCH="aarch64" ;;
  *) echo "Unsupported architecture: $RAW_ARCH" >&2; exit 1 ;;
esac

OUTPUT_DIR="${FOLIMELD_FLATPAK_OUTPUT:-$SCRIPT_DIR/releases/flatpak}"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(CDPATH= cd -- "$OUTPUT_DIR" && pwd)"
BUNDLE="$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.flatpak"
if [ -e "$BUNDLE" ] && [ "${FOLIMELD_FLATPAK_OVERWRITE:-0}" != "1" ]; then
  echo "Refusing to overwrite existing bundle: $BUNDLE" >&2
  echo "Set FOLIMELD_FLATPAK_OUTPUT or FOLIMELD_FLATPAK_OVERWRITE=1." >&2
  exit 1
fi

RUNTIME_PY_VER="$(flatpak run --user --command=python3 org.freedesktop.Platform//25.08 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "Freedesktop 25.08 runtime Python: ${RUNTIME_PY_VER} (${FLATPAK_ARCH})"

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/folimeld-flatpak.XXXXXXXX")"
trap 'rm -rf -- "$WORK_DIR"' EXIT

mkdir -p "$WORK_DIR/src" "$WORK_DIR/wheels"
cp -a "$SCRIPT_DIR/folimeld" "$SCRIPT_DIR/locales" "$SCRIPT_DIR/assets" "$SCRIPT_DIR/main.py" "$SCRIPT_DIR/LICENSE" "$WORK_DIR/src/"
if [ -d "$SCRIPT_DIR/licenses" ]; then
  cp -a "$SCRIPT_DIR/licenses" "$WORK_DIR/src/"
fi
# Remove any __pycache__ from staged source
find "$WORK_DIR/src" -name '__pycache__' -type d -exec rm -rf {} +

cp -a "$FLATPAK_DIR/${APP_ID}.yml" "$WORK_DIR/"
cp -a "$FLATPAK_DIR/${APP_ID}.desktop" "$WORK_DIR/"
cp -a "$FLATPAK_DIR/${APP_ID}.metainfo.xml" "$WORK_DIR/"
install -m755 "$FLATPAK_DIR/folimeld-flatpak-launch" "$WORK_DIR/folimeld-flatpak-launch"

# Fetch pinned runtime wheels using the Freedesktop SDK's own pip so platform/glibc/Python tags match exactly.
# Folimeld only uses QtCore/QtGui/QtWidgets (all in PySide6_Essentials), so omit the ~175 MB PySide6_Addons wheel.
flatpak run --user \
  --share=network \
  --filesystem="$WORK_DIR" \
  --filesystem="$SCRIPT_DIR:ro" \
  --command=pip3 \
  org.freedesktop.Sdk//25.08 \
  download \
  --only-binary=:all: \
  -c "$SCRIPT_DIR/constraints-release.txt" \
  -d "$WORK_DIR/wheels" \
  PySide6_Essentials shiboken6 PyMuPDF Pillow cryptography

# Record downloaded wheel inventory and SHA-256
(cd "$WORK_DIR/wheels" && sha256sum *.whl | sort) > "$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.wheels.sha256"

flatpak-builder \
  --user \
  --force-clean \
  --state-dir="$WORK_DIR/state" \
  --arch="$FLATPAK_ARCH" \
  --repo="$WORK_DIR/repo" \
  "$WORK_DIR/build" \
  "$WORK_DIR/${APP_ID}.yml"

flatpak build-bundle \
  --arch="$FLATPAK_ARCH" \
  --runtime-repo="https://dl.flathub.org/repo/flathub.flatpakrepo" \
  "$WORK_DIR/repo" \
  "$BUNDLE" \
  "$APP_ID"

echo
echo "Built Flatpak bundle: $BUNDLE"
sha256sum "$BUNDLE"
