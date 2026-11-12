# Leap 16.1の暗号化PDF・画像取込・日本語IME検証

実施日: 2026-11-12（日本時間）。許可済みの新規`Folimeld-openSUSE-Leap16.1-Amd64-Test`で、通常候補`folimeld-0.3.3-2.lp161.x86_64`を使用した。ELF SHA-256は`53fb285ac9efa231e4abf40d82bb69be0b411c04de21890cfd609fd3366cf567`で、[基礎検証](linux-opensuse-leap161-rpm_ja.md)と一致する。[PDF編集GUI試験](linux-opensuse-leap161-gui-verification_ja.md)の後の追加試験であり、設定・ログ・出力を`/home/folimeld-test/verification/extended-gui-20261112`へ分離した。

| 項目 | 結果 |
| --- | --- |
| 暗号化PDF | 自作AES-256 PDFを試験用パスワードで開き、1ページ目を右回転・別名保存。再認証してGUI再読込に成功 |
| 暗号化PDFのデータ | パスワード必須、誤パスワード拒否、正しいパスワードで認証。3ページ・回転[90,0,0]・各ページの文字保持 |
| 画像取込 | 青い200×300の合成PNG1枚をASCII名の専用コピーから既定設定で取り込み、PDF保存 |
| 画像PDFのデータ | 1ページ・画像1枚、描画中央RGB[0,0,255] |
| 原本 | 元PDF・暗号化PDF・PNGが保持した合成素材とバイト単位で一致 |
| 日本語IME | 通常候補のQtファイル名欄でnihongo→にほんご→日本語の変換・確定。ファイル選択はキャンセル |
| 整合性 | rpm -V、zypper verify --dry-runが成功。導入ELFは基礎検証時と一致 |

保存暗号化PDFのSHA-256は`0d7176b5b5ac4b6feed8c5a481946f3139a3cc77e2384bd381f5dc653be7a1b3`、画像PDFは`bf89b3febf002cfbb00efc7c02d52e3c9458a5fa0d8bebf3b627526ea50322d4`。照合は専用Ubuntu作業コピーのPyMuPDFで実施した。

画面証拠: [暗号化PDF読込](linux-opensuse-leap161-extended-gui-verification/01-encrypted-loaded.png)、[編集後保存](linux-opensuse-leap161-extended-gui-verification/02-encrypted-saved.png)、[再認証・再読込](linux-opensuse-leap161-extended-gui-verification/03-encrypted-reopened.png)、[画像取込](linux-opensuse-leap161-extended-gui-verification/04-image-imported.png)、[ひらがな](linux-opensuse-leap161-extended-gui-verification/05-ime-hiragana.png)、[漢字変換](linux-opensuse-leap161-extended-gui-verification/06-ime-kanji.png)、[確定後](linux-opensuse-leap161-extended-gui-verification/07-ime-committed.png)。ハッシュ・ツール版・ログ・照合結果は[検証JSON](linux-opensuse-leap161-extended-gui-verification-2026-11-12.json)に保存した。

## IME環境と制約

この新規試験環境にだけIBus/Mozcを追加した。最初の独立セッション起動はdbus-run-session不足で失敗し、標準リポジトリで提供元のdbus-1-daemonを確認して追加した。既存dbus-1パッケージだけでは同コマンドを提供しなかった。独立D-Bus内でmozc-jp、QT_IM_MODULE/GTK_IM_MODULE=ibus、XMODIFIERS=@im=ibusを使用し、全角半角キーで日本語モードへ切り替えた。アプリ・Windows・OS全体の設定は変更していない。

撮影はWSLg X11の候補ウィンドウだけを対象とした。所有者と起動引数を照合したGUIと専用IBusは終了済み。最小依存試験後に追加ツールを導入した環境であり、クリーン導入試験と区別する。

画像取込はASCII名の合成コピー1枚だけで、日本語画像名・多数画像・他形式の合格とは扱わない。暗号化条件も自作AES-256の1例。非ASCII名保存、GIO関連付け、梱包revision更新は[後続試験で確認した](linux-opensuse-leap161-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、Tumbleweed、ARM64は未確認。既存環境・配布物・版を保持し、公開は行っていない。
