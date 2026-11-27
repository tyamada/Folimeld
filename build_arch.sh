#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$(uname -s)" != "Linux" ]; then
  echo "This build script must be run on Arch Linux." >&2
  exit 1
fi
for tool in makepkg python3 tar sha256sum; do
  command -v "$tool" >/dev/null 2>&1 || {
    echo "Arch packaging requires $tool." >&2
    exit 1
  }
done

VERSION="${FOLIMELD_ARCH_VERSION:-$(python3 -c 'from folimeld import __version__; print(__version__)')}"
OUTPUT_DIR="${FOLIMELD_ARCH_OUTPUT:-$SCRIPT_DIR/releases/arch}"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(CDPATH= cd -- "$OUTPUT_DIR" && pwd)"

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/folimeld-arch.XXXXXXXX")"
trap 'rm -rf -- "$WORK_DIR"' EXIT

TARBALL="$WORK_DIR/Folimeld-${VERSION}.tar.gz"
tar -czf "$TARBALL" \
  --transform "s,^,Folimeld-${VERSION}/," \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  folimeld locales assets main.py LICENSE licenses packaging/linux/folimeld.desktop packaging/linux/arch/folimeld-arch-launch

TAR_SHA="$(sha256sum "$TARBALL" | awk '{print $1}')"

sed \
  -e "s|@VERSION@|${VERSION}|g" \
  -e "s|@SOURCE_URL@|Folimeld-${VERSION}.tar.gz|g" \
  -e "s|@SOURCE_SHA256@|${TAR_SHA}|g" \
  "$SCRIPT_DIR/packaging/linux/arch/PKGBUILD.in" > "$WORK_DIR/PKGBUILD"

(
  cd "$WORK_DIR"
  makepkg -f --noconfirm
  makepkg --printsrcinfo > .SRCINFO
)

PKG_FILE="$(ls "$WORK_DIR"/folimeld-"${VERSION}"-1-any.pkg.tar.* | head -n 1)"
PKG_NAME="$(basename "$PKG_FILE")"

if command -v namcap >/dev/null 2>&1; then
  echo "=== namcap PKGBUILD ==="
  namcap "$WORK_DIR/PKGBUILD" || true
  echo "=== namcap package ==="
  namcap "$PKG_FILE" || true
fi

cp "$PKG_FILE" "$OUTPUT_DIR/$PKG_NAME"
cp "$WORK_DIR/PKGBUILD" "$OUTPUT_DIR/PKGBUILD"
cp "$WORK_DIR/.SRCINFO" "$OUTPUT_DIR/.SRCINFO"

echo
echo "Built Arch package: $OUTPUT_DIR/$PKG_NAME"
sha256sum "$OUTPUT_DIR/$PKG_NAME"
