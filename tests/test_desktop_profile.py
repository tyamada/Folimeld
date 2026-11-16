from pathlib import Path
import pytest
from folimeld import desktop_profile, source_profile, distribution


@pytest.fixture
def desktop(monkeypatch, tmp_path):
    monkeypatch.setattr(desktop_profile.sys, "platform", "win32")
    monkeypatch.setattr(desktop_profile.sys, "frozen", True, raising=False)
    monkeypatch.setattr(desktop_profile.platform, "machine", lambda: "AMD64")
    monkeypatch.setattr(desktop_profile, "is_packaged", lambda: False)
    monkeypatch.setattr(distribution, "is_packaged", lambda: False)
    monkeypatch.setattr(desktop_profile, "_settings_file", None)
    monkeypatch.setattr(source_profile, "_settings_file", None)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    return tmp_path


def test_desktop_settings_and_logs_are_separate(desktop):
    uv = desktop / "Folimeld-UV/settings/settings.ini"
    uv.parent.mkdir(parents=True)
    uv.write_bytes(b"[General]\nlanguage=ja\n")
    original = uv.read_bytes()
    logs = desktop_profile.activate_desktop_profile("0.3.5")
    settings = source_profile.application_settings()
    assert Path(settings.fileName()) == desktop / "Folimeld-Desktop/settings/settings.ini"
    assert not settings.fallbacksEnabled()
    assert settings.value("language") is None
    settings.setValue("language", "en")
    settings.sync()
    assert source_profile.application_settings().value("language") == "en"
    assert uv.read_bytes() == original
    assert logs.parent == desktop / "Folimeld-Desktop/logs/0.3.5"
    assert desktop_profile.desktop_profile_active()
    assert not source_profile.source_profile_active()
    assert distribution.sponsors_available()


@pytest.mark.parametrize("kind", ["source", "packaged", "x86", "other_os"])
def test_invalid_desktop_environment_creates_no_profile(desktop, monkeypatch, kind):
    if kind == "source": monkeypatch.setattr(desktop_profile.sys, "frozen", False)
    if kind == "packaged": monkeypatch.setattr(desktop_profile, "is_packaged", lambda: True)
    if kind == "x86": monkeypatch.setattr(desktop_profile.platform, "machine", lambda: "x86")
    if kind == "other_os": monkeypatch.setattr(desktop_profile.sys, "platform", "darwin")
    with pytest.raises(RuntimeError): desktop_profile.activate_desktop_profile("0.3.5")
    assert not (desktop / "Folimeld-Desktop").exists()


def test_arm64_desktop_environment_is_supported(desktop, monkeypatch):
    monkeypatch.setattr(desktop_profile.platform, "machine", lambda: "ARM64")
    logs = desktop_profile.activate_desktop_profile("0.3.5")
    assert desktop_profile.desktop_profile_active()
    assert logs.parent == desktop / "Folimeld-Desktop/logs/0.3.5"


def test_profiles_cannot_be_combined(desktop, monkeypatch):
    monkeypatch.setattr(source_profile, "_settings_file", desktop / "uv.ini")
    with pytest.raises(RuntimeError, match="already active"):
        desktop_profile.activate_desktop_profile("0.3.5")
    monkeypatch.setattr(source_profile, "_settings_file", None)
    desktop_profile.activate_desktop_profile("0.3.5")
    monkeypatch.setattr(source_profile.sys, "frozen", False)
    monkeypatch.setattr(source_profile, "is_packaged", lambda: False)
    with pytest.raises(RuntimeError, match="already active"):
        source_profile.activate_source_profile("0.3.5")


@pytest.mark.parametrize("value", ["../bad", "", "bad/path"])
def test_version_cannot_escape_storage(desktop, value):
    with pytest.raises(ValueError): desktop_profile.activate_desktop_profile(value)
    assert not (desktop / "Folimeld-Desktop").exists()


def test_missing_localappdata_does_not_fall_back(desktop, monkeypatch):
    monkeypatch.delenv("LOCALAPPDATA")
    with pytest.raises(RuntimeError, match="LOCALAPPDATA"):
        desktop_profile.activate_desktop_profile("0.3.5")
    assert not desktop_profile.desktop_profile_active()


def test_failed_initialization_resets_profile(desktop):
    (desktop / "Folimeld-Desktop").write_text("blocked")
    with pytest.raises(OSError): desktop_profile.activate_desktop_profile("0.3.5")
    assert not desktop_profile.desktop_profile_active()


def test_unwritable_settings_does_not_activate(desktop, monkeypatch):
    class Unwritable:
        def isWritable(self): return False
    monkeypatch.setattr(desktop_profile, "desktop_settings", lambda: Unwritable())
    with pytest.raises(OSError): desktop_profile.activate_desktop_profile("0.3.5")
    assert not desktop_profile.desktop_profile_active()
