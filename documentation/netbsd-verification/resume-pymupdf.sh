#!/bin/sh
set -eu
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LD_LIBRARY_PATH=/usr/pkg/lib
ulimit -c 0
cd /home/folimeld/native-build
source=/home/folimeld/native-build/pymupdf-1.28.2
py=/home/folimeld/Folimeld/.venv-netbsd/bin/python
env -u CXX MUPDF_MAKE=/usr/pkg/bin/gmake CC=cc \
    PYMUPDF_SETUP_SWIG=/usr/pkg/bin/swig4.0 \
    PYMUPDF_SETUP_MUPDF_BUILD="$source/mupdf-1.28.2-source" \
    "$py" -m pip wheel --no-deps --no-build-isolation --no-clean \
    --wheel-dir wheels "$source"
echo PYMUPDF_BUILD_OK
