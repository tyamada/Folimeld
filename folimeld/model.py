import os
import secrets
import tempfile
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import NamedTuple

import fitz


class HistoryState(NamedTuple):
    pdf: bytes
    password: str | None
    protected: bool
    revision: int


class PasswordRequiredError(Exception):
    """Raised when a PDF requires a valid viewing password."""


def layout_with_cover(layout: str, cover: bool) -> str:
    for family in ("TwoColumn", "TwoPage"):
        if layout in (family + "Left", family + "Right"):
            return family + ("Right" if cover else "Left")
    return layout


def undoable(method):
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        with self.transaction():
            return method(self, *args, **kwargs)
    return wrapped


class PdfDocument:
    def __init__(self, history_limit_bytes: int = 128 * 1024 * 1024) -> None:
        self.history_limit_bytes = max(0, history_limit_bytes)
        self.doc: fitz.Document | None = None
        self.path: Path | None = None
        self.dirty = False
        self.view_password: str | None = None
        self.password_protected = False
        self._undo: list[HistoryState] = []
        self._redo: list[HistoryState] = []
        self._revision = 0
        self._next_revision = 0
        self._saved_revision = 0
        self._transaction_depth = 0

    @property
    def history_bytes(self) -> int:
        return sum(len(state.pdf) for stack in (self._undo, self._redo) for state in stack)

    def _trim_history(self) -> None:
        # Stack bottoms are the farthest reachable states. Keep the nearest
        # states; a snapshot larger than the budget cannot be retained.
        size = self.history_bytes
        for stack in (self._undo, self._redo):
            while stack and size > self.history_limit_bytes:
                size -= len(stack.pop(0).pdf)

    def _snapshot(self) -> HistoryState:
        assert self.doc is not None
        return HistoryState(
            self.doc.tobytes(encryption=fitz.PDF_ENCRYPT_NONE, no_new_id=True),
            self.view_password, self.password_protected, self._revision,
        )

    def _restore(self, state: HistoryState) -> None:
        data, password, protected, revision = state
        restored = fitz.open(stream=data, filetype="pdf")
        self.doc.close()
        self.doc = restored
        self.view_password = password
        self.password_protected = protected
        self._revision = revision
        self.dirty = revision != self._saved_revision

    @contextmanager
    def transaction(self):
        """Group edits into one history entry and roll back failed edits."""
        if self._transaction_depth:
            yield
            return
        if not self.loaded:
            raise RuntimeError("No PDF is loaded.")
        before = self._snapshot()
        self._transaction_depth += 1
        try:
            yield
            after = self._snapshot()
            if before[:3] != after[:3]:
                self._undo.append(before)
                self._redo.clear()
                self._trim_history()
                self._next_revision += 1
                self._revision = self._next_revision
            self.dirty = self._revision != self._saved_revision
        except Exception:
            self._restore(before)
            raise
        finally:
            self._transaction_depth -= 1

    @property
    def can_undo(self) -> bool:
        return self.loaded and bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return self.loaded and bool(self._redo)

    def undo(self) -> bool:
        if not self.can_undo:
            return False
        current = self._snapshot()
        self._restore(self._undo[-1])
        self._undo.pop()
        self._redo.append(current)
        self._trim_history()
        return True

    def redo(self) -> bool:
        if not self.can_redo:
            return False
        current = self._snapshot()
        self._restore(self._redo[-1])
        self._redo.pop()
        self._undo.append(current)
        self._trim_history()
        return True

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

    def open_generated(self, path: str) -> None:
        # Detach from the temporary file before replacing the current document.
        new_doc = fitz.open(stream=Path(path).read_bytes(), filetype="pdf")
        self.close()
        self.doc = new_doc
        self._revision = self._next_revision = 1
        self.dirty = True

    def close(self) -> None:
        if self.doc is not None:
            self.doc.close()
        self.doc = None
        self._undo.clear()
        self._redo.clear()
        self._revision = self._next_revision = self._saved_revision = 0
        self.dirty = False
        self.path = None
        self.view_password = None
        self.password_protected = False

    def _validate_rows(self, rows: list[int]) -> list[int]:
        assert self.doc is not None
        for row in rows:
            if type(row) is not int:
                raise TypeError("Page indexes must be integers.")
            if not 0 <= row < self.doc.page_count:
                raise IndexError("Page index out of range.")
        return sorted(set(rows))

    @undoable
    def set_view_password(self, password: str | None) -> None:
        assert self.doc is not None
        if password is not None and not isinstance(password, str):
            raise TypeError("Password must be a string or None.")
        self.view_password = password or None
        self.password_protected = bool(password)
        self.dirty = True

    @undoable
    def insert(self, path: str, after: int | None) -> None:
        assert self.doc is not None
        if after is not None:
            self._validate_rows([after])
        with fitz.open(path) as source:
            target = self.doc.page_count if after is None else after + 1
            self.doc.insert_pdf(source, start_at=target)
        self.dirty = True

    @undoable
    def insert_blank_after(self, rows: list[int]) -> list[int]:
        """Insert a same-sized blank page immediately after each selected page."""
        assert self.doc is not None
        selected = self._validate_rows(rows)
        if not selected:
            return []

        # Work backwards so earlier insertions do not change the source indexes.
        for row in reversed(selected):
            rect = self.doc[row].rect
            self.doc.new_page(pno=row + 1, width=rect.width, height=rect.height)
        self.dirty = True
        return [row + offset + 1 for offset, row in enumerate(selected)]

    @undoable
    def delete_pages(self, rows: list[int]) -> list[int]:
        """Delete selected pages and return the row to select afterward."""
        assert self.doc is not None
        selected = self._validate_rows(rows)
        if not selected:
            return []
        if len(selected) == self.doc.page_count:
            raise ValueError("At least one page must remain.")

        first = selected[0]
        for row in reversed(selected):
            self.doc.delete_page(row)
        self.dirty = True
        return [min(first, self.doc.page_count - 1)]

    @undoable
    def reorder(self, old: int, new: int) -> None:
        assert self.doc is not None
        self._validate_rows([old, new])
        if old == new:
            return
        # move_page inserts before its destination; -1 appends at the end.
        target = -1 if new == self.doc.page_count - 1 else new + (old < new)
        self.doc.move_page(old, target)
        self.dirty = True

    @undoable
    def move_selected(self, rows: list[int], direction: int) -> list[int]:
        assert self.doc is not None
        selected = set(self._validate_rows(rows))
        if type(direction) is not int or direction not in (-1, 1):
            raise ValueError("Move direction must be -1 or 1.")
        order = list(range(self.doc.page_count))
        scan = range(1, len(order)) if direction < 0 else range(len(order) - 2, -1, -1)
        for i in scan:
            neighbor = i + direction
            if i in selected and neighbor not in selected:
                order[i], order[neighbor] = order[neighbor], order[i]
                selected.remove(i)
                selected.add(neighbor)
        if order != list(range(self.doc.page_count)):
            self._reorder_pages(order)
            self.dirty = True
        return sorted(selected)

    def _reorder_pages(self, order: list[int]) -> None:
        """Move existing pages without rebuilding and stripping the catalog."""
        current = list(range(self.doc.page_count))
        for target, original in enumerate(order):
            source = current.index(original)
            if source != target:
                self.doc.move_page(source, target)
                current.insert(target, current.pop(source))

    @undoable
    def rotate(self, rows: list[int], degrees: int) -> None:
        assert self.doc is not None
        selected = self._validate_rows(rows)
        if type(degrees) is not int or degrees % 90:
            raise ValueError("Rotation must be an integer multiple of 90 degrees.")
        for row in selected:
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
        descriptor, name = tempfile.mkstemp(prefix=".folimeld-", suffix=".pdf", dir=destination.parent)
        os.close(descriptor)
        temp = Path(name)
        try:
            self.doc.save(str(temp), **options)
            # Prepare an independent editable document before releasing the
            # source file handle (required for replacement on Windows).
            backup = fitz.open(stream=self._snapshot()[0], filetype="pdf")
            self.doc.close()
            self.doc = backup
            temp.replace(destination)
            reopened = fitz.open(str(destination))
            try:
                if self.view_password and not reopened.authenticate(self.view_password):
                    raise PasswordRequiredError()
            except Exception:
                reopened.close()
                raise
            self.doc = reopened
            backup.close()
        finally:
            temp.unlink(missing_ok=True)
        self.path, self.dirty = destination, False
        self._saved_revision = self._revision

    @undoable
    def set_metadata(self, title: str, author: str, subject: str, keywords: str) -> None:
        assert self.doc is not None
        metadata = dict(self.doc.metadata)
        metadata.update(title=title, author=author, subject=subject, keywords=keywords)
        self.doc.set_metadata(metadata)
        self.dirty = True

    @undoable
    def set_details(self, version: str, layout: str, cover: bool,
                    right_to_left: bool) -> None:
        """Update PDF catalog viewer preferences shown on the Details tab."""
        assert self.doc is not None
        catalog = self.doc.pdf_catalog()

        normalized_version = version.strip().upper().removeprefix("PDF-")
        if layout in ("TwoPageLeft", "TwoPageRight") and normalized_version in {
            "1.0", "1.1", "1.2", "1.3", "1.4",
        }:
            normalized_version = "1.5"
        if normalized_version:
            if normalized_version not in {f"1.{minor}" for minor in range(8)} | {"2.0"}:
                raise ValueError("PDF version must be 1.0–1.7 or 2.0.")
            self.doc.xref_set_key(catalog, "Version", f"/{normalized_version}")

        if layout not in {"", "SinglePage", "OneColumn", "TwoColumnLeft",
                          "TwoColumnRight", "TwoPageLeft", "TwoPageRight"}:
            raise ValueError("Unsupported PDF page layout.")
        layout = layout_with_cover(layout, cover)
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
            self.doc.update_object(preferences, value if value_type == "dict" else "<<>>")
            self.doc.xref_set_key(catalog, "ViewerPreferences", f"{preferences} 0 R")
        self.doc.xref_set_key(preferences, "Direction", "/R2L" if right_to_left else "/L2R")
        self.dirty = True
