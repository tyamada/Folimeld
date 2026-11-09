#!/bin/sh
set -eu
export PATH=/usr/local/bin:/usr/local/sbin:/usr/X11R6/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PYTHONPATH=/usr/local/llvm22/lib/python3.14/site-packages
export LIBCLANG_LIBRARY_FILE=/usr/local/llvm22/lib/libclang.so.0.0
ulimit -c 0
cd /home/folimeld/native-build
py=/home/folimeld/Folimeld/.venv-openbsd/bin/python
env -u CXX PIPCL_SHOW_ENV=0 PYMUPDF_SETUP_SWIG=/usr/local/bin/swig PYMUPDF_SETUP_MUPDF_BUILD=/home/folimeld/native-build/pymupdf-1.28.2/mupdf-1.28.2-source "$py" -m pip wheel -v --no-deps --no-build-isolation --no-clean --wheel-dir wheels ./pymupdf-1.28.2
"$py" -m pip install wheels/pymupdf-1.28.2-*.whl
"$py" -m pip check
