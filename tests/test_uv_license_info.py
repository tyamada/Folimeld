import hashlib
import json
from pathlib import Path
import shutil

import pytest

from folimeld import license_info, source_profile
from folimeld.uv_license_info import uv_license_documents


@pytest.fixture
def legal_root(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    (tmp_path / 'documentation').mkdir()
    shutil.copytree(repo / 'documentation/windows-uv-licenses',
                    tmp_path / 'documentation/windows-uv-licenses')
    for name in ('LICENSE', 'windows-uv-runtime.json'):
        shutil.copyfile(repo / name, tmp_path / name)
    return tmp_path


def test_uv_inventory_uses_all_runtime_pins_and_no_pyinstaller(legal_root, monkeypatch):
    profile = json.loads((legal_root / 'windows-uv-runtime.json').read_text())
    calls = []

    def lookup(name):
        calls.append(name)
        return profile['dependencies'][name]

    monkeypatch.setattr('folimeld.uv_license_info.version', lookup)
    documents = dict(uv_license_documents(legal_root))
    assert set(calls) == set(profile['dependencies'])
    assert len(calls) == 14
    assert 'typing-extensions' in calls and 'PyInstaller' not in calls
    assert 'typing-extensions: installed 4.16.0' in documents['Windows uv installed packages']
    assert 'MIT License' in documents['Windows uv notices']
    assert 'Virtual Keyboard' in documents['Windows uv notices']


def test_uv_routing_does_not_read_stale_bundled_installed_notices(legal_root, monkeypatch):
    (legal_root / 'licenses').mkdir()
    (legal_root / 'licenses/Installed-packages.txt').write_text('OLD BUILD INVENTORY')
    monkeypatch.setattr(license_info.sys, '_MEIPASS', str(legal_root), raising=False)
    monkeypatch.setattr(license_info.sys, 'frozen', False, raising=False)
    monkeypatch.setattr(source_profile, 'source_profile_active', lambda: True)
    documents = dict(license_info.license_documents())
    assert 'Installed-packages' not in documents
    assert 'OLD BUILD INVENTORY' not in '\n'.join(documents.values())
    assert 'Windows uv sources' in documents


def test_frozen_store_route_preserves_bundled_notices(legal_root, monkeypatch):
    (legal_root / 'licenses').mkdir()
    (legal_root / 'licenses/Installed-packages.txt').write_text('EXISTING STORE INVENTORY')
    monkeypatch.setattr(license_info.sys, '_MEIPASS', str(legal_root), raising=False)
    monkeypatch.setattr(license_info.sys, 'frozen', True, raising=False)
    monkeypatch.setattr(source_profile, 'source_profile_active', lambda: True)
    documents = dict(license_info.license_documents())
    assert documents['Installed-packages'] == 'EXISTING STORE INVENTORY'
    assert 'Windows uv sources' not in documents


def test_uv_inventory_detects_notice_changes_but_allows_crlf(legal_root):
    path = legal_root / 'documentation/windows-uv-licenses/notices.txt'
    raw = path.read_bytes()
    path.write_bytes(raw.replace(b'\n', b'\r\n'))
    uv_license_documents(legal_root)
    path.write_bytes(raw + b'changed')
    with pytest.raises(ValueError, match='notice hash'):
        uv_license_documents(legal_root)


def test_uv_inventory_rejects_stale_dependency_or_runtime(legal_root):
    path = legal_root / 'windows-uv-runtime.json'
    profile = json.loads(path.read_text())
    profile['dependencies']['typing-extensions'] = '0.0'
    path.write_text(json.dumps(profile))
    with pytest.raises(ValueError, match='runtime profile'):
        uv_license_documents(legal_root)


def test_uv_view_reports_actual_version_drift(legal_root, monkeypatch):
    monkeypatch.setattr('folimeld.uv_license_info.version', lambda _: '0.0')
    documents = dict(uv_license_documents(legal_root))
    assert 'installed 0.0; pinned' in documents['Windows uv installed packages']
    assert 'DIFFERS FROM PIN' in documents['Windows uv installed packages']


def test_uv_profile_query_has_no_side_effect(monkeypatch):
    monkeypatch.setattr(source_profile, '_settings_file', None)
    assert not source_profile.source_profile_active()
    monkeypatch.setattr(source_profile, '_settings_file', Path('settings.ini'))
    assert source_profile.source_profile_active()


def test_ledger_source_status_and_notice_hash_are_explicit(legal_root):
    directory = legal_root / 'documentation/windows-uv-licenses'
    ledger = json.loads((directory / 'sources.json').read_text())
    assert hashlib.sha256((directory / 'notices.txt').read_bytes()).hexdigest() == ledger['notice_sha256']
    assert len(ledger['packages']) == 14
    assert sum(bool(item['sdists']) for item in ledger['packages']) == 10
    assert all('not verified' in item['source_verification'] for item in ledger['packages'])
