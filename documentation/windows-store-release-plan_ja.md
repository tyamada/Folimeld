# Microsoft Store公開計画

[日本語](windows-store-release-plan_ja.md) | [English](windows-store-release-plan.md)

## Folimeld 1.0.1.0の公開状況

Windows 11 x64向けMSIXの初回提出（Submission 1）はMicrosoft Storeの認定に合格し、2026年11月9日（日本時間）に公開しました。Store製品IDは `9P5X2JFZRJC3` で、[日本](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=ja-JP&gl=JP)と[米国](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=en-US&gl=US)で無料配信中です。初回版では応援購入を無効にしています。

Store配信版で導入と通常動作を確認し、メインウィンドウがPer-Monitor V2であることを確認しました。実施した確認とその範囲は[Windows 11 MSIX受入記録](windows-store-acceptance_ja.md)に記載しています。

旧ローカルWACKで発生したDPI警告の原因は未確認です。`runFullTrust` を宣言したStore提出全体は認定に合格しました。TEST92（DPI対応）、TEST88（ブロック済みの実行可能ファイル）、`runFullTrust` のStore認定における個別判定は未確認です。

## 登録と更新時の確認項目

更新には公開済みのMSIX製品登録を使用します。ビルド設定に入力する値は、事前にPartner Centerで確認します。

| Partner Centerの項目 | Store設定のキー |
| --- | --- |
| `Package/Identity/Name` | `identity_name` |
| `Package/Identity/Publisher` | `publisher` |
| `Package/Properties/PublisherDisplayName` | `publisher_display_name` |

1. 提出候補のパッケージ版、署名、ソースとの対応を確認します。
2. [掲載情報](windows-store-listing_ja.md)、[スクリーンショット](windows-store-screenshot-plan_ja.md)、[公開済みプライバシーポリシー](https://tyamada.github.io/Folimeld/privacy/)を確認します。
3. 認定結果を記録し、対象地域での公開を確認します。配信版のバージョンと変更の影響を受ける機能は、開発ビルドと分けて確認します。

## Store用ビルドの準備

`packaging/msix/store-config.example.json` を `build/store-config.json` へコピーし、先頭3項目に確認済みのMSIX登録情報を記入する。例の空欄は意図的で、そのままではStore用の検証に失敗する。ファイルには認証情報や秘密鍵を入れない。

`package_version` はMSIX用の4要素の版番号で、アプリ表示版 `folimeld/__init__.py` の `__version__` と分けて管理する。Storeモードでは先頭を1以上、末尾を0、各要素を65535以下にする。更新では同じIdentity/Publisherの前回MSIXより大きくする。以前のEXE/MSI製品や開発用MSIXを `-PreviousPackage` に指定しない。

Store用の最低OSはWindows 11を想定している。例の `minimum_windows_version` は `10.0.22000.0`、`maximum_tested_windows_version` は `10.0.26100.0`。設定例は実機試験の証拠ではなく、対応するOSと実際の検証結果に合わせて更新する。開発モードの既定の最低OSは従来のまま。

```powershell
# 設定とマニフェストのみ検証。EXEの再ビルド・MSIX生成・インストールは行わない
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json -ValidateOnly

# 設定が確定した後に提出候補を生成
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json
```

更新時は `-PreviousPackage` で前回のMSIXを指定できる。ARM64は同じコマンドに `-Architecture arm64` を追加し、ARM64のPython/PyInstaller環境でビルドする。`-PythonExecutable` で使用するPythonの絶対パスを指定でき、EXE生成にも同じPythonを渡す。

設定とマニフェストは `build/msix-preflight/<モード>/<アーキテクチャ>/` に出力する。生成MSIXの検査結果は同じ場所の `preflight.json`。Identity、版番号、OS設定、EXEのCPU種類、PDF関連付け、アイコン、ライセンスファイルとパッケージのSHA-256を確認する。静的検査の成功はPartner Centerとの登録一致、WACK成功、実機試験、ライセンス条件、審査通過を保証しない。

## Submission 2（Folimeld 1.0.2.0: x64 + ARM64 両対応）の公開計画

Windows 11 x64 に加え、Windows 11 ARM64（Surface Pro 11 等の Copilot+ PC / Snapdragon X Elite）へのネイティブ対応を追加した次期アップデート（Submission 2）の計画です。

- **版番号**: `1.0.2.0`（前回公開版 `1.0.1.0` より大きい4要素バージョン番号）
- **対象アーキテクチャ**: `x64` および `arm64`（PE Machine `0xAA64` ネイティブ）
- **配布形態・価格**: 完全無料（無料アプリのみとして応援購入・アドオン登録は無効を維持）
- **反映される新機能**:
  - Windows 11 ARM64 ネイティブ対応
  - 大規模 PDF 保存の高速化（進捗ダイアログ、重複ストリーム検査省略、別プロセス書き出し、クラッシュ保護）
  - Undo/Redo 履歴のディスク退避（AES-256-GCM 暗号化、最大 1 GiB）
  - サムネイル仮想化（1,000 ページ超の文書でもメモリ浪費を防ぐ表示最適化）
  - 画像フォルダー一括取り込み（PNG, JPEG, TIFF, BMP, WebP の PDF 化）
- **申請状況**: 2026年11月16日に Partner Center（Submission 2）へ両パッケージ（x64 および ARM64）を提出し、認定合格・公開完了（2026年11月21日更新）。対応ソースは GitHub Releases タグ [`windows-store-v1.0.2.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.2.0) にて公開済み。
- **パッケージ構成（生成・静的検査完了・提出済み）**:
  - `dist/Folimeld_1.0.2.0_x64.msix`（約 76.4 MB、SHA-256: `86E1617340093A4F0BC2DDFBCCC15FA5A0B97E3DE5ED229A93415B54F391C421`、PE Machine `0x8664`、静的検査合格）
  - `dist/Folimeld_1.0.2.0_arm64.msix`（約 62.9 MB、SHA-256: `6BC0890A56E9AD028F91770167EBE7C3DDE2BD187CD0628BB9914D03B6A516CE`、PE Machine `0xAA64`、静的検査合格）
  - Partner Center の同一申請（Submission 2）のパッケージ画面で両 MSIX をアップロードし、クライアント端末の CPU に応じて自動配信。
- **ビルド・事前検査コマンド**:
  ```powershell
  # x64 パッケージ生成と静的検査（前回版とのバージョン・同一ファミリー比較）
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture x64 `
    -PreviousPackage .\dist\Folimeld_1.0.1.0_x64.msix

  # ARM64 パッケージ生成と静的検査
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture arm64
  ```

## Submission 3（Folimeld 1.0.4.0: アプリ版 0.3.7 反映 / x64 + ARM64）の公開計画

Folimeld 0.3.7 の新機能（「サンプルPDFを開く…」「PDFを閉じる」・未読込時モードレス案内）を反映した次期アップデート（Submission 3）の計画です。なお、`1.0.3.0`（x64）は既存のパッケージフライト（`Folimeld 1.0.3.0 x64 Thumbnail Fix`）で使用済みのため、Partner Center の一意性要件に従いパッケージ版を `1.0.4.0` へ繰り上げました。

- **版番号**: パッケージ版 `1.0.4.0`（前回公開 `1.0.2.0` および旧フライト `1.0.3.0` より大きい4要素版）、アプリ表示版 `0.3.7`
- **対象アーキテクチャ**: `x64`（`0x8664`）および `arm64`（`0xAA64`）
- **配布形態・価格**: 完全無料（応援購入・アドオン登録および GitHub Sponsors メニューは無効／非表示を維持）
- **反映される 0.3.7 新機能**:
  - 「ファイル → サンプルPDFを開く…」および PDF 未読込時の案内からのサンプルPDFマンガ取得（言語フィルター、最新話／1話順、CC BY 4.0 表示、SHA-256 検証、検証済み原本のオフライン再利用、編集用作業コピーの展開）
  - 「ファイル → 閉じる（PDFを閉じる）」操作と未読込時のモードレス案内
- **審査・プライバシー整合性**:
  - 編集対象のユーザー PDF・画像は外部送信せずローカル処理する原則を維持。
  - 利用者が明示的に「サンプルPDFを開く…」を実行した場合のみ、固定 HTTPS（GitHub リリース）からカタログおよび指定サンプル PDF を取得する旨をプライバシーポリシー・Store 掲載文・審査メモへ明記する。
- **スクリーンショット素材**:
  - ドキュメント・Web サイト・Store 掲載用スクリーンショットは `testdata/tameshibu_episode1_2_en.pdf`（CC BY 4.0、作者：こまいろ日和 / Komairo Hiyori）のコピーを使用して日英それぞれ撮影済み（`build/store-listing/screenshots/ja-JP/`・`en-US/` 01〜06 および `documentation/screenshots/`。詳細は[スクリーンショット撮影計画](windows-store-screenshot-plan_ja.md)を参照）。
- **ビルド・準備状況（2026-11-22 時点）**:
  - リリース用ブランチ `release/windows-store-v1.0.4.0`（コミット `8f6b47c`、アプリ版 `0.3.7`）を確定し、`docs/privacy/index.html` にサンプルPDF取得時の通信仕様を反映済み。
  - `dist/Folimeld_1.0.4.0_x64.msix`（78,990,624 bytes / 約 75.3 MiB、SHA-256: `CD081C96BC0838BFE1B65E59814F29DFF31957D34119F3AF1BE51357A670B6A9`、PE Machine `0x8664`、静的検査 `build/msix-preflight/store/x64/preflight.json` 合格）を生成済み。対応ソース ZIP は `dist/source/Folimeld-source-2fee6f48a3bc5c09ec6e80c142d593c6b2781abc0ad9794912749a80a847450e.zip`、関連付け JSON は `dist/source/Folimeld_1.0.4.0_x64.msix-cd081c96bc0838bfe1b65e59814f29dff31957d34119f3af1be51357a670b6a9.json`。
  - `dist/Folimeld_1.0.4.0_arm64.msix`（62,377,071 bytes / 約 59.5 MiB、SHA-256: `9597D6F142A4520680BB1C943EC5ABA951549448CB8ADC30728A69379DAF7364`、PE Machine `0xAA64`、静的検査 `build/msix-preflight/store/arm64/preflight.json` 合格）を ARM64 実機で生成済み。関連付け JSON は `dist/source/Folimeld_1.0.4.0_arm64.msix-9597d6f142a4520680bb1c943ec5aba951549448cb8adc30728a69379daf7364.json`。
  - **申請・公開状況**: 2026年11月22日に Partner Center（Submission 3 / ID `1152921505702470707`）へ両パッケージ（x64・ARM64）、日英ストア掲載文・スクリーンショット各 6 枚、審査メモを提出し、自動公開設定へ変更。認定合格後、Microsoft Store にて `1.0.4.0`（x64・ARM64）の公開を確認済み（2026年11月24日確認）。
- **ビルド・事前検査コマンド**:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture x64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_x64.msix

  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture arm64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_arm64.msix
  ```
- **対応ソース公開**: GitHub Releases タグ [`windows-store-v1.0.4.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.4.0) にて対応ソース ZIP・`SHA256SUMS.txt`・`source-association.json` を公開済み。

## Submission 4（Folimeld 1.0.5.0: アプリ版 0.3.8 / Store 更新確認＋3 ティア サポーターバッジ UI）の公開記録

- **版番号**: パッケージ版 `1.0.5.0`、アプリ表示版 `0.3.8`（ブランチ `release/windows-store-v1.0.5.0`、コミット `9ef9c1e44edac9d47a84b6386ee703304684fa29`）
- **対象アーキテクチャ**: `x64`（`0x8664`）および `arm64`（`0xAA64`）
- **主な新機能（Store 版限定）**:
  - Windows 標準の `StoreContext.get_app_and_optional_store_package_updates_async()` による起動時更新確認と、更新版がある場合のステータスバー「更新する」ボタン（クリックで `ms-windows-store://pdp/?ProductId=9P5X2JFZRJC3` を開く）
  - 3 ティア サポーターバッジ UI（Bronze / Silver / Gold、`assets/tip-icon/` 同梱）
- **提出・公開状況**: 2026年11月25日に Partner Center（Submission 4 / ID `1152921505702500801`）へ x64・ARM64 両パッケージを提出し、同日認定合格・自動公開を確認済み。
  - `Folimeld_1.0.5.0_x64.msix`（83,404,506 bytes、SHA-256: `B430CBBA5C144E8F1FBC99302BA0B8AE4C8F580E923942D1689EFEE0CCBF6FDF`）
  - `Folimeld_1.0.5.0_arm64.msix`（66,785,943 bytes、SHA-256: `C5E9C8F2394EC1600EE4B69A5762FC6582A62575E120D1D8CC4511C41297F0EE`）
- **対応ソース公開**: GitHub Releases タグ [`windows-store-v1.0.5.0`](https://github.com/tyamada/Folimeld/releases/tag/windows-store-v1.0.5.0) にて対応ソース ZIP・`SHA256SUMS.txt`・`source-association.json` を公開済み。

## 公式資料

- [提出方式の比較](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path)
- [MSIXパッケージ要件と版番号](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Storeポリシー](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIXの名前予約](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)

## 診断の追跡状況（2026-11-04更新）

開発版0.3.3.4と0.3.3.5の旧ローカルWACKでは、任意TEST88がFAIL、必須TEST92がWARNINGでした。過去の診断ではアクセス時の実行コンテキストがDPI警告に関係する可能性が示されました。当時のWACKプロセスを直接追跡しておらず、原因は未確認です。TEST88の調査ではAPI参照と文字列の一致を確認しました。これらの結果から、通常動作で検出対象の外部プログラムが起動したかどうかは判断できません。
