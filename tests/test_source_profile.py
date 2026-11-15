from pathlib import Path

import pytest

from folimeld import source_profile


@pytest.fixture
def profile(monkeypatch, tmp_path):
    monkeypatch.setattr(source_profile.sys, 'platform', 'win32')
    monkeypatch.setattr(source_profile, 'is_packaged', lambda: False)
    monkeypatch.setattr(source_profile, '_settings_file', None)
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    return tmp_path / 'Folimeld-UV'


def test_uv_settings_are_explicit_persistent_and_have_no_fallback(profile):
    logs = source_profile.activate_source_profile('0.3.5')
    settings = source_profile.application_settings()
    assert Path(settings.fileName()).resolve() == (profile / 'settings/settings.ini').resolve()
    assert not settings.fallbacksEnabled()
    settings.setValue('language', 'ja')
    settings.sync()
    assert source_profile.application_settings().value('language') == 'ja'
    assert logs.parent == profile / 'logs/0.3.5'


def test_sessions_do_not_share_log_directory(profile, monkeypatch):
    first = source_profile.activate_source_profile('0.3.5')
    monkeypatch.setattr(source_profile, '_settings_file', None)
    second = source_profile.activate_source_profile('0.3.5')
    assert first != second and first.is_dir() and second.is_dir()


def test_packaged_process_is_rejected_before_creating_profile(profile, monkeypatch):
    monkeypatch.setattr(source_profile, 'is_packaged', lambda: True)
    with pytest.raises(RuntimeError, match='unpackaged'):
        source_profile.activate_source_profile('0.3.5')
    assert not profile.exists()


def test_missing_localappdata_does_not_fall_back_to_store(profile, monkeypatch):
    monkeypatch.delenv('LOCALAPPDATA')
    with pytest.raises(RuntimeError, match='LOCALAPPDATA'):
        source_profile.activate_source_profile('0.3.5')
    assert source_profile._settings_file is None


def test_unwritable_profile_does_not_fall_back(profile, monkeypatch):
    profile.write_text('blocking file')
    with pytest.raises(OSError):
        source_profile.activate_source_profile('0.3.5')
    assert source_profile._settings_file is None


def test_default_settings_constructor_is_preserved(monkeypatch):
    from PySide6 import QtCore

    monkeypatch.setattr(source_profile, '_settings_file', None)
    calls = []
    sentinel = object()

    def constructor(*args):
        calls.append(args)
        return sentinel

    monkeypatch.setattr(QtCore, 'QSettings', constructor)
    assert source_profile.application_settings() is sentinel
    assert calls == [()]
