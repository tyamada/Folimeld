# Dedicated onedir candidate. Existing Store/legacy specs remain unchanged.
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, SPECPATH)
from tools.windows_build_environment import validate_binary_sources
from tools.desktop_build import reviewed_legal_datas
from tools.desktop_qt import EXCLUDED_IMPORTS, filter_qt_payload
from PyInstaller.depend.bindepend import get_imports

root = Path(SPECPATH)
legal = reviewed_legal_datas(Path(os.environ["FOLIMELD_DESKTOP_LEGAL_ROOT"]))
a = Analysis([str(root / "launch_desktop.py")], pathex=[str(root)], binaries=[],
    datas=[(str(root / "locales"), "locales"),
           (str(root / "assets/Folimeld.iconset/icon_256x256.png"), "assets"),
           (str(root / "assets/folimeld-supporter-maid.png"), "assets"),
           (str(root / "LICENSE"), ".")] + legal,
    hiddenimports=["winrt.windows.foundation", "winrt.windows.foundation.collections"],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=EXCLUDED_IMPORTS, noarchive=False, optimize=0)
validate_binary_sources(a.binaries, [sys.prefix, sys.base_prefix, os.environ["SystemRoot"]])
a.binaries, a.datas, excluded = filter_qt_payload(a.binaries, a.datas, get_imports)
Path(WORKPATH, "desktop-qt-exclusions.json").write_text(
    json.dumps(excluded, indent=2), encoding="utf-8")
pyz = PYZ(sorted(a.pure))
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="FolimeldDesktop",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False,
    icon=str(root / "assets/Folimeld.ico"),
    version=os.environ["FOLIMELD_DESKTOP_VERSION_INFO"],
    manifest=str(root / "packaging/windows/Folimeld.manifest"))
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="FolimeldDesktop")
