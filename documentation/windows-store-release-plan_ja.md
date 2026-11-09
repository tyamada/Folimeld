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

## 公式資料

- [提出方式の比較](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path)
- [MSIXパッケージ要件と版番号](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Storeポリシー](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIXの名前予約](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)

## 診断の追跡状況（2026-11-04更新）

開発版0.3.3.4と0.3.3.5の旧ローカルWACKでは、任意TEST88がFAIL、必須TEST92がWARNINGでした。過去の診断ではアクセス時の実行コンテキストがDPI警告に関係する可能性が示されました。当時のWACKプロセスを直接追跡しておらず、原因は未確認です。TEST88の調査ではAPI参照と文字列の一致を確認しました。これらの結果から、通常動作で検出対象の外部プログラムが起動したかどうかは判断できません。
