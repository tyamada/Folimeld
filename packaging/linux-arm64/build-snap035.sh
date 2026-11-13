#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
: "${FOLIMELD_SNAP_TEMPLATE:?Set the verified ARM64 fix1 Snap template}"
: "${FOLIMELD_BUILD_ROOT:?Use an unused absolute output directory}"
printf '%s  %s\n' b1df00de5554b65757ab643a08ad191dd04532fb96d4d548ff9e9d8b15844b53 "$FOLIMELD_SNAP_TEMPLATE" | sha256sum -c
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$(git show -s --format=%ct HEAD)}
[[ $SOURCE_DATE_EPOCH =~ ^[0-9]{1,10}$ && $SOURCE_DATE_EPOCH -le 4294967295 ]]
export TZ=UTC PYTHONHASHSEED=0
# Rebuild the executable in a fresh venv using the same reviewed ARM64 pipeline.
# The intermediate DEB is not a publication candidate in this workflow.
bash packaging/linux-arm64/build-deb035.sh
stage="$FOLIMELD_BUILD_ROOT/snap-root"
unsquashfs -no-progress -d "$stage" "$FOLIMELD_SNAP_TEMPLATE"
grep -Fx 'name: folimeld' "$stage/meta/snap.yaml"
grep -Fx 'confinement: strict' "$stage/meta/snap.yaml"
grep -Fx 'base: core24' "$stage/meta/snap.yaml"
install -m755 "$FOLIMELD_BUILD_ROOT/dist/folimeld" "$stage/bin/folimeld"
install -m755 packaging/linux/folimeld-snap-launch "$stage/bin/folimeld-launch"
install -m644 assets/Folimeld.iconset/icon_256x256.png "$stage/meta/gui/icon.png"
sed 's|^Icon=.*|Icon=${SNAP}/meta/gui/icon.png|' packaging/linux/folimeld.desktop > "$stage/meta/gui/folimeld.desktop"
sed -i 's/^version: .*/version: 0.3.5/' "$stage/meta/snap.yaml"
# Keep the prior dependency notices and add all notices from the current executable.
"$FOLIMELD_BUILD_ROOT/venv/bin/python" - "$FOLIMELD_BUILD_ROOT/dist/folimeld" "$stage/usr/share/doc/folimeld/current-executable-notices.tar.gz" <<'PY'
from PyInstaller.archive.readers import CArchiveReader
import sys,tarfile,io,gzip
r=CArchiveReader(sys.argv[1])
with open(sys.argv[2],'wb') as out,gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as t:
 for n in sorted(r.toc):
  if n=='LICENSE' or n.startswith('licenses/'):
   b=r.extract(n);h=tarfile.TarInfo(n);h.size=len(b);h.mtime=0;h.mode=0o644;t.addfile(h,io.BytesIO(b))
PY
printf '%s\n' 'Folimeld 0.3.5 ARM64 strict Snap preview. Exact application source, third-party source correspondence, SHA-256 and limitations accompany the GitHub Release linux-snap-arm64-v0.3.5. Original dependency notices are retained; current executable notices are provided alongside them.' > "$stage/usr/share/doc/folimeld/Linux-distribution.txt"
snap pack --check-skeleton "$stage"
find "$stage" -exec touch -h -d "@$SOURCE_DATE_EPOCH" -- {} +
snap="$FOLIMELD_BUILD_ROOT/folimeld_0.3.5_arm64.snap"
env -u SOURCE_DATE_EPOCH mksquashfs "$stage" "$snap" -noappend -all-root -comp xz -processors 4 -mkfs-time "$SOURCE_DATE_EPOCH" -all-time "$SOURCE_DATE_EPOCH"
unsquashfs -cat "$snap" bin/folimeld | cmp - "$FOLIMELD_BUILD_ROOT/dist/folimeld"
"$FOLIMELD_BUILD_ROOT/venv/bin/python" tools/source_bundle.py --executable "$FOLIMELD_BUILD_ROOT/dist/folimeld" --artifact "$snap"
git diff --exit-code
sha256sum "$snap" "$FOLIMELD_BUILD_ROOT/dist/folimeld"
