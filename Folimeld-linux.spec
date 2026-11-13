# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.insert(0, SPECPATH)
from tools.license_bundle import license_datas
from tools.source_bundle import source_datas, record_artifact

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("locales", "locales"),
        ("assets/folimeld-supporter-maid.png", "assets"),
        ("assets/Folimeld.iconset/icon_256x256.png", "assets"),
    ] + license_datas(SPECPATH) + source_datas(SPECPATH, "linux"),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# Folimeld uses the desktop input method, so omit Qt Virtual Keyboard.
a.binaries = [entry for entry in a.binaries if "virtualkeyboard" not in entry[0].lower()]
a.datas = [entry for entry in a.datas if "virtualkeyboard" not in entry[0].lower()]
a.pure = [entry for entry in a.pure if "virtualkeyboard" not in entry[0].lower()]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="folimeld",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

record_artifact(exe.name, exe.name, Path(SPECPATH) / "dist" / "source", project_root=SPECPATH)
