# Windows Store In-App Purchases (Folimeld Supporter Badges — 3 Tiers)

[日本語](windows-store-purchases_ja.md) | [English](windows-store-purchases.md)

This feature is **exclusive to the Microsoft Store (MSIX) edition**. Non-Store builds (Desktop EXE, uv, macOS, Linux, BSD) do not display Store purchase UI or supporter badges. All PDF editing features remain free and identical regardless of purchase.

## Add-on specification (Durable / one-time purchases)

Aligned with App Store and Google Play, Folimeld offers **three one-time Durable tiers (Bronze / Silver / Gold)** with **Forever** product lifetime:

| Tier | Product ID (`OFFER_TOKEN`) | Japanese title (`ja-JP`) | English title (`en-US`) | Base price (USD) | Japan market price (JPY) |
| --- | --- | --- | --- | --- | --- |
| **Bronze** | `folimeld.supporter.bronze` | **Folimeld サポーターバッジ（ブロンズ）** | **Folimeld Supporter Badge (Bronze)** | **\$1.99** | **¥200** |
| **Silver** | `folimeld.supporter.silver` | **Folimeld サポーターバッジ（シルバー）** | **Folimeld Supporter Badge (Silver)** | **\$4.99** | **¥500** |
| **Gold** | `folimeld.supporter.gold` | **Folimeld サポーターバッジ（ゴールド）** | **Folimeld Supporter Badge (Gold)** | **\$9.99** | **¥1,000** |

- Product IDs are defined in `SUPPORTER_TIERS` inside [folimeld/store_support.py](../folimeld/store_support.py).
- Configure the USD base price tiers in Partner Center and override the Japan market price to **¥200 / ¥500 / ¥1,000**.

### In-app cosmetic changes after purchase (Store edition only)

Once Microsoft Store license verification confirms active ownership (`is_active == True`), the **highest owned tier (Gold > Silver > Bronze)** is displayed in three places with tier-specific colors and labels:

1. **Status bar (right corner)**: Tier-styled permanent supporter badge (18×18 icon + "Supporter (Bronze / Silver / Gold)" button; clicking opens the supporter dialog).
2. **Help menu**: "Support development…" updates to "Supporter (Bronze / Silver / Gold)…" with the supporter icon.
3. **About dialog**: Displays the 64×64 supporter icon, tier badge label, and thank-you message.

## Partner Center setup

1. Open Folimeld (`9P5X2JFZRJC3`) in Partner Center → **Add-ons → Create a new add-on** → create three **Durable** add-ons.
2. Set the developer Product IDs to `folimeld.supporter.bronze`, `folimeld.supporter.silver`, and `folimeld.supporter.gold` with Product lifetime **Forever**.
3. Set USD base price tiers to **\$1.99 / \$4.99 / \$9.99** and set Japan market overrides to **¥200 / ¥500 / ¥1,000**.
4. Add Japanese and English titles, descriptions, and 300×300 add-on icons. Clearly state that each is a one-time purchase displaying the selected tier badge in the status bar, Help menu, and About dialog, that the highest owned tier is shown if multiple are purchased, and that all PDF editing features remain free for everyone.
5. Submit all three add-ons for certification, then verify purchase, restart restore, multi-device restore, higher-tier upgrade display, offline cache behavior, and refund revocation on a Store-installed build.

## Implementation and testing

- Windows-only WinRT dependencies are pinned in `requirements.txt` (`winrt-runtime`, `winrt-Windows.Services.Store`, `winrt-Windows.Foundation`, `winrt-Windows.Foundation.Collections`).
- `StoreContext` is initialized with the Qt main window HWND and polled on the UI thread with a 100ms `QTimer` so the UI stays responsive during checkout.
- Purchase buttons remain disabled until Store product metadata is loaded, and display the Store-provided `formatted_price`.
- Entitlement is never persisted in local settings files; it is queried from the Store on startup, when opening the dialog, after purchase, and on manual refresh. Revoked/refunded licenses automatically fall back to the next highest owned tier or hide the badge. Transient network failures do not clear known ownership.
- Unit tests in [tests/test_store_support.py](../tests/test_store_support.py) verify 3-tier purchase confirmation, duplicate-click prevention, cancellation, errors, highest-tier precedence, revocation, status bar badge styling/visibility, About dialog rendering, and omission in non-Store builds.

Official documentation: https://learn.microsoft.com/en-us/windows/uwp/monetize/in-app-purchases-and-trials
