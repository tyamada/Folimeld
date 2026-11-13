#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
[[ $(uname -s) == Linux && $(dpkg --print-architecture) == arm64 ]]
. /etc/os-release
[[ $ID:$VERSION_ID == ubuntu:24.04 ]]
version=$(python3 -c 'from folimeld import __version__; print(__version__)')
[[ $version == 0.3.5 ]]
: "${FOLIMELD_WHEELHOUSE:?Set an exact, checksum-verified wheel directory}"
: "${FOLIMELD_BUILD_ROOT:?Use an unused absolute output directory}"
[[ $FOLIMELD_BUILD_ROOT == /* && ! -e $FOLIMELD_BUILD_ROOT ]]
mkdir -p "$FOLIMELD_BUILD_ROOT"
python3 -m venv "$FOLIMELD_BUILD_ROOT/venv"
py="$FOLIMELD_BUILD_ROOT/venv/bin/python"
"$py" -m pip install --no-index --find-links "$FOLIMELD_WHEELHOUSE" -r requirements.txt -c constraints-release.txt pyinstaller
"$py" -m pip check
"$py" -m pip freeze > "$FOLIMELD_BUILD_ROOT/build-dependencies.txt"
"$py" -c 'from importlib.metadata import version; assert version("pyinstaller")=="6.22.2"; from PySide6 import QtCore, QtGui, QtWidgets; import pymupdf'
site=$("$py" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
(cd "$site" && git apply --check "$root/packaging/linux-arm64/pyinstaller-6.22.2-base-library-order.patch" && git apply "$root/packaging/linux-arm64/pyinstaller-6.22.2-base-library-order.patch")
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$(git show -s --format=%ct HEAD)} PYTHONHASHSEED=0 TZ=UTC
"$py" tools/make_app_icon.py
"$py" -m PyInstaller --noconfirm --clean --distpath "$FOLIMELD_BUILD_ROOT/dist" --workpath "$FOLIMELD_BUILD_ROOT/pyinstaller" Folimeld-linux.spec
stage="$FOLIMELD_BUILD_ROOT/deb-root"
install -Dm755 "$FOLIMELD_BUILD_ROOT/dist/folimeld" "$stage/usr/bin/folimeld"
install -Dm644 packaging/linux/folimeld.desktop "$stage/usr/share/applications/folimeld.desktop"
install -Dm644 assets/Folimeld.iconset/icon_256x256.png "$stage/usr/share/icons/hicolor/256x256/apps/folimeld.png"
mkdir -p "$stage/DEBIAN"
libc=$(getconf GNU_LIBC_VERSION | cut -d ' ' -f 2)
sed -e "s/@VERSION@/$version/" -e 's/@ARCH@/arm64/' -e "s/@LIBC_VERSION@/$libc/" packaging/linux/control.in > "$stage/DEBIAN/control"
find "$stage" -exec touch -h -d "@$SOURCE_DATE_EPOCH" -- {} +
deb="$FOLIMELD_BUILD_ROOT/folimeld_0.3.5_arm64.deb"
dpkg-deb --root-owner-group --build "$stage" "$deb"
"$py" tools/source_bundle.py --executable "$FOLIMELD_BUILD_ROOT/dist/folimeld" --artifact "$deb"
"$FOLIMELD_BUILD_ROOT/venv/bin/pyi-archive_viewer" -r -b "$FOLIMELD_BUILD_ROOT/dist/folimeld" > "$FOLIMELD_BUILD_ROOT/archive.txt"
! grep -Ei 'virtualkeyboard|qtcore_probe_runtime' "$FOLIMELD_BUILD_ROOT/archive.txt"
file "$FOLIMELD_BUILD_ROOT/dist/folimeld"
sha256sum "$deb" "$FOLIMELD_BUILD_ROOT/dist/folimeld"
