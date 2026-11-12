# openSUSE Leap 16.1のPDF編集GUI検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-openSUSE-Leap16.1-Amd64-Test`で、通常候補`folimeld-0.3.3-2.lp161.x86_64`を使用した。導入済みELFのSHA-256は`53fb285ac9efa231e4abf40d82bb69be0b411c04de21890cfd609fd3366cf567`で、[基礎検証](linux-opensuse-leap161-rpm_ja.md)と一致する。

最小依存試験後の新規環境だけへPython、xdotool、xwininfo、ImageMagick、日本語フォント、データ照合転送用tarを追加した。設定・キャッシュ・ログは`/home/folimeld-test/verification/gui-20261112`へ分離した。診断用コードを混ぜず、WSLg X11で対象ウィンドウIDを確認して操作・撮影した。

| 操作 | 結果・証拠 |
| --- | --- |
| 日本語表示 | 自作3ページPDFと日本語UIを表示。[初期表示](linux-opensuse-leap161-gui-verification/01-loaded.png) |
| 回転直後 | 1ページ目を右回転し、保存・別編集を挟まず表示。[確認画面](linux-opensuse-leap161-gui-verification/02-confirmed-rotated.png) |
| Undo/Redo | 縦向きへ戻し、再び横向きへ回転。[Undo](linux-opensuse-leap161-gui-verification/03-confirmed-undo.png)、[Redo](linux-opensuse-leap161-gui-verification/04-redo.png) |
| ページ移動 | 回転したページを2ページ目へ移動。[移動後](linux-opensuse-leap161-gui-verification/05-moved.png) |
| 白紙挿入・削除 | 同サイズ白紙を直後へ挿入し4ページ、挿入白紙を削除して3ページへ復帰。[挿入](linux-opensuse-leap161-gui-verification/06-blank-inserted.png)、[削除](linux-opensuse-leap161-gui-verification/07-blank-deleted.png) |
| 保存・再読込 | 原本と別の`fixtures/suse-edited.pdf`へ保存し、GUIで開き直した。[保存後](linux-opensuse-leap161-gui-verification/08-saved.png)、[再読込](linux-opensuse-leap161-gui-verification/09-reopened.png) |

保存データを専用LeapビルドPythonのPyMuPDFで照合し、3ページ・元のページ順[2,1,3]・回転[0,90,0]・各ページの文字保持を確認した。保存PDFのSHA-256は`bb37633d4d03124f190e34a815f16b99414b6a0235a2acf7a05f11e9133e9e9b`。原本は`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。

最初のクリックはページ選択に至らず、回転・Undoも行われていなかった。選択状態を明示的に確認して再試行し、上記の確認画面を取得した。初期の`02-rotated.png`と`03-undo.png`は合格証拠から除外し、経過記録として保持した。ファイル選択でも補完の確定とダイアログ消失を観測して読込完了を判断した。

データ照合の最初の転送は試験環境のtar不足で失敗したため、tarを追加して再実行した。アプリの保存失敗ではない。証拠取得後、所有者と起動引数を照合した試験GUIだけを終了した。

画面ハッシュ・ツール版・ログ・除外画面・データ照合結果は[検証JSON](linux-opensuse-leap161-gui-verification-2026-11-12.json)に保存した。

IME、画像取込、暗号化PDFの編集・再認証は[後続試験で確認した](linux-opensuse-leap161-extended-gui-verification_ja.md)。GIO関連付け、非ASCII名保存、梱包revision更新も[追加確認した](linux-opensuse-leap161-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、Tumbleweed、ARM64は未検証である。追加依存を含むGUI試験と最小依存試験を区別する。既存環境・配布物・アプリ版は保持し、公開は行っていない。
