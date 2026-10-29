# Storeスクリーンショット撮影計画

[日本語](windows-store-screenshot-plan_ja.md) | [English](windows-store-screenshot-plan.md)

状態：計画のみ。撮影・掲載は未実施です。試験用Dynabookの到着後、通常動作を確認してから日英それぞれの画面を撮影します。設定の言語変更後はアプリを再起動します。初回は5枚ずつを目標にします。

| 順番・ファイル名 | 撮影する状態 | 日本語キャプション | 英語キャプション |
| --- | --- | --- | --- |
| 01-overview.png | 生成した3ページPDFを開き、全体のサムネイルとツールバーを表示 | ページを見ながらPDFを整理 | Organize PDF pages visually |
| 02-page-editing.png | コピーしたPDFで複数選択と回転・並べ替えの結果を表示 | 複数ページを選んで移動・回転 | Move and rotate selected pages |
| 03-image-import.png | 画像フォルダー取り込み画面で順序・ページサイズの選択を表示 | 画像フォルダーからPDFを作成 | Create a PDF from an image folder |
| 04-properties.png | 文書のプロパティの詳細タブを表示 | PDFのレイアウトと綴じ方向を設定 | Adjust PDF layout and binding direction |
| 05-password.png | 閲覧パスワード設定画面。入力値は空欄またはマスク表示 | PDFを開くためのパスワードを設定 | Set a password for opening a PDF |

素材は試験用ZIPの生成データをコピーして使用します。`testdata/`のマンガ、第三者の文書、個人ファイル、購入者情報は掲載素材に使いません。画像取り込みには`fixtures/`を指定し、PNG・JPEG・TIFFを選択します。PDFファイルは画像一覧の対象外です。

## 撮影条件と保存先

- 現在のMicrosoft要件ではDesktopはPNG、1366×768以上、1枚50MB以下です。可能なら1920×1080で実際のアプリ画面を撮影し、拡大補間で寸法を満たしません。画面が足りない場合は別のディスプレイを使います。
- 日本語は `build/store-listing/screenshots/ja-JP/`、英語は `build/store-listing/screenshots/en-US/` へ保存します。確定した画像だけを後日リポジトリや掲載用に追加します。
- 同じ候補パッケージ・ウィンドウサイズ・表示倍率で撮影し、アプリの版、パッケージSHA-256、OSビルド、言語、解像度・倍率、撮影日、素材ハッシュを `capture-record.json` に記録します。
- 実際のUIを使い、追加の宣伝文句・ロゴや未実装の画面を合成しません。通知、アカウント名、個人パス、パスワード、エラーを写しません。
- プロパティやパスワード操作で表示・保存結果が正しいことを確認してから撮影します。応援購入は実Storeで未検証のため撮影対象から外します。
- 最終提出候補で撮り直すか、画面・機能に差分がないことを確認します。開発用試験パッケージの画像だけでStore配信動作を確認済みとしません。

日英キャプションはいずれも200文字以内で用意しています。各言語の掲載画面へ画像・キャプションを個別に登録します。公開前に最新要件を再確認します。[Microsoftの画像要件](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images)
