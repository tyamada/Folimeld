#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
[[ $(uname -m) == aarch64 ]]
. /etc/os-release
[[ $ID == kali && $(dpkg --print-architecture) == arm64 ]]
: "${FOLIMELD_BUILD_ROOT:?Use an unused absolute output directory}"
: "${FOLIMELD_WHEELHOUSE:?Set an exact checksum-verified wheel directory}"
[[ $FOLIMELD_BUILD_ROOT == /* && ! -e $FOLIMELD_BUILD_ROOT ]]
[[ $(python3 -c 'from folimeld import __version__; print(__version__)') == 0.3.5 ]]
[[ -z $(git status --porcelain) ]]
mkdir -p "$FOLIMELD_BUILD_ROOT"
python3 -m venv "$FOLIMELD_BUILD_ROOT/venv"
py="$FOLIMELD_BUILD_ROOT/venv/bin/python"
"$py" -m pip install --no-index --find-links "$FOLIMELD_WHEELHOUSE" -r requirements.txt -c constraints-release.txt pyinstaller
"$py" -m pip check
"$py" -m pip freeze > "$FOLIMELD_BUILD_ROOT/build-dependencies.txt"
"$py" -c 'from importlib.metadata import version; assert version("pyinstaller")=="6.22.2"; from PySide6 import QtCore,QtGui,QtWidgets; import pymupdf'
site=$("$py" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
(cd "$site" && git apply --check "$root/packaging/linux/pyinstaller-6.22.2-base-library-order.patch" && git apply "$root/packaging/linux/pyinstaller-6.22.2-base-library-order.patch")
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$(git show -s --format=%ct HEAD)} PYTHONHASHSEED=0 TZ=UTC
"$py" tools/make_app_icon.py
"$py" -m PyInstaller --noconfirm --clean --distpath "$FOLIMELD_BUILD_ROOT/dist" --workpath "$FOLIMELD_BUILD_ROOT/pyinstaller" Folimeld-linux.spec
stage="$FOLIMELD_BUILD_ROOT/deb-root"
mkdir -p "$stage/DEBIAN" "$FOLIMELD_BUILD_ROOT/packages"
install -Dm755 "$FOLIMELD_BUILD_ROOT/dist/folimeld" "$stage/usr/bin/folimeld"
install -Dm644 packaging/linux/folimeld.desktop "$stage/usr/share/applications/folimeld.desktop"
install -Dm644 assets/Folimeld.iconset/icon_256x256.png "$stage/usr/share/icons/hicolor/256x256/apps/folimeld.png"
install -Dm644 LICENSE "$stage/usr/share/doc/folimeld/copyright"
libc=$(getconf GNU_LIBC_VERSION | cut -d ' ' -f2)
sed -e 's/@VERSION@/0.3.5/' -e 's/@ARCH@/arm64/' -e "s/@LIBC_VERSION@/$libc/" packaging/linux/control.in > "$stage/DEBIAN/control"
"$py" - "$FOLIMELD_BUILD_ROOT/dist/folimeld" "$stage/usr/share/doc/folimeld/third-party-notices.tar" <<'PYDOC'
import sys,tarfile,io
from PyInstaller.archive.readers import CArchiveReader
r=CArchiveReader(sys.argv[1])
with tarfile.open(sys.argv[2],'w') as t:
 for n in sorted(r.toc):
  if n=='LICENSE' or n.startswith('licenses/'):
   data=r.extract(n);h=tarfile.TarInfo(n);h.size=len(data);h.mode=0o644;h.mtime=0;t.addfile(h,io.BytesIO(data))
PYDOC
find "$stage" -exec touch -h -d "@$SOURCE_DATE_EPOCH" -- {} +
package="$FOLIMELD_BUILD_ROOT/packages/folimeld_0.3.5_arm64.deb"
dpkg-deb --root-owner-group --build "$stage" "$package"
[[ ! -e dist/folimeld && ! -L dist/folimeld ]]
mkdir -p dist
cp "$FOLIMELD_BUILD_ROOT/dist/folimeld" dist/folimeld
trap 'rm -f dist/folimeld' EXIT
"$py" tools/source_bundle.py --executable dist/folimeld --artifact "$package"
"$FOLIMELD_BUILD_ROOT/venv/bin/pyi-archive_viewer" -r -b "$FOLIMELD_BUILD_ROOT/dist/folimeld" > "$FOLIMELD_BUILD_ROOT/archive.txt"
! grep -Ei 'virtualkeyboard|qtcore_probe_runtime' "$FOLIMELD_BUILD_ROOT/archive.txt"
git diff --exit-code
sha256sum "$package" "$FOLIMELD_BUILD_ROOT/dist/folimeld"
