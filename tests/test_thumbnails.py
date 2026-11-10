from unittest.mock import patch

import fitz
import pytest
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow


@pytest.mark.parametrize('size,width', [(144, 700), (288, 700), (432, 700), (288, 1400)])
def test_viewport_search_matches_full_scan_without_visiting_every_page(size, width):
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        for _ in range(320):
            window.model.doc.new_page()
        window.thumbnail_size = size
        window.pages.set_thumbnail_size(size)
        window.resize(width, 600)
        window.show()
        app.processEvents()
        window.refresh()
        for target in (0, 159, 319):
            window.pages.scrollToItem(window.pages.item(target))
            app.processEvents()
            viewport = window.pages.viewport().rect()
            area = viewport.adjusted(0, -viewport.height(), 0, viewport.height())
            expected = [row for row in range(320)
                        if window.pages.visualItemRect(window.pages.item(row)).intersects(area)]
            with patch.object(window.pages, 'visualItemRect', wraps=window.pages.visualItemRect) as query:
                actual = [row for row, _rect in window.thumbnails.rows_in_rect(area)]
                assert actual == expected
                assert query.call_count < 100
    finally:
        window.close()


def drain(window):
    while window.thumbnails.pending:
        window.thumbnails.render_batch()


def test_thumbnail_reuse_rotation_reorder_and_document_replacement():
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        for _ in range(12):
            window.model.doc.new_page()
        with patch('folimeld.thumbnails.perf_counter', return_value=0), \
             patch.object(window.thumbnails, 'render_icon', wraps=window.thumbnails.render_icon) as render:
            window.refresh([0])
            assert render.call_count == 0
            window.thumbnails.render_batch()
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
        with patch.object(window.thumbnails, 'render_icon') as render:
            window.thumbnails.render_batch()
            render.assert_not_called()
        assert not window.thumbnails.pending
        assert not window.thumbnails.timer.isActive()
    finally:
        window.close()
        window.deleteLater()
        app.processEvents()


def test_slow_thumbnail_yields_before_rendering_four_pages():
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        for _ in range(5):
            window.model.doc.new_page()
        window.refresh()
        with patch('folimeld.thumbnails.perf_counter', side_effect=[0, 0.020]), \
             patch.object(window.thumbnails, 'render_icon', wraps=window.thumbnails.render_icon) as render:
            window.thumbnails.render_batch()
            assert render.call_count == 1
        assert len(window.thumbnails.pending) == 4
        drain(window)
        assert not window.thumbnails.timer.isActive()
    finally:
        window.model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()


def test_large_document_renders_near_viewport_and_releases_scrolled_out_icons(tmp_path):
    app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    try:
        window.model.doc = fitz.open()
        for _ in range(200):
            window.model.doc.new_page()
        window.show()
        app.processEvents()
        window.refresh([0])
        drain(window)
        first = window.pages.item(0)
        assert not first.icon().isNull()
        assert window.pages.item(199).icon().isNull()
        assert 0 < len(window.thumbnails.resident) <= 64

        assert window._save_to(str(tmp_path / 'saved.pdf'))
        assert window.thumbnails.document is window.model.doc
        drain(window)
        first = window.pages.item(0)

        window.pages.scrollToItem(window.pages.item(199))
        app.processEvents()
        window.thumbnails.update_viewport()
        drain(window)
        assert first.icon().isNull()
        assert not window.pages.item(199).icon().isNull()
        assert len(window.thumbnails.resident) <= 64
        assert window.selected_rows() == [0]

        window.pages.scrollToItem(first)
        app.processEvents()
        window.thumbnails.update_viewport()
        drain(window)
        assert not first.icon().isNull()
        assert window.pages.item(199).icon().isNull()
        window.resize(700, 500)
        app.processEvents()
        window.thumbnails.update_viewport()
        drain(window)
        viewport = window.pages.viewport().rect()
        for row in range(window.pages.count()):
            item = window.pages.item(row)
            if window.pages.visualItemRect(item).intersects(viewport):
                assert not item.icon().isNull()
        assert len(window.thumbnails.resident) <= 64

        # A pending render for the previous document must never touch the new one.
        window.pages.scrollToItem(window.pages.item(199))
        window.thumbnails.update_viewport()
        window.model.close()
        window.model.doc = fitz.open()
        window.model.doc.new_page()
        with patch.object(window.thumbnails, 'render_icon') as render:
            window.thumbnails.render_batch()
            render.assert_not_called()
        window.refresh()
        drain(window)
        assert window.pages.count() == 1
        assert not window.pages.item(0).icon().isNull()
    finally:
        window.model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()
