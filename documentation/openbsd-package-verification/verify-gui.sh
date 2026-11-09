#!/bin/sh
set -eu
export PYTHONPATH=/usr/local/share/folimeld/vendor
python3 - <<'PY'
import hashlib,json,pymupdf
from pathlib import Path
source=Path('/home/folimeld/Folimeld/build/openbsd-verification/gui-manual-after.pdf')
output=Path('/home/folimeld/gui-package-saved.pdf')
with pymupdf.open(source) as a,pymupdf.open(output) as b:
 assert len(a)==len(b)==8
 assert [p.rotation for p in b]==[90,90,0,0,0,0,0,0]
 for i in range(8):
  assert [hashlib.sha256(a.xref_stream(x)).hexdigest() for x in a[i].get_contents()]==[hashlib.sha256(b.xref_stream(x)).hexdigest() for x in b[i].get_contents()]
 record={'pages':8,'rotations':[p.rotation for p in b],'streams_preserved':True,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'pymupdf_module':pymupdf.__file__}
Path('/home/folimeld/openbsd-package/gui-save-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
PY
qpdf --check /home/folimeld/gui-package-saved.pdf
