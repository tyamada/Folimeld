"""Run against installed files, with no checkout or development venv on sys.path."""
from multiprocessing import freeze_support
from pathlib import Path
import json
import tempfile

import pymupdf
from PIL import Image
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow
from folimeld.image_import import inventory
from folimeld.image_import_dialog import ImageImportDialog


def main():
    assert pymupdf.__file__.startswith('/usr/pkg/share/folimeld/vendor/')
    application = QApplication([])
    window = MainWindow()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        with pymupdf.open() as document:
            page = document.new_page()
            widget = pymupdf.Widget()
            widget.field_name = 'test'
            widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
            widget.field_value = 'Package form'
            widget.rect = pymupdf.Rect(20, 20, 180, 50)
            page.add_widget(widget)
            document.save(root / 'form.pdf')
        window.open_path(str(root / 'form.pdf'))
        window.model.rotate([0], 90)
        assert window.model.undo() and window.model.redo()
        assert window._save_to(str(root / 'saved.pdf'))
        window.open_path(str(root / 'saved.pdf'))
        assert window.model.doc[0].rotation == 90
        assert next(window.model.doc[0].widgets()).field_value == 'Package form'
        Image.new('RGB', (64, 48), 'red').save(root / '1.png')
        Image.new('RGB', (64, 48), 'blue').save(root / '2.tiff', save_all=True,
                                               append_images=[Image.new('RGB', (64, 48), 'green')])
        dialog = ImageImportDialog(inventory(root), window.tr_)
        assert dialog.convert(window.model)
        assert window.model.doc.page_count == 3
        assert window._save_to(str(root / 'images.pdf'))
        window.open_path(str(root / 'images.pdf'))
        assert window.model.doc.page_count == 3
        window.model.close()
        window.close()
        dialog.deleteLater()
        window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        application.processEvents()
    print(json.dumps({'passed': True, 'pymupdf': pymupdf.VersionBind,
                      'module': pymupdf.__file__, 'form_save': True,
                      'undo_redo': True, 'image_worker_pages': 3, 'save_worker': True}))


if __name__ == '__main__':
    freeze_support()
    main()

