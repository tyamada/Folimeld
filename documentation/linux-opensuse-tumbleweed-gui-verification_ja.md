# Tumbleweed 20261110のPDF編集GUI検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-openSUSE-Tumbleweed-Amd64-Test`で通常候補`folimeld-0.3.3-2.tw20261110.x86_64`を使用した。スナップショット20261110、ELF SHA-256は`d5395dec696d6a001633ec642da8a784ac0220ab02ac1a8973392fdde0a20d43`で、[基礎検証](linux-opensuse-tumbleweed-rpm_ja.md)と一致する。

最小依存検証後の新規環境だけへPython3.14、GUI操作・撮影ツール、日本語フォントを追加した。設定・キャッシュ・ログは`/home/folimeld-test/verification/gui-20261112`へ分離し、診断用コードを混ぜず通常候補を起動した。WSLg X11の対象ウィンドウだけを識別・操作・撮影した。

| 操作 | 結果・画面証拠 |
| --- | --- |
| 日本語表示 | 自作3ページPDFと日本語UIを表示。[初期表示](linux-opensuse-tumbleweed-gui-verification/01-loaded.png) |
| 回転直後 | 選択状態を確認した1ページ目を右回転し、保存・別編集なしに表示。[回転](linux-opensuse-tumbleweed-gui-verification/02-rotated.png) |
| Undo/Redo | 縦向きへ戻し、横向きへ再回転。[Undo](linux-opensuse-tumbleweed-gui-verification/03-undo.png)、[Redo](linux-opensuse-tumbleweed-gui-verification/04-redo.png) |
| ページ移動 | 回転ページを2ページ目へ移動。[移動](linux-opensuse-tumbleweed-gui-verification/05-moved.png) |
| 白紙挿入・削除 | 直後へ同サイズ白紙を挿入して4ページ、挿入白紙を削除して3ページへ復帰。[挿入](linux-opensuse-tumbleweed-gui-verification/06-blank-inserted.png)、[削除](linux-opensuse-tumbleweed-gui-verification/07-blank-deleted.png) |
| 保存・再読込 | 原本と別のfixtures/suse-edited.pdfへ保存しGUIで開き直した。[保存](linux-opensuse-tumbleweed-gui-verification/08-saved.png)、[再読込](linux-opensuse-tumbleweed-gui-verification/09-reopened.png) |

専用TumbleweedビルドPythonのPyMuPDFで照合し、保存PDFは3ページ・元のページ順[2,1,3]・回転[0,90,0]・各ページの文字内容保持を確認した。保存PDF SHA-256は`1787b4b474f16e980d4ff2a8dfa1b8e1dbee09672babccb82046276d61b211ff`。原本は`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。

ファイル選択では補完候補の確定後に再度開くボタンを押し、ダイアログ消失を観測して再読込完了を判断した。証拠取得後、所有者と試験パスの起動引数を照合したGUIだけを終了した。OS・ツール版・画面ハッシュ・ログ・照合結果は[検証JSON](linux-opensuse-tumbleweed-gui-verification-2026-11-12.json)に保存した。

今回のGUI試験は追加依存導入後の環境であり、最小依存検証と区別する。IME、画像取込、暗号化PDFは[後続試験で確認した](linux-opensuse-tumbleweed-extended-gui-verification_ja.md)。非ASCII名保存、GIO関連付け、梱包revision更新も[追加確認した](linux-opensuse-tumbleweed-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、別スナップショット、ARM64は未検証。Leap/Fedoraの結果は流用せず、既存環境・配布物・アプリ版を保持し、公開は行っていない。
