#!/bin/bash
set -euo pipefail
[[ $(uname -m) == aarch64 ]]
. /etc/os-release
[[ $ID == kali ]]
: "${FOLIMELD_CFFI_BUILD_ROOT:?Use a new absolute build directory}"
: "${FOLIMELD_CFFI_SOURCE_ARCHIVE:?Use cffi2.1.1 source archive}"
: "${FOLIMELD_WHEELHOUSE:?Use verified official build wheels}"
[[ $FOLIMELD_CFFI_BUILD_ROOT == /* && ! -e $FOLIMELD_CFFI_BUILD_ROOT ]]
echo "dd31f52ea1086513bb9df30f8fcee9b8918323ae067a3d5b78bc826a000712be  $FOLIMELD_CFFI_SOURCE_ARCHIVE" | sha256sum -c
mkdir -p "$FOLIMELD_CFFI_BUILD_ROOT"
python3 -m venv "$FOLIMELD_CFFI_BUILD_ROOT/venv"
py="$FOLIMELD_CFFI_BUILD_ROOT/venv/bin/python"
"$py" -m pip install --no-index --find-links "$FOLIMELD_WHEELHOUSE" setuptools==84.0.0
# Install libffi-dev3.8.0-2 from the exact signed Kali index before running.
SOURCE_DATE_EPOCH=1794518400 "$py" -m pip wheel --no-build-isolation --no-deps --wheel-dir "$FOLIMELD_CFFI_BUILD_ROOT/wheels" "$FOLIMELD_CFFI_SOURCE_ARCHIVE"
sha256sum "$FOLIMELD_CFFI_BUILD_ROOT"/wheels/*.whl
