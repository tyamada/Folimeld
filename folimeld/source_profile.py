"""Explicit settings and logging profile for the Windows source/uv launcher."""
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import sys
from uuid import uuid4

from .windows_integration import is_packaged

_settings_file: Path | None = None


def activate_source_profile(version: str) -> Path:
    """Select the source profile before any settings readers are constructed."""
    global _settings_file
    if sys.platform != 'win32' or getattr(sys, 'frozen', False) or is_packaged():
        raise RuntimeError('The uv profile requires an unpackaged Windows source process.')
    from .desktop_profile import desktop_profile_active
    if _settings_file is not None or desktop_profile_active():
        raise RuntimeError('The uv profile is already active.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.+_-]*', version):
        raise ValueError('Invalid application version for the uv profile.')
    local = os.environ.get('LOCALAPPDATA', '')
    if not local or not Path(local).is_absolute():
        raise RuntimeError('An absolute LOCALAPPDATA directory is required.')
    root = Path(local) / 'Folimeld-UV'
    settings_file = root / 'settings' / 'settings.ini'
    session = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid4().hex
    logs = root / 'logs' / version / session
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=False)
    _settings_file = settings_file
    try:
        if not application_settings().isWritable():
            raise OSError('The uv settings file is not writable.')
    except Exception:
        _settings_file = None
        raise
    return logs


def application_settings():
    """Use the explicit INI for uv; preserve the existing defaults otherwise."""
    from PySide6.QtCore import QSettings
    from .desktop_profile import desktop_profile_active, desktop_settings

    if desktop_profile_active():
        return desktop_settings()
    if _settings_file is None:
        return QSettings()
    settings = QSettings(str(_settings_file), QSettings.Format.IniFormat)
    settings.setFallbacksEnabled(False)
    if settings.status() != QSettings.Status.NoError:
        raise OSError('The uv settings file could not be read.')
    return settings


def source_profile_active() -> bool:
    """Return whether the explicit uv profile has been activated."""
    return _settings_file is not None
