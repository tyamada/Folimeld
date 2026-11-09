"""Read-only comparison of GUI-saved PDFs with disposable source fixtures."""
import hashlib
import json
from pathlib import Path

import pymupdf as fitz


def contents(document, page):
    return [hashlib.sha256(document.xref_stream(xref)).hexdigest()
            for xref in page.get_contents()]


out = Path("build/netbsd-verification")
fixture = json.loads((out / "fixtures.json").read_text(encoding="utf-8"))
source_path = Path(fixture["source"])
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == fixture["source_sha256"]
assert hashlib.sha256((out / "source.pdf").read_bytes()).hexdigest() == fixture["source_sha256"]
destination = out / "日本語 saved.pdf"
order = [1, 0, 2, 3, 4, 5, 6, 7]
with fitz.open(out / "gui-before.pdf") as before, fitz.open(destination) as after:
    assert len(before) == len(after) == 8
    rows = []
    for index, original_index in enumerate(order):
        original, saved = before[original_index], after[index]
        assert contents(before, original) == contents(after, saved)
        assert tuple(original.mediabox) == tuple(saved.mediabox)
        assert saved.rotation == (90 if index == 1 else 0)
        rows.append({"saved_page": index + 1, "original_page": original_index + 1,
                     "rotation": saved.rotation, "content_matches": True})
recovery = out / "gui-recovered.pdf"
with fitz.open(out / "gui-before.pdf") as before, fitz.open(recovery) as after:
    assert len(after) == 8
    for index, original_index in enumerate(order):
        assert contents(before, before[original_index]) == contents(after, after[index])
        assert after[index].rotation == (90 if index < 2 else 0)
assert not list((out / "readonly").iterdir())
print(json.dumps({"passed": True, "pages": rows,
                  "source_unchanged": True,
                  "saved_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                  "recovery": {"passed": True, "rotations": [90, 90, 0, 0, 0, 0, 0, 0],
                               "readonly_directory_empty": True,
                               "sha256": hashlib.sha256(recovery.read_bytes()).hexdigest()}}, indent=2))
