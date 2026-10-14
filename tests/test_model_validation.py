import fitz
import pytest

from folimeld.model import PdfDocument


@pytest.fixture
def model(tmp_path):
    model = PdfDocument()
    model.doc = fitz.open()
    for _ in range(3):
        model.doc.new_page()
    model.save(str(tmp_path / "saved.pdf"))
    model.rotate([0], 90)
    model.rotate([1], 90)
    model.undo()
    yield model
    model.close()


@pytest.mark.parametrize("operation,error", [
    (lambda m: m.reorder(-1, 0), IndexError),
    (lambda m: m.reorder(0, 3), IndexError),
    (lambda m: m.reorder(3, 3), IndexError),
    (lambda m: m.move_selected([0, 3], 1), IndexError),
    (lambda m: m.move_selected([0], 0), ValueError),
    (lambda m: m.move_selected([0], 2), ValueError),
    (lambda m: m.move_selected([], True), ValueError),
    (lambda m: m.rotate([0, -1], 90), IndexError),
    (lambda m: m.rotate([0], 45), ValueError),
    (lambda m: m.rotate([0], 90.0), ValueError),
    (lambda m: m.rotate([True], 90), TypeError),
    (lambda m: m.delete_pages([0.0]), TypeError),
    (lambda m: m.insert_blank_after([3]), IndexError),
    (lambda m: m.insert("missing.pdf", -1), IndexError),
    (lambda m: m.insert("missing.pdf", 3), IndexError),
    (lambda m: m.set_details("1.99", "OneColumn", False, False), ValueError),
    (lambda m: m.set_details("1.", "OneColumn", False, False), ValueError),
    (lambda m: m.set_details("3.0", "OneColumn", False, False), ValueError),
    (lambda m: m.set_details("1.7", "Unknown", False, False), ValueError),
    (lambda m: m.set_view_password(123), TypeError),
])
def test_invalid_edit_preserves_document_history_and_save_point(model, operation, error):
    before = model._snapshot()
    history = (list(model._undo), list(model._redo))
    saved = model._saved_revision
    path = model.path
    with pytest.raises(error):
        operation(model)
    assert model._snapshot() == before
    assert (model._undo, model._redo) == history
    assert model._saved_revision == saved and model.path == path
    assert model.dirty
    assert model.redo() and model.doc[1].rotation == 90
    assert model.undo() and model.undo() and not model.dirty


@pytest.mark.parametrize("version", [f"1.{n}" for n in range(8)] + ["2.0", "PDF-1.7"])
def test_supported_versions(model, version):
    model.set_details(version, "SinglePage", False, False)
    expected = version.removeprefix("PDF-")
    assert model.doc.xref_get_key(model.doc.pdf_catalog(), "Version")[1] == "/" + expected


def test_duplicate_rotation_indexes_are_applied_once(model):
    model.rotate([2, 2], 90)
    assert model.doc[2].rotation == 90


def test_edit_without_document_has_clear_error():
    with pytest.raises(RuntimeError, match="No PDF is loaded"):
        PdfDocument().rotate([0], 90)


@pytest.mark.parametrize("old", range(3))
@pytest.mark.parametrize("new", range(3))
def test_reorder_all_destinations(model, old, new):
    for number, page in enumerate(model.doc):
        page.insert_text((30, 40), str(number))
    expected = [0, 1, 2]
    expected.insert(new, expected.pop(old))
    model.reorder(old, new)
    assert [int(page.get_text()) for page in model.doc] == expected
    if old != new:
        assert model.undo()
        assert [int(page.get_text()) for page in model.doc] == [0, 1, 2]
        assert model.redo()
        assert [int(page.get_text()) for page in model.doc] == expected
