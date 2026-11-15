import hashlib
import json
import platform

import pytest

import launch_uv


@pytest.fixture
def environment(tmp_path, monkeypatch):
    lock = b'example==1.0 --hash=sha256:example\n'
    (tmp_path / 'requirements-windows-uv.lock').write_bytes(lock)
    profile = {'python': {'version': '3.12.16'},
               'lock_sha256': hashlib.sha256(lock).hexdigest(),
               'dependencies': {'example': '1.0'}}
    (tmp_path / 'windows-uv-runtime.json').write_text(json.dumps(profile), encoding='utf-8')
    monkeypatch.setattr(launch_uv.sys, 'platform', 'win32')
    monkeypatch.setattr(launch_uv.sys, 'version_info', (3, 12, 16))
    monkeypatch.setattr(launch_uv.sys, 'prefix', str(tmp_path / '.venv'))
    monkeypatch.setattr(launch_uv.sys, 'base_prefix', str(tmp_path / 'python'))
    monkeypatch.setattr(launch_uv.struct, 'calcsize', lambda _: 8)
    monkeypatch.setattr(platform, 'machine', lambda: 'AMD64')
    monkeypatch.setattr(platform, 'python_implementation', lambda: 'CPython')
    monkeypatch.setattr('folimeld.windows_integration.is_packaged', lambda: False)
    monkeypatch.setattr(launch_uv, 'version', lambda _: '1.0')
    return tmp_path


def test_matching_dedicated_environment_is_accepted(environment):
    launch_uv.validate_environment(environment)


def test_shared_environment_is_rejected(environment, monkeypatch):
    monkeypatch.setattr(launch_uv.sys, 'prefix', str(environment / 'other'))
    with pytest.raises(RuntimeError, match='.venv'):
        launch_uv.validate_environment(environment)


def test_dependency_drift_is_rejected(environment, monkeypatch):
    monkeypatch.setattr(launch_uv, 'version', lambda _: '2.0')
    with pytest.raises(RuntimeError, match='Dependency version'):
        launch_uv.validate_environment(environment)


def test_lock_drift_is_rejected(environment):
    (environment / 'requirements-windows-uv.lock').write_text('changed')
    with pytest.raises(RuntimeError, match='dependency lock'):
        launch_uv.validate_environment(environment)


def test_python_patch_drift_is_rejected(environment, monkeypatch):
    monkeypatch.setattr(launch_uv.sys, 'version_info', (3, 12, 15))
    with pytest.raises(RuntimeError, match='Python version'):
        launch_uv.validate_environment(environment)


def test_windows_checkout_line_endings_do_not_invalidate_lock(environment):
    path = environment / 'requirements-windows-uv.lock'
    path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
    launch_uv.validate_environment(environment)


def test_distribution_lock_matches_runtime_pins():
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    profile = json.loads((root / 'windows-uv-runtime.json').read_text(encoding='utf-8'))
    text = (root / 'requirements-windows-uv.lock').read_text(encoding='utf-8')
    pins = dict(re.findall(r'^([\w.-]+)==([^\s\\]+)', text, re.M))
    assert pins == profile['dependencies'] and len(pins) == 14
    assert len(re.findall(r'--hash=sha256:[0-9a-f]{64}', text)) == 14
    assert hashlib.sha256(text.encode('utf-8')).hexdigest() == profile['lock_sha256']
