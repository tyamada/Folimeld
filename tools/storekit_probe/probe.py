"""Read-only Qt/ctypes/StoreKit integration probe, run inside a macOS app bundle."""
import ctypes
import json
from pathlib import Path
import sys


def main():
    if sys.platform != "darwin":
        raise SystemExit("This probe requires macOS 12 or later and a compiled StoreKit bridge.")

    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    library = ctypes.CDLL(str(Path(__file__).resolve().with_name("libStoreKitProbe.dylib")))
    library.folimeld_probe_start.argtypes = [ctypes.c_char_p]
    library.folimeld_probe_start.restype = None
    library.folimeld_probe_poll.argtypes = []
    library.folimeld_probe_poll.restype = ctypes.c_void_p
    library.folimeld_probe_free.argtypes = [ctypes.c_void_p]
    library.folimeld_probe_free.restype = None

    window = QWidget()
    window.setWindowTitle("Folimeld StoreKit probe — read only")
    layout = QVBoxLayout(window)
    identifier = QLineEdit()
    identifier.setPlaceholderText("App Store Connect product ID")
    button = QPushButton("Query product and entitlement")
    output = QTextEdit()
    output.setReadOnly(True)
    for widget in (identifier, button, output):
        layout.addWidget(widget)

    def start():
        product_id = identifier.text().strip()
        if not product_id:
            return
        button.setEnabled(False)
        output.append("Query started; no purchase or account sync will be requested.")
        library.folimeld_probe_start(product_id.encode("utf-8"))
        timeout.start(30000)

    def poll():
        while pointer := library.folimeld_probe_poll():
            try:
                message = json.loads(ctypes.string_at(pointer).decode("utf-8"))
            finally:
                library.folimeld_probe_free(pointer)
            output.append(json.dumps(message, ensure_ascii=False))
            if message.get("event") == "complete":
                timeout.stop()
                button.setEnabled(True)

    timer = QTimer(window)
    timer.timeout.connect(poll)
    timer.start(100)
    timeout = QTimer(window)
    timeout.setSingleShot(True)
    timeout.timeout.connect(lambda: output.append(
        "Still waiting after 30 seconds. This is not an unowned result. "
        "Close and reopen the probe if it does not complete."))
    button.clicked.connect(start)
    window.resize(640, 400)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
