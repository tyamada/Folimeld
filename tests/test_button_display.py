from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication

from folimeld.app import BUTTON_STYLES, MainWindow


@pytest.mark.parametrize("mode", BUTTON_STYLES)
def test_button_display_applies_and_persists(mode):
    app = QApplication.instance() or QApplication([])
    settings = {}
    with (patch("folimeld.app.QSettings") as factory,
          patch("folimeld.app.is_packaged", return_value=False)):
        factory.return_value.value.side_effect = lambda key, default=None: settings.get(key, default)
        factory.return_value.setValue.side_effect = settings.__setitem__
        window = MainWindow()
        try:
            assert window.button_display == "text"
            choices = [window.tr_("button_display_" + item) for item in BUTTON_STYLES]
            with patch("folimeld.app.QInputDialog.getItem", return_value=(choices[list(BUTTON_STYLES).index(mode)], True)):
                window.change_button_display()
            assert window.toolbar.toolButtonStyle() == BUTTON_STYLES[mode]
            assert settings["button_display"] == mode
            for action in window.toolbar.actions():
                if not action.isSeparator():
                    assert not action.icon().isNull()
                    assert action.toolTip()
            restored = MainWindow()
            try:
                assert restored.toolbar.toolButtonStyle() == BUTTON_STYLES[mode]
            finally:
                restored.close()
            with patch("folimeld.app.QInputDialog.getItem", return_value=("", False)):
                window.change_button_display()
            assert window.button_display == mode
        finally:
            window.close()
            app.processEvents()


def test_invalid_button_display_falls_back_to_text():
    app = QApplication.instance() or QApplication([])
    with (patch("folimeld.app.QSettings") as factory,
          patch("folimeld.app.is_packaged", return_value=False)):
        factory.return_value.value.side_effect = lambda key, default=None: "unknown" if key == "button_display" else default
        window = MainWindow()
        try:
            assert window.toolbar.toolButtonStyle() == BUTTON_STYLES["text"]
        finally:
            window.close()
            app.processEvents()
