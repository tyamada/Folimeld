from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import pytest
from PySide6.QtWidgets import QApplication, QWidget
from folimeld.store_support import OFFER_TOKENS, StoreSupport
from folimeld.support_dialog import SupportDialog, supporter_icon


@pytest.fixture
def service():
    _app = QApplication.instance() or QApplication([])
    parent = QWidget()
    store = StoreSupport(parent, Mock())
    yield store
    store.timer.stop()
    parent.close()


def operation(result=None, error=None):
    return NS(status=1, get_results=Mock(return_value=result, side_effect=error), close=Mock())


def license_for(*tiers: str):
    return NS(add_on_licenses={
        tier: NS(in_app_offer_token=OFFER_TOKENS[tier], is_active=True)
        for tier in tiers
    })


def product(tier: str, price: str):
    return NS(in_app_offer_token=OFFER_TOKENS[tier], product_kind='Durable',
              store_id=f'store-{tier}', price=NS(formatted_price=price))


def all_products():
    return {
        'bronze': product('bronze', '¥200'),
        'silver': product('silver', '¥500'),
        'gold': product('gold', '¥1,000'),
    }


def test_purchase_requires_verified_license_and_prevents_duplicates(service):
    service.products = all_products()
    service.context.request_purchase_async.return_value = operation(NS(status=0))
    service.context.get_app_license_async.return_value = operation(license_for('bronze'))
    service.context.get_associated_store_products_async.return_value = operation(
        NS(extended_error=NS(value=0), products=all_products()))
    service.purchase('bronze')
    service.purchase('bronze')
    service.context.request_purchase_async.assert_called_once_with('store-bronze')
    assert not service.owned
    service._poll()  # purchase result
    assert not service.owned
    service._poll()  # license result
    assert service.owned and service.highest_tier == 'bronze'
    service._poll()  # remaining catalog refresh
    assert not service.busy and service.message == 'support_thanks'


@pytest.mark.parametrize('status,message', [(2, 'support_cancelled'), (3, 'support_error'), (4, 'support_error')])
def test_failed_purchase_never_unlocks(service, status, message):
    service.products = all_products()
    service.context.request_purchase_async.return_value = operation(NS(status=status))
    service.purchase('silver')
    service._poll()
    assert not service.owned and not service.busy
    assert service.message == message


def test_highest_tier_precedence_and_revocation(service):
    service.owned_tiers = {'bronze', 'gold'}
    assert service.highest_tier == 'gold'
    service.context.get_app_license_async.return_value = operation(license_for('bronze'))
    service.context.get_associated_store_products_async.return_value = operation(error=OSError())
    service.refresh()
    service._poll()
    service._poll()
    assert service.highest_tier == 'bronze' and service.message == 'support_error'

    service.context.get_app_license_async.return_value = operation(license_for())
    service.context.get_associated_store_products_async.return_value = operation(error=OSError())
    service.refresh()
    service._poll()
    service._poll()
    assert not service.owned and service.highest_tier is None and service.message == 'support_error'


def test_network_failure_does_not_erase_known_ownership(service):
    service.owned_tiers = {'silver'}
    service.context.get_app_license_async.return_value = operation(error=OSError())
    service.refresh()
    service._poll()
    assert service.highest_tier == 'silver' and not service.busy


def test_hresult_zero_is_success_and_store_prices_are_displayed(service):
    service._products(NS(extended_error=NS(value=0), products=all_products()))
    dialog = SupportDialog(
        service,
        lambda key, **kw: (f"{kw['tier']} — {kw['price']}" if 'price' in kw
                           else f"{kw['tier']} — {kw['owned']}" if 'owned' in kw else key),
        service.parent(),
    )
    assert dialog.buy_buttons['bronze'].text().endswith('¥200')
    assert dialog.buy_buttons['silver'].text().endswith('¥500')
    assert dialog.buy_buttons['gold'].text().endswith('¥1,000')
    assert all(btn.isEnabled() for btn in dialog.buy_buttons.values())
    service.owned_tiers = {'silver'}
    service.changed.emit()
    assert not dialog.buy_buttons['silver'].isEnabled()
    assert dialog.buy_buttons['gold'].isEnabled()
    service.busy = True
    service.changed.emit()
    assert not any(btn.isEnabled() for btn in dialog.buy_buttons.values())


def test_unpublished_products_disable_purchase(service):
    service._products(NS(extended_error=NS(value=0), products={}))
    service.purchase('bronze')
    service.context.request_purchase_async.assert_not_called()
    assert service.message == 'support_unavailable'


def test_non_store_build_has_no_purchase_menu():
    from folimeld.app import MainWindow
    _app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=False):
        window = MainWindow()
        assert window.support is None
        assert window.supporter_badge is None
        assert not hasattr(window, 'support_action')
        window.close()


def test_store_build_supporter_badge_tiers_and_about():
    from folimeld.app import MainWindow
    _app = QApplication.instance() or QApplication([])
    with patch('folimeld.app.is_packaged', return_value=True), \
         patch('folimeld.store_support.StoreSupport.refresh'), \
         patch('folimeld.store_update.StoreUpdateChecker.check'):
        window = MainWindow()
        assert window.support is not None
        assert window.supporter_badge is not None
        assert window.supporter_badge.isHidden()

        window.support.owned_tiers = {'bronze'}
        window.support.changed.emit()
        assert not window.supporter_badge.isHidden()
        assert not window.support_action.icon().isNull()
        bronze_text = window.supporter_badge.text()

        window.support.owned_tiers = {'bronze', 'gold'}
        window.support.changed.emit()
        assert window.supporter_badge.text() != bronze_text

        with patch('folimeld.app.QMessageBox') as mock_box:
            window.about()
            mock_box.return_value.setIconPixmap.assert_called_once()
            mock_box.return_value.exec.assert_called_once()
            mock_box.about.assert_not_called()

        window.support.owned_tiers = set()
        window.support.changed.emit()
        assert window.supporter_badge.isHidden()

        with patch('folimeld.app.QMessageBox.about') as mock_about:
            window.about()
            mock_about.assert_called_once()

        window.support.timer.stop()
        window.close()


@pytest.mark.parametrize('tier', ['bronze', 'silver', 'gold'])
def test_tier_badge_icons_load(tier):
    _app = QApplication.instance() or QApplication([])
    icon = supporter_icon(tier)
    assert not icon.isNull()
    assert not icon.pixmap(32, 32).isNull()
