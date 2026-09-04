"""Generate PyInstaller's Windows version resource from the app version."""

from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from folimeld import __version__


def windows_version(version: str) -> tuple[int, int, int, int]:
    """Convert a three-part application version to a Windows version tuple."""
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Unsupported version format: {version!r}")
    return (*map(int, match.groups()), 0)


def version_info(version: str) -> str:
    numeric = ", ".join(map(str, windows_version(version)))
    return f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({numeric}),
    prodvers=({numeric}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u''),
            StringStruct(u'FileDescription', u'Folimeld'),
            StringStruct(u'FileVersion', u'{version}'),
            StringStruct(u'InternalName', u'Folimeld'),
            StringStruct(u'LegalCopyright', u'Copyright (C) 2026 Takuma Yamada'),
            StringStruct(u'OriginalFilename', u'Folimeld.exe'),
            StringStruct(u'ProductName', u'Folimeld'),
            StringStruct(u'ProductVersion', u'{version}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""


def main() -> int:
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else "build/version_info.txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(version_info(__version__), encoding="utf-8")
    print(f"Generated {destination} for Folimeld {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
