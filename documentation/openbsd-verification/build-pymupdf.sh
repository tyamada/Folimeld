#!/bin/sh
set -eu
export PATH=/usr/local/bin:/usr/local/sbin:/usr/X11R6/bin:/usr/bin:/bin:/usr/sbin:/sbin
ulimit -c 0
export PYTHONPATH=/usr/local/llvm22/lib/python3.14/site-packages
export LIBCLANG_LIBRARY_FILE=/usr/local/llvm22/lib/libclang.so.0.0
cd /home/folimeld/Folimeld
python3 -m venv --system-site-packages .venv-openbsd
py=/home/folimeld/Folimeld/.venv-openbsd/bin/python
"$py" -m pip install pipcl==13
cd /home/folimeld/native-build
"$py" - <<'PY'
import hashlib,tarfile
from pathlib import Path
for name,expected in [('pymupdf-1.28.2.tar.gz','5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249'),('mupdf-1.28.2-source.tar.gz','44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156')]:
 p=Path(name)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
 if name.startswith('mupdf-'):
  dest=Path('pymupdf-1.28.2')
 else:dest=Path('.')
 with tarfile.open(p) as a:a.extractall(dest,filter='data')
PY
patch -d /home/folimeld/native-build/pymupdf-1.28.2/mupdf-1.28.2-source -p1 < /home/folimeld/mupdf-llvm22-definition.patch
mkdir -p wheels
env -u CXX PIPCL_SHOW_ENV=0 PYMUPDF_SETUP_SWIG=/usr/local/bin/swig PYMUPDF_SETUP_MUPDF_BUILD=/home/folimeld/native-build/pymupdf-1.28.2/mupdf-1.28.2-source "$py" -m pip wheel --no-deps --no-build-isolation --no-clean --wheel-dir wheels ./pymupdf-1.28.2
"$py" -m pip install wheels/pymupdf-1.28.2-*.whl
"$py" -m pip check
