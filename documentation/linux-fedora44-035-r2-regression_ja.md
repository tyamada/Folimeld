# Fedora 44 revision2のPDF回帰確認

2026-11-13、許可済み専用Fedora44 Testの0.3.5 revision2を一般ユーザーの新規プロファイルで確認した。Fedora44版は未公開。旧候補・既存配布物・元の試験素材を保持した。

実行ELFのSHA-256は `c5fea766f7f508255a1c1bfdd68e1e59230d448b564f818d7a4150f0876da7f8`。今回の試験フォルダーは `/home/folimeld-test/verification/version035-r2-regression-20261113`。入力PDF2件とPNG1件を既存素材から新規コピーした。

## 確認結果

- PDFの右回転、Undo・Redo、後ろへの移動、同サイズの空白ページ挿入・削除を実画面で確認した。
- `保存_結果.pdf` へ別名保存し、ファイル選択ダイアログを閉じて再読込した。3ページ、元ページ順2→1→3、回転0/90/0度、各ページの本文が元PDFと一致した。
- 暗号化入力を試験パスワードで開き、先頭ページを90度回転して `encrypted-edited.pdf` へ別名保存した。再読込でパスワードが要求され、再認証・表示できた。ファイル検証でも暗号化、誤パスワード拒否、正パスワード認証、3ページの本文と回転90/0/0度を確認した。
- PNGから `image-created.pdf` を作成・保存した。1ページ・画像1件、描画中央のRGB値0/0/255を確認した。
- 元入力と今回の試験用入力コピーは、PDF・PNGともSHA-256一致で不変。Testへ検証用ライブラリを追加せず、専用Buildの既存PyMuPDFでデータ照合した。
- 完了後、UID・実行ファイル名・専用プロファイル環境変数を照合し、今回のアプリだけを終了した。

ファイル名入力ではQtの補完表示を確定し、ダイアログが閉じた後の表示を再読込の根拠とした。今回の日本語名入力は自動操作によるUnicode入力であり、IME変換試験とは区別する。WSLg X11と合成素材の範囲に限定し、通常デスクトップ・任意PDF・ARM64の合格とはしない。

[機械可読記録](linux-fedora44-035-r2-regression-2026-11-13.json)に実操作ログ・入力ハッシュ・保存PDFの照合結果・画面ハッシュを収録した。[日本語名再読込](linux-fedora44-035-r2-regression/07-reopened.png)、[暗号化PDF再読込](linux-fedora44-035-r2-regression/10-encrypted-reopened.png)、[画像PDF](linux-fedora44-035-r2-regression/13-image-created.png)も参照。

新ELFでのIME・GIO・ライセンス画面、削除再導入・新規最小依存導入、公式wheel実体・Fedora44固有SRPMと署名・最終配布資料の確認は残る。他OSや旧0.3.3の試験結果で代用しない。公開やGitコミットは行っていない。
