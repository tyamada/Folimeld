"""Explicit distribution labels for optional development-support guidance.

Labels control presentation, not a security or installation-origin guarantee.
"""
import sys

from PySide6.QtCore import QCoreApplication

from .source_profile import source_profile_active
from .windows_integration import is_packaged


def sponsors_available() -> bool:
    if is_packaged():
        return False
    if sys.platform == "linux" or sys.platform.startswith(("freebsd", "netbsd", "openbsd")):
        return True
    from .desktop_profile import desktop_profile_active
    if sys.platform == "win32" and getattr(sys, "frozen", False) and desktop_profile_active():
        return True
    if getattr(sys, "frozen", False):
        return False
    if sys.platform == "win32":
        return source_profile_active()
    app = QCoreApplication.instance()
    return (sys.platform == "darwin" and app is not None
            and app.property("folimeld_distribution") == "homebrew")
