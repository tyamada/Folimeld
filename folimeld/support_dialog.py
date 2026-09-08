import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


def supporter_icon():
    """Load the supporter artwork from source or bundled assets."""
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return QIcon(str(root / "assets" / "folimeld-supporter-maid.png"))


class SupportDialog(QDialog):
    def __init__(self, service, tr, parent):
        super().__init__(parent)
        self.service, self.tr = service, tr
        self.setWindowTitle(tr("support_title"))
        self.setMinimumWidth(380)
        layout = QVBoxLayout(self)
        preview = QLabel()
        preview.setPixmap(supporter_icon().pixmap(64, 64))
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview.setAccessibleName(tr("supporter"))
        layout.addWidget(preview)
        description = QLabel(tr("support_description"))
        description.setWordWrap(True)
        layout.addWidget(description)
        self.status = QLabel()
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.buy = QPushButton()
        self.buy.clicked.connect(service.purchase)
        layout.addWidget(self.buy)
        self.refresh_button = QPushButton(tr("support_refresh"))
        self.refresh_button.clicked.connect(service.refresh)
        layout.addWidget(self.refresh_button)
        close = QPushButton(tr("support_close"))
        close.clicked.connect(self.close)
        layout.addWidget(close)
        service.changed.connect(self.render)
        self.render()

    def render(self):
        service = self.service
        self.status.setText(self.tr(service.message))
        price = service.product.price.formatted_price if service.product else ""
        self.buy.setText(self.tr("support_buy", price=price))
        self.buy.setVisible(not service.owned)
        self.buy.setEnabled(not service.busy and service.product is not None)
        self.refresh_button.setEnabled(not service.busy)
