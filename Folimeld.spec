# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path
sys.path.insert(0, SPECPATH)
from tools.license_bundle import license_datas
from tools.source_bundle import source_datas, record_artifact
from tools.windows_build_environment import validate_binary_sources

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("locales", "locales"),
        ("assets/folimeld-supporter-maid.png", "assets"),
        ("assets/Folimeld.iconset/icon_256x256.png", "assets"),
    ] + license_datas(SPECPATH) + source_datas(SPECPATH, "windows"),
    hiddenimports=["winrt.windows.foundation", "winrt.windows.foundation.collections"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
validate_binary_sources(a.binaries, [sys.prefix, sys.base_prefix, os.environ["SystemRoot"]])
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
    manifest=str(Path(SPECPATH) / "packaging" / "windows" / "Folimeld.manifest"),
)

record_artifact(exe.name, exe.name, Path(SPECPATH) / "dist" / "source", project_root=SPECPATH)
