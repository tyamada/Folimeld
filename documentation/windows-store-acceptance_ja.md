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

## 参考資料

- [Microsoft: MSIXパッケージの実行・デバッグ・テスト](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-debug)
- [Microsoft: Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)
