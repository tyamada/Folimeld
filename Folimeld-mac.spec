# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.insert(0, SPECPATH)
from tools.license_bundle import license_datas
from tools.source_bundle import source_datas, record_artifact

from folimeld import __build__, __version__

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("locales", "locales"),
        ("assets/folimeld-supporter-maid.png", "assets"),
    ] + license_datas(SPECPATH) + source_datas(SPECPATH, "macos"),
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
        "CFBundleVersion": __build__,
        "CFBundleDocumentTypes": [
            {
                "CFBundleTypeName": "PDF document",
                "CFBundleTypeRole": "Editor",
                "CFBundleTypeExtensions": ["pdf"],
                "CFBundleTypeMIMETypes": ["application/pdf"],
                "LSHandlerRank": "Owner",
                "LSItemContentTypes": ["com.adobe.pdf"],
            }
        ],
    },
)

record_artifact(exe.name, exe.name, Path(SPECPATH) / "dist" / "source", project_root=SPECPATH)
