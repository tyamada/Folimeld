import io
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import fitz
import pytest

from folimeld.history import Snapshot
from folimeld.model import PdfDocument
from folimeld.temporary_data import (CHUNK_SIZE, MAGIC, OVERHEAD, decrypt_from,
                                     encrypt_to, new_key)


@pytest.mark.parametrize('size', [0, 16, 24, 33])
def test_only_256_bit_keys_are_accepted(size):
    encrypted = io.BytesIO()
    encrypt_to(encrypted, b'Sensitive bytes', new_key())
    with pytest.raises(ValueError, match='256-bit'):
        encrypt_to(io.BytesIO(), b'Sensitive bytes', b'x' * size)
    with pytest.raises(OSError, match='authenticated'):
        decrypt_from(encrypted, b'x' * size)


@pytest.mark.parametrize('size', [0, 17, CHUNK_SIZE + 31])
def test_encrypted_round_trip_and_randomized_ciphertext(size):
    data = (b'Sensitive PDF content. ' * (size // 23 + 1))[:size]
    key = new_key()
    first, second = io.BytesIO(), io.BytesIO()
    encrypt_to(first, data, key)
    encrypt_to(second, data, key)
    assert first.getvalue() != second.getvalue()
    assert len(first.getvalue()) == len(data) + OVERHEAD
    if size > 100:
        assert b'Sensitive PDF content.' not in first.getvalue()
    assert decrypt_from(first, key) == decrypt_from(second, key) == data


@pytest.mark.parametrize('corrupt', ['header', 'nonce', 'ciphertext', 'tag', 'truncate', 'append', 'key'])
def test_corruption_never_returns_unauthenticated_plaintext(corrupt):
    stream = io.BytesIO()
    key = new_key()
    encrypt_to(stream, b'A confidential document' * 50, key)
    data = bytearray(stream.getvalue())
    if corrupt == 'truncate':
        del data[-20:]
    elif corrupt == 'append':
        data += b'extra'
    elif corrupt == 'key':
        key = new_key()
    else:
        index = {'header': 0, 'nonce': len(MAGIC), 'ciphertext': len(MAGIC) + 12, 'tag': -1}[corrupt]
        data[index] ^= 1
    with pytest.raises(OSError):
        decrypt_from(io.BytesIO(data), key)


def test_short_write_fails_without_releasing_in_memory_snapshot():
    snapshot = Snapshot(b'Original document')
    stream = io.BytesIO()
    with patch('folimeld.history.TemporaryFile', return_value=stream), \
            patch.object(stream, 'write', return_value=1):
        with pytest.raises(OSError, match='Incomplete'):
            snapshot.spill()
    assert stream.closed
    assert snapshot.in_memory and snapshot.read() == b'Original document'
    assert snapshot._key is None and snapshot.disk_size == 0
    snapshot.close()


def test_corrupted_disk_history_preserves_current_document_and_stacks():
    model = PdfDocument(history_limit_bytes=0)
    model.doc = fitz.open()
    model.doc.new_page().insert_text((20, 30), 'Private text')
    try:
        model.set_view_password('user-secret')
        model.rotate([0], 90)
        snapshot = model._undo[-1].pdf
        stream = snapshot._file
        stream.seek(0)
        stored = stream.read()
        assert b'%PDF' not in stored[:100] and b'user-secret' not in stored
        assert snapshot.disk_size == len(stored) == snapshot.size + OVERHEAD
        stream.seek(len(MAGIC) + 12)
        stream.write(bytes([stored[len(MAGIC) + 12] ^ 1]))
        stream.flush()
        before = model._snapshot()
        history = list(model._undo)
        with pytest.raises(OSError, match='authenticated'):
            model.undo()
        assert model._snapshot() == before
        assert model._undo == history and model.can_undo and model.dirty
        retained_key = snapshot._key
        assert retained_key is not None
    finally:
        model.close()
    assert snapshot._key is None and stream.closed


def test_disk_budget_includes_encryption_overhead():
    model = PdfDocument(history_limit_bytes=0)
    model.doc = fitz.open()
    model.doc.new_page()
    try:
        model.history_disk_limit_bytes = len(model._snapshot().pdf)
        model.rotate([0], 90)
        assert not model.can_undo and model.history_disk_bytes == 0
    finally:
        model.close()


def test_save_worker_authenticates_input_before_parsing_pdf(tmp_path):
    from folimeld.pdf_save import save_worker

    source = tmp_path / 'source.encrypted'
    with source.open('wb') as stream:
        encrypt_to(stream, b'PDF data that must not be parsed with a wrong key', new_key())
    connection = type('Connection', (), {'send': lambda self, message: setattr(self, 'message', message),
                                          'close': lambda self: None})()
    with patch('folimeld.pdf_save.fitz.open') as parse_pdf:
        save_worker(str(source), str(tmp_path / 'output.pdf'), {}, connection, new_key())
        parse_pdf.assert_not_called()
    assert connection.message[0] == 'error'
    assert not (tmp_path / 'output.pdf').exists()


def test_abrupt_process_exit_leaves_ciphertext_without_a_key_file(tmp_path):
    source = '''
import os, sys
from folimeld.temporary_data import encrypt_to, new_key
stream = open(sys.argv[1], 'wb')
encrypt_to(stream, b'%PDF confidential document content' * 100, new_key())
os._exit(17)
'''
    destination = tmp_path / 'staging.encrypted'
    result = subprocess.run([sys.executable, '-c', source, str(destination)],
                            cwd=Path(__file__).resolve().parent.parent,
                            capture_output=True, timeout=30)
    assert result.returncode == 17, result.stderr
    stored = destination.read_bytes()
    assert stored.startswith(MAGIC) and b'%PDF confidential document content' not in stored
    assert list(tmp_path.iterdir()) == [destination]
    with pytest.raises(OSError, match='authenticated'):
        decrypt_from(io.BytesIO(stored), new_key())
