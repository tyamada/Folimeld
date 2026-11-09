"""Read-only form/encryption/image checks for files saved through the GUI."""
import hashlib
from io import BytesIO
import json
from pathlib import Path

import pymupdf as fitz
from PIL import Image


out = Path("build/netbsd-verification")


def fields(document):
    return [{"name": widget.field_name, "type": widget.field_type,
             "value": widget.field_value, "choices": widget.choice_values,
             "rect": list(widget.rect)}
            for page in document for widget in page.widgets()]


with fitz.open(out / "forms.pdf") as source:
    expected = fields(source)
results = {}
for filename, encrypted in [("gui-forms.pdf", False), ("gui-encrypted.pdf", True)]:
    with fitz.open(out / filename) as saved:
        assert bool(saved.needs_pass) == encrypted
        if encrypted:
            assert saved.authenticate("wrong-test-password") == 0
            assert saved.authenticate("netbsd-user-test") > 0
        assert len(saved) == 1 and saved[0].rotation == 90
        assert fields(saved) == expected
        results[filename] = {"passed": True, "encrypted": encrypted,
                             "rotation": saved[0].rotation, "fields": fields(saved)}

images = []
with fitz.open(out / "gui-images.pdf") as saved:
    assert len(saved) == 2
    for index, filename in enumerate(["image 1.png", "image 2.jpg"]):
        source_path = out / "images 日本語" / filename
        references = saved[index].get_images(full=True)
        assert len(references) == 1
        embedded = saved.extract_image(references[0][0])
        assert (embedded["width"], embedded["height"]) == (640, 480)
        with Image.open(source_path) as original, Image.open(BytesIO(embedded["image"])) as actual:
            assert original.convert("RGB").tobytes() == actual.convert("RGB").tobytes()
        check = "decoded RGB pixels"
        images.append({"page": index + 1, "source": filename, "matched": check})
results["gui-images.pdf"] = {"passed": True, "images": images}
for filename in ("gui-forms.pdf", "gui-encrypted.pdf", "gui-images.pdf"):
    results[filename]["sha256"] = hashlib.sha256((out / filename).read_bytes()).hexdigest()
print(json.dumps({"passed": True, "results": results}, indent=2))
