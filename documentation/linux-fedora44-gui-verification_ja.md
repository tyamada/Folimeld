# Fedora 44のPDF編集GUI検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-Fedora44-Amd64-Test`で、通常の導入済み候補`folimeld-0.3.3-1.fc44.x86_64`を検証した。[最小依存導入試験](linux-fedora44-rpm-verification_ja.md)の後、GUI操作・撮影ツールと日本語フォントを追加した環境である。

実行ファイルのSHA-256は`8347c123b1af32f37b98898c3b6e3e9db778798cf09f708ee671ad194bdc15ae`で、生成時・再導入時と一致した。診断用改変は行っていない。設定・キャッシュ・ログは`/home/folimeld-test/verification/gui-20261112`へ分離した。

## 確認結果

| 操作 | 結果・画面証拠 |
| --- | --- |
| 日本語UI・PDF表示 | 自作3ページPDFを表示。[初期表示](linux-fedora44-gui-verification/01-loaded.png) |
| 回転 | 1ページ目を右回転。保存や別の編集を挟まず表示。[回転直後](linux-fedora44-gui-verification/02-rotated.png) |
| Undo/Redo | 縦向きへ戻し、再び回転表示。[Undo](linux-fedora44-gui-verification/03-undo.png)、[Redo](linux-fedora44-gui-verification/04-redo.png) |
| ページ移動 | 回転済みページを後ろへ移動。[移動後](linux-fedora44-gui-verification/05-moved.png) |
| 白紙挿入・削除 | 同サイズの白紙を直後へ挿入し4ページ、挿入白紙だけを削除し3ページへ復帰。[挿入](linux-fedora44-gui-verification/06-blank-inserted.png)、[削除](linux-fedora44-gui-verification/07-blank-deleted.png) |
| 別名保存・再読込 | 原本と別の`fixtures/fedora-edited.pdf`を保存し、GUIで開き直した。[保存後](linux-fedora44-gui-verification/08-saved.png)、[再読込](linux-fedora44-gui-verification/09-reopened.png) |

PyMuPDFで保存データを照合し、3ページ・元のページ順`[2,1,3]`・回転角度`[0,90,0]`・各ページの文字内容保持を確認した。保存PDFのSHA-256は`7b54eee33d7c281a015dae02e2941dd59c317af66d9ec19605cfcf0d2491bab6`。原本は`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`のまま不変だった。

Windows画面全体の撮影は行わず、Linux側の`xwininfo`で対象IDを確認し、`xdotool`とImageMagickで候補ウィンドウだけを操作・撮影した。ファイル選択の補完が最初のクリックを受け取ったため、ダイアログの消失を再観測して再読込完了を判断した。試験後、所有者と起動引数を照合したGUIだけを終了した。

記録・設定・ログ・9画面のハッシュは[検証JSON](linux-fedora44-gui-verification-2026-11-12.json)に保存した。

## 未確認事項

続いてFedora44のIME、画像フォルダ取込、暗号化PDFの編集・保存・再認証を[追加検証した](linux-fedora44-extended-gui-verification_ja.md)。非ASCIIパスの別名保存とGIOによるPDF関連付けも[後続試験で確認した](linux-fedora44-update-nonascii-verification_ja.md)。通常ファイルマネージャー操作、完全なLinuxデスクトップやARM64は未確認で、Fedora45の結果は流用しない。

GUIツールは`xdotool`、`xwininfo`、`ImageMagick`、フォントは`google-noto-sans-cjk-fonts`を使用した。最初に指定した`xorg-x11-utils`はFedora44に存在せず、依存解決で終了したため、実在する`xwininfo`へ訂正した。既存環境・配布物・版は保持し、公開は行っていない。
