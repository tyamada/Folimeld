from pathlib import Path
import secrets

import fitz


class PasswordRequiredError(Exception):
    """Raised when a PDF requires a valid viewing password."""


class PdfDocument:
    def __init__(self) -> None:
        self.doc: fitz.Document | None = None
        self.path: Path | None = None
        self.dirty = False
        self.view_password: str | None = None
        self.password_protected = False

    @property
    def loaded(self) -> bool:
        return self.doc is not None

    def open(self, path: str, password: str | None = None) -> None:
        new_doc = fitz.open(path)
        was_protected = bool(new_doc.needs_pass)
        if was_protected and (password is None or not new_doc.authenticate(password)):
            new_doc.close()
            raise PasswordRequiredError()
        self.close()
        self.doc, self.path, self.dirty = new_doc, Path(path), False
        self.password_protected = was_protected
        self.view_password = password if was_protected else None

    def close(self) -> None:
        if self.doc is not None:
            self.doc.close()
        self.doc = None

    def set_view_password(self, password: str | None) -> None:
        assert self.doc is not None
        self.view_password = password or None
        self.password_protected = bool(password)
        self.dirty = True

    def insert(self, path: str, after: int | None) -> None:
        assert self.doc is not None
        with fitz.open(path) as source:
            target = self.doc.page_count if after is None else after + 1
            self.doc.insert_pdf(source, start_at=target)
        self.dirty = True

    def insert_blank_after(self, rows: list[int]) -> list[int]:
        """Insert a same-sized blank page immediately after each selected page."""
        assert self.doc is not None
        selected = sorted(set(rows))
        if not selected:
            return []
        if selected[0] < 0 or selected[-1] >= self.doc.page_count:
            raise IndexError("Page index out of range.")

        # Work backwards so earlier insertions do not change the source indexes.
        for row in reversed(selected):
            rect = self.doc[row].rect
            self.doc.new_page(pno=row + 1, width=rect.width, height=rect.height)
        self.dirty = True
        return [row + offset + 1 for offset, row in enumerate(selected)]

    def delete_pages(self, rows: list[int]) -> list[int]:
        """Delete selected pages and return the row to select afterward."""
        assert self.doc is not None
        selected = sorted(set(rows))
        if not selected:
            return []
        if selected[0] < 0 or selected[-1] >= self.doc.page_count:
            raise IndexError("Page index out of range.")
        if len(selected) == self.doc.page_count:
            raise ValueError("At least one page must remain.")

        first = selected[0]
        for row in reversed(selected):
            self.doc.delete_page(row)
        self.dirty = True
        return [min(first, self.doc.page_count - 1)]

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
        options = {"garbage": 4, "deflate": True}
        if self.view_password:
            options.update(
                encryption=fitz.PDF_ENCRYPT_AES_256,
                user_pw=self.view_password,
                owner_pw=secrets.token_urlsafe(24),
                permissions=(fitz.PDF_PERM_ACCESSIBILITY | fitz.PDF_PERM_PRINT |
                             fitz.PDF_PERM_COPY | fitz.PDF_PERM_ANNOTATE |
                             fitz.PDF_PERM_FORM | fitz.PDF_PERM_ASSEMBLE |
                             fitz.PDF_PERM_MODIFY),
            )
        else:
            options["encryption"] = fitz.PDF_ENCRYPT_NONE
        if self.path and destination.resolve() == self.path.resolve():
            temp = destination.with_name(destination.stem + ".folimeld.tmp.pdf")
            self.doc.save(str(temp), **options)
            self.doc.close()
            temp.replace(destination)
            self.doc = fitz.open(str(destination))
        else:
            self.doc.save(str(destination), **options)
            self.doc.close()
            self.doc = fitz.open(str(destination))
        if self.view_password:
            self.doc.authenticate(self.view_password)
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
