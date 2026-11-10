#!/bin/sh
# Run as a regular user on OpenBSD 8.0 amd64 or arm64; pass verified upstream archives.
set -eu
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 DEPENDENCY_SOURCE_DIRECTORY NEW_WORK_DIRECTORY OUTPUT_DIRECTORY" >&2
    exit 2
fi
sources=$(cd "$1" && pwd)
work=$2
output=$3
test ! -e "$work"
mkdir -p "$work" "$output"
work=$(cd "$work" && pwd)
output=$(cd "$output" && pwd)
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PYTHONPATH=/usr/local/llvm22/lib/python3.14/site-packages
export LIBCLANG_LIBRARY_FILE=/usr/local/llvm22/lib/libclang.so.0.0
python3 -m venv --system-site-packages "$work/venv"
py=$work/venv/bin/python
"$py" -m pip install pipcl==13
"$py" - "$sources" "$work" <<'PY'
import hashlib
from pathlib import Path
import sys
import tarfile
sources, work = map(Path, sys.argv[1:])
archives = {
    'pymupdf-1.28.2.tar.gz': '5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249',
    'mupdf-1.28.2-source.tar.gz': '44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156',
}
for name, expected in archives.items():
    archive = sources / name
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
        raise ValueError(f'Source checksum mismatch: {name}')
    destination = work / 'pymupdf-1.28.2' if name.startswith('mupdf-') else work
    with tarfile.open(archive) as bundle:
        bundle.extractall(destination, filter='data')
PY
patch -d "$work/pymupdf-1.28.2/mupdf-1.28.2-source" -p1 \
    < "$script_dir/../packaging/openbsd/mupdf-llvm22-definition.patch"
env -u CXX PIPCL_SHOW_ENV=0 PYMUPDF_SETUP_SWIG=/usr/local/bin/swig \
    PYMUPDF_SETUP_MUPDF_BUILD="$work/pymupdf-1.28.2/mupdf-1.28.2-source" \
    "$py" -m pip wheel --no-deps --no-build-isolation --wheel-dir "$output" \
    "$work/pymupdf-1.28.2"
sha256 "$output"/*.whl
