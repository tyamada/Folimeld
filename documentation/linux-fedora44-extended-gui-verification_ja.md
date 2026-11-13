# Fedora 44の暗号化PDF・画像取込・IME追加検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-Fedora44-Amd64-Test`で、通常候補`folimeld-0.3.3-1.fc44.x86_64`を使用した。ELF SHA-256は`8347c123b1af32f37b98898c3b6e3e9db778798cf09f708ee671ad194bdc15ae`。[基礎導入試験](linux-fedora44-rpm-verification_ja.md)と[PDF編集GUI試験](linux-fedora44-gui-verification_ja.md)の後の追加試験である。

設定・キャッシュ・ログ・新規保存先を`/home/folimeld-test/verification/extended-gui-20261112`へ分離し、WSLg X11で候補ウィンドウだけを操作・撮影した。診断用コードは使用していない。

| 項目 | 結果 |
| --- | --- |
| 暗号化PDF | 自作AES-256 PDFを試験パスワードで開き、1ページ目を右回転して別名保存。再び認証してGUI再読込に成功 |
| 暗号化PDFの保存データ | パスワード必須・誤パスワード拒否・正しいパスワードで認証。3ページ、回転[90,0,0]、各ページの文字内容を保持 |
| 画像フォルダ取込 | 青い合成PNG（200×300）1枚を画像サイズに合わせて取り込み、新規PDFへ保存 |
| 画像PDFの保存データ | 1ページ、画像1枚、描画中央RGB[0,0,255] |
| 原本 | 元PDF・暗号化PDF・PNGが保持した合成素材とバイト単位で一致 |
| 日本語IME | Qtファイル名欄でnihongo→にほんご→日本語の変換・確定。ファイル選択はキャンセル |
| 整合性 | 導入ELFは基礎検証時と一致、rpm -Vとdnf checkが成功 |

保存暗号化PDFのSHA-256は`5673816bea49f43009df8e602195386d2639c583ef382ef2980be90c5ddee3af`、画像PDFは`bf2834a78d9746decd7c781618a2bc569f3aa5b7a04f1847e41e89be9ae980a2`。データ照合には専用Ubuntu作業コピーのPyMuPDFを使用した。

画面証拠: [暗号化PDF表示](linux-fedora44-extended-gui-verification/01-encrypted-loaded.png)、[編集後保存](linux-fedora44-extended-gui-verification/02-encrypted-saved.png)、[再認証後の再読込](linux-fedora44-extended-gui-verification/03-encrypted-reopened.png)、[画像取込](linux-fedora44-extended-gui-verification/04-image-imported.png)、[ひらがな](linux-fedora44-extended-gui-verification/05-ime-hiragana.png)、[漢字変換](linux-fedora44-extended-gui-verification/06-ime-kanji.png)、[変換確定](linux-fedora44-extended-gui-verification/07-ime-committed.png)。各ハッシュ・ツール版・ログは[検証JSON](linux-fedora44-extended-gui-verification-2026-11-12.json)に保存した。

## 環境と制約

この新規試験環境だけへIBus/Mozc、dbus-daemon、dbus-toolsを追加した。独立したdbus-run-sessionでmozc-jpを使用し、QT_IM_MODULE/GTK_IM_MODULEをibus、XMODIFIERSを@im=ibusとした。日本語入力モードへの切替は全角半角キーを使用した。所有者と引数を照合した候補GUIと専用IBusは終了済み。

画像選択では最初に親フォルダが選択され「対応する画像がありません」と表示された。通知を閉じ、合成PNGのコピーを新規image-inputフォルダへ置き、絶対パスで選び直して成功した。今回の画像取込試験はASCII名のコピーを使用しており、日本語画像名の取込成功とは扱わない。

WSLg X11の限定試験であり、完全なLinuxデスクトップ、他のIME・画像・暗号化条件、ARM64は未確認。PDF関連付けと非ASCIIパスの別名保存は[後続試験で確認した](linux-fedora44-update-nonascii-verification_ja.md)。追加GUI依存を含むため、最小依存クリーン試験と区別する。既存環境・配布物・版を保持し、公開は行っていない。
