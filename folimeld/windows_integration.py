"""Windows Explorer integration for the packaged application."""

import ctypes
from pathlib import Path
import sys

APPMODEL_ERROR_NO_PACKAGE = 15700


def is_packaged() -> bool:
    """Return whether the current process has an MSIX package identity."""
    if sys.platform != "win32":
        return False
    try:
        length = ctypes.c_uint32()
        result = ctypes.windll.kernel32.GetCurrentPackageFullName(
            ctypes.byref(length), None,
        )
    except AttributeError:
        return False
    return result != APPMODEL_ERROR_NO_PACKAGE


def open_command(executable: str) -> str:
    """Return the command stored in the Windows Open With registration."""
    return f'"{Path(executable).resolve()}" "%1"'


def register_open_with() -> bool:
    """Register the frozen executable in Explorer's Open With application list."""
    if sys.platform != "win32" or not getattr(sys, "frozen", False) or is_packaged():
        return False

    try:
        import winreg
    except ImportError:
        return False

    try:
        shell32 = ctypes.windll.shell32
    except AttributeError:
        return False

    executable = str(Path(sys.executable).resolve())
    application_key = r"Software\Classes\Applications\Folimeld.exe"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, application_key) as key:
        winreg.SetValueEx(key, "FriendlyAppName", 0, winreg.REG_SZ, "Folimeld")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                          application_key + r"\SupportedTypes") as key:
        winreg.SetValueEx(key, ".pdf", 0, winreg.REG_SZ, "")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                          application_key + r"\shell\open\command") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, open_command(executable))

    # Tell Explorer that file-association information has changed.
    shell32.SHChangeNotify(0x08000000, 0, None, None)
    return True
