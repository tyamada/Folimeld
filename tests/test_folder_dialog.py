import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow
from folimeld.folder_dialog import onedrive_directories, select_image_folder


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows registry integration')
def test_onedrive_environment_deduplicates_and_ignores_missing(tmp_path):
    import winreg
    with patch('folimeld.folder_dialog.sys.platform', 'win32'), patch.dict(
        'os.environ', {'OneDrive': str(tmp_path), 'OneDriveConsumer': str(tmp_path),
                       'OneDriveCommercial': str(tmp_path / 'missing')}, clear=True,
    ), patch.object(winreg, 'OpenKey', side_effect=OSError):
        assert onedrive_directories() == [tmp_path]


def test_onedrive_not_added_on_other_platforms():
    with patch('folimeld.folder_dialog.sys.platform', 'linux'):
        assert onedrive_directories() == []


def test_folder_picker_adds_onedrive_sidebar_and_returns_folder(tmp_path):
    app = QApplication.instance() or QApplication([])
    observed = []

    def accept(dialog):
        observed.extend(dialog.sidebarUrls())
        dialog.selectFile(str(tmp_path))
        return 1

    with patch('folimeld.folder_dialog.onedrive_directories', return_value=[tmp_path]), patch(
        'folimeld.folder_dialog.QFileDialog.exec', accept,
    ):
        assert Path(select_image_folder(None, 'Images', str(tmp_path))) == tmp_path
    assert QUrl.fromLocalFile(str(tmp_path)) in observed


def test_exit_action_preserves_unsaved_confirmation():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    with patch.object(window, 'confirm_discard', return_value=False) as confirm:
        window.exit_action.trigger()
        assert window.isVisible()
        confirm.assert_called_once()
    with patch.object(window, 'confirm_discard', return_value=True) as confirm:
        window.exit_action.trigger()
        assert not window.isVisible()
        confirm.assert_called_once()
