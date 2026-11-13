#!/bin/bash
set -euxo pipefail
root="$HOME/folimeld-fix1-reproducible"
patch_dir=$(cd -- "$1" && pwd)
inputs=$(cd -- "$2" && pwd)
commit=0a4e2366255f2f7096fd73a24a1a69f30019371f
version=0.3.4+fix1
cd "$root/source"
test "$(git rev-parse HEAD)" = "$commit"
test -z "$(git status --porcelain)"
test "$(dpkg --print-architecture)" = arm64
SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$(git show -s --format=%ct HEAD)}
if [[ ! "$SOURCE_DATE_EPOCH" =~ ^[0-9]{1,10}$ ]] || (( 10#$SOURCE_DATE_EPOCH > 4294967295 )); then
    printf '%s\n' 'SOURCE_DATE_EPOCH must be an unsigned 32-bit Unix timestamp' >&2
    exit 2
fi
export SOURCE_DATE_EPOCH=$((10#$SOURCE_DATE_EPOCH))
export TZ=UTC
export PYTHONHASHSEED=0
normalize_mtimes() {
    find "$1" -exec touch -h -d "@$SOURCE_DATE_EPOCH" -- {} +
}
stage=$(mktemp -d "$root/stage.XXXXXXXX")
out="$root/output"
python3 -m venv "$stage/venv"
py="$stage/venv/bin/python"
"$py" -m pip install --disable-pip-version-check -r requirements.txt -c constraints-release.txt pyinstaller
"$py" -m pip check
"$py" -m pip freeze > "$out/build-dependencies.txt"
"$py" -c 'from importlib.metadata import version; assert version("pyinstaller") == "6.22.2"'
site_packages=$("$py" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
(
    cd "$site_packages"
    git apply --check "$patch_dir/pyinstaller-6.22.2-base-library-order.patch"
    git apply "$patch_dir/pyinstaller-6.22.2-base-library-order.patch"
)
git apply --check "$patch_dir/source-bundle.patch"
git apply "$patch_dir/source-bundle.patch"
cp "$root/inputs/public-Folimeld-linux.spec" Folimeld-linux.spec
sed -i 's/^__version__ = "0.3.3"$/__version__ = "0.3.4+fix1"/' folimeld/__init__.py
git diff -- Folimeld-linux.spec folimeld/__init__.py > "$out/build-overlay.patch"
git status --short
"$py" -c 'from folimeld import __version__; assert __version__ == "0.3.4+fix1"'
"$py" -m PyInstaller --noconfirm --clean Folimeld-linux.spec
"$stage/venv/bin/pyi-archive_viewer" -r -b dist/folimeld > "$out/archive-arm64.txt"
if grep -Ei 'virtualkeyboard|qtcore_probe_runtime' "$out/archive-arm64.txt"; then exit 1; fi
deb_template="$inputs/folimeld_0.3.4_arm64.deb"
snap_template="$inputs/folimeld_0.3.4_arm64.snap"
printf '%s\n' '33f5fbc490f189330032be6f33be267d6d1706e46a1c595de814f1b942e78731  folimeld_0.3.4_arm64.deb' '2467427c2c7e68b9c3082a8aee2ee257adfeccd231f47b8b19e97a76164adc4f  folimeld_0.3.4_arm64.snap' | (cd "$inputs" && sha256sum -c)
test "$(dpkg-deb -f "$deb_template" Architecture)" = arm64
test "$(dpkg-deb -f "$deb_template" Package)" = folimeld
test "$(dpkg-deb -f "$deb_template" Version)" = 0.3.4
dpkg-deb -R "$deb_template" "$stage/deb"
install -m755 dist/folimeld "$stage/deb/usr/bin/folimeld"
install -Dm644 "$root/inputs/Linux-distribution.txt" "$stage/deb/usr/share/doc/folimeld/Linux-distribution.txt"
install -Dm644 "$root/inputs/third-party-notices.tar.gz" "$stage/deb/usr/share/doc/folimeld/third-party-notices.tar.gz"
sed -i "s/^Version: .*/Version: $version/" "$stage/deb/DEBIAN/control"
if test -f "$stage/deb/DEBIAN/md5sums"; then
    (cd "$stage/deb" && find usr -type f -print0 | sort -z | xargs -0 md5sum > DEBIAN/md5sums)
fi
deb="$out/folimeld_${version}_arm64.deb"
normalize_mtimes "$stage/deb"
dpkg-deb --root-owner-group --build "$stage/deb" "$deb"
dpkg-deb --extract "$deb" "$stage/deb-check"
cmp dist/folimeld "$stage/deb-check/usr/bin/folimeld"
unsquashfs -no-progress -d "$stage/snap" "$snap_template"
grep -Fx 'name: folimeld' "$stage/snap/meta/snap.yaml"
grep -Fx 'confinement: strict' "$stage/snap/meta/snap.yaml"
install -m755 dist/folimeld "$stage/snap/bin/folimeld"
install -Dm644 "$root/inputs/Linux-distribution.txt" "$stage/snap/usr/share/doc/folimeld/Linux-distribution.txt"
install -Dm644 "$root/inputs/third-party-notices.tar.gz" "$stage/snap/usr/share/doc/folimeld/third-party-notices.tar.gz"
sed -i "s/^version: .*/version: $version/" "$stage/snap/meta/snap.yaml"
snap pack --check-skeleton "$stage/snap"
snap="$out/folimeld_${version}_arm64.snap"
normalize_mtimes "$stage/snap"
# Explicit SquashFS timestamp flags are used in place of its environment default.
env -u SOURCE_DATE_EPOCH mksquashfs "$stage/snap" "$snap" \
    -noappend -all-root -comp xz -processors 4 \
    -mkfs-time "$SOURCE_DATE_EPOCH" -all-time "$SOURCE_DATE_EPOCH"
unsquashfs -cat "$snap" bin/folimeld | cmp - dist/folimeld
"$py" tools/source_bundle.py --executable dist/folimeld --artifact "$deb"
"$py" tools/source_bundle.py --executable dist/folimeld --artifact "$snap"
cp dist/source/* "$out/"
{
 dpkg-deb -f "$deb" Package Version Architecture
 unsquashfs -cat "$snap" meta/snap.yaml | sed -n '1,65p'
 file dist/folimeld
 readelf -h dist/folimeld | grep 'Machine:'
 sha256sum dist/folimeld
 stat -c '%s %n' "$deb" "$snap"
 sha256sum "$deb" "$snap"
} > "$out/static-check.log"
(cd "$out"; sha256sum -- *.deb *.snap) > "$out/SHA256SUMS.txt"
