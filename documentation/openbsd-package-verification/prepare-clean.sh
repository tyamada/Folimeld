#!/bin/sh
set -eu
sets=/home/folimeld/openbsd-package/sets
root=/home/folimeld/openbsd-clean
mkdir -p "$sets" "$root"
cd "$sets"
ftp -o SHA256.sig https://cdn.openbsd.org/pub/OpenBSD/8.0/amd64/SHA256.sig
for name in base80.tgz xbase80.tgz xshare80.tgz xfont80.tgz; do
    test -f "$name" || ftp -o "$name" "https://cdn.openbsd.org/pub/OpenBSD/8.0/amd64/$name"
    signify -C -p /etc/signify/openbsd-80-base.pub -x SHA256.sig "$name"
    tar -xzpf "$name" -C "$root"
done
cp /etc/resolv.conf "$root/etc/resolv.conf"
mkdir -p "$root/etc/ssl" "$root/etc/signify" "$root/tmp" "$root/packages"
cp /etc/ssl/cert.pem "$root/etc/ssl/cert.pem"
cp /etc/signify/openbsd-80-pkg.pub "$root/etc/signify/"
echo https://cdn.openbsd.org/pub/OpenBSD > "$root/etc/installurl"
chmod 1777 "$root/tmp"
cd "$root/dev"
sh MAKEDEV std
echo CLEAN_BASE_READY
