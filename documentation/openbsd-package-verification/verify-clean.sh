#!/bin/sh
set -eu
exec > /home/folimeld/openbsd-package/clean-verification.txt 2>&1
root=/home/folimeld/openbsd-clean
mount -u -o dev /home
trap 'mount -u -o nodev /home' EXIT
tar -xzpf "$root/var/sysmerge/etc.tgz" -C "$root"
test ! -f "$root/var/sysmerge/xetc.tgz" || tar -xzpf "$root/var/sysmerge/xetc.tgz" -C "$root"
mkdir -p "$root/var/run" "$root/var/log"
(cd "$root/dev" && sh MAKEDEV fd random)
chroot "$root" /sbin/ldconfig /usr/local/lib /usr/X11R6/lib
cp /etc/resolv.conf "$root/etc/resolv.conf"
cp /etc/ssl/cert.pem "$root/etc/ssl/cert.pem"
echo https://cdn.openbsd.org/pub/OpenBSD > "$root/etc/installurl"
mkdir -p "$root/packages" "$root/tmp/smoke-home"
chmod 1777 "$root/tmp"
chmod 777 "$root/tmp/smoke-home"
mount -t cd9660 -o ro /dev/cd0c "$root/packages"
cp /home/folimeld/openbsd-package/signed/*.tgz "$root/tmp/"
install -m 644 /root/.signify/folimeld-80-pkg.pub "$root/etc/signify/folimeld-80-pkg.pub"
cp /home/folimeld/openbsd-package/smoke.py "$root/tmp/smoke.py"
cp /home/folimeld/openbsd-package/release-unsigned/build-record.json "$root/tmp/"
echo INSTALL_SIGNED_PACKAGES
chroot "$root" /usr/bin/env PKG_PATH=/packages:installpath /usr/sbin/pkg_add -I \
    /tmp/folimeld-mupdf-1.28.2.tgz /tmp/folimeld-0.3.3.tgz
echo NONPRIVILEGED_SMOKE
chroot "$root" /usr/bin/su -m nobody -c 'cd /tmp && env HOME=/tmp/smoke-home QT_QPA_PLATFORM=offscreen PYTHONNOUSERSITE=1 PYTHONPATH=/usr/local/share/folimeld/vendor:/usr/local/share/folimeld /usr/local/bin/python3.14 /tmp/smoke.py'
chroot "$root" /usr/local/bin/python3.14 - <<'PY'
import hashlib,json
from pathlib import Path
record=json.loads(Path('/tmp/build-record.json').read_text())
for name,expected in record['payload_files'].items():
    p=Path('/usr/local')/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,name
Path('/tmp/keep-user.pdf').write_bytes(b'user document retained\n')
Path('/tmp/smoke-home/.config').mkdir(exist_ok=True)
Path('/tmp/smoke-home/.config/keep-setting').write_text('retained')
print('PAYLOAD_HASHES_OK',len(record['payload_files']))
print('DEVELOPMENT_CHECKOUT_ABSENT',not Path('/home/folimeld/Folimeld').exists())
print('COMPILER_ABSENT',not Path('/usr/bin/cc').exists())
PY
echo REMOVE_AND_REINSTALL
chroot "$root" /usr/sbin/pkg_delete folimeld folimeld-mupdf
test ! -e "$root/usr/local/bin/folimeld"
test -e "$root/tmp/keep-user.pdf"
test -e "$root/tmp/smoke-home/.config/keep-setting"
chroot "$root" /usr/bin/env PKG_PATH=/packages:installpath /usr/sbin/pkg_add -I \
    /tmp/folimeld-mupdf-1.28.2.tgz /tmp/folimeld-0.3.3.tgz
chroot "$root" /usr/bin/su -m nobody -c 'cd /tmp && env HOME=/tmp/smoke-home QT_QPA_PLATFORM=offscreen PYTHONNOUSERSITE=1 PYTHONPATH=/usr/local/share/folimeld/vendor:/usr/local/share/folimeld /usr/local/bin/python3.14 /tmp/smoke.py'
echo CLEAN_VERIFICATION_PASSED
