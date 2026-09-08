import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import fitz
import pytest
from PySide6.QtWidgets import QApplication

from folimeld.android_probe import ProbeSession, ProbeWindow, copy_file


@pytest.fixture
def sample(tmp_path):
    path = tmp_path / "source.pdf"
    with fitz.open() as doc:
        page = doc.new_page(width=300, height=500)
        page.insert_text((30, 40), "Android probe")
        doc.new_page(width=400, height=600)
        doc.save(path)
    return path


def test_open_render_rotate_export_reopen(sample, tmp_path):
    session = ProbeSession()
    try:
        original = sample.read_bytes()
        session.open(str(sample))
        assert not session.preview(0).isNull()
        session.pdf.rotate([0], 90)
        assert session.preview(0).width() > session.preview(0).height()
        destination = tmp_path / "export.pdf"
        session.export(str(destination))
        assert not session.pdf.dirty
        assert sample.read_bytes() == original
        with fitz.open(destination) as doc:
            assert doc.page_count == 2
            assert doc[0].rotation == 90
            assert "Android probe" in doc[0].get_text()
        session.open(str(destination))
        assert session.pdf.doc[0].rotation == 90
    finally:
        session.close()


def test_failed_export_retains_edit(sample, tmp_path):
    session = ProbeSession()
    try:
        session.open(str(sample))
        session.pdf.rotate([0], 90)
        with pytest.raises(OSError):
            session.export(str(tmp_path / "missing" / "out.pdf"))
        assert session.pdf.dirty
        assert session.pdf.doc[0].rotation == 90
    finally:
        session.close()


def test_failed_open_retains_previous_document(sample, tmp_path):
    session = ProbeSession()
    try:
        session.open(str(sample))
        session.pdf.rotate([0], 90)
        invalid = tmp_path / "invalid.pdf"
        invalid.write_text("not a PDF")
        with pytest.raises(Exception):
            session.open(str(invalid))
        assert session.pdf.dirty
        assert session.pdf.doc[0].rotation == 90
    finally:
        session.close()


def test_qfile_copy_spans_chunks_and_truncates(tmp_path):
    source, destination = tmp_path / "in", tmp_path / "out"
    data = b"0123456789" * 300000
    source.write_bytes(data)
    destination.write_bytes(data * 2)
    copy_file(str(source), str(destination))
    assert destination.read_bytes() == data


def test_window_navigation_and_rotation(sample):
    app = QApplication.instance() or QApplication([])
    window = ProbeWindow()
    try:
        assert not window.save_button.isEnabled()
        window.session.open(str(sample))
        window.refresh()
        assert not window.previous.isEnabled()
        assert window.next.isEnabled()
        window.next.click()
        assert window.page == 1
        assert not window.next.isEnabled()
        window.rotate_button.click()
        assert window.session.pdf.doc[1].rotation == 90
        assert not window.image.pixmap().isNull()
    finally:
        window.session.pdf.dirty = False
        window.close()
        app.processEvents()
