# 変更履歴

[日本語](CHANGELOG_ja.md) | [English](CHANGELOG.md)

## 未リリース

- Linux向けRPMビルド（Fedora・Leap16.1・Tumbleweed・AlmaLinux9）、既存パッケージの上書き拒否、非同期サムネイル回転の表示修正、PyInstaller全文・LibTIFF LZW告知をmainへ統合。ソース版を0.3.5へ同期（既存の他OS配布物は変更せず）。
- 公開済みDEB 0.3.5をUbuntu24.04.4で追加検証し、Mozc変換、GIO、暗号化PDFの編集保存・再認証、画像取込保存を確認。Debian/Kaliの追加機能は未再試験。

- OpenBSD 8.0 / amd64向けに本体・専用MuPDF依存の署名付きパッケージ、対応ソース、ビルド工具と日英インストール手順を追加

- WindowsビルドのDLL検索パスをPython・Windows・Gitの必要な場所に限定し、無関係なツール由来のDLL混入を防止。ネイティブバイナリの収集元を検査し、想定外の場所ならビルドを停止
- Windows実行ファイルにPer-Monitor V2のDPI対応マニフェストを追加。後続の実機試験でもWACKのDPI警告が残り、原因を継続調査
- 日英のStore掲載文下書き・スクリーンショット計画・公開情報確認表と、試験用Dynabook到着後の手順・結果記録テンプレートを追加
- 対応ソース・実行ファイルのハッシュを照合した短期署名の開発用MSIX試験一式と、別PCでの導入・記録・範囲を限定した後始末スクリプトを追加
- Windows x64の暗号化依存についてチェックサム照合済みのOpenSSL・Rustソースとネイティブ依存の告知を収集し、再収集ツール・整合性テスト・調査記録を追加
- 画像変換の中間PDFを直接暗号化して書き出し、認証後にメモリから開くよう変更。認証・変換失敗時の編集中文書の保持と一時ファイルの削除を検証
- 履歴退避と保存用の一時入力をAES-256-GCMで暗号化し、鍵をファイルや設定へ保存せず、認証完了後のみPDF処理へ渡すよう変更。改ざん・短い書き込み・異常終了・保存失敗時の復旧を検証し、暗号化メタデータを含む履歴容量計算と依存ライブラリの告知を更新
- Microsoftへの移行問い合わせの回答待ちに進める作業として、実装に基づく日英のプライバシーポリシー下書きと公開前の一時データ・ログ確認項目を追加
- Microsoft Store公開方針をMSIX方式として記録し、開発/Storeビルドの分離、提出版番号とIdentityの事前検証、生成MSIXの静的検査を追加。既存EXE/MSI登録からの移行・名前の扱いと実Identityの取得は確認待ち
- 補助文書・検証記録・README用画像を `docs/` から `documentation/` へ移動し、文書リンクと配布用ソースZIPの収集処理を更新
- ドキュメントのファイル名を英語版は `ベース名.md`、日本語版は `ベース名_ja.md` に統一し、文書間のリンクと翻訳同期ルールを更新
- PDF保存時のストリーム重複検査を省き、大きな画像PDFの保存を高速化。保存中の進捗画面と別プロセスでの書き出しを追加し、失敗時の編集内容・履歴の保持と、書き出し失敗時の既存保存先の保護を検証
- メモリ上限128 MiBを超えるUndo・Redo履歴をローカルの一時ファイルへ最大1 GiB退避し、大きな文書でも履歴を利用可能に変更。文書終了・履歴分岐時に不要な一時履歴を解放
- サムネイル管理を専用クラスへ分離し、スクロール時の表示範囲探索と連続選択ページの移動を効率化
- 配布・CI用の依存バージョン制約、未使用コード検査、モデル・履歴層の型検査、容量制限付きローカルエラーログを追加
- Windowsで画像変換プロセスが結果を返さず終了した場合のパイプ切断も検知し、待ち続ける問題を修正

- ファイルメニューに「終了」を追加。画像フォルダ選択で全種類のファイル名を表示し、Windowsでは設定済みOneDriveフォルダへのショートカットを追加

- 画像フォルダを一覧表示し、名前・作成日時・更新日時の昇順／降順で新規PDFへ一括取り込み。画像の除外、ページサイズ選択、進捗表示とキャンセルに対応

- 性能計測でUndo/Redoの実行有無を記録し、画像PDF3件の各3回の計測と3 OSのCI成功を記録
- 大きなPDFではサムネイルを表示範囲と前後に限定し、画面外の画像を解放してスクロール時に再描画。通常は最大64枚を保持し、64ページ以下の文書は全ページを保持
- 保存後、編集失敗時のロールバック後、プロパティ画面を閉じた際に、差し替えられたPDFとサムネイルを再同期
- 性能計測に全体スクロールと保持サムネイル数を追加し、1,000ページPDFで改善前後を各3回比較
- PDF操作の入力検証と編集エラー表示を強化し、失敗時の履歴・保存状態の保持を検証
- 単一ページの並べ替えを1回の移動に変更し、サムネイルの連続描画を約16msで区切る
- Windows・Linux・macOS向けのテストCI、静的チェック、PDF性能計測ツール、配布前の検証手順を追加
- 保存失敗後も編集内容とUndo・Redo履歴を保持し、再保存できるよう修正。一時ファイル名の衝突と失敗時の残留を防止
- スクロールする見開きレイアウトの表紙設定について、プロパティ画面と保存内容の不整合を修正
- サムネイルを再利用し、表示範囲を優先して少数ずつ描画。回転時は対象ページのみ再描画
- Undo・Redo履歴のPDFデータに合計128 MiBの上限を設定し、古い履歴から削除

## 0.3.5 Linux DEB amd64試験版 - 2026-11-13

- Ubuntu 24.04.4・Debian 13.6・Kali Rolling 2026.3の専用WSL2/WSLgで更新・削除再導入・起動と日本語PDF回転/Undoを確認した[amd64 DEB試験版](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5)を公開。Ubuntuでは追加の編集・保存再読込・最小chroot起動も確認。
- ソース870入力、実ネイティブ214項目、Ubuntu対応ソース61件、署名付きSourcesインデックス53件、公開12添付を照合。IME/GIO/暗号化PDF/画像GUIの未再試験を明記し、既存0.3.4・ARM64・Snapとlatestを保持。

## 0.3.5 openSUSE Tumbleweed 20261110 amd64試験版 - 2026-11-13

- 専用WSL2/WSLgで検証した0.3.5-1.tw20261110のamd64 RPMを[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.5)で公開。主要GUI・日本語名保存/GIO・Mozc入力・暗号化PDF・画像PDF、更新・削除再導入・新規最小installroot起動を確認。
- 864入力を専用ソースコミットへ固定し、実配布206実体、署名検証済み35 SRPMと11添付を照合。最小rootは通常のローリングリポジトリを用いたchrootで、独立した20261110環境のブートではない。他スナップショット・通常デスクトップ・ARM64・公開0.3.4からの移行等は未検証。既存Releaseとlatestを保持。

## 0.3.5 openSUSE Leap 16.1 amd64試験版 - 2026-11-13

- 専用WSL2/WSLgで検証したamd64 RPM（0.3.5-1）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.5)で試験公開。PDF編集・日本語名保存/GIO再読込・暗号化PDF・画像PDF・Mozc日本語入力、更新・削除再導入・新規最小installroot起動を確認。
- 対応ソース858入力を専用コミットへ固定。実配布209ネイティブ実体、署名検証済み36 SRPMと11添付を照合。通常デスクトップ・ARM64・Tumbleweed・公開Ubuntu/Debian 0.3.4からの移行は対象外。合成入力での失敗と再試験・来歴上の制約を明記し、既存配布物とlatestを保持。

## 0.3.5 Fedora 44 amd64試験版 - 2026-11-13

- Fedora 44専用WSL2/WSLgで検証したamd64 RPM（0.3.5-2）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/fedora44-amd64-v0.3.5)で試験公開。PDF編集・日本語名保存再読込・暗号化PDF・画像PDF・日本語入力・GIO、更新・削除再導入・新規最小installroot起動を確認。
- 対応ソース822入力、実配布207ネイティブ実体、署名検証済み37 SRPMと11添付を照合。通常デスクトップ・ARM64・公開Ubuntu/Debian 0.3.4からの移行等は未検証。既存配布物とlatestを保持。

## 0.3.5 Fedora 45 amd64試験版 - 2026-11-13

- Fedora 45のWSL2／WSLgで検証したamd64 RPM（0.3.5-2）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.5)で試験公開（日本時間）。
- PDF編集・日本語名保存と再読込・暗号化PDF・画像PDF・日本語入力・GIO、更新・削除再導入・新規最小依存installrootでのoffscreen起動を確認。通常デスクトップ・Fedora 44・ARM64・公開Ubuntu／Debian 0.3.4からの移行は未検証。
- 対応ソース785入力を専用コミットへ固定し、依存ソース別添・第三者告知・検証記録・制限事項・SHA-256チェックサムを含む11件を添付。RPMとチェックサムは未署名。既存配布物とlatestは保持。

## 0.3.5 AlmaLinux 9 amd64試験版 - 2026-11-12

- AlmaLinux 9.8のWSL2／WSLgで検証したamd64 RPM（0.3.5-5）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.5)で試験公開。
- PDF編集・日本語名での別名保存と再読込・日本語入力、候補間の更新・削除再導入・最小依存起動を確認。通常デスクトップ・ARM64・AlmaLinux 10・公開Ubuntu／Debian 0.3.4からの移行は未検証。
- サムネイル描画修正とPyInstaller・LibTIFF LZW・ICU・Qt/MuPDFの補足告知を反映。対応ソース、依存ソース資料、検証記録、既知の制約とSHA-256チェックサムを添付。既存Ubuntu／Debian 0.3.4や他OSの配布物は保持。

## 0.3.4 - 2026-11-10

- 2026年11月10日、Folimeld 0.3.4のLinux版を公開しました。
- Ubuntu 24.04・Debian 13向けにamd64／ARM64のDEB、Ubuntu 24.04向けにamd64／ARM64のSnapを公開しました。
- 対応ソースとSHA-256チェックサムは[Linux版0.3.4のGitHub Release](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.4)で確認できます。

## 0.3.3_1 FreeBSD ARM64版の試験公開 - 2026-11-10

- FreeBSD 15.1 ARM64（aarch64）向けにFolimeld 0.3.3のパッケージ改訂1を試験公開しました。
- MacBook Air M5上のQEMU（HVF）で、Xorgデスクトップ環境での導入と動作を確認しました。
- パッケージ、対応ソース、導入手順は[FreeBSD ARM64版のGitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-aarch64-v0.3.3_1)で確認できます。

## 1.0.1.0 - 2026-11-09

- 2026年11月9日、Folimeld 1.0.1.0（Windows 11 x64）を日本と米国のMicrosoft Storeで無料公開しました。 [日本のMicrosoft Store](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=ja-JP&gl=JP) · [米国のMicrosoft Store](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=en-US&gl=US)

## 0.3.3 - 2026-09-09

- 配布用debをUbuntu 22.04でビルドし、Ubuntu 22.04以降に対応。X11依存ライブラリの指定も補完
- ライセンス全文と第三者の告知をバージョン情報から専用画面へ移動し、ヘルプメニューに「ライセンス」を追加
- ARM64環境でWindows EXE / MSIX、Linux deb / Snapのビルドを検証
- Linux用スクリプトの改行、Snapの出力先、Debian最小構成でのフォント設定依存を修正
- ビルド時のソース保存と配布物の対応記録を追加し、ソースZIP名の記録を修正

## 0.3.2 - 2026-09-07

- 通常起動時、WinRTなどのパッケージ情報がなくてもバージョン情報を表示できるよう修正
- バージョン情報に著作権、ライセンス全文、第三者の告知、ソースコードへのリンクを追加
- 各OSのビルドにライセンス文書と依存パッケージの告知を同梱

## 0.3.1 - 2026-09-06

- 表紙のチェック状態に応じてページ表示の説明とレイアウト変更案内を即時更新
- 文書のプロパティの詳細に「ページを表示」を追加し、選択中のページレイアウトの説明をリアルタイムに表示
- ページ表示の説明を上端揃えに変更し、表紙選択時の翻訳エラーを修正

## 0.3.0 - 2026-09-04

- プロジェクトのライセンスをGNU Affero General Public License v3.0へ変更
- アプリのバージョンを一元管理し、各配布形式のメタデータへ自動反映
- Folimeldの新しいアプリアイコンと、各OS・Microsoft Store向け画像を追加
- PDFファイルの関連付けをMSIXマニフェストへ移行
- Microsoft Store向けx64 MSIXのビルドに対応
- ARM64 MSIXのビルド手順と、アーキテクチャ誤指定の検出を追加
- READMEをGitHub公開向けに再構成し、開発手順と変更履歴を別文書へ分離

## 0.2.5 - 2026-09-03

- スクロール動作を改善

## 0.2.4 - 2026-08-31

- Ubuntuに対応

## 0.2.3 - 2026-08-31

- PDFバージョンの自動変更に対応

## 0.2.2 - 2026-08-30

- macOS向けビルド手順、アイコン、署名を整備

## 0.2.1 - 2026-08-30

- macOS上でWindows依存処理を安全に無効化

## 0.2.0 - 2026-08-30

- アプリ名をFolimeldへ変更

## 0.1.0 - 2026-08-29

- 最初のリリース
