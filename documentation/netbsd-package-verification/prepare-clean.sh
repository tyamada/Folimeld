#!/bin/sh
set -eu
root=/home/folimeld/netbsd-clean
sets=/home/folimeld/netbsd-sets
cd "$sets"
for name in base etc xbase xetc xfont; do
    actual=$(sha512 -q "$name.tar.xz")
    expected=$(sed -n "s/^SHA512 ($name.tar.xz) = //p" SHA512)
    [ -n "$expected" ] && [ "$actual" = "$expected" ]
    tar -xpf "$name.tar.xz" -C "$root"
done
cd "$root/dev"
sh MAKEDEV std
mkdir -p "$root/usr/pkg" "$root/tmp" "$root/etc/ssl/certs"
chmod 1777 "$root/tmp"
cp /etc/resolv.conf "$root/etc/resolv.conf"
cp /etc/openssl/certs/ca-certificates.crt "$root/etc/ssl/certs/ca-certificates.crt"
cp /home/folimeld/netbsd-release/folimeld-0.3.3.tgz "$root/tmp/"
PKG_PATH=https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/x86_64/11.0_2026Q3/All \
    /usr/pkg/sbin/pkg_add -P "$root" "$root/tmp/folimeld-0.3.3.tgz"
PKG_PATH=https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/x86_64/11.0_2026Q3/All \
    /usr/pkg/sbin/pkg_add -P "$root" pkg_install
