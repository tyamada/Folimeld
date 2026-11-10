#!/bin/sh
# Prepare native dependencies using the recorded NetBSD build procedures.
set -eu
[ "$(uname -s)" = NetBSD ] || exit 1
project=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
work=${NETBSD_BUILD_DIR:-"$project/build/netbsd-native"}
prefix=${NETBSD_NATIVE_PREFIX:-"$project/.venv-netbsd"}
mkdir -p "$work/patches"
cp "$project"/documentation/netbsd-verification/patches/*.patch "$work/patches/"
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export SSL_CERT_FILE=/etc/openssl/certs/ca-certificates.crt
cd "$work"
archive=pyside-setup-everywhere-src-6.11.2.tar.xz
if [ ! -f "$archive" ]; then
    ftp -o "$archive" "https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/$archive"
fi
[ "$(sha256 -q "$archive")" = cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8 ]
if [ ! -d pyside-setup-everywhere-src-6.11.2 ]; then
    tar -xf "$archive"
fi
# Render the preserved verification recipes with paths for this checkout.
python3.12 - "$project" "$work" "$prefix" <<'PY'
from pathlib import Path
import shlex
import sys
project, work, prefix = map(Path, sys.argv[1:])
for name in ('build-pyside.sh', 'build-pymupdf.sh'):
    text = (project / 'documentation/netbsd-verification' / name).read_text()
    text = text.replace('/home/folimeld/Folimeld/.venv-netbsd', str(prefix))
    text = text.replace('/home/folimeld/Folimeld', str(project))
    text = text.replace('/home/folimeld/native-build', str(work))
    text = text.replace('python3.12 -m venv --system-site-packages .venv-netbsd',
                        'python3.12 -m venv --system-site-packages ' + shlex.quote(str(prefix)))
    (work / name).write_text(text)
PY
sh "$work/build-pyside.sh"
sh "$work/build-pymupdf.sh"
"$prefix/bin/python" -m pip install --no-deps --force-reinstall "$work"/wheels/pymupdf-1.28.2-*.whl
