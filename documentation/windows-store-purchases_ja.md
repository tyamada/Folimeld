# Windows 応援購入（Folimeld サポーターバッジ）

[日本語](windows-store-purchases_ja.md) | [English](windows-store-purchases.md)

この仕様は **Microsoft Store（MSIX）版限定** です。通常 EXE・uv・macOS・Linux・BSD 版では Store 購入 UI およびサポーターバッジは表示されません。PDF 編集機能はすべての環境・購入有無にかかわらず無料で同一です。

## 商品仕様（Store アドオン）

| 項目 | 設定値 |
| --- | --- |
| 商品名（日本語 / `ja-JP`） | **Folimeld サポーターバッジ** |
| 商品名（英語 / `en-US`） | **Folimeld Supporter Badge** |
| 種別 | **Durable（永続 / 1回限りの買い切り）** |
| 有効期限（Product lifetime） | **Forever（無期限）** |
| 開発者指定 Product ID（`OFFER_TOKEN`） | `folimeld.supporter`（[folimeld/store_support.py](../folimeld/store_support.py)） |
| 基準価格ティア | **\$2.99 USD**（Microsoft Store 標準ティアで各国通貨へ自動換算） |

### 購入後のアプリ内変化（Store 版限定）

Microsoft Store のライセンス照会で所有が確認（`is_active == True`）されると、アプリ内の以下 3 箇所にサポーターバッジが表示されます：

1. **ステータスバー右端**: 常設サポーターバッジ（18×18 アイコン＋「サポーター」ボタン、クリックでサポーターダイアログを表示）
2. **ヘルプメニュー**: 「開発を応援する…」がサポーターアイコン付き「サポーター…」へ変化
3. **バージョン情報（About）ダイアログ**: 64×64 サポーターアイコンと感謝メッセージを表示

## Partner Center 登録手順

1. Partner Center の Folimeld（`9P5X2JFZRJC3`）で **Add-ons → Create a new add-on** を開き、種別 **Durable** を選択する。
2. 開発者指定の Product ID に **`folimeld.supporter`** を設定し、有効期限を **Forever** にする。
3. 価格ティアに **\$2.99 USD** を設定する（必要に応じ `View conversion table` で日本円換算額を確認）。
4. 日英の説明文と 300×300 アドオンアイコンを登録する。説明には「1回限りの買い切り購入でステータスバー・ヘルプメニュー・バージョン情報にサポーターバッジが表示されること」「PDF 編集機能は全ユーザー無料で同一であること」を明記する。
5. アドオンを提出して認定を通し、限定公開（Hidden / Package flight）または Store 配信版でプロモーションコード／実購入による導入・再起動復元・別 PC 復元・オフライン挙動・返金反映を実機確認する。

## ローカル MSIX の署名（開発確認用）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\sign_dev_msix.ps1 -PackagePath .\dist\Folimeld_1.0.4.0_x64.msix
```

- マニフェストの Publisher に一致する開発用証明書で署名済みコピーを `build/dev-signing/` へ出力します（元の未署名 MSIX は変更しません）。
- 証明書を信頼しても Store の商品登録や実課金テスト環境の関連付けは完了しません。実購入の検証は Partner Center で関連付けた Store 経由インストール版で行います。

## 実装と検証

- 依存は `requirements.txt` に Windows 限定で指定（`winrt-runtime`, `winrt-Windows.Services.Store`, `winrt-Windows.Foundation`, `winrt-Windows.Foundation.Collections`）。
- `StoreContext` へ Qt メインウィンドウの HWND を渡し、WinRT 非同期操作を Qt タイマー（100ms）で監視するため、購入待ちの間も UI は応答します。
- 商品情報が得られるまで購入ボタンは無効です。価格は Store が返す `formatted_price` をそのまま表示します。
- 購入状態はローカル設定ファイルへ保存せず、起動時・ダイアログ表示時・購入後・再確認ボタンで Store へ照会します。返金・失効時は再確認時にバッジとアイコンを自動的に非表示へ戻します。通信エラーだけでは既知の購入権利を削除しません。
- 単体テストは [tests/test_store_support.py](../tests/test_store_support.py) で購入成功・重複防止・キャンセル・障害・権利取り消し・ステータスバーバッジ・バージョン情報表示・非 Store 版非表示を検証します。

公式資料: https://learn.microsoft.com/en-us/windows/uwp/monetize/in-app-purchases-and-trials
