"""Small-fixture unit checks; real PDF acquisition is an explicit integration step."""
import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest
import pymupdf as fitz
from tools import sample_inputs as inputs


@pytest.fixture(autouse=True)
def isolated_checkout(tmp_path, monkeypatch):
    monkeypatch.setattr(inputs, 'REPO_ROOT', tmp_path / 'checkout')


def fixture_entry(tmp_path):
    folder=tmp_path/'input';folder.mkdir()
    path=folder/'tiny.pdf'
    with fitz.open() as pdf:
        pdf.new_page();pdf.save(path)
    entry={'sample_id':'ep3_ja','filename':'tiny.pdf','bytes':path.stat().st_size,
           'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    return folder,path,entry


def test_pinned_manifest_and_filipino_alias():
    entries=inputs.pinned_entries()
    assert len(entries)==51
    assert any(e['sample_id']=='ep1_fil' for e in entries)
    assert inputs.MANIFEST_URL.endswith('/manga-pdf-20261103-v1/pdf-manifest.json')


def test_explicit_input_verification_and_no_network(tmp_path):
    folder,path,entry=fixture_entry(tmp_path)
    with patch.object(inputs,'pinned_entries',return_value=[entry]),patch.object(inputs,'download_sample',side_effect=AssertionError('No network')):
        assert inputs.resolve_sample_input(input_dir=folder)==path
        path.write_bytes(b'corrupt')
        with pytest.raises(ValueError,match='mismatch'):
            inputs.resolve_sample_input(input_dir=folder)


def test_missing_input_fails_instead_of_skip(tmp_path):
    with pytest.raises(FileNotFoundError,match='Prepare the required input'):
        inputs.resolve_sample_input(cache_dir=tmp_path/'cache')


def test_cache_and_download_are_opt_in(tmp_path):
    folder,path,entry=fixture_entry(tmp_path)
    with patch.object(inputs,'pinned_entries',return_value=[entry]),patch.object(inputs,'download_sample',return_value=path) as download:
        assert inputs.resolve_sample_input(cache_dir=tmp_path/'cache',download=True)==path
        download.assert_called_once()
    original=tmp_path/'cache/originals'/ (entry['sha256']+'.pdf')
    original.parent.mkdir(parents=True);original.write_bytes(path.read_bytes())
    with patch.object(inputs,'pinned_entries',return_value=[entry]),patch.object(inputs,'download_sample',side_effect=AssertionError('Offline')):
        assert inputs.resolve_sample_input(cache_dir=tmp_path/'cache')==original


def test_filipino_alias_resolves_without_changing_ids(tmp_path):
    folder,path,entry=fixture_entry(tmp_path);entry['sample_id']='ep1_fil'
    with patch.object(inputs,'pinned_entries',return_value=[entry]):
        assert inputs.resolve_sample_input('ep1_tl',input_dir=folder)==path


def test_repository_cache_is_rejected():
    with pytest.raises(ValueError,match='outside'):
        inputs.external_directory(inputs.REPO_ROOT/'build/sample-cache')


def test_user_pages_link_to_catalogues_without_individual_comic_links():
    import re
    root=Path(__file__).resolve().parents[1]
    for name,lang in [('README.md','en'),('README_ja.md','ja'),('docs/index.html','en'),('docs/index_ja.html','ja')]:
        text=(root/name).read_text(encoding='utf-8')
        assert 'https://tyamada.github.io/manga-prompt-kit/samples/'+lang+'/' in text
        assert not re.search(r'(?:href=["\']|\]\()[^\s"\')<>]*tameshibu[^\s"\')<>]*\.pdf',text,re.I)
