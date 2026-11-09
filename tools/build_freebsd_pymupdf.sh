#!/bin/sh
# Build the PyMuPDF version required for safe widget reading on FreeBSD.
set -eu

if [ "$(uname -s)" != "FreeBSD" ]; then
    echo "This script must be run on FreeBSD." >&2
    exit 1
fi

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
WORK_DIR="${FOLIMELD_FREEBSD_PYMUPDF_BUILD:-$REPO_ROOT/build/freebsd-pymupdf}"
CLANG_DIR="${FOLIMELD_FREEBSD_CLANG_LIBRARY_DIR:-/usr/local/llvm19/lib}"
BOOTSTRAP_PYTHON="${FOLIMELD_FREEBSD_PYTHON:-python3.12}"

for tool in gmake swig pkg-config cc patch; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Missing $tool. Install gmake, swig, pkgconf, and llvm19 first." >&2
        exit 1
    fi
done
if [ ! -f "$CLANG_DIR/libclang.so" ]; then
    echo "libclang.so not found in $CLANG_DIR; install llvm19." >&2
    exit 1
fi

mkdir -p "$WORK_DIR"
WORK_DIR="$(CDPATH= cd -- "$WORK_DIR" && pwd)"
PYTHON_EXE="$WORK_DIR/.venv/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
    "$BOOTSTRAP_PYTHON" -m venv "$WORK_DIR/.venv"
fi
"$PYTHON_EXE" -m pip install \
    pip==26.3 setuptools==84.2.1 wheel==0.48.0 pipcl==13 clang==19.1.7

"$PYTHON_EXE" - "$WORK_DIR" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
import tarfile
import urllib.request

root = Path(sys.argv[1])


def fetch(url, path, expected):
    if not path.exists():
        partial = path.with_name(path.name + '.part')
        with urllib.request.urlopen(url, timeout=60) as response, partial.open('wb') as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
        if hashlib.sha256(partial.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'Source checksum mismatch: {partial}')
        partial.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError(f'Source checksum mismatch: {path}')


sdist = root / 'pymupdf-1.28.2.tar.gz'
if not sdist.exists():
    with urllib.request.urlopen('https://pypi.org/pypi/PyMuPDF/1.28.2/json', timeout=60) as response:
        metadata = json.load(response)
    source_url = next(item['url'] for item in metadata['urls'] if item['packagetype'] == 'sdist')
else:
    source_url = None
fetch(source_url, sdist, '5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249')
with tarfile.open(sdist) as archive:
    archive.extractall(root, filter='data')
source = root / 'pymupdf-1.28.2'
engine = source / 'mupdf-1.28.2-source.tar.gz'
fetch('https://mupdf.com/downloads/archive/mupdf-1.28.2-source.tar.gz', engine,
      '44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156')
with tarfile.open(engine) as archive:
    archive.extractall(source, filter='data')
PY

SOURCE_DIR="$WORK_DIR/pymupdf-1.28.2"
ENGINE_DIR="$SOURCE_DIR/mupdf-1.28.2-source"
patch -d "$ENGINE_DIR" -p1 < "$REPO_ROOT/packaging/freebsd/pymupdf-1.28.2-freebsd.patch"
mkdir -p "$WORK_DIR/wheels"
# Upstream appends its BSD compiler default; do not duplicate an existing CXX.
env -u CXX MUPDF_MAKE="$(command -v gmake)" CC=cc \
    LD_LIBRARY_PATH="$CLANG_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    PYMUPDF_SETUP_SWIG="$(command -v swig)" PYMUPDF_SETUP_MUPDF_BUILD="$ENGINE_DIR" \
    "$PYTHON_EXE" -m pip wheel --no-deps --no-build-isolation --no-clean \
    --wheel-dir "$WORK_DIR/wheels" "$SOURCE_DIR"
"$PYTHON_EXE" -m pip freeze > "$WORK_DIR/build-requirements.txt"
sha256 "$WORK_DIR"/wheels/pymupdf-1.28.2-*.whl
