#!/usr/bin/env bash
set -euo pipefail
b=${FOLIMELD_BROTLI_BUILD_BASE:?Use a new absolute dependency build directory}
archive=${FOLIMELD_BROTLI_SOURCE_ARCHIVE:?Set the checksum-verified official source archive}
[[ $b == /* && ! -e $b ]]
[[ $(uname -m) == aarch64 ]]
mkdir -p "$b/source" "$b/build"
echo "38f9c17ee36c2e930ce00975b50fcd246a8e5594c1bcf43cd56b14118786b82a  $archive" | sha256sum --check
tar -xzf "$archive" --strip-components=1 -C "$b/source"
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1794528000} TZ=UTC
cmake -S "$b/source" -B "$b/build" -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DCMAKE_SKIP_RPATH=ON -DCMAKE_INSTALL_PREFIX="$b/install" -DCMAKE_INSTALL_LIBDIR=lib
cmake --build "$b/build" --parallel 4
LD_LIBRARY_PATH="$b/build${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ctest --test-dir "$b/build" --parallel 4 --output-on-failure
cmake --install "$b/build"
sha256sum "$b/install/lib/libbrotlicommon.so.1" "$b/install/lib/libbrotlidec.so.1"
