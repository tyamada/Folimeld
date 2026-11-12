# AlmaLinux 9.8の暗号化PDF・画像・IME検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-AlmaLinux9-Amd64-Test`で通常候補`folimeld-0.3.3-1.alma9_8.x86_64`を使用した。ELF SHA-256は`e7df5b946593a785d5d2c68ba15caa110903ee86b70b30eea784ba8a56f34914`で[基礎検証](linux-almalinux9-rpm_ja.md)と一致する。[PDF編集GUI試験](linux-almalinux9-gui-verification_ja.md)の後の追加試験で、設定・ログ・保存先を`/home/folimeld-test/verification/extended-gui-20261112`へ分離した。

| 項目 | 結果 |
| --- | --- |
| 暗号化PDF | 自作AES-256 PDFを試験パスワードで開き、1ページ目を右回転して別名保存。再認証してGUI再読込に成功 |
| 暗号化PDFデータ | パスワード必須、誤パスワード拒否、正しいパスワードで認証。3ページ・回転[90,0,0]・各ページの文字保持 |
| 画像取込 | 青い200×300の合成PNG1枚をASCII名コピーから既定設定で取込み、PDF保存 |
| 画像PDFデータ | 1ページ・画像1枚、描画中央RGB[0,0,255] |
| 原本 | 元PDF・暗号化PDF・PNGが保持した合成素材とバイト単位で一致 |
| 日本語IME | 通常候補のQtファイル名欄でnihongo→にほんご→日本語の変換・確定。ファイル選択はキャンセル |
| 整合性 | 導入ELF一致、rpm -Vとdnf checkが成功 |

保存暗号化PDF SHA-256は`0e35f618c17b2796ef947c8cae5f8f529eae10d4d1081056195b33bdc45ea251`、画像PDFは`2c52ebebdf59e4df3f76ebdcda51a54d7747f9ab257a356342140e4090580753`。データ照合には専用UbuntuコピーのPyMuPDFを使用した。

画面証拠: [暗号化PDF読込](linux-almalinux9-extended-gui-verification/01-encrypted-loaded.png)、[編集後保存](linux-almalinux9-extended-gui-verification/02-encrypted-saved.png)、[再認証・再読込](linux-almalinux9-extended-gui-verification/03-encrypted-reopened.png)、[画像取込](linux-almalinux9-extended-gui-verification/04-image-imported.png)、[ひらがな](linux-almalinux9-extended-gui-verification/05-ime-hiragana.png)、[漢字変換](linux-almalinux9-extended-gui-verification/06-ime-kanji.png)、[確定](linux-almalinux9-extended-gui-verification/07-ime-committed.png)。OS・ツール版・ログ・照合結果・画面ハッシュは[検証JSON](linux-almalinux9-extended-gui-verification-2026-11-12.json)に保存した。

## 環境と制約

新規試験環境だけへIBus/Mozcとdbus-daemonを追加した。前のGUIツール段階でEPELを追加済みの環境であり、標準リポジトリだけで通った最小依存試験とは区別する。独立dbus-run-sessionでmozc-jp、QT_IM_MODULE/GTK_IM_MODULE=ibus、XMODIFIERS=@im=ibusを使用し、全角半角キーで日本語モードへ切り替えた。

WSLg X11の候補ウィンドウだけを識別・操作・撮影した。所有者と起動引数を照合したGUIと専用IBusは終了済み。アプリ本体・既存環境・Windows設定は変更していない。

ASCII名PNG1枚・自作AES-256 PDF1例の限定試験であり、日本語画像名、多数画像、他の暗号化・IME条件の合格とは扱わない。非ASCII名保存、専用D-BusでのGIO関連付け、梱包revision更新は[後続試験で確認した](linux-almalinux9-update-nonascii-verification_ja.md)。完全なLinuxデスクトップ、他EL系OS、AlmaLinux10、ARM64は未確認。既存配布物・アプリ版を保持し、公開は行っていない。
