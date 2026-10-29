"""Check all selection patterns against an independent adjacent-swap oracle."""
import fitz
import pytest

from folimeld.model import PdfDocument


@pytest.mark.parametrize('direction', [-1, 1])
@pytest.mark.parametrize('mask', range(64))
def test_move_selection_patterns(mask, direction):
    selected = {row for row in range(6) if mask & (1 << row)}
    expected = list(range(6))
    selection = set(selected)
    for row in (range(1, 6) if direction < 0 else range(4, -1, -1)):
        neighbor = row + direction
        if row in selection and neighbor not in selection:
            expected[row], expected[neighbor] = expected[neighbor], expected[row]
            selection.remove(row)
            selection.add(neighbor)
    model = PdfDocument()
    try:
        model.doc = fitz.open()
        for number in range(6):
            model.doc.new_page().insert_text((30, 40), str(number))
        model.doc.set_toc([[1, 'Original first page', 1]])
        assert model.move_selected(list(selected), direction) == sorted(selection)
        assert [int(page.get_text()) for page in model.doc] == expected
        assert model.doc.get_toc() == [[1, 'Original first page', expected.index(0) + 1]]
        if expected != list(range(6)):
            assert model.undo()
            assert [int(page.get_text()) for page in model.doc] == list(range(6))
            assert model.redo()
            assert [int(page.get_text()) for page in model.doc] == expected
    finally:
        model.close()
