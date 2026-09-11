import fitz
import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QKeySequence
from folimeld.model import PdfDocument
from folimeld.app import MainWindow
from folimeld.dialogs import PropertiesDialog


@pytest.fixture
def model():
    model = PdfDocument()
    model.doc = fitz.open()
    for width in (100, 200, 300):
        page = model.doc.new_page(width=width, height=400)
        page.insert_text((20, 40), str(width))
    yield model
    model.close()


def state(model):
    return [(p.rect.width, p.rect.height, p.rotation, p.get_text()) for p in model.doc]


def test_multiple_edits_round_trip(model, tmp_path):
    source = tmp_path / 'source.pdf'
    with fitz.open() as doc:
        doc.new_page(width=500, height=600)
        doc.save(source)
    states = [state(model)]
    operations = [lambda: model.rotate([0, 2], 90),
                  lambda: model.insert_blank_after([0, 2]),
                  lambda: model.delete_pages([1, 3]),
                  lambda: model.reorder(0, 2),
                  lambda: model.move_selected([1, 2], -1),
                  lambda: model.insert(str(source), 0)]
    for operation in operations:
        operation()
        states.append(state(model))
    for expected in reversed(states[:-1]):
        assert model.undo()
        assert state(model) == expected
    assert not model.dirty
    assert not model.undo()
    for expected in states[1:]:
        assert model.redo()
        assert state(model) == expected
    assert not model.redo()


def test_save_point_branch_and_no_ops(model, tmp_path):
    model.rotate([0], 90)
    model.save(str(tmp_path / 'saved.pdf'))
    model.rotate([1], 90)
    assert model.undo() and not model.dirty
    assert model.undo() and model.dirty
    assert model.redo() and not model.dirty
    model.move_selected([0], -1)
    model.rotate([], 90)
    model.delete_pages([])
    assert model.can_redo and not model.dirty
    with pytest.raises(ValueError):
        model.delete_pages(list(range(3)))
    assert model.can_redo and not model.dirty
    model.rotate([2], 180)
    assert not model.can_redo and model.dirty
    model.save(str(tmp_path / 'saved.pdf'))
    assert model.undo() and model.dirty
    assert model.redo() and not model.dirty


def test_password_history_and_reopen(model, tmp_path):
    model.set_view_password('secret')
    model.save(str(tmp_path / 'encrypted.pdf'))
    model.set_view_password(None)
    assert model.undo()
    assert model.view_password == 'secret' and model.password_protected
    assert not model.dirty
    assert model.undo()
    assert model.view_password is None and not model.password_protected
    assert model.redo()
    model.open(str(tmp_path / 'encrypted.pdf'), 'secret')
    assert not model.can_undo and not model.can_redo
    model.rotate([0], 90)
    assert model.undo()
    assert model.doc[0].rotation == 0
    assert model.view_password == 'secret'
    model.close()
    assert not model.can_undo and not model.can_redo


def test_failed_group_rolls_back(model):
    original = state(model)
    with pytest.raises(IndexError):
        with model.transaction():
            model.rotate([0], 90)
            model.rotate([1, 99], 90)
    assert state(model) == original
    assert not model.can_undo and not model.dirty


def test_ui_and_grouped_properties(model):
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        assert not window.undo_action.isEnabled()
        assert not window.redo_action.isEnabled()
        window.model = model
        window.refresh([0])
        assert window.undo_action.shortcuts() == QKeySequence.keyBindings(QKeySequence.StandardKey.Undo)
        window.rotate(90)
        assert window.undo_action.isEnabled()
        window.undo_action.trigger()
        assert model.doc[0].rotation == 0
        assert window.redo_action.isEnabled()
        window.redo_action.trigger()
        assert model.doc[0].rotation == 90
        before = model.doc.metadata.copy()
        dialog = PropertiesDialog(model, window.tr_, window)
        dialog.title.setText('History test')
        dialog.pdf_version.setCurrentText('1.7')
        dialog.page_layout.setCurrentText('TwoPageRight')
        dialog.cover_page.setChecked(True)
        dialog.accept()
        assert model.doc.metadata['title'] == 'History test'
        model.undo()
        assert model.doc.metadata == before
        model.redo()
        assert model.doc.metadata['title'] == 'History test'
        assert model.doc.pagelayout == 'TwoPageRight'
    finally:
        model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()
