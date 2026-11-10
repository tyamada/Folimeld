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

画像取り込みは4ページ生成、並べ替え・除外、A4指定、設定画面でのキャンセルまで確認しました。2026-10-30に開発PCへ成果物を回収し、アプリの操作経路から独立した検査31項目がすべて成功しました。編集後のページ順・回転・描画、目次と内部リンクの移動先・リンク領域、注釈、フォームのフィールド参照と値、添付の内容、メタデータを照合しました。変更後のPDFは新パスワードで開き、旧パスワードを拒否します。画像PDFは全4ページがA4相当（各辺1 pt以内）で、EXIF補正・透過の白背景合成・TIFFの2フレームを元画像と画素比較して一致しました。検査はアプリと同じPyMuPDFエンジンとPillowを使用しており、別エンジンとの互換性の証明ではありません。記録・ハッシュ・描画確認画像は `build/store-acceptance/dynabook-20261030/` に保管しました。受領データの構造は `outputs/outputs/` です。試験用PCの原記録は変更していません。初回回収時点で残った項目の追加試験結果は以下に記載します。クリーンインストール済みであること、DPI修正版のWACK・更新・実Store購入・強制停止・最終Store版は未確認です。

追加で別エンジンの検査を実施し、pypdf 6.10.0による構造解析とPopplerによる全10ページの描画を含む20項目が成功しました。描画を目視確認し、フォームの値、注釈、目次・リンク移動先、添付、ページ順・回転、暗号化も別の解析ライブラリで照合しました。PopplerのSymbol・ArialUnicode表示フォント警告は原本でも発生し、今回の素材には目視での欠落はありませんでした。任意のフォントやすべての閲覧ソフトでの互換性を保証する結果ではありません。証拠は同じ試験フォルダーの `cross-engine-review.json` と `poppler/` に保存しました。

別フォルダーでの再導入後、追加実機試験を完了しました。72枚（約486 MiB）の使い捨て画像の変換31%時点でキャンセルし、元の24ページ文書と基準PDFのハッシュを保持しました。不正画像によるワーカー失敗でも文書を保持し、保存先を使用中にした保存失敗では既存ファイルのハッシュと編集中の文書を保持して別名保存・再読込できました。約162 MiBのディスク退避履歴からUndo/Redoでき、履歴・画像・保存用の一時入力には暗号化形式の識別子がありPDFヘッダーはありませんでした。これはヘッダー観察であり暗号学的検証ではありません。観察した一時保存先では通常終了・キャンセル・失敗後の残留はありませんでした。履歴上限での破棄、ログのローテーション、アプリの強制終了は未検証です。

追加でメモリ約16 GiB、SSD約237 GiB、導入後の空き約176 GiB、画面1366×768を記録しました。設定の保存実体はパッケージの `SystemAppData/Helium/User.dat`、ログは `LocalCache/Local/Folimeld/Folimeld/logs/folimeld.log` でした。ログ561 bytesにはエラー1件があり、既知の試験パスワードと本文文字列はありませんでした。設定値は公開せずキー名の存在まで確認しました。管理者操作後の基準記録で登録アプリ0件、パッケージ保存フォルダーなし、追加証明書の信頼なし、出力PDF保持を確認しました。追加の原記録は試験用PCの `outputs/remaining-tests-20261030/` にあり、開発PCへの再回収は未実施です。確認内容の要約は開発PCの同じ試験フォルダーに `remaining-tests-review.json` として保存しました。

残りは[優先順位と実施条件](windows-store-acceptance_ja.md#残りの試験の優先順位2026-10-30)に従います。WACK 10.0.28000.2957で開発候補0.3.3.0を検査済みです。終了コード0でも合格とはせず、XMLの総合判定は `WARNING`、内訳は22 PASS・任意項目1 FAIL・必須項目1 WARNING、`PARTIAL_RUN=FALSE` と記録しました。任意の「ブロック済み実行可能ファイル」はCreateProcessWと実行ファイル名に似た文字列の参照、必須のDPI検査はバイナリを処理できないこととDPI非対応を指摘しています。元のXMLと表示用HTMLは試験用PCの `outputs/remaining-tests-20261030/wack-0.3.3.0-20261030-204447/` に保管しました。ChatGPTは通常起動を維持し、WACKだけ管理者PowerShellで実行する運用です。0.3.3.0のアプリ登録・試験所有記録は更新試験の基準として保持しています。

DPI宣言の不足を実際のEXEで確認し、`packaging/windows/Folimeld.manifest` とWindows用specへPer-Monitor V2宣言を追加しました。修正版0.3.3.2を再ビルドし、埋め込みマニフェスト（PerMonitorV2、true/pm、asInvoker、長いパス、既存OS宣言とCommon Controls）の6項目、MSIX関連テスト22件、静的検査・ソース対応検査・署名CMS・ZIP整合性を確認しました。試験用ZIPは `build/store-test-bundles/Folimeld-Windows11-x64-wack-dpi-test.zip`、SHA-256は `76d18eff4ba9b9f34d2c27c845bef079432c9edd275abd9c15425b409bf237e5`、MSIXのSHA-256は `a2256a1d1ec1f86d36bef6d515e17333386eca3f6c13daf7bcec001e80864b8a` です。短期試験証明書は以前と異なり、期限は2026-11-06 12:06:48 UTCです。0.3.3.1はDPI修正前のため、以後の試験では使用しません。0.3.3.2の試験用PCへのZIP転送とサイズ・SHA-256の一致を確認し、新しい試験フォルダーへ展開しました。0.3.3.0から0.3.3.2への更新と原本PDF4件・既定のPDFアプリ・旧所有記録の保持を確認しました。ただしQtCoreのDLL読み込みで「指定されたプロシージャが見つかりません」が発生し、GUI設定保持・保存・再読込・高DPI表示・WACK再実行は未確認です。旧版専用のInstall/Remove/WACKスクリプトは流用せず、更新前後の版・所有状態・今回追加した証明書信頼を確認する別の手順を試験用PC側で準備します。

起動不具合を調べると、ビルド環境のPATHからPoppler/libheif由来のICU・OpenSSL・UCRT/API-set DLLが混入していました。QtCoreが必要とするICU関数20件は混入したICUには存在せず、Windows標準ICUには存在します。開発PCの独立ローダー検査でも0.3.3.2のDLL構成でエラー127を再現しました。`tools/windows_build_environment.py` でビルド子プロセスのPATHをPython・Windows・Gitに限定し、specでPython/Windows以外のネイティブDLL収集を拒否するよう変更しました。修正版0.3.3.3のDLL一覧・内容は正常動作済み0.3.3.0と完全一致し、QtCore読込とWindows標準ICU使用を確認しました。関連32テスト、DPI宣言、静的検査、署名・ソース対応・ZIP整合性も確認済みです。実機の起動とWACK成功はまだ確認していません。

次の試験用ZIPは `build/store-test-bundles/Folimeld-Windows11-x64-runtime-0.3.3.3-test.zip`（85,312,153 bytes、SHA-256 `8cac5f76fce06a3aa52da7a264eaec8d480e8230fa3678ef834644cd1d9d10cf`）です。MSIXのSHA-256は `f3297505bde1fe694c43af875614815e19b3ada5c4fbdad16be0cb611b3365c3`、短期試験証明書の期限は2026-11-06 12:45:01 UTCです。試験用PCへの転送・0.3.3.2からの更新・起動・WACKは未実施で、現在の0.3.3.2と元の0.3.3.0の所有記録を保管して別の更新手順を準備します。検証記録は `runtime-comparison.json`、`qt-icu-diagnosis.json`、`native-loader-review.json` に保存しました。

任意の実行ファイル参照について、アプリソース内には外部シェル・列挙された外部プログラムの起動処理は見つかりませんでした。報告と同じ綴りの文字列は元EXEの圧縮アーカイブ内にあり、`cmD` の残る1件はアイコンリソース内でした。これは文字列位置の調査であり、WACKが評価した箇所や実行時の挙動を完全に特定したものではありません。誤検出と断定せず、`blocked-executable-review.json` に記録しました。Microsoftの[Desktop Bridge検査説明](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-desktop-bridge-app-tests)では任意検査は情報扱いですが、指摘を削除せず保持します。

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

## 診断の追跡状況（2026-11-04更新）

この更新を、上記の10月30日付記録の「未実施」状態より優先します。0.3.3.3は試験PCで更新・起動・PDF保存と再読込・Explorerから開く・新規再導入に成功し、原本文書・既定PDFアプリ・旧証拠を保持しました。UPX無効の0.3.3.4単一EXEと0.3.3.5フォルダー形式も通常動作・ワーカー確認に成功しました。両候補のWACKは22 PASS・任意TEST88 FAIL・必須TEST92 WARNINGで同一でした。終了コード0を合格とは扱いません。実EXEのDPI宣言・実行時認識値2と警告が併存しており、値2だけでPer-Monitor V2動作を証明したとは扱いません。150%・200%表示は未試験です。

独立した0.3.3.13 r2のHosted Probe比較では、同じ外部host・導入済み対象パス・DACLを維持しました。一致パッケージのコンテキストでは成功し、対照では実行アクセスとCreateActCtxがアクセス拒否、manifest依存照会がE_FAILでした。同一hashコピーは両方成功し、順逆で傾向が一致しました。アクセスコンテキストに関する仮説を支持しますが、package graphや未取得token claimsも変わり得ます。元WACKのtoken・失敗openを直接追跡した結果ではなく、WACK不具合の確定ではありません。後続のDLL観測・問い合わせ資料作成ではWACKもHosted API比較も追加実行していません。

TEST88の元0.3.3.5 XMLは16ファイルに対応する40メッセージで、API参照10件・短語30件です。必要なmultiprocessing spawnは実同梱コードとソースの対応、ワーカー観測で裏付けています。Qtの起動参照とOpenGLの条件付きグラフ表示経路は静的調査であり、実行証明ではありません。後日の0.3.3.13 r2通常動作で主プロセスを5時点観測し、Qt6Core・Qt6Gui・Qt6Widgets・qwindowsは一覧に存在、opengl32sw・qdirect2dはその瞬間に不掲載でした。元対象16ファイルのhashは後日のペイロード記録と全件一致しますが、OS記録は元WACK環境と異なります。点時刻の不掲載は全期間・workerの状態・外部起動の不存在を証明しません。WACKの一致offsetや完全な判定仕様は不明で、誤検出・Store合格とは断定しません。

今回所有するパッケージ・追加証明書信頼・保存領域は削除し、保護対象のhash/ACL照合を別記録に保持しました。原ログ・診断ZIP・PC固有記録は公開リポジトリ外へ保管します。検出回避のための製品DACL変更・検出語置換・必要なspawn除去は行っていません。Microsoftへの技術窓口確認と別件の予約名移行は追返信への回答待ちで、DPI/TEST88の統合説明は本更新時点で未送信の下書きです。Store配信版・購入・ARM64と他の未完了受入試験は別課題として残します。
