"""Collect license data for all PyInstaller targets (no network required)."""

from pathlib import Path
from folimeld.license_info import installed_notices


def license_datas(project_root):
    root = Path(project_root)
    target = root / "build" / "legal" / "Installed-packages.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(installed_notices(), encoding="utf-8")
    return [(str(root / "LICENSE"), "."), (str(root / "licenses"), "licenses"),
            (str(target), "licenses")]
