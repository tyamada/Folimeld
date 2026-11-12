# AlmaLinux 9.8のPDF編集GUI検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-AlmaLinux9-Amd64-Test`で、通常候補`folimeld-0.3.3-1.alma9_8.x86_64`を使用した。ELF SHA-256は`e7df5b946593a785d5d2c68ba15caa110903ee86b70b30eea784ba8a56f34914`で[基礎検証](linux-almalinux9-rpm_ja.md)と一致する。診断用改変は行っていない。

## GUI試験環境

最小依存試験後にGUI操作・撮影ツールを追加した。標準リポジトリにはxdotoolとImageMagickがなかったため、この新規試験環境だけへextras提供のepel-releaseを導入し、EPELの署名検証を維持して取得した。CRBの追加有効化は不要だった。

Python3.12、xorg-x11-utils、日本語フォントも追加した。ImageMagickは6系で、撮影にはmagickではなくimportコマンドを使用した。設定・キャッシュ・ログは`/home/folimeld-test/verification/gui-20261112`へ分離した。EPELを使わずに成功したアプリ本体の最小依存導入と、今回のEPEL追加後のGUI試験を区別する。ビルド側や既存環境のリポジトリは変更していない。

## 確認結果

| 操作 | 結果・画面証拠 |
| --- | --- |
| 日本語表示 | 自作3ページPDFと日本語UIを表示。[初期表示](linux-almalinux9-gui-verification/01-loaded.png) |
| 回転直後 | 選択した1ページ目を右回転し、保存・別編集なしで表示。[回転](linux-almalinux9-gui-verification/02-rotated.png) |
| Undo/Redo | 縦向きへ戻し、横向きへ再回転。[Undo](linux-almalinux9-gui-verification/03-undo.png)、[Redo](linux-almalinux9-gui-verification/04-redo.png) |
| ページ移動 | 回転ページを2ページ目へ移動。[移動](linux-almalinux9-gui-verification/05-moved.png) |
| 白紙挿入・削除 | 直後へ同サイズ白紙を挿入し4ページ、挿入白紙を削除し3ページへ復帰。[挿入](linux-almalinux9-gui-verification/06-blank-inserted.png)、[削除](linux-almalinux9-gui-verification/07-blank-deleted.png) |
| 保存・再読込 | 原本と別のfixtures/alma-edited.pdfへ保存しGUIで開き直した。[保存](linux-almalinux9-gui-verification/08-saved.png)、[再読込](linux-almalinux9-gui-verification/09-reopened.png) |

専用AlmaLinux9ビルドPythonのPyMuPDFで照合し、保存PDFは3ページ・元のページ順[2,1,3]・回転[0,90,0]・各ページの文字保持を確認。保存PDF SHA-256は`a4b59c294f738774a0974003b6fdd50e747d21bb71d78f1c056326cfe6b87cdd`。原本は`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。

WSLg X11で対象IDを識別し、候補ウィンドウだけを操作・撮影した。メニューIDや項目位置は他OSと異なるため再観測した。保存ファイルの再読込は補完確定後のダイアログ消失と表示で判断した。証拠取得後、所有者・試験パスを照合したGUIだけを終了した。

OS・ツール版・有効リポジトリ一覧・ログ・9画面のハッシュとデータ照合結果は[検証JSON](linux-almalinux9-gui-verification-2026-11-12.json)に保存した。

IME、画像取込、暗号化PDFは[後続試験で確認した](linux-almalinux9-extended-gui-verification_ja.md)。非ASCII名保存、専用D-BusでのGIO関連付け、梱包revision更新も[追加確認した](linux-almalinux9-update-nonascii-verification_ja.md)。完全なLinuxデスクトップ、アプリ版間移行は未確認。他EL系OS、AlmaLinux10、ARM64の合格とは扱わない。既存環境・配布物・アプリ版を保持し、公開は行っていない。
