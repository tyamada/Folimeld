from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow
from folimeld.i18n import I18n, LANGUAGES


@pytest.mark.parametrize("platform", ["linux", "win32", "darwin"])
def test_sponsors_entry_is_linux_only(platform):
    app = QApplication.instance() or QApplication([])
    with patch("folimeld.app.sys.platform", platform), patch("folimeld.app.is_packaged", return_value=False):
        window = MainWindow()
    try:
        assert hasattr(window, "sponsors_action") == (platform == "linux")
        if platform == "linux":
            with patch("folimeld.support_dialog.QDesktopServices.openUrl", return_value=False) as open_url:
                window.sponsors_action.trigger()
                dialog = window.sponsors_dialog
                assert dialog.isVisible()
                open_url.assert_not_called()
                dialog.open_button.click()
                assert open_url.call_args.args[0].toString() == "https://github.com/sponsors/tyamada"
                assert dialog.error.isVisible()
                open_url.return_value = True
                dialog.open_button.click()
                assert not dialog.error.isVisible()
                dialog.close()
                window.sponsors_action.trigger()
                assert window.sponsors_dialog is dialog
    finally:
        window.close()
        window.deleteLater()
        app.processEvents()


def test_sponsors_translations():
    translator = I18n()
    for language in LANGUAGES:
        translator.load(language)
        for key in ("sponsors_description", "sponsors_open", "sponsors_open_error"):
            assert translator.tr(key) and translator.tr(key) != key
