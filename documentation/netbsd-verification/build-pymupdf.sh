#!/bin/sh
set -eu
[ "$(uname -s)" = NetBSD ] || { echo 'Run this inside the documented NetBSD VM.' >&2; exit 1; }
patch_dir=$(CDPATH= cd -- "$(dirname -- "$0")/patches" && pwd)
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LD_LIBRARY_PATH=/usr/pkg/lib
ulimit -c 0
cd /home/folimeld/Folimeld
python3.12 -m venv --system-site-packages .venv-netbsd
py=/home/folimeld/Folimeld/.venv-netbsd/bin/python
"$py" -m pip install pipcl==13 clang==21.1.7
apply_checked() {
    directory=$1
    patch_file=$2
    if patch -C -f -d "$directory" -p0 < "$patch_file"; then
        patch -f -d "$directory" -p0 < "$patch_file"
    elif patch -C -f -R -d "$directory" -p0 < "$patch_file"; then
        echo "Already applied: $patch_file"
    else
        echo "Cannot apply: $patch_file" >&2
        exit 1
    fi
}
site=$($py -c 'import pathlib,pipcl; print(pathlib.Path(pipcl.__file__).parent.parent)')
apply_checked "$site" "$patch_dir/pipcl-netbsd-suffix.patch"
cd /home/folimeld/native-build
"$py" - <<'PY'
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request

def fetch(url, path, expected):
    path = Path(path)
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as response, path.open('wb') as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError(f'Hash mismatch: {path}')

with urllib.request.urlopen('https://pypi.org/pypi/PyMuPDF/1.28.2/json', timeout=60) as response:
    metadata = json.load(response)
url = next(item['url'] for item in metadata['urls'] if item['packagetype'] == 'sdist')
fetch(url, 'pymupdf-1.28.2.tar.gz', '5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249')
with tarfile.open('pymupdf-1.28.2.tar.gz') as archive:
    archive.extractall(filter='data')
source = Path('pymupdf-1.28.2')
engine = source / 'mupdf-1.28.2-source.tar.gz'
fetch('https://mupdf.com/downloads/archive/mupdf-1.28.2-source.tar.gz', engine,
      '44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156')
with tarfile.open(engine) as archive:
    archive.extractall(source, filter='data')
PY
source=/home/folimeld/native-build/pymupdf-1.28.2
for patch_name in mupdf-sha2.patch mupdf-tesseract-endian.patch mupdf-netbsd-link.patch; do
    apply_checked "$source/mupdf-1.28.2-source" "$patch_dir/$patch_name"
done
mkdir -p wheels
env -u CXX MUPDF_MAKE=/usr/pkg/bin/gmake CC=cc \
    PYMUPDF_SETUP_SWIG=/usr/pkg/bin/swig4.0 \
    PYMUPDF_SETUP_MUPDF_BUILD="$source/mupdf-1.28.2-source" \
    "$py" -m pip wheel --no-deps --no-build-isolation --no-clean \
    --wheel-dir wheels "$source"
echo PYMUPDF_BUILD_OK
