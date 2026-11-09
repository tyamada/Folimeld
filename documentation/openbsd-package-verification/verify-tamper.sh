#!/bin/sh
set -eu
base=/home/folimeld/openbsd-package
python3 - <<'PY'
from pathlib import Path
p=Path('/home/folimeld/openbsd-package/signed/folimeld-0.3.3.tgz')
data=bytearray(p.read_bytes())
data[-16]^=1
Path('/home/folimeld/openbsd-package/tampered-package.tgz').write_bytes(data)
PY
if signify -zV -t pkg -x "$base/tampered-package.tgz" > /dev/null 2> "$base/tampered-signature.txt"; then
 echo 'Unexpectedly accepted a tampered package' >&2
 exit 1
fi
echo TAMPERED_PACKAGE_REJECTED >> "$base/tampered-signature.txt"
cat "$base/tampered-signature.txt"
