# Dynabook到着後の初回試験手順

[日本語](windows11-test-day_ja.md) | [English](windows11-test-day.md)

予定：2026-10-30（日本時間）。注文済みDynabookの実型番・CPU・メモリ・OSエディションは到着後に確認します。到着・試験結果はまだ未確認です。初回は実機への直接導入と通常動作を試し、VM構築や強制停止試験は行いません。

## 1. 到着と導入前の確認

- 販売店の保証条件、付属品、回復・再インストール手順を確認します。不具合や返品条件を確認する前に初期化しません。
- 型番、CPU、メモリ、SSD容量、画面解像度、Windowsの版・ビルド・x64、ライセンス認証状態を記録します。個人アカウントやプロダクトキーは記録・共有しません。
- BIOSの管理ロック、前の利用者・組織の管理登録がある場合は販売店に確認します。回避操作はしません。
- クリーンインストールが必要なら、販売店の回復方法・ライセンスを確認してから実施します。整備済みという説明だけでクリーン環境と扱いません。
- Windows Updateと必要なメーカー更新を適用し、求められた再起動を完了します。更新後のOSビルドを記録します。
- 試験用ユーザーを用意し、Python・Visual Studio・Folimeld旧版を追加しません。可能なら導入前のイメージを保存します。既存ランタイムなどの初期状態も分かる範囲で記録します。

## 2. 試験用一式の準備と導入

試験用ZIPをコピーし、ローカルの書き込み可能な場所へ展開します。ZIP横のJSONのSHA-256と照合します。例：

```powershell
Get-FileHash .\Folimeld-Windows11-x64-test.zip -Algorithm SHA256
```

`bundle.json`の証明書期限を確認します。現在の一式は7日間有効です。期限切れ・ハッシュ不一致・既存の`Folimeld.Dev`があれば、いったん止めて確認します。

展開先の手順書に従い、同じ試験ユーザーの管理者Windows PowerShellで実行します。Installは試験PCの証明書信頼とアプリ登録を変更します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Install
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Launch
```

## 3. 通常動作の試験表

[結果記録テンプレート](windows11-test-result-template.json)を試験用フォルダーへコピーし、実測値・結果を追記できます。状態は `not_run`、`pass`、`fail`、`partially_verified` を使い、未確認部分を具体的に残します。テンプレート原本は変更しません。

各行を「未実施／合格／不合格」にし、実結果・証拠ファイル名を追記します。原本は保管し、素材のコピー・別名保存先を使用します。すべて初期状態は未実施です。

| ID | 操作 | 期待する結果 |
| --- | --- | --- |
| T01 | 導入・登録Identityから起動 | 起動し、依存不足のエラーがない。版を確認できる |
| T02 | 日本語・空白入りパスのsample PDFを開く | 3ページを表示。メタデータ・目次・注釈・フォーム・添付が素材と一致 |
| T03 | 複数選択、回転・移動・Undo・Redo | 対象ページと順序が期待どおりに変わり、戻せる |
| T04 | コピーに別名保存し、閉じて再度開く | 編集結果が残り、リンク・注釈・フォーム・添付・メタデータを元と比較できる |
| T05 | password.pdfを開く・別コピーでパスワード変更 | 試験用`folimeld-test-only`で開く。保存後は新しい指定どおりのパスワードで開く |
| T06 | fixturesの画像取り込み、並べ替え、除外、A4指定、キャンセル | JPEG・PNGとTIFF各フレームを期待どおり処理。キャンセル時は元の文書を保持 |
| T07 | 日本語／英語に切替・再起動、ライセンスを表示 | 選択言語を保持。OpenSSL・Rust・CFFI/libffiの告知を閲覧できる |
| T08 | Explorerの「プログラムから開く」でFolimeldを選択 | 正しい文書を開く。利用者が希望しない既定アプリ変更をしない |
| T09 | Inspectで導入結果を保存 | installation-report.jsonが生成され、対象版・登録を確認できる |
| T10 | Removeでアプリ・追加した証明書信頼を解除 | 試験対象を削除。元からの信頼と素材を保持。実際の設定・ログ残留を記録 |

掲載画像も撮影する場合はT09の後、アプリを削除するT10の前に行います。

メニューや表示から確認できないPDF要素は未確認として残し、ビルドPCなどの独立したPDF検査で補完します。通常の起動成功だけで複雑なPDFの保存互換性を合格にしません。

## 4. 記録・後始末

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Inspect
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Remove
```

bundle.json、artifact-source.json、test-state.json、installation-report.json、保存したPDF、手動結果を同じ試験IDで保管します。導入失敗でも状態ファイルを削除せず後始末を行います。[導入・削除の詳細](windows-store-test-bundle_ja.md)を参照してください。

掲載画像は通常動作の確認後に[撮影計画](windows-store-screenshot-plan_ja.md)に従って撮影します。更新試験・WACK・実Store購入・OS強制停止試験・最終Store版の確認は[受入試験表](windows-store-acceptance_ja.md)に残します。PCに接続して試験していない結果を記入しません。
