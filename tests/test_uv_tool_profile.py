from pathlib import Path
import pytest
from folimeld import desktop_profile, distribution, source_profile, uv_tool_profile


@pytest.fixture
def uv_tool(monkeypatch, tmp_path):
    monkeypatch.setattr(uv_tool_profile.sys, "platform", "win32")
    monkeypatch.setattr(uv_tool_profile.sys, "frozen", False, raising=False)
    monkeypatch.setattr(uv_tool_profile.platform, "machine", lambda: "AMD64")
    monkeypatch.setattr(uv_tool_profile, "is_packaged", lambda: False)
    monkeypatch.setattr(distribution, "is_packaged", lambda: False)
    monkeypatch.setattr(distribution.sys, "platform", "win32")
    monkeypatch.setattr(distribution.sys, "frozen", False, raising=False)
    monkeypatch.setattr(desktop_profile, "_settings_file", None)
    monkeypatch.setattr(source_profile, "_settings_file", None)
    monkeypatch.setattr(uv_tool_profile, "_settings_file", None)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    return tmp_path


def test_uv_tool_settings_and_logs_are_separate(uv_tool):
    source_uv = uv_tool / "Folimeld-UV/settings/settings.ini"
    source_uv.parent.mkdir(parents=True)
    source_uv.write_bytes(b"[General]\nlanguage=ja\n")
    desktop_ini = uv_tool / "Folimeld-Desktop/settings/settings.ini"
    desktop_ini.parent.mkdir(parents=True)
    desktop_ini.write_bytes(b"[General]\nlanguage=fr\n")

    logs = uv_tool_profile.activate_uv_tool_profile("0.3.5")
    settings = source_profile.application_settings()
    assert Path(settings.fileName()) == uv_tool / "Folimeld-UV-Tool/settings/settings.ini"
    assert not settings.fallbacksEnabled()
    assert settings.value("language") is None
    settings.setValue("language", "en")
    settings.sync()
    assert source_profile.application_settings().value("language") == "en"
    assert source_uv.read_bytes() == b"[General]\nlanguage=ja\n"
    assert desktop_ini.read_bytes() == b"[General]\nlanguage=fr\n"
    assert logs.parent == uv_tool / "Folimeld-UV-Tool/logs/0.3.5"
    assert uv_tool_profile.uv_tool_profile_active()
    assert not desktop_profile.desktop_profile_active()
    assert not source_profile.source_profile_active()
    assert distribution.sponsors_available()


@pytest.mark.parametrize("kind", ["frozen", "packaged", "x86", "other_os"])
def test_invalid_uv_tool_environment_creates_no_profile(uv_tool, monkeypatch, kind):
    if kind == "frozen":
        monkeypatch.setattr(uv_tool_profile.sys, "frozen", True, raising=False)
    if kind == "packaged":
        monkeypatch.setattr(uv_tool_profile, "is_packaged", lambda: True)
    if kind == "x86":
        monkeypatch.setattr(uv_tool_profile.platform, "machine", lambda: "x86")
    if kind == "other_os":
        monkeypatch.setattr(uv_tool_profile.sys, "platform", "linux")
    with pytest.raises(RuntimeError):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    assert not (uv_tool / "Folimeld-UV-Tool").exists()


def test_arm64_uv_tool_environment_is_supported(uv_tool, monkeypatch):
    monkeypatch.setattr(uv_tool_profile.platform, "machine", lambda: "ARM64")
    logs = uv_tool_profile.activate_uv_tool_profile("0.3.5")
    assert uv_tool_profile.uv_tool_profile_active()
    assert logs.parent == uv_tool / "Folimeld-UV-Tool/logs/0.3.5"


def test_profiles_cannot_be_combined_with_uv_tool(uv_tool, monkeypatch):
    monkeypatch.setattr(source_profile, "_settings_file", uv_tool / "uv.ini")
    with pytest.raises(RuntimeError, match="already active"):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    monkeypatch.setattr(source_profile, "_settings_file", None)

    monkeypatch.setattr(desktop_profile, "_settings_file", uv_tool / "desktop.ini")
    with pytest.raises(RuntimeError, match="already active"):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    monkeypatch.setattr(desktop_profile, "_settings_file", None)

    uv_tool_profile.activate_uv_tool_profile("0.3.5")
    monkeypatch.setattr(source_profile.sys, "platform", "win32")
    monkeypatch.setattr(source_profile.sys, "frozen", False, raising=False)
    monkeypatch.setattr(source_profile, "is_packaged", lambda: False)
    with pytest.raises(RuntimeError, match="already active"):
        source_profile.activate_source_profile("0.3.5")


@pytest.mark.parametrize("value", ["../bad", "", "bad/path"])
def test_version_cannot_escape_uv_tool_storage(uv_tool, value):
    with pytest.raises(ValueError):
        uv_tool_profile.activate_uv_tool_profile(value)
    assert not (uv_tool / "Folimeld-UV-Tool").exists()


def test_missing_localappdata_does_not_fall_back(uv_tool, monkeypatch):
    monkeypatch.delenv("LOCALAPPDATA")
    with pytest.raises(RuntimeError, match="LOCALAPPDATA"):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    assert not uv_tool_profile.uv_tool_profile_active()


def test_failed_initialization_resets_uv_tool_profile(uv_tool):
    (uv_tool / "Folimeld-UV-Tool").write_text("blocked")
    with pytest.raises(OSError):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    assert not uv_tool_profile.uv_tool_profile_active()


def test_unwritable_settings_does_not_activate(uv_tool, monkeypatch):
    class Unwritable:
        def isWritable(self):
            return False

    monkeypatch.setattr(uv_tool_profile, "uv_tool_settings", lambda: Unwritable())
    with pytest.raises(OSError):
        uv_tool_profile.activate_uv_tool_profile("0.3.5")
    assert not uv_tool_profile.uv_tool_profile_active()
