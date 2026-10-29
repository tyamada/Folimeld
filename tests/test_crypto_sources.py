import hashlib
import io
import json
import tarfile
from unittest.mock import patch

import pytest

from tools.fetch_crypto_sources import download, legal_texts, verified_sdist


def test_download_rejects_corruption_preserving_existing_file(tmp_path):
    destination = tmp_path / 'source.crate'
    destination.write_bytes(b'existing')
    with patch('tools.fetch_crypto_sources.urlopen', return_value=io.BytesIO(b'corrupted')):
        with pytest.raises(ValueError, match='Checksum mismatch'):
            download('https://static.crates.io/example', destination, hashlib.sha256(b'expected').hexdigest())
    assert destination.read_bytes() == b'existing'
    assert not destination.with_suffix('.crate.part').exists()


def test_download_reuses_only_verified_files(tmp_path):
    destination = tmp_path / 'source.crate'
    data = b'verified'
    digest = hashlib.sha256(data).hexdigest()
    with patch('tools.fetch_crypto_sources.urlopen', return_value=io.BytesIO(data)) as fetch:
        download('https://static.crates.io/example', destination, digest)
        assert fetch.call_count == 1
    with patch('tools.fetch_crypto_sources.urlopen', side_effect=AssertionError('Unexpected network')):
        download('https://static.crates.io/example', destination, digest)


@pytest.mark.parametrize('filename', ['../source.tar.gz', '..\\source.tar.gz'])
def test_sdist_rejects_unsafe_record_paths(tmp_path, filename):
    record = {'package': 'cryptography==50.0.2', 'files': [{'filename': filename, 'sha256': '0' * 64}]}
    (tmp_path / 'cryptography==50.0.2.json').write_text(json.dumps(record))
    with pytest.raises(ValueError, match='Unsafe source filename'):
        verified_sdist(tmp_path, 'cryptography', '50.0.2')


def test_sdist_rejects_modified_source(tmp_path):
    record = {'package': 'cffi==2.1.1', 'files': [{'filename': 'cffi.tar.gz', 'sha256': '0' * 64}]}
    (tmp_path / 'cffi==2.1.1.json').write_text(json.dumps(record))
    (tmp_path / 'cffi.tar.gz').write_bytes(b'modified')
    with pytest.raises(ValueError, match='Source checksum mismatch'):
        verified_sdist(tmp_path, 'cffi', '2.1.1')


def test_legal_texts_read_nested_documents_without_extracting_paths(tmp_path):
    source = tmp_path / 'example.tar.gz'
    with tarfile.open(source, 'w:gz') as archive:
        for name, text in [('example/LICENSE', b'root notice'), ('example/vendor/NOTICE', b'vendor notice')]:
            entry = tarfile.TarInfo(name)
            entry.size = len(text)
            archive.addfile(entry, io.BytesIO(text))
        link = tarfile.TarInfo('example/COPYING')
        link.type = tarfile.SYMTYPE
        link.linkname = '/outside'
        archive.addfile(link)
    result = legal_texts(source)
    assert 'root notice' in result and 'vendor notice' in result
    assert 'COPYING' not in result
    assert list(tmp_path.iterdir()) == [source]


def test_missing_legal_documents_fail(tmp_path):
    source = tmp_path / 'empty.tar.gz'
    with tarfile.open(source, 'w:gz'):
        pass
    with pytest.raises(ValueError, match='No license documents'):
        legal_texts(source)
