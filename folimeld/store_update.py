"""Microsoft Store package update checker. All WinRT calls stay on the UI thread."""
from PySide6.QtCore import QObject, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices

from .windows_integration import is_packaged

STORE_PRODUCT_ID = "9P5X2JFZRJC3"
STORE_PRODUCT_URI = f"ms-windows-store://pdp/?ProductId={STORE_PRODUCT_ID}"
STORE_WEB_URL = f"https://apps.microsoft.com/detail/{STORE_PRODUCT_ID}"


def open_store_product_page() -> bool:
    """Open Folimeld's product page in the Microsoft Store app, with web fallback."""
    if QDesktopServices.openUrl(QUrl(STORE_PRODUCT_URI)):
        return True
    return QDesktopServices.openUrl(QUrl(STORE_WEB_URL))


def store_update_button_style() -> str:
    """Return a subtle status-bar pill button stylesheet for available Store updates."""
    return (
        "QToolButton#store_update_button {"
        " border: 1px solid #0067C0;"
        " border-radius: 10px;"
        " background-color: #EBF5FF;"
        " color: #004E96;"
        " padding: 1px 8px;"
        " font-weight: 600;"
        " }"
        "QToolButton#store_update_button:hover {"
        " background-color: #D6EBFF;"
        " }"
    )


class StoreUpdateChecker(QObject):
    changed = Signal()

    def __init__(self, parent, context=None):
        super().__init__(parent)
        self.context = context
        self.update_available = False
        self.mandatory = False
        self.busy = False
        self.operation = None
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._poll)

    def _context(self):
        if self.context is None:
            if not is_packaged():
                raise RuntimeError("Store update checks require package identity")
            from winrt.windows.services.store import StoreContext
            from winrt.runtime.interop import initialize_with_window
            self.context = StoreContext.get_default()
            initialize_with_window(self.context, int(self.parent().winId()))
        return self.context

    def check(self) -> None:
        if self.busy:
            return
        self.busy = True
        try:
            self.operation = self._context().get_app_and_optional_store_package_updates_async()
            self.timer.start()
        except Exception:
            self._finish(False, False)

    def _poll(self) -> None:
        try:
            if int(self.operation.status) == 0:  # AsyncStatus.STARTED
                return
            self.timer.stop()
            operation, self.operation = self.operation, None
            try:
                result = operation.get_results()
            finally:
                operation.close()
            updates = list(result) if result is not None else []
            mandatory = any(bool(getattr(item, "mandatory", False)) for item in updates)
            self._finish(len(updates) > 0, mandatory)
        except Exception:
            self._finish(False, False)

    def _finish(self, available: bool, mandatory: bool) -> None:
        self.timer.stop()
        self.operation = None
        self.busy = False
        self.update_available = available
        self.mandatory = mandatory
        self.changed.emit()
