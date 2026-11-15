import pytest
from tools.desktop_qt import EXCLUDED_IMPORTS, filter_qt_payload, forbidden


def baseline():
    return [("PySide6/" + name, name, "BINARY") for name in
            ("Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll", "plugins/platforms/qwindows.dll")]


def test_plugins_cannot_reintroduce_excluded_dependencies():
    rows = baseline() + [("PySide6/plugins/imageformats/qpdf.dll", "qpdf", "BINARY"),
        ("PySide6/plugins/iconengines/optional.dll", "optional", "BINARY"),
        ("PySide6/Qt6Charts.dll", "charts", "BINARY")]
    def imports(source):
        return {("Qt6Quick.dll", "quick")} if source == "optional" else set()
    kept, data, removed = filter_qt_payload(rows,
        [("PySide6/qml/QtQuick/file.qml", "qml", "DATA"), ("locales/ja.qm", "ja", "DATA")], imports)
    assert kept == sorted(baseline())
    assert data == [("locales/ja.qm", "ja", "DATA")]
    assert len(removed) == 4


def test_retained_code_dependencies_fail_closed():
    with pytest.raises(ValueError, match="requires excluded"):
        filter_qt_payload(baseline(), [], lambda source: {("Qt6Network.dll", "network")})
    with pytest.raises(ValueError, match="Unresolved Qt"):
        filter_qt_payload(baseline(), [], lambda source: {("Qt6Gui.dll", None)})
    with pytest.raises(ValueError, match="Missing Desktop Qt"):
        filter_qt_payload([], [], lambda source: set())


def test_scope_and_native_support():
    assert "PySide6.QtVirtualKeyboard" in EXCLUDED_IMPORTS
    assert "PySide6.QtQuick" in EXCLUDED_IMPORTS
    assert "PySide6.QtWidgets" not in EXCLUDED_IMPORTS
    assert forbidden("PySide6/plugins/platforminputcontexts/qtvirtualkeyboardplugin.dll")
    assert forbidden("PySide6/Qt6FutureModule.dll")
    assert forbidden("PySide6/pyside6qml.abi3.dll")
    for name in ("PySide6/Qt6Svg.dll", "PySide6/opengl32sw.dll",
                 "PySide6/plugins/platforms/qwindows.dll", "locales/qml/readme.txt"):
        assert not forbidden(name)

