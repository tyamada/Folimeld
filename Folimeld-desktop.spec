# Dedicated onedir candidate. Existing Store/legacy specs remain unchanged.
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, SPECPATH)
from tools.windows_build_environment import validate_binary_sources
from tools.desktop_build import reviewed_legal_datas
from tools.desktop_crt import load_crt_manifest, normalize_crt_payload, verify_collected_crt
from tools.desktop_qt import EXCLUDED_IMPORTS, filter_qt_payload
from tools.desktop_runtime_terms import verify_runtime_terms
from PyInstaller.depend.bindepend import get_imports

root = Path(SPECPATH)
work_dir = Path(workpath)
work_dir.mkdir(parents=True, exist_ok=True)
crt_manifest, crt_manifest_hash = load_crt_manifest(root)
legal = reviewed_legal_datas(Path(os.environ["FOLIMELD_DESKTOP_LEGAL_ROOT"]))
runtime_terms = verify_runtime_terms(Path(os.environ["FOLIMELD_DESKTOP_LEGAL_ROOT"]))
(work_dir / "desktop-runtime-terms.json").write_text(
    json.dumps(runtime_terms, indent=2), encoding="utf-8")
a = Analysis([str(root / "launch_desktop.py")], pathex=[str(root)], binaries=[],
    datas=[(str(root / "locales"), "locales"),
           (str(root / "assets/Folimeld.iconset/icon_256x256.png"), "assets"),
           (str(root / "assets/folimeld-supporter-maid.png"), "assets"),
           (str(root / "LICENSE"), ".")] + legal,
    hiddenimports=["winrt.windows.foundation", "winrt.windows.foundation.collections"],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=EXCLUDED_IMPORTS, noarchive=False, optimize=0)
validate_binary_sources(a.binaries, [sys.prefix, sys.base_prefix, os.environ["SystemRoot"]])
a.binaries, a.datas, excluded = filter_qt_payload(a.binaries, a.datas, get_imports)
(work_dir / "desktop-qt-exclusions.json").write_text(
    json.dumps(excluded, indent=2), encoding="utf-8")
a.binaries, a.datas, crt_record = normalize_crt_payload(
    a.binaries, a.datas, Path(os.environ["FOLIMELD_DESKTOP_CRT_ROOT"]), crt_manifest)
crt_record["manifest_sha256"] = crt_manifest_hash
(work_dir / "desktop-crt-inputs.json").write_text(
    json.dumps(crt_record, indent=2), encoding="utf-8")
pyz = PYZ(sorted(a.pure))
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="FolimeldDesktop",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=False, console=False,
    contents_directory="_internal",
    icon=str(root / "assets/Folimeld.ico"),
    version=os.environ["FOLIMELD_DESKTOP_VERSION_INFO"],
    manifest=str(root / "packaging/windows/Folimeld.manifest"))
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="FolimeldDesktop")

crt_collected = verify_collected_crt(Path(coll.name), crt_manifest)
(work_dir / "desktop-crt-collected.json").write_text(
    json.dumps(crt_collected, indent=2), encoding="utf-8")

verify_runtime_terms(Path(coll.name) / "_internal/licenses", require_reviewed=False)
