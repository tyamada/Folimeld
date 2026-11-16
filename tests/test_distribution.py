import pytest
from PySide6.QtCore import QSettings

from folimeld import distribution
from folimeld.app import MainWindow, run


@pytest.mark.parametrize("platform,uv,label,frozen,packaged,expected", [
    ("linux", False, None, False, False, True),
    ("linux", False, None, True, False, True),
    ("freebsd15", False, None, False, False, True),
    ("netbsd11", False, None, False, False, True),
    ("openbsd8", False, None, False, False, True),
    ("dragonfly6", False, None, False, False, False),
    ("darwin", False, "homebrew", False, False, True),
    ("darwin", False, None, False, False, False),
    ("darwin", False, "homebrew", True, False, False),
    ("win32", True, None, False, False, True),
    ("win32", False, "uv-tool", False, False, True),
    ("win32", False, "uv-tool", True, False, False),
    ("win32", False, "uv-tool", False, True, False),
    ("win32", False, "desktop", True, False, True),
    ("win32", False, "desktop", True, True, False),
    ("win32", False, "desktop", False, False, False),
    ("win32", False, None, False, False, False),
    ("win32", True, None, True, False, False),
    ("win32", True, "homebrew", False, True, False),
    ("win32", False, "homebrew", False, False, False),
])
def test_distribution_guidance_matrix(qapp, monkeypatch, tmp_path, platform, uv, label,
                                      frozen, packaged, expected):
    previous = qapp.property("folimeld_distribution")
    qapp.setProperty("folimeld_distribution", label)
    monkeypatch.setattr(distribution.sys, "platform", platform)
    monkeypatch.setattr(distribution.sys, "frozen", frozen, raising=False)
    monkeypatch.setattr(distribution, "source_profile_active", lambda: uv)
    monkeypatch.setattr("folimeld.desktop_profile.desktop_profile_active",
                        lambda: label == "desktop" and frozen and not packaged)
    monkeypatch.setattr("folimeld.uv_tool_profile.uv_tool_profile_active",
                        lambda: label == "uv-tool" and not frozen and not packaged)
    # GUI construction uses the default settings factory; no profile files in this matrix.
    settings = lambda: QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
    monkeypatch.setattr("folimeld.app.application_settings", settings)
    monkeypatch.setattr("folimeld.i18n.application_settings", settings)
    monkeypatch.setattr(distribution, "is_packaged", lambda: packaged)
    monkeypatch.setattr("folimeld.app.is_packaged", lambda: False)
    try:
        assert distribution.sponsors_available() is expected
        window = MainWindow()
        assert hasattr(window, "sponsors_action") is expected
        window.close()
    finally:
        qapp.setProperty("folimeld_distribution", previous)


@pytest.mark.parametrize("platform,frozen,uv,label", [
    ("win32", False, False, "homebrew"),
    ("darwin", True, False, "homebrew"),
    ("darwin", False, True, "homebrew"),
    ("darwin", False, False, "unknown"),
])
def test_invalid_channel_is_rejected_before_application(monkeypatch, platform, frozen, uv, label):
    monkeypatch.setattr(distribution.sys, "platform", platform)
    monkeypatch.setattr(distribution.sys, "frozen", frozen, raising=False)
    with pytest.raises(RuntimeError, match="Homebrew"):
        run(source_uv=uv, distribution=label)
