"""Create disposable inputs for the NetBSD GUI verification."""
import hashlib
import json
from pathlib import Path
import shutil

import pymupdf as fitz
from PIL import Image, ImageDraw


def main():
    out = Path("build/netbsd-verification")
    out.mkdir(parents=True, exist_ok=True)
    source = Path("testdata/tameshibu_episode3_ja.pdf")
    shutil.copyfile(source, out / "source.pdf")
    with fitz.open() as document:
        page = document.new_page()
        for index, (name, kind) in enumerate([
            ("text", fitz.PDF_WIDGET_TYPE_TEXT),
            ("check", fitz.PDF_WIDGET_TYPE_CHECKBOX),
            ("combo", fitz.PDF_WIDGET_TYPE_COMBOBOX),
            ("empty_combo", fitz.PDF_WIDGET_TYPE_COMBOBOX),
        ]):
            widget = fitz.Widget()
            widget.field_name = name
            widget.field_type = kind
            widget.rect = fitz.Rect(50, 50 + index * 60, 240, 80 + index * 60)
            if name == "text":
                widget.field_value = "NetBSD preserved value"
            elif name == "check":
                widget.field_value = "Yes"
            elif name == "combo":
                widget.choice_values = ["Alpha", "Beta"]
                widget.field_value = "Alpha"
            else:
                widget.choice_values = []
                widget.field_value = ""
            page.add_widget(widget)
        document.save(out / "forms.pdf")
        document.save(out / "encrypted.pdf", encryption=fitz.PDF_ENCRYPT_AES_256,
                      owner_pw="netbsd-owner-test", user_pw="netbsd-user-test",
                      permissions=-1)
    images = out / "images 日本語"
    images.mkdir(exist_ok=True)
    for index, extension in enumerate(["png", "jpg"]):
        image = Image.new("RGB", (640, 480), (220, 235 - index * 20, 245))
        ImageDraw.Draw(image).text((40, 40), f"NetBSD image {index + 1}", fill="black")
        image.save(images / f"image {index + 1}.{extension}")
    readonly = out / "readonly"
    readonly.mkdir(exist_ok=True)
    readonly.chmod(0o555)
    (out / "fixtures.json").write_text(json.dumps({
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "encrypted_user_password": "netbsd-user-test",
        "encrypted_owner_password": "netbsd-owner-test",
        "purpose": "Disposable test fixtures; passwords are not credentials.",
    }, indent=2), encoding="utf-8")
    print("FIXTURES_READY")


if __name__ == "__main__":
    main()
