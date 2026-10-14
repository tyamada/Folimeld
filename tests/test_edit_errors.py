from unittest.mock import patch

import fitz
import pytest
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow


@pytest.mark.parametrize("method,args", [
    ("rotate", (90,)), ("move", (1,)), ("reorder_page", (0, 1)),
])
def test_edit_errors_are_reported(method, args):
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        window.model.doc.new_page()
        window.model.doc.new_page()
        window.refresh([0])
        model_method = 'move_selected' if method == 'move' else 'reorder' if method == 'reorder_page' else method
        failure = OSError('simulated edit failure')
        with patch.object(window.model, model_method, side_effect=failure), \
             patch.object(window, 'error') as report:
            getattr(window, method)(*args)
            report.assert_called_once_with(failure)
        assert window.model.loaded and not window.model.dirty
    finally:
        window.close()
        window.deleteLater()
        app.processEvents()


def test_properties_failure_rolls_back_and_keeps_dialog_open():
    from folimeld.dialogs import PropertiesDialog

    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    dialog = None
    try:
        window.model.doc = fitz.open()
        window.model.doc.new_page()
        before = window.model._snapshot()
        dialog = PropertiesDialog(window.model, window.tr_, window)
        dialog.title.setText('Must be rolled back')
        with patch.object(window.model, 'set_details', side_effect=OSError('failed')), \
             patch('folimeld.dialogs.QMessageBox.critical') as report:
            dialog.accept()
        report.assert_called_once()
        assert dialog.result() == 0
        assert window.model._snapshot() == before
        assert not window.model.can_undo and not window.model.dirty
    finally:
        if dialog:
            dialog.deleteLater()
        window.close()
        window.deleteLater()
        app.processEvents()
