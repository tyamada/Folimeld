"""Resource root resolution across frozen, wheel-installed, and source layouts."""
from pathlib import Path
import sys


def resource_root() -> Path:
    """Return the root directory containing assets, locales, and license data."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass is not None:
        return Path(meipass)
    package_resources = Path(__file__).resolve().parent / "_resources"
    if package_resources.is_dir():
        return package_resources
    return Path(__file__).resolve().parent.parent
