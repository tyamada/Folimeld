from pathlib import Path
import base64, hashlib, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
p=Path('build/openbsd-vm')
siglines=(p/'SHA256.sig').read_bytes().splitlines(keepends=True)
sig=base64.b64decode(siglines[1])
key=base64.b64decode((p/'openbsd-80-base.pub').read_bytes().splitlines()[1])
assert sig[:10] == key[:10]
Ed25519PublicKey.from_public_bytes(key[10:]).verify(sig[10:], b''.join(siglines[2:]))
h=hashlib.file_digest((p/'install80.iso').open('rb'),'sha256').hexdigest()
expected=[x.decode().strip().split(' = ')[1] for x in siglines[2:] if x.startswith(b'SHA256 (install80.iso)')][0]
assert h == expected, (h,expected)
r={'signature':'Ed25519 verified','key_source':'https://raw.githubusercontent.com/openbsd/src/master/etc/signify/openbsd-80-base.pub','iso':'install80.iso','sha256':h,'checksum_match':True}
(p/'media-verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
