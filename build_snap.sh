#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$(uname -s)" != Linux ]; then
  echo 'Run this script on Ubuntu 24.04 (or in a matching build environment).' >&2
  exit 1
fi
command -v snapcraft >/dev/null
if [ ! -x dist/folimeld ]; then
  echo 'Run bash build_linux.sh first to create dist/folimeld.' >&2
  exit 1
fi

VERSION="$(python3 -c 'from folimeld import __version__; print(__version__)')"
ARCH="$(dpkg --print-architecture)"
OUTPUT_DIR="$SCRIPT_DIR/releases/ubuntu"
mkdir -p "$OUTPUT_DIR"
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/folimeld-snap.XXXXXXXX")"
trap 'rm -rf -- "$WORK_DIR"' EXIT
mkdir -p "$WORK_DIR/snap/gui" "$WORK_DIR/payload/bin"
install -m755 dist/folimeld "$WORK_DIR/payload/bin/folimeld"
install -m755 packaging/linux/folimeld-snap-launch "$WORK_DIR/payload/bin/folimeld-launch"
install -m644 assets/Folimeld.iconset/icon_256x256.png "$WORK_DIR/snap/gui/icon.png"
sed 's|^Icon=.*|Icon=${SNAP}/meta/gui/icon.png|' \
  packaging/linux/folimeld.desktop > "$WORK_DIR/snap/gui/folimeld.desktop"
sed "s/@VERSION@/$VERSION/" packaging/linux/snapcraft.yaml.in > "$WORK_DIR/snap/snapcraft.yaml"
cd "$WORK_DIR"
snapcraft pack "$@" --output "$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.snap"
"${FOLIMELD_LINUX_VENV:-$SCRIPT_DIR/.venv-linux}/bin/python" "$SCRIPT_DIR/tools/source_bundle.py" \
  --executable "$SCRIPT_DIR/dist/folimeld" \
  --artifact "$OUTPUT_DIR/folimeld_${VERSION}_${ARCH}.snap" \
  --source-dir "$SCRIPT_DIR/dist/source"
echo "Built Snap package: releases/ubuntu/folimeld_${VERSION}_${ARCH}.snap"
