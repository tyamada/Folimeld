# Microsoft Store公開計画

[日本語](windows-store-release-plan_ja.md) | [English](windows-store-release-plan.md)

## 登録方式と現在の状況

2026-10-29（日本時間）、ChromeのPartner Centerで、Folimeldが「EXE または MSI アプリ」として登録済みで、「アプリのセットアップ: 下書き段階」の未公開状態であることを確認した。MSIX用のIdentity情報は取得できていない。

公開方針としてMSIX方式を選択した。同日、「新しい製品」→「MSIX または PWA アプリ」でFolimeldの名前の使用可否を確認したところ、「この名前は使用できません」と表示された。画面で案内されたMicrosoftの問い合わせ先へ、既存登録と名前予約を保持したままEXE/MSIからMSIXへ移行する正式な手順を問い合わせた。

Microsoftから2026-10-29 21:19（日本時間）に、開始済みの提出方式は変更できず、新規製品登録が必要との回答を受けた。名前の解放はサポートで支援できると案内されたが、Folimeld名を保持したまま移管できることや、第三者による予約を防げることは確約されていない。2026-10-30 07:37（日本時間）に、製品名がFolimeldであることと、同じ既存の開発者アカウント内で新規MSIX製品に名前を確保したいことを返信し、具体的な手順を再確認した。現在はこの追加確認への回答待ち。既存登録の改名・削除、名前の解放、新規の製品名予約は行っておらず、実Identityも未取得。

EXE/MSI提出ではサイレント対応のオフラインインストーラー、信頼されたCAにつながるコード署名、提出後に変更しない版別HTTPS URLが必要。既存ユーザーへの更新配信もアプリ側の責任となる。`build_exe.bat` が生成する単体実行ファイルは、このインストーラーではない。

MSIX提出ではStoreによる署名・ホスティング・更新配信を利用できる。MSIX登録に対応する次の値を取得してからStore用設定へ転記する。EXE/MSI側の「アプリケーション ID」を代入しない。

| Partner Centerの項目 | Store設定のキー |
|---|---|
| `Package/Identity/Name` | `identity_name` |
| `Package/Identity/Publisher` | `publisher` |
| `Package/Properties/PublisherDisplayName` | `publisher_display_name` |

## Partner Center確認結果と次の対応

1. 2026-10-29（日本時間）、「アプリとゲーム」→「新しい製品」→「MSIX または PWA アプリ」でFolimeldを入力して「使用可能か確認」を実行し、「この名前は使用できません」と表示された。
2. 同日、OutlookからMicrosoftへ英語の問い合わせメールを送信し、「送信済みアイテム」で送信を確認した。既存登録のMSIXへの形式変更可否、別のMSIX登録が必要な場合の名前予約の移管・関連付け方法、既存登録と名前予約を保持した手続きの支援を問い合わせた。
3. 同日21:19の回答で、提出方式の変更は不可、新規製品登録が必要と確認した。Microsoftは製品名の確認を求め、名前の解放を支援できると案内した。既存製品の改名で旧名を解放・再予約する一般例と、未公開EXE/MSI下書きを削除できない場合の参考手順も案内された。ただし、これを現在の下書きに適用できるかは未確認で、改名・再提出・審査取消・削除は実施していない。
4. 2026-10-30 07:37に、利用者が確認した返信下書きを `reportap@microsoft.com` へ送信し、「送信済みアイテム」で宛先・本文・送信日時を確認した。同じ既存の開発者アカウントを使う旨を明記し、下記3点を質問した。手順を確認・合意するまでは名前を解放しないよう依頼しており、今回の返信は解放の実行依頼ではない。
5. 追加回答で名前確保の実施順・担当・リスクを確認し、利用者と手順を合意してから登録操作を進める。それまでは既存登録・予約名を保持する。新規MSIX登録と名前確保が完了したら「製品の管理」→「製品ID」で上記3項目を取得する。

追加確認した3点：

- 同じ開発者アカウント内の新規MSIX製品へ、名前を第三者に開放せず直接移管・関連付けできるか。
- 解放・再予約が必要なら、新規MSIX製品を作る時点を含む正確な作業順序、Microsoftと開発者の担当、第三者による予約を避ける方法。
- 未公開のEXE/MSI下書きの改名・削除が必要か、必要ならどの段階で行うか。

名前予約を削除すると、その名前を別の開発者が予約できる状態になるため、未公開でも削除による引継ぎを前提にしない。既存登録と名前予約は保持したまま。

問い合わせ記録：

- 送信日：2026-10-29（日本時間）
- 送信元：takumayamada22@outlook.jp（Outlook）
- 宛先：reportapp@microsoft.com
- 件名：Guidance requested: Moving Folimeld from EXE/MSI to MSIX while retaining its reserved name
- 初回問い合わせの状態：回答受領済み。提出方式変更は不可、新規製品登録が必要
- Microsoft回答：2026-10-29 21:19（日本時間）、Microsoft Store Report App Teamから受信
- 追加返信：2026-10-30 07:37（日本時間）、`reportap@microsoft.com` 宛てに送信済み
- 追加返信の件名：Re: Guidance requested: Moving Folimeld from EXE/MSI to MSIX while retaining its reserved name
- 現在の状態：同じ開発者アカウント内での名前確保手順・担当・リスクについて追加回答待ち。名前の解放は未承認・未実施

初回送信先は `reportapp@microsoft.com`、回答元と今回の返信先は `reportap@microsoft.com` で、実際のメールに表示された別々の宛先を記録している。

## 実施順と完了条件

| 順序 | 作業 | 現状・完了条件 |
|---|---|---|
| 1 | 登録方式・名前・Identityの確定 | Microsoft回答で提出方式変更不可・新規製品登録が必要と確認。2026-10-30に同じ開発者アカウント内でのFolimeld名確保手順を追加確認し、回答待ち。既存登録・名前予約は保持、解放は未承認・未実施。実Identityは未取得 |
| 2 | 提出用ビルドと静的検査 | 開発/Storeモード、版番号・設定・生成MSIXの検査を実装。実Identityでの生成は未実施 |
| 3 | プライバシー・サポート・対応ソース | 日英のプライバシーポリシー下書きと履歴・保存用入力・画像変換中間PDFの暗号化を実装。公開者・窓口・公開URL、依存ソース、OS停止時の残留・実MSIXの削除検証は未完了 |
| 4 | Windows 11 x64受入試験 | クリーン環境で導入・PDF関連付け・編集・保存・子プロセス・更新・削除を確認 |
| 5 | WACK・掲載資料・限定配信 | WACK結果、日英の説明と画面、年齢区分、runFullTrustの使用理由を準備し、Store配信版で再検証 |
| 6 | 応援購入・ARM64 | Storeライセンスでの購入・復元・返金・障害とARM64実機を検証。未検証の構成を公開済みと扱わない |
| 7 | 一般公開と保守 | 公開の判断、問い合わせ対応、修正版の更新配信を確認 |

## 名前確保手順の追加回答待ちの間に進める作業

2026-10-29、日英の[Store掲載文下書き](windows-store-listing_ja.md)、[スクリーンショット計画](windows-store-screenshot-plan_ja.md)、[公開情報の確認表](windows-store-publication-decisions_ja.md)、[Dynabook到着後の初回試験手順](windows11-test-day_ja.md)を準備しました。2026-10-30にDynabook B65/DN（Core i5-8250U、Windows 11 Pro 25H2、26200.9818、x64）で初回試験を実施しました。掲載用画像撮影と公開情報の確定は未完了です。

別の試験用PCで[署名済み試験用一式の準備・導入・削除手順](windows-store-test-bundle_ja.md)を使用しました。対象は `Folimeld.Dev` 0.3.3.0 x64、MSIXのSHA-256は `b3025711dbb3bdfdee9728ef6790c801232570949ddc76302a658e34a4a44646` です。試験用PCのチャット「Microsoft Storeテスト環境を設定」の記録を確認し、導入・起動、日本語パスのPDF読込、回転・移動・Undo/Redo、別名保存・再読込、パスワード変更後の再読込、日英切替の保持、ライセンス表示、Explorerから開く、InspectとRemoveの完了を確認しました。パスワード変更と管理者操作の成功には利用者の報告を含みます。削除後の状態ファイルは `removed`、今回追加した証明書の信頼は解除済みです。削除後のアプリ登録の直接照会は実行環境のアクセス制限により未確認です。ビルドPCへの信頼登録・導入は行っていません。

画像取り込みは4ページ生成、並べ替え・除外、A4指定、設定画面でのキャンセルまで確認しました。2026-10-30に開発PCへ成果物を回収し、アプリの操作経路から独立した検査31項目がすべて成功しました。編集後のページ順・回転・描画、目次と内部リンクの移動先・リンク領域、注釈、フォームのフィールド参照と値、添付の内容、メタデータを照合しました。変更後のPDFは新パスワードで開き、旧パスワードを拒否します。画像PDFは全4ページがA4相当（各辺1 pt以内）で、EXIF補正・透過の白背景合成・TIFFの2フレームを元画像と画素比較して一致しました。検査はアプリと同じPyMuPDFエンジンとPillowを使用しており、別エンジンとの互換性の証明ではありません。記録・ハッシュ・描画確認画像は `build/store-acceptance/dynabook-20261030/` に保管しました。受領データの構造は `outputs/outputs/` です。試験用PCの原記録は変更していません。変換処理中のキャンセル、クリーンインストール済みであること、メモリ・ディスク・画面の詳細、WACK・更新・実Store購入・強制停止・最終Store版は引き続き未確認です。

[暗号化のネイティブ依存調査](crypto-dependency-audit_ja.md) でOpenSSL 4.0.3とCargo.lockのRust依存32件のソースを照合し、OpenSSL・Rust依存・CFFI内libffiの告知を収集しました。全体の依存調査とwheelのビルド来歴確認は継続します。

[Windows 11 MSIX受入試験表](windows-store-acceptance_ja.md) に候補の記録と導入・ワーカー・更新・削除・認定の試験を定義しました。実施していない試験は未実施として扱います。

[プライバシーポリシー下書き](privacy-policy_ja.md) と [英語版](privacy-policy.md) を作成済み。これは現在の実装を説明する公開前ドラフトで、まだ公開URLとして使用しない。

- 履歴退避・保存用入力・画像変換中間PDFはAES-256-GCMで暗号化する実装へ変更済み。改ざん・誤った鍵・短い書き込みの拒否、暗号化失敗時の文書保持、ワーカー失敗後の一時入力削除、プロセス急終了後に残った暗号コンテナに平文や鍵ファイルがないことを自動テストで確認する。これはOS停止時の確実な消去や残留ファイルの自動回収を保証する検証ではない。
- 提出候補のMSIXで設定・ログの実際の保存先と、手動削除・アンインストール時の挙動を確認する。保存・画像変換の通常終了やワーカー失敗の既存単体テストだけで、すべての異常終了時の削除を保証しない。
- 正式な公開者、サポート窓口、問い合わせ情報の保存期間・運用、施行日を確定する。移行問い合わせメールの送信元を、そのまま公開窓口として採用しない。
- 公開前に最終パッケージと文書を照合し、未確定項目を解消してからポリシーの公開URLを用意する。プライバシー文書の存在だけでStoreポリシーへの適合を完了扱いにしない。

確認した実装：設定・Store照会は `folimeld/app.py` と `folimeld/store_support.py`、履歴は `folimeld/model.py` と `folimeld/history.py`、保存・画像変換の一時データは `folimeld/pdf_save.py` と `folimeld/image_import_dialog.py`、暗号コンテナは `folimeld/temporary_data.py`、ログは `folimeld/diagnostics.py`。追加した `cryptography`・CFFIおよび内包OpenSSLなどの実バイナリに対応するソース・告知の確認も、公開前の依存ソース作業に含める。

## Store用ビルドの準備

`packaging/msix/store-config.example.json` を `build/store-config.json` へコピーし、先頭3項目に確認済みのMSIX登録情報を記入する。例の空欄は意図的で、そのままではStore用の検証に失敗する。ファイルには認証情報や秘密鍵を入れない。

`package_version` はMSIX用の4要素の版番号で、アプリ表示版 `folimeld/__init__.py` の `__version__` と分けて管理する。Storeモードでは先頭を1以上、末尾を0、各要素を65535以下にする。例の `1.0.0.0` は未提出の設定例。更新では同じIdentity/Publisherの前回MSIXより大きくする。以前のEXE/MSI製品や開発用MSIXを `-PreviousPackage` に指定しない。

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
- [EXE/MSIパッケージ要件](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements)
- [EXE/MSIの更新](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/publish-update-to-your-app-on-store)
- [MSIXパッケージ要件と版番号](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Storeポリシー](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
- [MSIXの名前予約](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)
- [EXE/MSIの予約名管理](https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/msi/manage-app-name-reservations)
