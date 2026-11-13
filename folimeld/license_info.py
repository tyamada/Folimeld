"""License documents shared by the application and the packaging specs."""

from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
import re
import sys


SOURCE_URL = "https://github.com/tyamada/Folimeld"


def installed_notices(*, strict: bool = True) -> str:
    """Collect notices; packaging requires metadata, source runs may omit it."""
    names = ["PySide6", "PySide6_Essentials", "PySide6_Addons", "shiboken6", "PyMuPDF", "Pillow",
             "cryptography", "cffi", "pycparser", "PyInstaller"]
    if sys.platform == "win32":
        names += ["winrt-runtime", "winrt-Windows.Services.Store",
                  "winrt-Windows.Foundation", "winrt-Windows.Foundation.Collections"]
    sections = []
    pyside_requires = None
    for name in names:
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            if (name in {"PySide6_Essentials", "PySide6_Addons"}
                    and pyside_requires is not None and name.lower() not in pyside_requires):
                sections.append(f"{name}: not used by this monolithic PySide6 distribution.")
                continue
            if strict:
                raise
            sections.append(f"{name}: package metadata is not available in this environment.")
            continue
        if name == "PySide6":
            pyside_requires = {
                re.split(r"[\s<>=!~;\[]", requirement, maxsplit=1)[0].lower().replace("-", "_")
                for requirement in (getattr(dist, "requires", None) or [])
            }
        license_name = dist.metadata.get("License-Expression") or dist.metadata.get("License", "")
        sections.append(f"{name} {dist.version}\n{license_name}\n")
        for file in sorted(dist.files or []):
            if any(part.lower().startswith(("license", "copying", "notice")) for part in file.parts):
                path = Path(dist.locate_file(file))
                if path.is_file():
                    sections.append(f"--- {file} ---\n{path.read_text(encoding='utf-8', errors='replace')}")
    python_license = Path(sys.base_prefix) / "LICENSE.txt"
    if not python_license.exists():
        import sysconfig
        python_license = Path(sysconfig.get_path("stdlib")) / "LICENSE.txt"
    if not python_license.exists():
        if strict:
            raise FileNotFoundError("Python LICENSE.txt is required for packaging")
        sections.append(f"Python {sys.version}\nLICENSE.txt is not available in this environment.")
    else:
        sections.append(f"Python {sys.version}\n{python_license.read_text(encoding='utf-8')}")
    return "\n\n".join(sections)


def license_documents() -> list[tuple[str, str]]:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    documents = [("Folimeld", (root / "LICENSE").read_text(encoding="utf-8"))]
    for path in sorted((root / "licenses").glob("*.txt")):
        documents.append((path.stem, path.read_text(encoding="utf-8")))
    bundled = root / "licenses" / "Installed-packages.txt"
    if not bundled.exists() and not getattr(sys, "frozen", False):
        documents.append(("Installed-packages", installed_notices(strict=False)))
    return documents
