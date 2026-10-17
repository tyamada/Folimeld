import multiprocessing
from pathlib import Path
from unittest.mock import patch

import fitz
import pytest
from PIL import Image
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QProgressDialog

from folimeld.image_import import ImageEntry, convert_images, inventory, sort_entries
from folimeld.image_import_dialog import ImageImportDialog
from folimeld.model import PdfDocument


@pytest.mark.parametrize('field', ['name', 'created', 'modified'])
@pytest.mark.parametrize('descending', [False, True])
def test_order(field, descending):
    entries = [ImageEntry(Path(name), created, modified) for name, created, modified in
               [('10.png', 2, 1), ('2.png', 1, 2), ('1.png', 1, 2), ('3.png', None, None)]]
    expected = {
        ('name', False): ['1.png', '2.png', '3.png', '10.png'],
        ('name', True): ['10.png', '3.png', '2.png', '1.png'],
        ('created', False): ['1.png', '2.png', '10.png', '3.png'],
        ('created', True): ['10.png', '1.png', '2.png', '3.png'],
        ('modified', False): ['10.png', '1.png', '2.png', '3.png'],
        ('modified', True): ['1.png', '2.png', '10.png', '3.png'],
    }
    assert [e.path.name for e in sort_entries(entries, field, descending)] == expected[field, descending]


def test_inventory_does_not_decode_or_recurse(tmp_path):
    (tmp_path / '2.PNG').write_bytes(b'not an image')
    (tmp_path / 'ignore.pdf').touch()
    (tmp_path / 'sub').mkdir()
    (tmp_path / 'sub' / '1.jpg').touch()
    with patch('PIL.Image.open', side_effect=AssertionError('Decoded too soon')):
        assert [e.path.name for e in inventory(tmp_path)] == ['2.PNG']


def test_convert_orientation_transparency_tiff_and_save(tmp_path):
    transparent = tmp_path / 'transparent.png'
    Image.new('RGBA', (100, 50), (255, 0, 0, 0)).save(transparent)
    rotated = tmp_path / 'rotated.jpg'
    exif = Image.Exif()
    exif[274] = 6
    Image.new('RGB', (100, 50), 'red').save(rotated, exif=exif)
    tiff = tmp_path / 'multi.tiff'
    Image.new('RGB', (20, 30), 'blue').save(tiff, save_all=True,
                                                   append_images=[Image.new('RGB', (30, 20), 'green')])
    output = tmp_path / 'generated.pdf'
    convert_images([transparent, rotated, tiff], output)
    model = PdfDocument()
    model.open_generated(str(output))
    output.unlink()  # The model must not depend on the temporary file.
    assert model.doc.page_count == 4
    assert model.path is None and model.dirty and not model.can_undo
    assert model.doc[1].rect.height > model.doc[1].rect.width
    assert model.doc[0].get_pixmap().pixel(1, 1) == (255, 255, 255)
    model.rotate([0], 90)
    assert model.undo() and model.dirty
    saved = tmp_path / 'saved.pdf'
    model.save(str(saved))
    assert not model.dirty
    with fitz.open(saved) as doc:
        assert doc.page_count == 4
    model.close()


def test_failure_and_animated_webp(tmp_path):
    broken = tmp_path / 'broken.png'
    broken.write_bytes(b'broken')
    with pytest.raises(ValueError, match='broken.png'):
        convert_images([broken], tmp_path / 'failed.pdf')
    animated = tmp_path / 'animated.webp'
    Image.new('RGB', (10, 10), 'red').save(animated, save_all=True,
                                                  append_images=[Image.new('RGB', (10, 10), 'blue')])
    with pytest.raises(ValueError, match='Animated WebP'):
        convert_images([animated], tmp_path / 'failed.pdf')


def test_dialog_defaults_order_worker_and_cancel(tmp_path):
    app = QApplication.instance() or QApplication([])
    for name, color in [('10.png', 'blue'), ('2.png', 'red')]:
        Image.new('RGB', (50, 100), color).save(tmp_path / name)
    tr = lambda key, **kwargs: key.format(**kwargs)
    dialog = ImageImportDialog(inventory(tmp_path), tr)
    assert dialog.sort.currentData() == 'name'
    assert dialog.direction.currentIndex() == 0
    assert dialog.table.item(0, 0).text() == '2.png'
    dialog.size.setCurrentIndex(1)
    model = PdfDocument()
    assert dialog.convert(model)
    assert model.doc.page_count == 2
    assert model.doc[0].get_pixmap().pixel(200, 200) == (255, 0, 0)
    assert model.doc[0].rect.width == pytest.approx(595, abs=1)
    previous = model.doc

    def cancel():
        for widget in app.topLevelWidgets():
            if isinstance(widget, QProgressDialog):
                widget.cancel()
    QTimer.singleShot(0, cancel)
    assert not dialog.convert(model)
    assert model.doc is previous
    assert not multiprocessing.active_children()
    broken = tmp_path / 'broken.png'
    broken.write_bytes(b'broken')
    dialog.entries.append(ImageEntry(broken, None, None))
    with patch('folimeld.image_import_dialog.QMessageBox.warning') as warning:
        assert not dialog.convert(model)
        assert 'broken.png' in warning.call_args.args[2]
    assert model.doc is previous
    dialog.entries.pop()
    dialog.table.selectRow(0)
    dialog.exclude()
    assert len(dialog.entries) == 1
    model.close()
    dialog.close()
