# 別のWindows 11試験用PC／VMでの検証

[日本語](windows-store-test-bundle_ja.md) | [English](windows-store-test-bundle.md)

受入試験先として選択した、別のWindows 11 x64試験用PC／VMで開発用パッケージを使用します。導入・WACKは実際に試験先で実施するまで未実施です。ビルドPCでの署名準備だけでは、導入後の動作を確認したことにはなりません。

## ビルドPCでの準備

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/prepare_msix_test.ps1 `
  -Package dist/Folimeld_0.3.3.0_x64.msix `
  -OutputDirectory build/store-test-bundles/new-run
```

Windows SDKのSignToolと、`dist/source/` にある入力パッケージの対応ソース記録が必要です。7日間有効な自己署名の開発用証明書を作り、一時PFXは後始末で削除します。ビルドPCへの証明書ストア登録・アプリ導入はしません。既存の出力先や別Identityのパッケージは拒否します。署名後の実行ファイルの内容と元の対応ソース記録を照合します。CMS署名は信頼登録せずに検証するため、ビルドPCのAuthenticode信頼判定は成功しない場合があります。この証明書・パッケージはローカル試験用で、Store提出用ではありません。

生成したディレクトリ全体を移送します。署名済みMSIX、公開証明書、`bundle.json`、`artifact-source.json`、対応ソースZIP、`test_msix_on_vm.ps1`が含まれます。署名でパッケージのハッシュは変わるため、入力パッケージと元のソース記録も保管します。試験用素材・説明書を追加した場合は、それらも一緒に移送します。秘密鍵は移送しません。有効期限を過ぎたら再生成します。

## 試験用PC／VMでの実行

ディレクトリをローカルの書き込み可能な場所へコピーします。導入・後始末は同じ試験ユーザーの管理者Windows PowerShellで実行します。これらのスクリプトには試験先のPython・Windows SDKは不要です。可能ならクリーンなVMスナップショットから開始します。既存の`Folimeld.Dev`登録がある場合は上書きしません。

```powershell
# ハッシュ確認、公開証明書のLocalMachine/TrustedPeopleへの信頼登録、
# 現ユーザーへの導入と結果記録
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Install
# 登録されたアプリIdentityから起動
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Launch
# 導入結果の記録を更新
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Inspect
```

[受入試験表](windows-store-acceptance_ja.md) に沿って実際の結果と画面を記録します。導入だけでGUI・更新・削除・WACKを合格にしません。認定試験を行う場合のSDK・WACK導入は別途必要です。`bundle.json`、`artifact-source.json`、`test-state.json`、`installation-report.json`と手動の試験結果を保存します。共有前に個人文書のパスや内容を除きます。

```powershell
# 同じPC・ユーザーの管理者PowerShellで、この試験の導入と新規に追加した
# 証明書の信頼だけを解除。記録は残します
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_msix_on_vm.ps1 -Action Remove
```

信頼登録後に導入が失敗した場合も後始末できます。失敗時はエラーと状態ファイルを保管し、後始末してから新しいコピーで再試行します。導入から後始末までの間に一式を変更したり状態ファイルを削除したりしないでください。元からある証明書の信頼は保持し、別の版が導入されていた場合は自動削除しません。ユーザーのPDFの明示的な削除や設定・ログの手動消去は行いません。アンインストール後の実際の残留状況は別途記録します。

参考：[Microsoftの署名用証明書の作成と試験先での信頼登録](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing)。
