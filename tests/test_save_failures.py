from pathlib import Path
from unittest.mock import patch

import fitz
import pytest

from folimeld.model import PdfDocument


@pytest.mark.parametrize('failure', ['write', 'replace', 'reopen'])
@pytest.mark.parametrize('encrypted', [False, True])
@pytest.mark.parametrize('overwrite', [False, True])
def test_failed_save_preserves_editing_and_history(tmp_path, failure, encrypted, overwrite):
    source = tmp_path / 'source.pdf'
    model = PdfDocument()
    model.doc = fitz.open()
    model.doc.new_page()
    if encrypted:
        model.set_view_password('secret')
    model.save(str(source))
    original = source.read_bytes()
    destination = source if overwrite else tmp_path / 'destination.pdf'
    if not overwrite:
        destination.write_bytes(original)
    model.rotate([0], 90)
    revision = model._saved_revision
    real_open = fitz.open

    def open_document(*args, **kwargs):
        if args and str(args[0]) == str(destination):
            raise OSError('simulated reopen failure')
        return real_open(*args, **kwargs)

    def partial_write(document, filename, **kwargs):
        Path(filename).write_bytes(b'incomplete PDF')
        raise OSError('simulated write failure')

    if failure == 'write':
        context = patch.object(fitz.Document, 'save', autospec=True, side_effect=partial_write)
    elif failure == 'replace':
        context = patch.object(Path, 'replace', side_effect=PermissionError('simulated file lock'))
    else:
        context = patch('folimeld.model.fitz.open', side_effect=open_document)
    try:
        with context, pytest.raises(OSError):
            model.save(str(destination))
        assert model.loaded and not model.doc.is_closed
        assert model.doc[0].rotation == 90 and model.dirty
        assert model._saved_revision == revision
        assert model.path == source
        assert model.view_password == ('secret' if encrypted else None)
        if failure != 'reopen':
            assert destination.read_bytes() == original
        if not overwrite:
            assert source.read_bytes() == original
        assert set(tmp_path.iterdir()) == {source, destination}
        assert model.undo() and model.doc[0].rotation == 0
        assert model.redo() and model.doc[0].rotation == 90
        model.save(str(destination))
        assert not model.dirty
        recovered = tmp_path / 'recovered.pdf'
        model.save(str(recovered))
        assert not model.dirty
        with fitz.open(recovered) as saved:
            assert bool(saved.needs_pass) == encrypted
            if encrypted:
                assert saved.authenticate('secret')
            assert saved[0].rotation == 90
    finally:
        model.close()
