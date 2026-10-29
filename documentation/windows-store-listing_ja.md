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
<!-- /store:features -->

## 提出担当者用メモ（掲載文に含めない）

- 初回提出の「このバージョンの新機能」は空欄にします。GitHub版の履歴をStoreで公開済みの更新として転記しません。
- アプリ価格・公開地域・カテゴリ（候補：仕事効率化）・年齢区分は未確定です。年齢区分は実際の申告内容に従って回答します。
- 応援購入を含める場合、実Storeでの商品取得・購入・復元を確認し、商品説明と表示価格を照合してから、その案内を掲載文に追加します。現時点で価格・購入可否は約束しません。
- 公開者・サポート・ポリシーURLは[確認表](windows-store-publication-decisions_ja.md)で確定します。名称から推測した値や問い合わせメールの送信元を自動採用しません。

### runFullTrustの使用理由案

FolimeldはPySide6/QtとPyMuPDFを使用するWin32デスクトップPDF編集アプリです。利用者が選択したローカルPDF・画像を読み書きし、Qtのデスクトップ画面でページを表示・編集します。PDF保存と画像変換には別のネイティブプロセスを使用します。このデスクトップ実行モデルのためrunFullTrustを宣言します。アプリ自身が管理者権限を要求する機能は実装していません。

これは制限付き機能の申告用下書きで、承認済みではありません。最終マニフェスト・実行動作に照らして確認します。開発用証明書の導入手順をStore利用者向け説明へ含めません。

## 確認元

- [README](../README_ja.md)、`folimeld/app.py`、`folimeld/model.py`、`folimeld/image_import.py`、`packaging/msix/AppxManifest.xml.in`
- [Microsoftの掲載項目](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/add-and-edit-store-listing-info)：説明10,000文字以内、機能は20件以内・各200文字以内、初回提出の新機能欄は空欄
- [Microsoftの機能申告](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations)
