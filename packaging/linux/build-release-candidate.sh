#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
test -z "$(git status --porcelain)"
out="$(realpath "$1")"
lock="$(realpath "$2")"
notices="$(realpath "$3")"
deb_template="$(realpath "$4")"
snap_template="${5:-}"
arch="$(dpkg --print-architecture)"
case "$arch" in amd64|arm64) ;; *) exit 2 ;; esac
test "$(dpkg-deb -f "$deb_template" Architecture)" = "$arch"
test "$(dpkg-deb -f "$deb_template" Package)" = folimeld
test "$(dpkg-deb -f "$deb_template" Version)" = 0.3.4
test ! -e "$out/folimeld_0.3.4_$arch.deb"
test -z "$snap_template" || test ! -e "$out/folimeld_0.3.4_$arch.snap"
stage="$(mktemp -d "$HOME/folimeld-release-$arch.XXXXXXXX")"
python3 -m venv "$stage/venv"
py="$stage/venv/bin/python"
"$py" -m pip install --disable-pip-version-check -r "$lock"
mkdir -p build
"$py" tools/write_version_info.py build/version_info.txt
test "$("$py" -c 'from folimeld import __version__; print(__version__)')" = 0.3.4
"$py" -m PyInstaller --noconfirm --clean Folimeld-linux.spec
"$stage/venv/bin/pyi-archive_viewer" -r -b dist/folimeld > "$out/archive-$arch.txt"
if grep -Ei 'virtualkeyboard|qtcore_probe_runtime' "$out/archive-$arch.txt"; then exit 1; fi

dpkg-deb --raw-extract "$deb_template" "$stage/deb"
install -m755 dist/folimeld "$stage/deb/usr/bin/folimeld"
install -Dm644 licenses/Linux-distribution.txt "$stage/deb/usr/share/doc/folimeld/Linux-distribution.txt"
install -Dm644 "$notices" "$stage/deb/usr/share/doc/folimeld/third-party-notices.tar.gz"
deb="$out/folimeld_0.3.4_$arch.deb"
dpkg-deb --root-owner-group --build "$stage/deb" "$stage/candidate.deb"
dpkg-deb --extract "$stage/candidate.deb" "$stage/deb-check"
cmp dist/folimeld "$stage/deb-check/usr/bin/folimeld"
install -m644 "$stage/candidate.deb" "$deb"
"$py" tools/source_bundle.py --executable dist/folimeld --artifact "$deb"

if [[ -n "$snap_template" ]]; then
    test "$arch" = arm64
    unsquashfs -no-progress -d "$stage/snap" "$snap_template"
    grep -Fx 'name: folimeld' "$stage/snap/meta/snap.yaml"
    grep -E '^version: .*0\.3\.4' "$stage/snap/meta/snap.yaml"
    grep -Fx 'confinement: strict' "$stage/snap/meta/snap.yaml"
    install -m755 dist/folimeld "$stage/snap/bin/folimeld"
    install -Dm644 licenses/Linux-distribution.txt "$stage/snap/usr/share/doc/folimeld/Linux-distribution.txt"
    install -Dm644 "$notices" "$stage/snap/usr/share/doc/folimeld/third-party-notices.tar.gz"
    mksquashfs "$stage/snap" "$stage/candidate.snap" -noappend -all-root -comp xz -processors 4
    unsquashfs -cat "$stage/candidate.snap" bin/folimeld | cmp - dist/folimeld
    snap="$out/folimeld_0.3.4_$arch.snap"
    install -m644 "$stage/candidate.snap" "$snap"
    "$py" tools/source_bundle.py --executable dist/folimeld --artifact "$snap"
fi
cp dist/source/* "$out/"
(cd "$out"; sha256sum folimeld_0.3.4_*) > "$out/SHA256SUMS-$arch.txt"
printf '%s\n' "$stage" > "$out/build-stage-$arch.txt"
