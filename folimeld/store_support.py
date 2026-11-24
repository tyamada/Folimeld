"""Microsoft Store durable supporter add-ons (Bronze / Silver / Gold). All WinRT calls stay on the UI thread."""
from PySide6.QtCore import QObject, QTimer, Signal
from .windows_integration import is_packaged

SUPPORTER_TIERS = (
    ("bronze", "folimeld.supporter.bronze"),
    ("silver", "folimeld.supporter.silver"),
    ("gold", "folimeld.supporter.gold"),
)
TIER_ORDER = ("bronze", "silver", "gold")
OFFER_TOKENS = dict(SUPPORTER_TIERS)


class StoreSupport(QObject):
    changed = Signal()

    def __init__(self, parent, context=None):
        super().__init__(parent)
        self.context = context
        self.owned_tiers: set[str] = set()
        self.products: dict[str, object] = {}
        self.busy = False
        self.message = "support_loading"
        self.operation = None
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._poll)

    @property
    def owned(self) -> bool:
        return bool(self.owned_tiers)

    @property
    def highest_tier(self) -> str | None:
        for tier in reversed(TIER_ORDER):
            if tier in self.owned_tiers:
                return tier
        return None

    def _context(self):
        if self.context is None:
            if not is_packaged():
                raise RuntimeError("Store purchases require package identity")
            from winrt.windows.services.store import StoreContext
            from winrt.runtime.interop import initialize_with_window
            self.context = StoreContext.get_default()
            initialize_with_window(self.context, int(self.parent().winId()))
        return self.context

    def _run(self, factory, callback):
        self.busy = True
        self.message = "support_loading"
        self.changed.emit()
        try:
            self.operation = factory()
            self.callback = callback
            self.timer.start()
        except Exception:
            self._finish("support_error")

    def _poll(self):
        try:
            if int(self.operation.status) == 0:  # AsyncStatus.STARTED
                return
            self.timer.stop()
            operation, self.operation = self.operation, None
            try:
                result = operation.get_results()  # raises on cancellation/error
            finally:
                operation.close()
            self.callback(result)
        except Exception:
            self._finish("support_error")

    def _finish(self, message):
        self.timer.stop()
        self.operation = None
        self.busy = False
        self.message = message
        self.changed.emit()

    def refresh(self):
        if self.busy:
            return
        self.products = {}
        self._run(lambda: self._context().get_app_license_async(), self._license)

    def _license(self, license):
        licenses = list(license.add_on_licenses.values())
        self.owned_tiers = {
            tier for tier, token in SUPPORTER_TIERS
            if any(item.in_app_offer_token == token and item.is_active for item in licenses)
        }
        self.changed.emit()
        if len(self.owned_tiers) == len(SUPPORTER_TIERS):
            self._finish("support_thanks")
        else:
            self._run(lambda: self._context().get_associated_store_products_async(["Durable"]),
                      self._products)

    def _products(self, result):
        if result.extended_error.value < 0:
            self._finish("support_error")
            return
        available = list(result.products.values())
        self.products = {}
        for tier, token in SUPPORTER_TIERS:
            product = next((p for p in available
                            if p.in_app_offer_token == token and p.product_kind == "Durable"), None)
            if product is not None:
                self.products[tier] = product
        if self.owned:
            self._finish("support_thanks")
        else:
            self._finish("support_ready" if self.products else "support_unavailable")

    def purchase(self, tier: str):
        if self.busy or tier in self.owned_tiers or tier not in self.products:
            return
        product = self.products[tier]
        self._run(lambda: self._context().request_purchase_async(product.store_id), self._purchased)

    def _purchased(self, result):
        # StorePurchaseStatus: SUCCEEDED=0, ALREADY_PURCHASED=1, NOT_PURCHASED=2.
        if int(result.status) in (0, 1):
            self.products = {}
            self._run(lambda: self._context().get_app_license_async(), self._license)
        else:
            self._finish("support_cancelled" if int(result.status) == 2 else "support_error")
