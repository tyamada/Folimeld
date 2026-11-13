#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
[[ $(uname -m) == aarch64 ]]
. /etc/os-release
[[ $ID:$VERSION_ID == fedora:45 ]]
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
# Existing packaging helper expects project/dist. Refuse to replace any prior output.
[[ ! -e dist/folimeld && ! -L dist/folimeld ]]
mkdir -p dist
cp "$FOLIMELD_BUILD_ROOT/dist/folimeld" dist/folimeld
trap 'rm -f dist/folimeld' EXIT
FOLIMELD_LINUX_OUTPUT="$FOLIMELD_BUILD_ROOT/packages" FOLIMELD_RPM_REVISION=1 "$py" tools/package_linux_rpm.py
"$FOLIMELD_BUILD_ROOT/venv/bin/pyi-archive_viewer" -r -b "$FOLIMELD_BUILD_ROOT/dist/folimeld" > "$FOLIMELD_BUILD_ROOT/archive.txt"
! grep -Ei 'virtualkeyboard|qtcore_probe_runtime' "$FOLIMELD_BUILD_ROOT/archive.txt"
git diff --exit-code
sha256sum "$FOLIMELD_BUILD_ROOT/packages/folimeld-0.3.5-1.fc45.aarch64.rpm" "$FOLIMELD_BUILD_ROOT/dist/folimeld"
