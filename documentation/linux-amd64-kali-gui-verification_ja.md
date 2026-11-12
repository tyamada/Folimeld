# Kali amd64のWSLg GUI検証

実施日: 2026-11-12（日本時間）。新規の`Folimeld-Kali-Amd64-Test`だけを変更した。Kali Rolling 2026.3、一般ユーザー`folimeld-test`、Ubuntu 24.04で生成した内部版0.3.3のDEBを使用した。公開用成果物ではない。

## 方法

Windowsの画面取得APIはWSLgの対象画像を返さなかったため、Kali内のX11ウィンドウを`xwininfo`で識別し、`xdotool`で対象IDへ入力、ImageMagickで対象ウィンドウだけを撮影した。Windowsの他アプリは操作していない。

前回の必須依存のみの導入試験の後、日本語フォント、IBus/Mozc、Linux GUI・MIME検証ツールをこの新規Kaliへ追加した。IBusは独立したD-Busセッションで使用した。以前の最小依存試験と今回のGUI試験の環境を区別する。

## 確認した結果

| 項目 | 結果・証拠 |
| --- | --- |
| 日本語UIとPDF表示 | 合成した3ページのPDFと日本語を表示。[初期画面](linux-amd64-kali-gui-verification/01-loaded.png) |
| 回転・白紙挿入 | 1ページ目を右回転し、白紙を挿入。[4ページの画面](linux-amd64-kali-gui-verification/03-blank-inserted.png) |
| Undo/Redo・白紙削除 | ページ数が4→3→4→3へ変化することを実画面で確認 |
| Mozc入力 | ローマ字`nihongo`→`にほんご`→`日本語`を変換・確定。[変換画面](linux-amd64-kali-gui-verification/04-mozc-conversion.png) |
| 別名保存と再読込 | 日本語名で保存し、GUIから`日本語.pdf`を再読込。[再読込画面](linux-amd64-kali-gui-verification/06-reopened.png) |
| PDFデータ照合 | 保存後は3ページ、回転`[90, 0, 0]`、全ページの抽出文字列を保持。原本SHA-256は不変 |
| 暗号化PDF | 自作AES-256 PDFを試験用閲覧パスワードで開き、日本語を含む3ページを表示。[復号後画面](linux-amd64-kali-gui-verification/07-encrypted-opened.png) |
| 画像からPDF | 日本語名の画像フォルダを選択し、青色PNGから1ページPDFを作成・保存。[取込画面](linux-amd64-kali-gui-verification/08-image-imported.png)。データ検査で埋め込み画像1枚、中央画素RGB`[0, 0, 255]`を確認。元画像は不変 |
| MIME関連付け | `application/pdf`の既定は`folimeld.desktop`。`gio open`から候補を起動し、保存したPDFを表示。[関連付け起動画面](linux-amd64-kali-gui-verification/09-mime-launched.png) |
| 関連テスト | 専用Ubuntuビルド環境でサムネイル・日本語UI・ファイル選択の既存テスト16件と16サブテストが成功（1.59秒） |

詳細、依存版、コマンド結果、ハッシュは[検証JSON](linux-amd64-kali-gui-verification-2026-11-12.json)を参照する。導入・更新・削除試験は[前回のKali記録](linux-amd64-kali-verification-2026-11-12.json)に分けている。

## 制約と残る確認

- WSLgのX11経路での結果であり、完全なLinuxデスクトップ環境やファイルマネージャーでのダブルクリックは未検証。関連付け起動はGIOで確認した。
- 回転直後の空白は、後続調査でQtアイコンの配置位置が更新されない問題と判明し、共通コードを修正した。[修正・検証記録](linux-thumbnail-redraw-verification_ja.md)。修正入りRPMをFedoraで確認後、DEBも再ビルドし、新規Kaliで回転直後・Undo/Redo・保存再読込を確認した。[DEBの追加検証記録](linux-deb-thumbnail-fix-verification_ja.md)。本記録のIME等は修正前候補の結果として保持する。
- ダイアログが確定時に破棄されると、対象IDに送る合成入力のキー解放で`BadWindow`が起きる場合があった。明示的なキー解放と再観測を行った。アプリ固有の障害とは断定しない。
- `.pdf`を省略して保存すると拡張子は自動付与されず、指定名のままPDFを保存した。今回アプリの保存動作は変更していない。
- ページ移動の実画面検証、暗号化PDFの編集後再保存、実際のLinuxデスクトップでの操作は残る。上記の限定した合格結果だけを記録し、全面的な対応済み表記や公開は行わない。

既存Ubuntu/Debian、既存配布物、WindowsのWSL設定は保持した。試験で起動した候補のGUIプロセスは、保存と証拠取得後に識別して終了した。
