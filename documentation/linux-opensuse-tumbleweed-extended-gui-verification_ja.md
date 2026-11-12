# Tumbleweed 20261110の暗号化PDF・画像・IME検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-openSUSE-Tumbleweed-Amd64-Test`で通常候補`folimeld-0.3.3-2.tw20261110.x86_64`を使用した。ELF SHA-256は`d5395dec696d6a001633ec642da8a784ac0220ab02ac1a8973392fdde0a20d43`で[基礎検証](linux-opensuse-tumbleweed-rpm_ja.md)と一致する。[PDF編集GUI試験](linux-opensuse-tumbleweed-gui-verification_ja.md)の後の追加試験で、設定・ログ・出力を`/home/folimeld-test/verification/extended-gui-20261112`へ分離した。

| 項目 | 結果 |
| --- | --- |
| 暗号化PDF | 自作AES-256 PDFを試験パスワードで開き、1ページ目を右回転して別名保存。再認証してGUI再読込に成功 |
| 暗号化PDFデータ | パスワード必須、誤パスワード拒否、正しいパスワードで認証。3ページ・回転[90,0,0]・各ページの文字保持 |
| 画像取込 | 青い200×300の合成PNG1枚をASCII名コピーから既定設定で取込み、PDF保存 |
| 画像PDFデータ | 1ページ・画像1枚、描画中央RGB[0,0,255] |
| 原本 | 元PDF・暗号化PDF・PNGが保持した合成素材とバイト単位で一致 |
| 日本語IME | 通常候補のQtファイル名欄でnihongo→にほんご→日本語の変換・確定。選択はキャンセル |
| 整合性 | 導入ELF一致、rpm -Vとzypper verify --dry-run成功 |

保存暗号化PDFのSHA-256は`8d83008ffe4595bb3e13042dbd7fa2b5db7cb28830c04e83a4e19cbe474557f6`、画像PDFは`977ecce838944b066ff0fe1f54a20a80d734bb218b471a63667b9c88ad81739e`。データ照合には専用UbuntuコピーのPyMuPDFを使用した。

画面証拠: [暗号化PDF読込](linux-opensuse-tumbleweed-extended-gui-verification/01-encrypted-loaded.png)、[編集後保存](linux-opensuse-tumbleweed-extended-gui-verification/02-encrypted-saved.png)、[再認証・再読込](linux-opensuse-tumbleweed-extended-gui-verification/03-encrypted-reopened.png)、[画像取込](linux-opensuse-tumbleweed-extended-gui-verification/04-image-imported.png)、[ひらがな](linux-opensuse-tumbleweed-extended-gui-verification/05-ime-hiragana.png)、[漢字変換](linux-opensuse-tumbleweed-extended-gui-verification/06-ime-kanji.png)、[確定](linux-opensuse-tumbleweed-extended-gui-verification/07-ime-committed.png)。OS・ツール版・ログ・照合結果・画面ハッシュは[検証JSON](linux-opensuse-tumbleweed-extended-gui-verification-2026-11-12.json)に保存した。

## 環境と制約

新規試験環境だけへIBus/Mozc、dbus-1-daemonを追加した。独立dbus-run-session内でmozc-jp、QT_IM_MODULE/GTK_IM_MODULE=ibus、XMODIFIERS=@im=ibusを使用し、全角半角キーで日本語モードへ切り替えた。Tumbleweedの導入パッケージはlibdbus-1-3とdbus-1-daemonで、Leapにあったdbus-1というまとめパッケージの有無を前提にしない。

依存導入コマンドは終了コード0だったが、systemdのトリガー処理でユーザーセッション非稼働・Luaスクリプトの警告が表示された。WSLのsystemdユーザーセッション警告も引き続き区別し、Windows/WSLの設定は変更していない。rpm -Vとzypperの依存検証、日本語入力の実動作は上記のとおり確認した。

撮影はWSLg X11の対象候補ウィンドウだけに限定した。所有者と起動引数を確認したGUIと専用IBusは終了済み。最小依存試験後の追加GUI依存環境であり、クリーン導入結果と区別する。

ASCII名PNG1枚・自作AES-256 PDF1例の限定試験であり、日本語画像名、多数画像、他の暗号化・IME条件の合格とは扱わない。非ASCII名保存、GIO関連付け、梱包revision更新は[後続試験で確認した](linux-opensuse-tumbleweed-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、別スナップショット、ARM64は未確認。既存環境・配布物・アプリ版を保持し、公開は行っていない。
