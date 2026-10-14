from unittest.mock import patch

import fitz
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow


def drain(window):
    while window._pending_thumbnails:
        window._render_thumbnail_batch()


def test_thumbnail_reuse_rotation_reorder_and_document_replacement():
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        for _ in range(12):
            window.model.doc.new_page()
        with patch.object(window, 'render_icon', wraps=window.render_icon) as render:
            window.refresh([0])
            assert render.call_count == 0
            window._render_thumbnail_batch()
            assert render.call_count == 4
            drain(window)
            assert render.call_count == 12
            first = window.pages.item(0)
            window.rotate(90)
            drain(window)
            assert render.call_count == 13
            rotated = window.pages.item(0)
            assert rotated is not first
            window.reorder_page(0, 5)
            drain(window)
            assert render.call_count == 13
            assert window.pages.item(5) is rotated
            window.undo()
            drain(window)
            assert render.call_count == 25
            window.thumbnail_size = 144
            window.refresh()
            drain(window)
            assert render.call_count == 37
    finally:
        window.model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()


def test_pending_renders_are_cancelled_when_document_changes():
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        window.model.doc.new_page()
        window.refresh()
        window.model.close()
        with patch.object(window, 'render_icon') as render:
            window._render_thumbnail_batch()
            render.assert_not_called()
        assert not window._pending_thumbnails
        assert not window._thumbnail_timer.isActive()
    finally:
        window.close()
        window.deleteLater()
        app.processEvents()
