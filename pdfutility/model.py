from pathlib import Path

import fitz


class PdfDocument:
    def __init__(self) -> None:
        self.doc: fitz.Document | None = None
        self.path: Path | None = None
        self.dirty = False

    @property
    def loaded(self) -> bool:
        return self.doc is not None

    def open(self, path: str) -> None:
        new_doc = fitz.open(path)
        if new_doc.needs_pass:
            new_doc.close()
            raise ValueError("Encrypted PDFs are not supported.")
        self.close()
        self.doc, self.path, self.dirty = new_doc, Path(path), False

    def close(self) -> None:
        if self.doc is not None:
            self.doc.close()
        self.doc = None

    def insert(self, path: str, after: int | None) -> None:
        assert self.doc is not None
        with fitz.open(path) as source:
            target = self.doc.page_count if after is None else after + 1
            self.doc.insert_pdf(source, start_at=target)
        self.dirty = True

    def reorder(self, old: int, new: int) -> None:
        assert self.doc is not None
        if old == new:
            return
        order = list(range(self.doc.page_count))
        page = order.pop(old)
        order.insert(new, page)
        self.doc.select(order)
        self.dirty = True

    def move_selected(self, rows: list[int], direction: int) -> list[int]:
        assert self.doc is not None
        selected = set(rows)
        order = list(range(self.doc.page_count))
        scan = range(1, len(order)) if direction < 0 else range(len(order) - 2, -1, -1)
        for i in scan:
            neighbor = i + direction
            if i in selected and neighbor not in selected:
                order[i], order[neighbor] = order[neighbor], order[i]
                selected.remove(i)
                selected.add(neighbor)
        if order != list(range(self.doc.page_count)):
            self.doc.select(order)
            self.dirty = True
        return sorted(selected)

    def rotate(self, rows: list[int], degrees: int) -> None:
        assert self.doc is not None
        for row in rows:
            page = self.doc[row]
            page.set_rotation((page.rotation + degrees) % 360)
        if rows:
            self.dirty = True

    def save(self, path: str) -> None:
        assert self.doc is not None
        destination = Path(path)
        if self.path and destination.resolve() == self.path.resolve():
            temp = destination.with_name(destination.stem + ".pdfutility.tmp.pdf")
            self.doc.save(str(temp), garbage=4, deflate=True)
            self.doc.close()
            temp.replace(destination)
            self.doc = fitz.open(str(destination))
        else:
            self.doc.save(str(destination), garbage=4, deflate=True)
            self.doc.close()
            self.doc = fitz.open(str(destination))
        self.path, self.dirty = destination, False

    def set_metadata(self, title: str, author: str, subject: str, keywords: str) -> None:
        assert self.doc is not None
        metadata = dict(self.doc.metadata)
        metadata.update(title=title, author=author, subject=subject, keywords=keywords)
        self.doc.set_metadata(metadata)
        self.dirty = True

    def set_details(self, version: str, layout: str, cover: bool,
                    right_to_left: bool) -> None:
        """Update PDF catalog viewer preferences shown on the Details tab."""
        assert self.doc is not None
        catalog = self.doc.pdf_catalog()

        normalized_version = version.strip().upper().removeprefix("PDF-")
        if normalized_version:
            if not normalized_version.startswith("1.") and normalized_version != "2.0":
                raise ValueError("PDF version must be 1.0–1.7 or 2.0.")
            self.doc.xref_set_key(catalog, "Version", f"/{normalized_version}")

        if layout in ("TwoPageLeft", "TwoPageRight"):
            layout = "TwoPageRight" if cover else "TwoPageLeft"
        if layout:
            set_layout = getattr(self.doc, "set_pagelayout", None)
            if set_layout is None:
                set_layout = getattr(self.doc, "set_page_layout", None)
            if set_layout is None:
                raise RuntimeError("This PyMuPDF version cannot edit the page layout.")
            set_layout(layout)

        value_type, value = self.doc.xref_get_key(catalog, "ViewerPreferences")
        if value_type == "xref":
            preferences = int(value.split()[0])
        else:
            preferences = self.doc.get_new_xref()
            self.doc.update_object(preferences, "<<>>")
            self.doc.xref_set_key(catalog, "ViewerPreferences", f"{preferences} 0 R")
        self.doc.xref_set_key(preferences, "Direction", "/R2L" if right_to_left else "/L2R")
        self.dirty = True
