import fitz
import pytest
from PySide6.QtWidgets import QApplication

from folimeld.dialogs import PropertiesDialog
from folimeld.model import PdfDocument


@pytest.fixture
def model(tmp_path):
    source = tmp_path / 'source.pdf'
    with fitz.open() as doc:
        for number in range(4):
            doc.new_page().insert_text((20, 40), str(number))
        doc.set_metadata({'title': 'Original title', 'author': 'Original author'})
        doc.set_xml_metadata('<metadata>original</metadata>')
        catalog = doc.pdf_catalog()
        for key, value in {
            'Version': '/1.7', 'PageLayout': '/TwoPageRight',
            'PageMode': '/UseOutlines', 'Lang': '(ja-JP)',
            'ViewerPreferences': '<</Direction /R2L /HideToolbar true>>',
        }.items():
            doc.xref_set_key(catalog, key, value)
        doc.set_toc([[1, 'First page', 1]])
        doc.save(source)
    model = PdfDocument()
    model.open(str(source))
    yield model
    model.close()


def properties(doc):
    catalog = doc.pdf_catalog()
    return (doc.metadata, doc.get_xml_metadata(), {
        key: doc.xref_get_key(catalog, key)
        for key in ('Version', 'PageLayout', 'PageMode', 'Lang',
                    'ViewerPreferences/Direction', 'ViewerPreferences/HideToolbar')
    })


@pytest.mark.parametrize('operation,expected', [
    (lambda m: m.reorder(0, 3), [1, 2, 3, 0]),
    (lambda m: m.reorder(3, 0), [3, 0, 1, 2]),
    (lambda m: m.move_selected([0, 2], 1), [1, 0, 3, 2]),
    (lambda m: m.move_selected([1, 3], -1), [1, 0, 3, 2]),
])
@pytest.mark.parametrize('overwrite', [False, True])
def test_reorder_preserves_properties(model, tmp_path, operation, expected, overwrite):
    before = properties(model.doc)
    operation(model)
    assert properties(model.doc) == before
    assert [int(page.get_text().strip()) for page in model.doc] == expected
    assert model.doc.get_toc() == [[1, 'First page', expected.index(0) + 1]]
    assert model.undo()
    assert properties(model.doc) == before
    assert [int(page.get_text().strip()) for page in model.doc] == list(range(4))
    assert model.redo()
    destination = model.path if overwrite else tmp_path / 'saved.pdf'
    model.save(str(destination))
    assert properties(model.doc) == before
    assert [int(page.get_text().strip()) for page in model.doc] == expected
    assert model.doc.get_toc() == [[1, 'First page', expected.index(0) + 1]]


@pytest.mark.parametrize('indirect', [False, True])
def test_properties_dialog_preserves_viewer_preferences(model, indirect):
    app = QApplication.instance() or QApplication([])
    if indirect:
        catalog = model.doc.pdf_catalog()
        value = model.doc.xref_get_key(catalog, 'ViewerPreferences')[1]
        preferences = model.doc.get_new_xref()
        model.doc.update_object(preferences, value)
        model.doc.xref_set_key(catalog, 'ViewerPreferences', f'{preferences} 0 R')
    before = properties(model.doc)
    dialog = PropertiesDialog(model, lambda key: key)
    assert dialog.scroll_direction.currentData() is True
    dialog.accept()
    assert properties(model.doc) == before
    model.save(str(model.path))
    assert properties(model.doc) == before
    dialog.deleteLater()
    app.processEvents()
