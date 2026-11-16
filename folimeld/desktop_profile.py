"""Isolated profile for the frozen, unpackaged Windows Desktop distribution."""
from datetime import datetime, timezone
import os
from pathlib import Path
import platform
import re
import sys
import struct
from uuid import uuid4

from .windows_integration import is_packaged

_settings_file: Path | None = None


def validate_desktop_environment() -> None:
    if (sys.platform != "win32" or not getattr(sys, "frozen", False)
            or struct.calcsize("P") != 8
            or is_packaged() or platform.machine().lower() not in {"amd64", "x86_64", "arm64", "aarch64"}):
        raise RuntimeError("Folimeld Desktop requires an unpackaged frozen 64-bit Windows process.")


def activate_desktop_profile(version: str) -> Path:
    global _settings_file
    validate_desktop_environment()
    from .source_profile import source_profile_active
    from .uv_tool_profile import uv_tool_profile_active
    if _settings_file is not None or source_profile_active() or uv_tool_profile_active():
        raise RuntimeError("A separate distribution profile is already active.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+_-]*", version):
        raise ValueError("Invalid Desktop version.")
    local = os.environ.get("LOCALAPPDATA", "")
    if not local or not Path(local).is_absolute():
        raise RuntimeError("An absolute LOCALAPPDATA directory is required.")
    root = Path(local) / "Folimeld-Desktop"
    settings = root / "settings/settings.ini"
    session = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid4().hex
    logs = root / "logs" / version / session
    settings.parent.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=False)
    _settings_file = settings
    try:
        if not desktop_settings().isWritable():
            raise OSError("Desktop settings are not writable.")
    except Exception:
        _settings_file = None
        raise
    return logs


def desktop_profile_active() -> bool:
    return _settings_file is not None


def desktop_settings():
    from PySide6.QtCore import QSettings
    if _settings_file is None:
        raise RuntimeError("Desktop profile is not active.")
    settings = QSettings(str(_settings_file), QSettings.Format.IniFormat)
    settings.setFallbacksEnabled(False)
    if settings.status() != QSettings.Status.NoError:
        raise OSError("Desktop settings could not be read.")
    return settings
