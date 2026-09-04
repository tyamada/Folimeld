# -*- mode: python ; coding: utf-8 -*-

from folimeld import __version__

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[("locales", "locales")],
    hiddenimports=[],
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
)

app = BUNDLE(
    exe,
    name="Folimeld.app",
    icon="assets/Folimeld.icns",
    bundle_identifier="com.folimeld.Folimeld",
    info_plist={
        "CFBundleShortVersionString": __version__,
        "CFBundleVersion": __version__,
    },
)
