# -*- mode: python ; coding: utf-8 -*-

import sys
sys.path.insert(0, SPECPATH)
from tools.license_bundle import license_datas

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("locales", "locales"),
        ("assets/Folimeld.iconset/icon_256x256.png", "assets"),
    ] + license_datas(SPECPATH),
    hiddenimports=["winrt.windows.foundation", "winrt.windows.foundation.collections"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Folimeld",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/Folimeld.ico",
    version="build/version_info.txt",
)
