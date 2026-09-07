"""License documents shared by the application and the packaging specs."""

from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
import sys


SOURCE_URL = "https://github.com/tyamada/Folimeld"


def installed_notices(*, strict: bool = True) -> str:
    """Collect notices; packaging requires metadata, source runs may omit it."""
    names = ["PySide6", "PySide6_Essentials", "PySide6_Addons", "shiboken6", "PyMuPDF", "Pillow"]
    if sys.platform == "win32":
        names += ["winrt-runtime", "winrt-Windows.Services.Store",
                  "winrt-Windows.Foundation", "winrt-Windows.Foundation.Collections"]
    sections = []
    for name in names:
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            if strict:
                raise
            sections.append(f"{name}: package metadata is not available in this environment.")
            continue
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
