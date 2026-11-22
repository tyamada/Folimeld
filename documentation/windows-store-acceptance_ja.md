# Windows 11 MSIX受入試験

[日本語](windows-store-acceptance_ja.md) | [English](windows-store-acceptance.md)

アプリの版番号だけでなく、特定のパッケージに対してこの試験表を使用します。結果は `build/store-acceptance/<run>/` に保存し、公開用の確認記録は内容を確認して別途公開します。結果の証拠がない項目は未実施です。単体テストや未署名の開発用パッケージだけでStore公開可能とは判断しません。

## 候補の記録

パッケージ名・SHA-256、実行ファイルのSHA-256、ソースZIP・ハッシュ・対応JSON、パッケージのIdentity・Publisher・版・CPU、署名・配布経路、OSビルド、Python・依存ライブラリの版、Windows SDK・WACKの版、試験日・担当者を記録します。`dist/source/` の対応記録を候補と一緒に保管します。個人文書やパスワードは証拠に含めません。

```powershell
# 開発用パッケージの生成。インストールや証明書の変更はしません
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_msix.ps1
# パッケージのハッシュ。実際に生成したファイル名に置き換えます
Get-FileHash .\dist\Folimeld_0.3.3.0_x64.msix -Algorithm SHA256
```

静的検査の記録は `build/msix-preflight/development/x64/preflight.json` です。Storeビルドでは `development` が `store` になります。パッケージ内の実行ファイルのハッシュと対応JSONを照合します。Store候補の生成は、[公開計画](windows-store-release-plan_ja.md) に従って実Identityを確認してから行います。

## 試験表

Pythonを導入していないクリーンなWindows 11 x64試験環境で実施します。試験用ファイルはコピーを使用し、原本を保管します。各行に手順・期待値・実際の結果・証拠・合格／不合格／未実施を記録します。同時に複数の候補を試験しません。

| 分野 | 必要な動作と証拠 |
| --- | --- |
| 導入・起動 | 署名済み試験パッケージを導入し、スタートメニューから起動。ライセンス全文・ビルドソース情報を表示でき、開発PC固有パスやランタイム依存の不足がない |
| PDF関連付け | 日本語・空白を含むパスでもExplorerから正しい文書を開ける。関連付けの選択は利用者の指定を尊重 |
| 編集・履歴 | 回転・移動・削除・プロパティ・パスワードが動作し、保存後もUndo/Redoが可能。ディスク退避した履歴を復元できる |
| 保存ワーカー | 新規・上書き保存を再度開き、本文・画像・リンク・注釈・フォーム・メタデータ・パスワードを確認。書き込み失敗時は保存先と編集内容を保持 |
| 画像ワーカー | PNG・JPEG・複数ページTIFF、並び順・向き・透過・A4を確認。キャンセル・失敗時に既存文書を保持し、処理後に暗号化した中間ファイルを削除 |
| 一時データ | 実際の一時保存先と履歴・保存・画像変換の暗号コンテナを観察。通常終了・ワーカー失敗時の削除を確認し、本体の強制終了・OS停止時の残留は使い捨て文書で別途記録 |
| 設定・ログ | パッケージ化したアプリの実保存先を記録。再起動後の設定保持、ログのローテーションと試験パスワード・文書内容がないことを確認。手動削除とアンインストールの結果は分けて記録 |
| 更新・削除 | 同じIdentity・Publisherで版番号が大きい署名済みパッケージへ更新し、設定・起動・関連付けを確認。ユーザーのPDFを削除せず、アンインストール・再導入時の挙動を記録 |
| Store購入 | 実際のStore配信候補で購入・復元・キャンセル／返金・サービス利用不可時を確認。開発Identityの結果で購入機能を検証済みにしない |
| 認定 | 実際の署名済み候補で最新のWindows App Certification Kitを実行し、全結果を保存して失敗を調査。静的検査の成功をWACK成功と扱わない |

証明書の信頼設定変更・導入・WACKは試験環境で行います。ARM64はネイティブビルドと実機結果が別途必要です。修正後は影響する試験を再実施し、一般公開前にStore配信版でも再検証します。

## 開発版での過去の確認

開発版では、画像変換の中断、書き込み失敗、ディスク上の履歴、ローカルWACKを確認しました。これらの結果は下記のStore配信版の受入結果と分けて扱います。上記の試験表は今後の候補にも使用します。

## 参考資料

- [Microsoft: MSIXパッケージの実行・デバッグ・テスト](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-debug)
- [Microsoft: Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)

## Store配信版1.0.1.0の受入記録（2026-11-09）

Submission 1はMicrosoft Storeの認定に合格しました。Folimeld 1.0.1.0は2026年11月9日（日本時間）に日本と米国で公開されました。試験PCにはStore署名付きの `TakumaYamada.Folimeld` 1.0.1.0 x64を導入しました。

| 確認項目 | 結果 |
| --- | --- |
| Storeからの導入、起動、正常終了 | 成功 |
| PDF表示と別名保存 | 成功 |
| 画像2件のPDF変換と保存 | 成功 |
| PDF保存、画像変換、画像PDF保存のワーカー | 3種類すべての起動と終了を確認 |
| 応援購入 | 初回版にメニューが表示されないことを確認 |
| メインウィンドウのDPIコンテキスト | Per-Monitor V2を確認 |

メインウィンドウのDPIコンテキストを `GetWindowDpiAwarenessContext` で取得し、`AreDpiAwarenessContextsEqual` で比較しました。Per-Monitor V2との比較はtrue、Per-Monitor V1との比較はfalseでした。この確認は、実行中のメインウィンドウが対象です。150％・200％での表示確認は未実施です。

### 認定に関する未確認事項

| 項目 | 状況 |
| --- | --- |
| 旧ローカルWACKのDPI警告 | 原因は未確認。[過去の診断概要](windows-store-release-plan_ja.md#診断の追跡状況2026-11-04更新)を参照。 |
| TEST92とTEST88 | Store認定における個別判定は未確認。 |
| `runFullTrust` | 宣言を含む提出全体は認定に合格。機能単独の判定や審査コメントは未確認。 |

## Store候補1.0.2.0の準備と受入計画（Submission 2: x64 & ARM64）

Windows 11 ARM64 ネイティブ対応および大規模PDF機能強化を含む Submission 2（版番号 `1.0.2.0`）の受入計画です。2026年11月16日に Partner Center へ x64 および ARM64 の両パッケージを提出し、現在認定審査（Certification）中です。審査通過後に実際の Store 配信パッケージを用いて以下の受入試験を実施します。

### 候補パッケージと静的検査

| 項目 | x64 候補 | ARM64 候補 |
| --- | --- | --- |
| パッケージファイル | `dist/Folimeld_1.0.2.0_x64.msix` | `dist/Folimeld_1.0.2.0_arm64.msix` |
| パッケージ Identity | `TakumaYamada.Folimeld` | `TakumaYamada.Folimeld` |
| パッケージ Publisher | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` |
| パッケージ Family Name | `TakumaYamada.Folimeld_hn3600vb3j7rp` | `TakumaYamada.Folimeld_hn3600vb3j7rp` |
| 版番号 | `1.0.2.0` | `1.0.2.0` |
| 対象CPU (PE Machine) | `x64` (`0x8664`) | `arm64` (`0xAA64`) |
| パッケージ SHA-256 | `86E1617340093A4F0BC2DDFBCCC15FA5A0B97E3DE5ED229A93415B54F391C421` | `6BC0890A56E9AD028F91770167EBE7C3DDE2BD187CD0628BB9914D03B6A516CE` |
| 静的検査 (`msix_preflight`) | 合格 (`build/msix-preflight/store/x64/preflight.json`) | 合格 (`build/msix-preflight/store/arm64/preflight.json`) |
| ソースバンドル関連付け | `dist/source/Folimeld_1.0.2.0_x64.msix-86e1617340093a4f0bc2ddfbccc15fa5a0b97e3de5ed229a93415b54f391c421.json` | `dist/source/Folimeld_1.0.2.0_arm64.msix-6bc0890a56e9ad028f91770167ebe7c3dde2bd187cd0628bb9914d03b6a516ce.json` |

### Submission 2 受入確認項目

| 確認項目 | 対象 | 必要な動作と確認内容 | 状況 |
| --- | --- | --- | --- |
| 1.0.1.0 からの更新試験 | x64 | 署名済み 1.0.1.0 導入環境に 1.0.2.0 を更新導入。設定値、履歴、PDF 関連付けが正常に引き継がれることを確認 | 未実施 |
| ARM64 実機導入・起動 | ARM64 | Copilot+ PC（Snapdragon X Elite 等）の Windows 11 ARM64 でのネイティブ起動、正常終了、UI 操作の確認 | 未実施 |
| 大規模 PDF 保存高速化 | 両方 | 大規模文書での別プロセス保存、保存中進捗ダイアログ表示、上書き保存時の元ファイル保護を確認 | 単体テスト合格、実機確認待ち |
| 暗号化 Undo/Redo 履歴退避 | 両方 | メモリ上限（128 MiB）超過時の AES-256-GCM 暗号化一時退避と、復元・安全消去を確認 | 単体テスト合格、実機確認待ち |
| 画像フォルダー一括取り込み | 両方 | 画像一括取り込みダイアログからの PDF 作成、並び替え、回転、一時ファイル削除を確認 | 単体テスト合格、実機確認待ち |
| 完全無料アプリ維持 | 両方 | アプリ内購入メニューが表示されず、全機能が無料で利用できることを確認 | 確認済み |

## Store候補1.0.3.0の準備と受入計画（Submission 3: アプリ版 0.3.7 / x64 & ARM64）

Folimeld 0.3.7 の新機能（「サンプルPDFを開く…」「PDFを閉じる」・未読込時のモードレス案内）を反映した Submission 3（パッケージ版 `1.0.3.0`、アプリ表示版 `0.3.7`）の候補記録および受入計画です。x64 候補は 2026年11月22日に `release/windows-store-v1.0.3.0`（コミット `d21ec64eee8e33567a12c222069d4350051e96dc`）から生成・静的検査を完了しました。ARM64 候補は ARM64 実機で同一コミットからビルド後に追記します。

### 候補パッケージと静的検査

| 項目 | x64 候補 | ARM64 候補 |
| --- | --- | --- |
| パッケージファイル | `dist/Folimeld_1.0.3.0_x64.msix`（78,990,289 bytes） | 未生成（ARM64 実機ビルド待ち） |
| パッケージ Identity | `TakumaYamada.Folimeld` | `TakumaYamada.Folimeld` |
| パッケージ Publisher | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` | `CN=B897C2D7-6B65-499A-A779-BF572E2D81ED` |
| パッケージ Family Name | `TakumaYamada.Folimeld_hn3600vb3j7rp` | `TakumaYamada.Folimeld_hn3600vb3j7rp` |
| 版番号 / アプリ表示版 | `1.0.3.0` / `0.3.7` | `1.0.3.0` / `0.3.7` |
| 対象CPU (PE Machine) | `x64` (`0x8664`) | `arm64` (`0xAA64`) |
| パッケージ SHA-256 | `9017C3BBDDCD3F332D60D482E84434447A17D0E43416B6A899D1A375445894DC` | 未生成 |
| 静的検査 (`msix_preflight`) | 合格 (`build/msix-preflight/store/x64/preflight.json`) | 未実施 |
| ソースバンドル関連付け | `dist/source/Folimeld_1.0.3.0_x64.msix-9017c3bbddcd3f332d60d482e84434447a17d0e43416b6a899d1a375445894dc.json` | 未生成 |

### Submission 3 受入確認項目

| 確認項目 | 対象 | 必要な動作と確認内容 | 状況 |
| --- | --- | --- | --- |
| 前版からの更新試験 | 両方 | 署名済み `1.0.1.0` または `1.0.2.0` から `1.0.3.0` へ更新導入し、設定値・履歴・PDF 関連付けが正常に引き継がれることを確認 | 未実施 |
| サンプルPDF取得（オンライン） | 両方 | MSIX コンテナ内で「ファイル → サンプルPDFを開く…」を実行し、言語フィルター・並び順・CC BY 4.0 表示・SHA-256 検証・作業コピー展開が動作することを確認 | 未実施 |
| サンプルPDF再利用（オフライン） | 両方 | 一度取得・検証した原本をオフライン環境で再展開し、編集・別名保存しても原本キャッシュが書き換わらないことを確認 | 未実施 |
| PDF を閉じる・未読込時案内 | 両方 | 「ファイル → 閉じる」で開いている文書を閉じた後、未読込時のモードレス案内が表示され、そこからサンプルPDF取得または通常ファイル選択へ進めることを確認 | 未実施 |
| 無料・Sponsors 非表示維持 | 両方 | Store 版でアプリ内購入および GitHub Sponsors メニューが表示されず、全機能が無料で利用できることを確認 | 未実施 |
