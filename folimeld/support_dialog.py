from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from .store_support import TIER_ORDER


SPONSORS_URL = "https://github.com/sponsors/tyamada"

TIER_COLORS = {
    "bronze": ("#CD7F32", "#FFF7F0", "#7A4414"),
    "silver": ("#9EA7B3", "#F4F6F9", "#3D4652"),
    "gold": ("#D4AF37", "#FFFBF0", "#7A5B00"),
}

TIER_ICON_FILES = {
    "bronze": "tip_bronze.png",
    "silver": "tip_silver.png",
    "gold": "tip_gold.png",
}


class SponsorsDialog(QDialog):
    def __init__(self, tr, parent):
        super().__init__(parent)
        self.setWindowTitle(tr("support_title"))
        self.setMinimumWidth(380)
        layout = QVBoxLayout(self)
        description = QLabel(tr("sponsors_description"))
        description.setWordWrap(True)
        layout.addWidget(description)
        self.open_button = QPushButton(tr("sponsors_open"))
        self.open_button.clicked.connect(self.open_sponsors)
        layout.addWidget(self.open_button)
        self.error = QLabel(tr("sponsors_open_error"))
        self.error.setWordWrap(True)
        self.error.hide()
        layout.addWidget(self.error)
        close = QPushButton(tr("support_close"))
        close.clicked.connect(self.close)
        layout.addWidget(close)

    def open_sponsors(self):
        self.error.setVisible(not QDesktopServices.openUrl(QUrl(SPONSORS_URL)))


def supporter_icon(tier: str | None = None) -> QIcon:
    """Load the tier-specific badge artwork from source or bundled assets."""
    from .resources import resource_root
    root = resource_root()
    if tier in TIER_ICON_FILES:
        path = root / "assets" / "tip-icon" / TIER_ICON_FILES[tier]
        if path.is_file():
            return QIcon(str(path))
    return QIcon(str(root / "assets" / "folimeld-supporter-maid.png"))


def supporter_badge_style(tier: str) -> str:
    """Return a status-bar badge stylesheet tailored to the supporter tier."""
    border, bg, fg = TIER_COLORS.get(tier, TIER_COLORS["bronze"])
    return (
        f"QToolButton#supporter_badge {{"
        f" border: 1px solid {border};"
        f" border-radius: 10px;"
        f" background-color: {bg};"
        f" color: {fg};"
        f" padding: 1px 8px;"
        f" font-weight: 600;"
        f" }}"
    )


class SupportDialog(QDialog):
    def __init__(self, service, tr, parent):
        super().__init__(parent)
        self.service, self.tr = service, tr
        self.setWindowTitle(tr("support_title"))
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)
        previews = QHBoxLayout()
        previews.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for tier in TIER_ORDER:
            preview = QLabel()
            preview.setPixmap(supporter_icon(tier).pixmap(56, 56))
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview.setAccessibleName(tr(f"supporter_badge_{tier}"))
            previews.addWidget(preview)
        layout.addLayout(previews)
        description = QLabel(tr("support_description"))
        description.setWordWrap(True)
        layout.addWidget(description)
        self.status = QLabel()
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.buy_buttons: dict[str, QPushButton] = {}
        for tier in TIER_ORDER:
            button = QPushButton()
            button.setObjectName(f"buy_{tier}")
            button.setIcon(supporter_icon(tier))
            button.setIconSize(QSize(24, 24))
            button.clicked.connect(lambda checked=False, t=tier: service.purchase(t))
            layout.addWidget(button)
            self.buy_buttons[tier] = button
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
        for tier, button in self.buy_buttons.items():
            tier_label = self.tr(f"supporter_tier_{tier}")
            if tier in service.owned_tiers:
                button.setText(self.tr("support_owned_tier", tier=tier_label, owned=self.tr("support_owned")))
                button.setEnabled(False)
            elif tier in service.products:
                price = service.products[tier].price.formatted_price
                button.setText(self.tr("support_buy_tier", tier=tier_label, price=price))
                button.setEnabled(not service.busy)
            else:
                button.setText(tier_label)
                button.setEnabled(False)
        self.refresh_button.setEnabled(not service.busy)
