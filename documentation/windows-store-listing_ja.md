# Microsoft Store掲載文（日本語下書き）

[日本語](windows-store-listing_ja.md) | [English](windows-store-listing.md)

公開前ドラフト。2026-10-29のREADME・実装に基づきます。試験PCで機能を確認し、実際のStore提出候補と一致させてから転記します。製品名はFolimeldを想定しますが、MSIX登録と名前引継ぎは回答待ちです。初回の対象はWindows 11 x64を想定し、ARM64や他OSの検証済みという説明は含めません。

## 短い説明

<!-- store:short -->
PDFのページを見ながら並べ替え・回転・挿入・削除。画像フォルダーからのPDF作成にも対応。
<!-- /store:short -->

## 説明

<!-- store:description -->
Folimeldは、PDFのページをサムネイルで確認しながら整理できるデスクトップアプリです。資料のページ順を整えたり、向きを修正したり、別のPDFからページを追加したりできます。文書は端末内で処理し、編集のためにPDFや画像を開発者のサーバーへ送信しません。

複数のページを選択して、移動・回転・削除をまとめて操作できます。Undo・Redoで操作を戻したり、やり直したりでき、保存後も履歴を使えます。別のPDFを開くと履歴はリセットされます。

JPEG・PNG・BMP・TIFF・WebPの画像フォルダーから、新しいPDFを作成できます。画像を名前や日時で並べ替え、不要な画像を除外し、画像に合わせたページサイズまたはA4を選べます。複数ページTIFFにも対応します。

文書のプロパティでは、PDFバージョン・ページレイアウト・綴じ方向を変更できます。閲覧パスワードの設定・解除にも対応しています。

ご利用にあたって
画像フォルダーのサブフォルダーとアニメーションWebPは対象外です。保存中の編集・キャンセルはできません。Undo・Redoの履歴には容量の上限があります。大きな文書では編集・保存時のメモリ使用量と待ち時間が増える場合があります。重要なPDFはコピーで動作を確認し、保存後に内容を確認してください。
<!-- /store:description -->

## 主な機能

Partner Centerへは各行の文字列だけを転記し、箇条書き記号は含めません。

<!-- store:features -->
- サムネイルを見ながらPDFページを並べ替え
- 複数ページの移動・回転・削除
- 別のPDFや空白ページの挿入
- 保存後も使えるUndo・Redo
- 画像フォルダーからPDFを作成
- 複数ページTIFF・画像の向き・透過画像に対応
- PDFバージョン・ページレイアウト・綴じ方向の変更
- 閲覧パスワードの設定・解除
- 日本語・英語など8言語の画面表示
- Windows 11 ARM64（Copilot+ PC等）ネイティブ動作
<!-- /store:features -->

## このバージョンの新機能（Submission 3 / 1.0.3.0 / アプリ版 0.3.7）

<!-- store:whats_new_1_0_3_0 -->
- 「ファイル → サンプルPDFを開く…」およびPDF未読込時の案内から、サンプルPDFマンガ（CC BY 4.0）を1冊ずつ取得してすぐ試せる機能を追加しました（言語フィルター・話数順・SHA-256検証・検証済み原本のオフライン再利用に対応）。
- 編集中のPDFを閉じる操作（「ファイル → 閉じる」）と、PDF未読込時の案内画面を追加しました。
- 編集するユーザーのPDFや画像は引き続き端末内のみで処理し、外部サーバーへ送信しません（サンプルPDF取得時のみ、利用者の操作に応じて公開配布元からサンプルを取得します）。
<!-- /store:whats_new_1_0_3_0 -->

## このバージョンの新機能（Submission 2 / 1.0.2.0）

<!-- store:whats_new -->
- Windows 11 ARM64（Surface Pro 11等のCopilot+ PC）へのネイティブ対応を追加しました。
- 大容量PDFの保存処理を大幅に高速化し、進捗ダイアログを追加しました。
- 編集履歴（Undo/Redo）を一時ファイルへ退避可能にし、大容量PDF編集時の安定性を向上しました。
- サムネイル表示を最適化し、1,000ページを超える文書でも高速かつ滑らかにスクロールできるよう改善しました。
- 画像フォルダー（JPEG, PNG, BMP, TIFF, WebP）から新規PDFを一括作成する機能を追加しました。
- 内部セキュリティの強化（編集一時データの暗号化処理を強化）。
<!-- /store:whats_new -->

## 提出担当者用メモ（掲載文に含めない）

- Submission 2の「このバージョンの新機能」には上記の `store:whats_new` を転記します。
- アプリ価格は「無料」、アプリ内購入（アドオン）は無効のまま提供します。
- カテゴリ（仕事効率化）および年齢区分を維持します。
- 公開者・サポート・ポリシーURLは[確認表](windows-store-publication-decisions_ja.md)で確定します。名称から推測した値や問い合わせメールの送信元を自動採用しません。

### runFullTrustの使用理由案

FolimeldはPySide6/QtとPyMuPDFを使用するWin32デスクトップPDF編集アプリです。利用者が選択したローカルPDF・画像を読み書きし、Qtのデスクトップ画面でページを表示・編集します。PDF保存と画像変換には別のネイティブプロセスを使用します。このデスクトップ実行モデルのためrunFullTrustを宣言します。アプリ自身が管理者権限を要求する機能は実装していません。

これは制限付き機能の申告用下書きで、承認済みではありません。最終マニフェスト・実行動作に照らして確認します。開発用証明書の導入手順をStore利用者向け説明へ含めません。

## 確認元

- [README](../README_ja.md)、`folimeld/app.py`、`folimeld/model.py`、`folimeld/image_import.py`、`packaging/msix/AppxManifest.xml.in`
- [Microsoftの掲載項目](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/add-and-edit-store-listing-info)：説明10,000文字以内、機能は20件以内・各200文字以内、初回提出の新機能欄は空欄
- [Microsoftの機能申告](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations)
