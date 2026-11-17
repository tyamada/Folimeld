from unittest.mock import patch

import fitz
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow


def make_window():
    with patch("folimeld.app.is_packaged", return_value=False):
        window = MainWindow()
    window.show()
    QApplication.processEvents()
    return window


def test_empty_prompt_is_dismissible_and_all_menus_remain_available():
    window = make_window()
    dialog = window.empty_dialog
    assert dialog.isVisible()
    assert dialog.windowModality() == Qt.WindowModality.NonModal
    assert not dialog.isModal()
    assert QApplication.activeModalWidget() is None
    assert all(action.isEnabled() for action in window.menuBar().actions())
    assert all(action.isEnabled() for action in (
        window.open_action, window.import_images_action, window.exit_action,
        window.help_action))
    assert not window.close_pdf_action.isEnabled()
    window.help_action.trigger()
    assert window.help_dialog.isVisible()
    assert dialog.isVisible()
    window.empty_close_button.click()
    assert not dialog.isVisible()
    window.update_state()
    QApplication.processEvents()
    assert not dialog.isVisible()  # Do not trap the user in a reopening prompt.
    window.close()


def test_prompt_buttons_and_file_actions_use_existing_entry_points():
    window = make_window()
    with patch.object(window, "select_pdf", return_value="") as select:
        window.empty_open_button.click()
        window.open_action.trigger()
        assert select.call_count == 2
    with patch("folimeld.app.select_image_folder", return_value="") as select:
        window.empty_import_button.click()
        window.import_images_action.trigger()
        assert select.call_count == 2
    assert window.empty_dialog.isVisible()
    window.exit_action.trigger()
    assert not window.isVisible()
    assert not window.empty_dialog.isVisible()


def test_close_pdf_confirms_unsaved_changes_and_reopens_prompt(tmp_path):
    path = tmp_path / "sample.pdf"
    with fitz.open() as pdf:
        pdf.new_page()
        pdf.save(path)
    window = make_window()
    window.open_path(str(path))
    assert not window.empty_dialog.isVisible()
    assert window.close_pdf_action.isEnabled()
    window.model.rotate([0], 90)
    with patch.object(window, "confirm_discard", return_value=False):
        window.close_pdf_action.trigger()
    assert window.model.loaded and window.model.dirty
    with patch.object(window, "confirm_discard", return_value=True):
        window.close_pdf_action.trigger()
    assert not window.model.loaded
    assert not window.model.can_undo
    assert window.pages.count() == 0
    assert not window.thumbnails.pending
    assert window.empty_dialog.isVisible()
    assert not window.close_pdf_action.isEnabled()
    window.open_path(str(path))
    QApplication.processEvents()
    assert window.model.loaded
    assert window.pages.count() == 1
    assert not window.thumbnails.paused
    assert not window.empty_dialog.isVisible()
    window.close()


def test_pdf_opened_before_startup_prompt_suppresses_it(tmp_path):
    path = tmp_path / "startup.pdf"
    with fitz.open() as pdf:
        pdf.new_page()
        pdf.save(path)
    with patch("folimeld.app.is_packaged", return_value=False):
        window = MainWindow()
    window.open_path(str(path))
    window.show()
    QApplication.processEvents()
    assert window.empty_dialog is None
    window.close()


def test_empty_prompt_dismisses_with_escape_and_window_close():
    from PySide6.QtTest import QTest
    window = make_window()
    QTest.keyClick(window.empty_dialog, Qt.Key.Key_Escape)
    assert not window.empty_dialog.isVisible()
    assert window.isVisible()
    window.show_empty_dialog()
    window.empty_dialog.close()
    assert not window.empty_dialog.isVisible()
    assert window.isVisible()
    window.close()
