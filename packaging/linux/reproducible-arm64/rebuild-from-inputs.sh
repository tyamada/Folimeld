#!/bin/bash
set -euo pipefail
root="$HOME/folimeld-fix1-reproducible"
inputs=$(realpath "$1")
implementation=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
commit=0a4e2366255f2f7096fd73a24a1a69f30019371f
test "$(dpkg --print-architecture)" = arm64
. /etc/os-release
test "$ID:$VERSION_ID" = ubuntu:24.04
test ! -e "$root/repo"
test ! -e "$root/output"
apt_packages=()
for package in "$inputs"/apt/*.deb; do
    if [[ ${package##*/} != folimeld_0.3.4_arm64.deb ]]; then
        apt_packages+=("$package")
    fi
done
sudo apt-get -y --no-install-recommends \
    -o Dir::Etc::sourcelist=/dev/null -o Dir::Etc::sourceparts=- \
    install "${apt_packages[@]}"
mkdir -p "$root/inputs" "$root/output"
for file in public-Folimeld-linux.spec Linux-distribution.txt third-party-notices.tar.gz; do
    if [[ "$inputs" != "$root/inputs" ]]; then
        cp "$inputs/$file" "$root/inputs/"
    fi
done
git init "$root/repo"
cp "$inputs/source.shallow" "$root/repo/.git/shallow"
git -C "$root/repo" fetch --no-tags "$inputs/source.bundle" HEAD
git -C "$root/repo" worktree add --detach "$root/source" "$commit"
cmp "$inputs/constraints-release.txt" "$root/source/constraints-release.txt"
export PIP_NO_INDEX=1 PIP_FIND_LINKS="$inputs/wheels" PIP_CONSTRAINT="$inputs/build-dependencies.txt"
bash "$implementation/build-fix1.sh" "$implementation/patches" "$inputs"
cmp "$inputs/build-overlay.patch" "$root/output/build-overlay.patch"
cmp "$inputs/build-dependencies.txt" "$root/output/build-dependencies.txt"
(cd "$root/output" && sha256sum -c SHA256SUMS.txt)
