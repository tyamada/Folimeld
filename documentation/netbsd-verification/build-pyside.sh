#!/bin/sh
set -eu
[ "$(uname -s)" = NetBSD ] || { echo 'Run this inside the documented NetBSD VM.' >&2; exit 1; }
patch_dir=$(CDPATH= cd -- "$(dirname -- "$0")/patches" && pwd)
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PKG_CONFIG_PATH=/usr/pkg/qt6/lib/pkgconfig:/usr/pkg/lib/pkgconfig
export LD_LIBRARY_PATH=/home/folimeld/Folimeld/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib
ulimit -c 0
cd /home/folimeld/Folimeld
python3.12 -m venv --system-site-packages .venv-netbsd
prefix=/home/folimeld/Folimeld/.venv-netbsd
cd /home/folimeld/native-build
source=pyside-setup-everywhere-src-6.11.2
for patch_name in pyside-helper.patch pyside-modules.patch; do
    if patch -C -f -d "$source" -p0 < "$patch_dir/$patch_name"; then
        patch -f -d "$source" -p0 < "$patch_dir/$patch_name"
    elif ! patch -C -f -R -d "$source" -p0 < "$patch_dir/$patch_name"; then
        echo "Cannot apply: $patch_name" >&2
        exit 1
    fi
done
sed -i 's@#!/bin/bash@#!/usr/pkg/bin/bash@g' "$source/sources/shiboken6/cmake/ShibokenHelpers.cmake"
cmake -S pyside-setup-everywhere-src-6.11.2 -B pyside-build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX="$prefix" \
    -DCMAKE_PREFIX_PATH='/usr/pkg/qt6;/usr/pkg' \
    -DPython_EXECUTABLE="$prefix/bin/python" \
    -DPYTHON_SITE_PACKAGES="$prefix/lib/python3.12/site-packages" \
    -DMODULES='Core;Gui;Widgets' \
    -DCLANG_INSTALL_DIR=/usr/pkg \
    -DLLVM_INSTALL_DIR=/usr/pkg
sed -i 's@#!/bin/bash@#!/usr/pkg/bin/bash@g' pyside-build/.qfp/bin/shiboken_wrapper.sh
cmake --build pyside-build --parallel 4
cmake --install pyside-build
"$prefix/bin/python" -c 'import PySide6; from PySide6.QtWidgets import QApplication; print(PySide6.__version__)'
echo PYSIDE_BUILD_OK
