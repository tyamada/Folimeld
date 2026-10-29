from unittest.mock import patch

import fitz
import pytest
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from folimeld.app import MainWindow


def crash_worker(source, destination, options, connection):
    # A native library can exit without a Python exception or result message.
    connection.close()


@pytest.mark.parametrize('failure', [False, True])
def test_spawned_save_keeps_qt_responsive_and_preserves_editing(tmp_path, failure):
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
    ticks = []
    timer = QTimer(window)
    timer.setInterval(5)

    def heartbeat():
        ticks.append(window.confirm_discard())
        assert not window._save_to(str(tmp_path / 'reentrant.pdf'))
        dialog = QApplication.activeModalWidget()
        if dialog is not None:
            dialog.reject()
            assert dialog.isVisible()

    timer.timeout.connect(heartbeat)
    try:
        window.model.doc = fitz.open()
        window.model.doc.new_page().insert_text((30, 40), 'Edited PDF')
        window.model.set_view_password('secret')
        window.model.rotate([0], 90)
        destination = tmp_path / 'saved.pdf'
        destination.write_bytes(b'Existing destination')
        timer.start()
        with patch.object(QMessageBox, 'critical') as report:
            if failure:
                with patch('folimeld.pdf_save.save_worker', crash_worker):
                    assert not window._save_to(str(destination))
                report.assert_called_once()
                assert destination.read_bytes() == b'Existing destination'
                assert window.model.dirty and window.model.path is None
            else:
                assert window._save_to(str(destination))
                report.assert_not_called()
                assert not window.model.dirty
                with fitz.open(destination) as saved:
                    assert saved.needs_pass and saved.authenticate('secret')
                    assert saved[0].rotation == 90
                    assert saved[0].get_text().strip() == 'Edited PDF'
        assert ticks and not any(ticks)
        assert not window._saving and not window.thumbnails.paused
        assert window.model.undo() and window.model.doc[0].rotation == 0
        assert window.model.redo() and window.model.doc[0].rotation == 90
        assert {p.name for p in tmp_path.iterdir()} == {'saved.pdf'}
    finally:
        timer.stop()
        window.model.dirty = False
        window.close()


def test_spawned_save_reports_python_failure_and_preserves_model(tmp_path):
    from folimeld.model import PdfDocument
    from folimeld.pdf_save import save_with_progress

    model = PdfDocument()
    model.doc = fitz.open()
    model.doc.new_page()
    model.rotate([0], 90)
    try:
        def writer(document, destination, options):
            save_with_progress(document, destination, {**options, 'garbage': 'invalid'}, None, 'Saving')

        with pytest.raises(OSError):
            model.save(str(tmp_path / 'saved.pdf'), writer=writer)
        assert model.doc[0].rotation == 90 and model.dirty and model.can_undo
        assert not list(tmp_path.iterdir())
    finally:
        model.close()
