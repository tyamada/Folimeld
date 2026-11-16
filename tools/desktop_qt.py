"""Desktop-only Qt collection policy. Never used by Store/uv specs."""
from pathlib import Path, PurePosixPath

# Keep optional SVG/image and OpenGL support until native acceptance permits removal.
ALLOWED_QT = frozenset({"Core", "Gui", "Widgets", "Svg", "SvgWidgets", "OpenGL", "OpenGLWidgets"})
ALL_MODULES = (
    "3DAnimation 3DCore 3DExtras 3DInput 3DLogic 3DRender Bluetooth Charts Concurrent "
    "Core DataVisualization DBus Designer Graphs GraphsWidgets Gui Help HttpServer "
    "Location Multimedia MultimediaWidgets Network NetworkAuth Nfc OpenGL OpenGLWidgets "
    "Pdf PdfWidgets Positioning PrintSupport Qml Quick Quick3D QuickControls2 QuickTest "
    "QuickWidgets RemoteObjects Scxml Sensors SerialBus SerialPort SpatialAudio Sql StateMachine "
    "Svg SvgWidgets Test TextToSpeech UiTools VirtualKeyboard WebChannel WebEngineCore "
    "WebEngineQuick WebEngineWidgets WebSockets WebView Widgets Xml"
).split()
EXCLUDED_IMPORTS = sorted("PySide6.Qt" + name for name in ALL_MODULES if name not in ALLOWED_QT)
BLOCKED_DIRS = frozenset({"qml", "multimedia", "platforminputcontexts", "sqldrivers",
    "designer", "texttospeech", "virtualkeyboard", "renderers", "sceneparsers",
    "geometryloaders", "webview"})


def _path(name):
    return PurePosixPath(str(name).replace("\\", "/")).as_posix().lower()


def forbidden(name):
    path = _path(name)
    parts = PurePosixPath(path).parts
    # Scope data/plugin decisions to PySide6, not application/locales/legal data.
    if "pyside6" not in parts:
        return False
    if any(part in BLOCKED_DIRS for part in parts):
        return True
    base = parts[-1]
    if (base == "qpdf.dll" or base.startswith("pyside6qml.")
            or "qtvirtualkeyboard" in base or base.startswith("ffmpeg")):
        return True
    for prefix, suffix in (("qt6", ".dll"), ("qt", ".pyd")):
        if base.startswith(prefix) and base.endswith(suffix):
            return base[len(prefix):-len(suffix)] not in {x.lower() for x in ALLOWED_QT}
    return False


def filter_qt_payload(binaries, datas, get_imports):
    """Remove unused plugins; reject unresolved Qt dependencies of retained files.

    get_imports is PyInstaller's PE import reader. No input files are modified.
    Returns audit entries as well as filtered TOCs. Dynamic-load acceptance is separate.
    """
    removed = []
    kept = []
    resolved_in_toc = {
        PurePosixPath(_path(row[0])).name
        for row in binaries
        if not forbidden(row[0]) and Path(row[1]).is_file()
    }
    for row in binaries:
        name, source, kind = row
        if forbidden(name):
            removed.append({"path": name, "reason": "Desktop Qt exclusion policy"})
            continue
        imports = get_imports(source)
        denied = []
        for imported, resolved in imports:
            base = PurePosixPath(_path(imported)).name
            if base.startswith("qt6") and base.endswith(".dll"):
                if base[3:-4] not in {x.lower() for x in ALLOWED_QT}:
                    denied.append(base)
                elif not resolved and base not in resolved_in_toc:
                    raise ValueError(f"Unresolved Qt dependency: {name}: {base}")
        if denied:
            if "/plugins/" in "/" + _path(name):
                removed.append({"path": name, "reason": "Excluded Qt plugin dependency", "imports": sorted(denied)})
                continue
            raise ValueError(f"Retained binary requires excluded Qt modules: {name}: {sorted(denied)}")
        kept.append(row)
    filtered_data = []
    for row in datas:
        if forbidden(row[0]):
            removed.append({"path": row[0], "reason": "Desktop Qt data exclusion policy"})
        else:
            filtered_data.append(row)
    names = {PurePosixPath(_path(row[0])).name for row in kept}
    required = {"qt6core.dll", "qt6gui.dll", "qt6widgets.dll", "qwindows.dll"}
    if not required <= names:
        raise ValueError(f"Missing Desktop Qt payload: {sorted(required - names)}")
    return sorted(kept), sorted(filtered_data), sorted(removed, key=lambda row: row["path"])
