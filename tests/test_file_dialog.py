import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QFileDialog, QFileSystemModel

from folimeld.app import MainWindow
from folimeld.folder_dialog import select_image_folder


class FileDialogTests(unittest.TestCase):
    def test_image_folder_picker_shows_files_but_accepts_only_directories(self):
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as directory:
            for name in ("image.png", "notes.txt", "document.pdf"):
                (Path(directory) / name).touch()
            (Path(directory) / "subfolder").mkdir()
            parent = Mock()
            parent.tr_.return_value = "Import images"
            settings = Mock()
            settings.value.return_value = directory
            observed = []

            def inspect_picker():
                for widget in app.topLevelWidgets():
                    if isinstance(widget, QFileDialog):
                        model = widget.findChild(QFileSystemModel)
                        root = model.index(directory)
                        names = {model.fileName(model.index(row, 0, root))
                                 for row in range(model.rowCount(root))}
                        observed.append((widget.fileMode(), names))
                        widget.reject()

            QTimer.singleShot(250, inspect_picker)
            original = select_image_folder
            with patch("folimeld.app.QSettings", return_value=settings), patch(
                "folimeld.app.select_image_folder",
                wraps=select_image_folder,
            ) as picker:
                # A real QWidget is unnecessary for this method's other actions.
                picker.side_effect = lambda _parent, *args, **kwargs: original(None, *args, **kwargs)
                MainWindow.import_image_folder(parent)
            self.assertEqual(len(observed), 1)
            self.assertEqual(observed[0][0], QFileDialog.FileMode.Directory)
            self.assertTrue({"image.png", "notes.txt", "document.pdf", "subfolder"} <= observed[0][1])
            settings.setValue.assert_not_called()

    def test_uses_and_remembers_last_open_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = str(Path(directory) / "document.pdf")
            parent = object()
            settings = Mock()
            settings.value.return_value = directory
            with patch("folimeld.app.QSettings", return_value=settings), patch(
                "folimeld.app.QFileDialog.getOpenFileName",
                return_value=(selected, "PDF (*.pdf)"),
            ) as dialog:
                result = MainWindow.select_pdf(parent, "Open")

            self.assertEqual(result, selected)
            dialog.assert_called_once_with(parent, "Open", directory, "PDF (*.pdf)")
            settings.setValue.assert_called_once_with("last_open_directory", directory)

    def test_missing_saved_directory_falls_back_to_pictures(self):
        with tempfile.TemporaryDirectory() as pictures:
            settings = Mock()
            parent = object()
            settings.value.return_value = "missing-directory"
            with patch("folimeld.app.QSettings", return_value=settings), patch(
                "folimeld.app.QStandardPaths.writableLocation", return_value=pictures,
            ), patch(
                "folimeld.app.QFileDialog.getOpenFileName", return_value=("", ""),
            ) as dialog:
                result = MainWindow.select_pdf(parent, "Open")

        self.assertEqual(result, "")
        dialog.assert_called_once_with(parent, "Open", pictures, "PDF (*.pdf)")
        settings.setValue.assert_not_called()


if __name__ == "__main__":
    unittest.main()
