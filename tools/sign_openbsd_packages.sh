#!/bin/sh
# Secret keys must stay outside the source tree and release directory.
set -eu
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 SECRET_KEY UNSIGNED_DIRECTORY SIGNED_DIRECTORY" >&2
    exit 2
fi
key=$1
input=$(cd "$2" && pwd)
test ! -e "$3"
mkdir -p "$3"
output=$(cd "$3" && pwd)
for package in "$input"/*.tgz; do
    signify -Sz -s "$key" -m "$package" -x "$output/$(basename "$package")"
done
