from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QWidget

from folimeld.store_update import (
    STORE_PRODUCT_URI,
    STORE_WEB_URL,
    StoreUpdateChecker,
    open_store_product_page,
)


@pytest.fixture
def checker():
    _app = QApplication.instance() or QApplication([])
    parent = QWidget()
    service = StoreUpdateChecker(parent, Mock())
    yield service
    service.timer.stop()
    parent.close()


def operation(result=None, error=None):
    return NS(status=1, get_results=Mock(return_value=result, side_effect=error), close=Mock())


def test_update_available_sets_flag_and_mandatory(checker):
    checker.context.get_app_and_optional_store_package_updates_async.return_value = operation(
        [NS(mandatory=True)]
    )
    checker.check()
    checker.check()  # ignored while busy
    checker.context.get_app_and_optional_store_package_updates_async.assert_called_once()
    assert checker.busy
    checker._poll()
    assert not checker.busy
    assert checker.update_available is True
    assert checker.mandatory is True


def test_no_updates_keeps_flag_false(checker):
    checker.context.get_app_and_optional_store_package_updates_async.return_value = operation([])
    checker.check()
    checker._poll()
    assert not checker.busy
    assert checker.update_available is False
    assert checker.mandatory is False


def test_error_silently_leaves_update_unavailable(checker):
    checker.context.get_app_and_optional_store_package_updates_async.return_value = operation(
        error=OSError("offline")
    )
    checker.check()
    checker._poll()
    assert not checker.busy
    assert checker.update_available is False


def test_open_store_product_page_prefers_store_uri_and_falls_back_to_web():
    with patch("folimeld.store_update.QDesktopServices.openUrl", return_value=True) as mock_open:
        assert open_store_product_page() is True
        mock_open.assert_called_once_with(QUrl(STORE_PRODUCT_URI))

    with patch("folimeld.store_update.QDesktopServices.openUrl", side_effect=[False, True]) as mock_open:
        assert open_store_product_page() is True
        assert mock_open.call_args_list[0].args == (QUrl(STORE_PRODUCT_URI),)
        assert mock_open.call_args_list[1].args == (QUrl(STORE_WEB_URL),)


def test_non_store_build_has_no_update_checker_or_button():
    from folimeld.app import MainWindow
    _app = QApplication.instance() or QApplication([])
    with patch("folimeld.app.is_packaged", return_value=False):
        window = MainWindow()
        assert window.store_update is None
        assert window.store_update_button is None
        window.close()


def test_store_build_shows_update_button_and_opens_store():
    from folimeld.app import MainWindow
    _app = QApplication.instance() or QApplication([])
    with patch("folimeld.app.is_packaged", return_value=True), \
         patch("folimeld.store_support.StoreSupport.refresh"), \
         patch("folimeld.store_update.StoreUpdateChecker.check"):
        window = MainWindow()
        assert window.store_update is not None
        assert window.store_update_button is not None
        assert window.store_update_button.isHidden()

        window.store_update.update_available = True
        window.store_update.changed.emit()
        assert not window.store_update_button.isHidden()

        with patch("folimeld.app.open_store_product_page") as mock_open:
            window.store_update_button.click()
            mock_open.assert_called_once()

        window.store_update.update_available = False
        window.store_update.changed.emit()
        assert window.store_update_button.isHidden()

        window.support.timer.stop()
        window.store_update.timer.stop()
        window.close()
