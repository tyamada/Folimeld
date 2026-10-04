from unittest.mock import patch

import fitz
import pytest
from PySide6.QtWidgets import QApplication, QToolBar

from folimeld.app import MainWindow
from folimeld.dialogs import PropertiesDialog


@pytest.mark.parametrize('cover', [False, True])
@pytest.mark.parametrize('version', ['1.4', '1.7'])
def test_toolbar_binding_round_trip(cover, version, tmp_path):
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        actions = (window.properties_action, window.right_binding_action,
                   window.right_binding_cover_action)
        toolbar = window.findChild(QToolBar)
        assert all(action in toolbar.actions() for action in actions)
        assert all(not action.isEnabled() for action in actions)
        source = tmp_path / 'source.pdf'
        with fitz.open() as doc:
            doc.new_page()
            doc.xref_set_key(doc.pdf_catalog(), 'Version', '/' + version)
            doc.save(source)
        window.model.open(str(source))
        window.refresh()
        assert all(action.isEnabled() for action in actions)
        with patch('folimeld.app.PropertiesDialog') as dialog:
            window.properties_action.trigger()
            dialog.assert_called_once_with(window.model, window.tr_, window)
            dialog.return_value.exec.assert_called_once()
        actions[2 if cover else 1].trigger()
        model = window.model
        expected_layout = 'TwoPageRight' if cover else 'TwoPageLeft'
        assert model.doc.pagelayout == expected_layout
        assert model.dirty and window.undo_action.isEnabled()
        dialog = PropertiesDialog(model, window.tr_, window)
        assert dialog.page_layout.currentText() == expected_layout
        assert dialog.scroll_direction.currentData() is True
        assert dialog.cover_page.isChecked() == cover
        assert dialog.pdf_version.currentText() == ('1.5' if version == '1.4' else version)
        dialog.reject()
        window.undo_action.trigger()
        assert not model.dirty and not model.can_undo
        window.redo_action.trigger()
        target = tmp_path / 'saved.pdf'
        model.save(str(target))
        with fitz.open(target) as doc:
            assert doc.pagelayout == expected_layout
            preferences = int(doc.xref_get_key(doc.pdf_catalog(), 'ViewerPreferences')[1].split()[0])
            assert doc.xref_get_key(preferences, 'Direction')[1] == '/R2L'
    finally:
        window.model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()
