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
- **申請状況**: 2026年11月16日に Partner Center（Submission 2）へ両パッケージ（x64 および ARM64）を提出完了。現在認定審査（Certification）中。
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

## Submission 3（Folimeld 1.0.3.0: アプリ版 0.3.7 反映 / x64 + ARM64）の公開計画

Folimeld 0.3.7 の新機能（「サンプルPDFを開く…」「PDFを閉じる」・未読込時モードレス案内）を反映した次期アップデート（Submission 3）の計画です。

- **版番号**: パッケージ版 `1.0.3.0`（前回提出 `1.0.2.0` より大きい4要素版）、アプリ表示版 `0.3.7`
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
  - リリース用ブランチ `release/windows-store-v1.0.3.0`（コミット `d21ec64eee8e33567a12c222069d4350051e96dc`、アプリ版 `0.3.7`）を確定し、`docs/privacy/index.html` にサンプルPDF取得時の通信仕様を反映済み。
  - `dist/Folimeld_1.0.3.0_x64.msix`（78,990,289 bytes / 約 75.3 MiB、SHA-256: `9017C3BBDDCD3F332D60D482E84434447A17D0E43416B6A899D1A375445894DC`、PE Machine `0x8664`、静的検査 `build/msix-preflight/store/x64/preflight.json` 合格）を生成済み。対応ソース ZIP は `dist/source/Folimeld-source-ed842cf28552a7712d7ceb3dce1a5b86e6ac990b8dc3765489f0e681624df4cb.zip`、関連付け JSON は `dist/source/Folimeld_1.0.3.0_x64.msix-9017c3bbddcd3f332d60d482e84434447a17d0e43416b6a899d1a375445894dc.json`。
  - `dist/Folimeld_1.0.3.0_arm64.msix` は ARM64 実機上で同一ブランチ `release/windows-store-v1.0.3.0` からネイティブビルド予定。両パッケージ揃い次第、Partner Center（Submission 3）へ提出する。
- **ビルド・事前検査コマンド**:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture x64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_x64.msix

  powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1 `
    -Store -StoreConfig .\build\store-config.json -Architecture arm64 `
    -PreviousPackage .\dist\Folimeld_1.0.2.0_arm64.msix
  ```
- **対応ソース公開**: 認定・公開後にタグ `windows-store-v1.0.3.0` として対応ソース ZIP・`SHA256SUMS.txt`・`source-association.json` を公開する。

## 公式資料

- [提出方式の比較](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path)
- [MSIXパッケージ要件と版番号](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Storeポリシー](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIXの名前予約](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)

## 診断の追跡状況（2026-11-04更新）

開発版0.3.3.4と0.3.3.5の旧ローカルWACKでは、任意TEST88がFAIL、必須TEST92がWARNINGでした。過去の診断ではアクセス時の実行コンテキストがDPI警告に関係する可能性が示されました。当時のWACKプロセスを直接追跡しておらず、原因は未確認です。TEST88の調査ではAPI参照と文字列の一致を確認しました。これらの結果から、通常動作で検出対象の外部プログラムが起動したかどうかは判断できません。
