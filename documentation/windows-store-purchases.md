# Windows Store In-App Purchase (Folimeld Supporter Badge)

[日本語](windows-store-purchases_ja.md) | [English](windows-store-purchases.md)

This feature is **exclusive to the Microsoft Store (MSIX) edition**. Non-Store builds (Desktop EXE, uv, macOS, Linux, BSD) do not display Store purchase UI or the supporter badge. All PDF editing features remain free and identical regardless of purchase.

## Add-on specification

| Property | Value |
| --- | --- |
| Product title (`ja-JP`) | **Folimeld サポーターバッジ** |
| Product title (`en-US`) | **Folimeld Supporter Badge** |
| Add-on type | **Durable (one-time purchase)** |
| Product lifetime | **Forever** |
| Developer Product ID (`OFFER_TOKEN`) | `folimeld.supporter` ([folimeld/store_support.py](../folimeld/store_support.py)) |
| Base price tier | **\$2.99 USD** (auto-converted globally via Microsoft Store price tiers) |

### In-app cosmetic changes after purchase (Store edition only)

Once Microsoft Store license verification confirms active ownership (`is_active == True`), the supporter badge is displayed in three places:

1. **Status bar (right corner)**: Permanent supporter badge (18×18 icon + "Supporter" button; clicking opens the supporter dialog).
2. **Help menu**: "Support development…" updates to "Supporter…" with the supporter icon.
3. **About dialog**: Displays the 64×64 supporter icon and thank-you message.

## Partner Center setup

1. Open Folimeld (`9P5X2JFZRJC3`) in Partner Center → **Add-ons → Create a new add-on** → select **Durable**.
2. Set the developer Product ID to **`folimeld.supporter`** and Product lifetime to **Forever**.
3. Set the base price tier to **\$2.99 USD** (inspect exact local currency conversions via `View conversion table` if needed).
4. Add Japanese and English descriptions and a 300×300 add-on icon. Clearly state that this is a one-time purchase displaying a supporter badge in the status bar, Help menu, and About dialog, and that all PDF editing features remain free for everyone.
5. Submit the add-on for certification, then verify purchase, restart restore, multi-device restore, offline cache behavior, and refund revocation on a Store-installed build (via Hidden / Package flight and promotional codes or real purchase).

## Implementation and testing

- Windows-only WinRT dependencies are pinned in `requirements.txt` (`winrt-runtime`, `winrt-Windows.Services.Store`, `winrt-Windows.Foundation`, `winrt-Windows.Foundation.Collections`).
- `StoreContext` is initialized with the Qt main window HWND and polled on the UI thread with a 100ms `QTimer` so the UI stays responsive during checkout.
- The purchase button remains disabled until Store product metadata is loaded, and displays the Store-provided `formatted_price`.
- Entitlement is never persisted in local settings files; it is queried from the Store on startup, when opening the dialog, after purchase, and on manual refresh. Revoked/refunded licenses automatically hide the badge and revert the Help menu. Transient network failures do not clear known ownership.
- Unit tests in [tests/test_store_support.py](../tests/test_store_support.py) verify purchase confirmation, duplicate-click prevention, cancellation, errors, revocation, status bar badge visibility, About dialog badge rendering, and omission in non-Store builds.

Official documentation: https://learn.microsoft.com/en-us/windows/uwp/monetize/in-app-purchases-and-trials
