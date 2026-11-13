# AlmaLinux 9 revision3の補足告知画面・操作確認

2026-11-12。専用Testへ導入した[revision3候補](linux-almalinux9-035-notices-r3_ja.md)を、新規日本語プロフィールで起動して確認した。既存プロフィールは使用していない。

## ライセンス画面

実アプリから次の4タブを開き、本文が表示されることを確認した。

- [ICU-73.2](linux-almalinux9-035-notices-r3-license/01-icu.png)
- [MuPDF-source-notices](linux-almalinux9-035-notices-r3-license/02-mupdf.png)
- [Qt-additional-referenced-licenses](linux-almalinux9-035-notices-r3-license/03-qt-additional.png)
- [Qt-source-notices](linux-almalinux9-035-notices-r3-license/04-qt-source.png)

Qt告知は約9MBだが、タブ切替、[末尾へのスクロール](linux-almalinux9-035-notices-r3-license/05-qt-scrolled.png)、画面を閉じて[PDF表示へ戻る操作](linux-almalinux9-035-notices-r3-license/06-returned-pdf.png)が応答した。精密な表示時間・メモリー測定ではなく、この専用環境での操作確認である。

試験対象のELFがrevision3のハッシュと一致し、原本PDFは不変だった。ユーザーと専用環境変数を照合して試験アプリだけを終了した。ログ・6画面のハッシュは[GUI検証JSON](linux-almalinux9-035-notices-r3-license-2026-11-12.json)に保存した。

## 同じrevision3の削除再導入

GUI終了後、専用Testだけでdnf remove／installを実行した。削除時は依存の自動削除を無効にし、4パッケージファイルの消失・再導入後のハッシュ復元を確認した。既存回帰用プロフィールのPDF・設定6ファイルは前後不変。rpm -Vとdnf check、新規プロフィールで再導入後offscreen・xcb各12秒の起動も成功し、試験プロセスを終了した。

[削除再導入JSON](linux-almalinux9-035-notices-r3-lifecycle-2026-11-12.json)にコマンド結果・復元ハッシュ・保持ファイルを保存した。これはGUIツール等を追加済みの専用Testでの試験で、新規最小依存導入・完全なデスクトップ試験とは区別する。

## 公開前の残項目

補足文書の収録・ソース対応だけでなく、実アプリで読めることを確認した。旧候補の証跡で置き換えず、revision3そのものを対象にした。

残る確認は、QtPdf/PDFium等の実ビルド選択と生成告知の対応、完全な内包成分・変更パッチの対応整理、公開版・最終ソースの確定。通常デスクトップ、任意の設定移行、全フォントの使用確認等は今回の範囲外として公開稿に明記する。公開は行っていない。
