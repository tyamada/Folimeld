# Dedicated onedir candidate. Existing Store/legacy specs remain unchanged.
import os
from pathlib import Path
import sys
sys.path.insert(0, SPECPATH)
from tools.windows_build_environment import validate_binary_sources
from tools.desktop_build import reviewed_legal_datas

root = Path(SPECPATH)
legal = reviewed_legal_datas(Path(os.environ["FOLIMELD_DESKTOP_LEGAL_ROOT"]))
a = Analysis([str(root / "launch_desktop.py")], pathex=[str(root)], binaries=[],
    datas=[(str(root / "locales"), "locales"),
           (str(root / "assets/Folimeld.iconset/icon_256x256.png"), "assets"),
           (str(root / "assets/folimeld-supporter-maid.png"), "assets"),
           (str(root / "LICENSE"), ".")] + legal,
    hiddenimports=["winrt.windows.foundation", "winrt.windows.foundation.collections"],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False, optimize=0)
validate_binary_sources(a.binaries, [sys.prefix, sys.base_prefix, os.environ["SystemRoot"]])
a.binaries = sorted(a.binaries)
a.datas = sorted(a.datas)
pyz = PYZ(sorted(a.pure))
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="FolimeldDesktop",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False,
    icon=str(root / "assets/Folimeld.ico"),
    version=os.environ["FOLIMELD_DESKTOP_VERSION_INFO"],
    manifest=str(root / "packaging/windows/Folimeld.manifest"))
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="FolimeldDesktop")
