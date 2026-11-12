# Fedora 45の画像・暗号化PDF・日本語IME検証

実施日: 2026-11-12（日本時間）。許可済みの新規WSL2 `Folimeld-Fedora45-Amd64-Test`で、導入済みの非公開候補`folimeld-0.3.3-4.fc45.x86_64`を確認した。実行ファイルのSHA-256は`88d3979a88ebdefb59cc064c01bb7a1d14ce81a3832407cf488111310a659800`で、[描画修正候補](linux-thumbnail-redraw-verification_ja.md)と一致する。

## 試験方法と結果

WSLgのX11ウィンドウIDを毎回確認し、`xdotool`で対象を操作、ImageMagickで対象ウィンドウだけを撮影した。通常の導入済みバイナリを使用し、アプリの診断用改変は行っていない。設定・キャッシュ・出力は`/home/folimeld-test/verification/extended-gui-20261112`へ分離した。

| 項目 | 結果 |
| --- | --- |
| 暗号化PDFの読込 | 自作のAES-256 PDFへ試験用閲覧パスワードを入力し、3ページを表示 |
| 暗号化PDFの編集・保存 | 1ページ目を右回転し、原本と別の`encrypted-edited.pdf`へ保存 |
| 保存後のGUI再読込 | 再び閲覧パスワードを要求し、認証後に回転済み3ページを表示 |
| 保存データの照合 | パスワード必須、誤パスワード拒否、正しいパスワードで認証、回転[90,0,0]、各ページの文字内容保持 |
| 画像フォルダ取込 | 青い200×300の合成PNG1枚を既定の画像サイズ設定で読み込み、`image-created.pdf`へ保存 |
| 画像PDFの照合 | 1ページ・画像1枚、描画した中央画素のRGB[0,0,255]を確認 |
| 原本 | 元PDF、暗号化PDF、PNGがUbuntuに保持した合成素材とバイト単位で一致 |
| 日本語IME | 通常候補のQtファイル選択ダイアログで`nihongo`→`にほんご`→`日本語`の変換・確定を確認。選択はキャンセル |
| 導入状態 | `rpm -V folimeld`と`dnf check`が成功 |

保存した暗号化PDFのSHA-256は`e8dac2241eff8ddb37492638ad53324aa33d8b2466cb11bc19e300fa8e086a24`、画像PDFは`b51cc2979a027deeb2607a099b13b35400cf65f145ac4566834057b24fde2c46`。照合は専用Ubuntu作業コピーのPyMuPDFで実施した。

画面証拠: [暗号化PDF読込](linux-fedora-extended-gui-verification/01-encrypted-loaded.png)、[編集後保存](linux-fedora-extended-gui-verification/02-encrypted-saved.png)、[再認証・再読込後](linux-fedora-extended-gui-verification/03-encrypted-reopened.png)、[画像取込](linux-fedora-extended-gui-verification/04-image-imported.png)、[ひらがな](linux-fedora-extended-gui-verification/05-ime-hiragana.png)、[漢字変換](linux-fedora-extended-gui-verification/06-ime-kanji.png)、[確定後](linux-fedora-extended-gui-verification/07-ime-committed.png)。詳細なハッシュ・版・ログは[検証JSON](linux-fedora-extended-gui-verification-2026-11-12.json)に保存した。

## IME環境と制約

最小依存の試験後、この新規Fedoraだけへ`ibus`、`ibus-mozc`、`dbus-daemon`、`dbus-tools`を追加した。`dbus-run-session`内でIBusを起動し、`mozc-jp`、`QT_IM_MODULE=ibus`、`GTK_IM_MODULE=ibus`、`XMODIFIERS=@im=ibus`を使用した。OS全体やWindowsの設定は変更していない。

最初の合成キー入力はフォーカス・モードが適切でなく、暗号化PDFの入力をやり直した。入力欄への明示的なフォーカスとマウスでの確定後に成功した。IMEも英数モードから全角半角キーで切り替えて観測した。アプリの不具合と断定しない。試験後は所有者・引数を照合した候補GUIと専用IBusを終了した。

これはFedora 45 x86_64のWSLg X11における限定試験で、完全なLinuxデスクトップ、他の入力方式、複数画像・各種暗号化設定、Fedora 44、ARM64は未検証。追加GUI依存を含む環境であり、最小依存でのクリーン導入・削除再導入を今回繰り返した結果ではない。[以前のRPM導入試験](linux-fedora-rpm_ja.md)と区別する。既存環境・配布物・アプリ版を保持し、公開は行っていない。

## 追加: 非ASCIIパスとPDF関連付け

同日の続行で、専用の`mime-gui-20261112`ディレクトリへ原本をコピーし、`日本語 パス/関連付け 試験.pdf`を使用した。設定も別のXDGディレクトリに分離し、`gio mime application/pdf folimeld.desktop`で、この試験設定にだけ既定アプリを指定した。

最初のセッションバスなしの`gio open`は終了コード0でもGUIが現れなかった。成功として数えず、独立した`dbus-run-session`で再実行したところ、導入済みdesktopエントリの`Exec=folimeld %f`から候補が起動し、日本語・空白入りのフルパスがプロセス引数へ渡り、3ページの表示を確認した。通常セッションへの設定反映やファイルマネージャーのダブルクリック操作は試していない。

原本とコピーのSHA-256はともに`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。証拠取得後、対象パスと所有者を照合したGUIと専用D-Busセッションを終了した。[画面証拠](linux-fedora-extended-gui-verification/08-mime-nonascii-loaded.png)、[関連付け検証JSON](linux-fedora-mime-verification-2026-11-12.json)。この追加結果は先の7画面を収めた検証JSONとは別に保存した。
