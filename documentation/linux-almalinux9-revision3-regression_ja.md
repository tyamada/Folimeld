# AlmaLinux9 revision3の編集・暗号化PDF・画像・IME回帰

実施日: 2026-11-12（日本時間）。[告知入り新候補](linux-almalinux9-notices-candidate_ja.md)の続き。専用Test環境の`folimeld-0.3.3-3.alma9_8.x86_64`、ELF SHA-256`b0915988edbfcea48704cf013f5961b5c496d7b6689a888f019cff9034f46455`を使用した。既存候補・配布物は保持し、公開していない。

設定・合成素材コピー・ログ・出力は`/home/folimeld-test/verification/revision3-regression-20261112`に分離した。GUIツール/EPEL追加後の既存専用Test環境でのWSLg X11試験であり、新規最小環境の導入試験とは区別する。

## 確認結果

| 項目 | GUI確認とデータ照合 |
| --- | --- |
| 回転・Undo/Redo | 右回転直後のサムネイル、Undoで元の向きへ復帰、Redoで回転復帰 |
| 移動・白紙 | 回転ページを後ろへ移動、白紙挿入で4ページ、挿入白紙を削除して3ページ |
| 保存・再読込 | 「保存 結果.pdf」へ別名保存し、一覧からGUIで開き直した。3ページ・元の順[2,1,3]・回転[0,90,0]・各ページの文字保持 |
| 暗号化PDF | 自作AES-256 PDFを開き、1ページ目を回転し別名保存。保存後PDFを再認証してGUI読込。データ照合でパスワード必須・誤パスワード拒否・試験パスワード受理・3ページ・回転[90,0,0]・文字保持 |
| 画像取込 | 青い200×300 PNG1枚を既定設定で取込み、image-created.pdfへ保存。1ページ・画像1枚・描画中央RGB[0,0,255] |
| 日本語IME | 独立D-BusのIBus/Mozcでnihongo→にほんご→日本語の変換・確定。ファイル選択はキャンセル |
| 整合性 | 実行ファイルのハッシュ一致、rpm -Vとdnf check成功 |

PyMuPDFによるデータ照合には専用Build環境の既存仮想環境を使用し、アプリ候補は変更していない。

| 保存出力 | SHA-256 |
| --- | --- |
| 保存 結果.pdf | 2fccb4805ee3b652fc12429c4f1abbfc1a462b3f0a7194e131f6150394ad89ae |
| encrypted-edited.pdf | 4df5eec0e26c335a24dd080a609b4c1510f0764b2f45544340cee5c49798d07c |
| image-created.pdf | 2c60f3840a466c569c790891b0c5bd5a0e54750bed70df244f4558b3ad8e9072 |

## 保存操作と自動入力の記録

別名保存の前に保存ボタンを押したため、今回新規作成した試験用`fixtures/原本_日本語.pdf`コピーへ編集内容を上書きした。このコピーは元のままではなく、ハッシュ`6661b4f08cd45156d42ffdec0c9c418a4bdc7873e873615c141cde22ba035cdb`で保持した。元の合成素材は以前の試験ディレクトリに保持され、SHA-256`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`と一致した。暗号化入力とPNGも元の素材と一致する。新規コピーへの保存を、原本不変の試験結果として扱わない。

パス補完やウィンドウ指定のキー入力では、ファイル選択の確定・パスワード入力が意図どおりにならない場面があった。一覧から対象を選び、実際にダイアログが消えたことを確認して再読込を判定した。画像保存では合成キー入力によりfolimeld-testのsが欠落し、存在しない保存先のエラーが1回出た。短い保存名を画面で確認して保存し直し、データ照合まで成功した。これらの入力失敗をアプリ機能の合格・不合格と混同しない。

## 画面と機械可読記録

有効な画面証拠: [回転](linux-almalinux9-revision3-regression/01-rotated.png)、[Undo](linux-almalinux9-revision3-regression/02-undo.png)、[Redo・移動](linux-almalinux9-revision3-regression/03-redo-moved.png)、[白紙挿入](linux-almalinux9-revision3-regression/04-blank-inserted.png)、[保存PDF再読込](linux-almalinux9-revision3-regression/06-reopen-confirmed.png)、[暗号化PDF保存](linux-almalinux9-revision3-regression/08-encrypted-saved.png)、[再認証・再読込](linux-almalinux9-revision3-regression/09-encrypted-reopened.png)、[画像設定](linux-almalinux9-revision3-regression/10-image-options.png)、[画像取込](linux-almalinux9-revision3-regression/11-image-imported.png)、[画像保存](linux-almalinux9-revision3-regression/12-image-saved.png)、[ひらがな](linux-almalinux9-revision3-regression/13-ime-hiragana.png)、[漢字](linux-almalinux9-revision3-regression/14-ime-kanji.png)、[確定](linux-almalinux9-revision3-regression/15-ime-committed.png)。

05-edited-reopened.pngは読込ダイアログが消える前の主画面、07-encrypted-loaded.pngは最初のパスワード入力が成功する前の主画面である。ファイルは保持するが、再読込・暗号化認証の証拠として使わない。実際の成功画面は06と09。

初期素材のハッシュ、保存データ、IMEエンジン、整合性コマンド、ログ、入力失敗の区別、全15画面のハッシュは[検証JSON](linux-almalinux9-revision3-regression-2026-11-12.json)に保存した。専用IBusへ終了要求を送り、所有者と試験環境を照合したGUIを終了した。

## 残る範囲

後続で、新ELFの[GIO関連付け・削除再導入・再起動](linux-almalinux9-revision3-lifecycle_ja.md)を確認した。以下はGUI回帰実施時点の範囲であり、新規最小導入や通常デスクトップ等は引き続き残る。

この新ELFではGIO関連付けと削除再導入をまだ再試験していない。日本語保存名は試したが、日本語を含む親ディレクトリからの関連付け起動は旧候補の結果と分ける。単一の合成PDF・AES-256 PDF・PNG・Mozc条件であり、幅広い入力や完全なデスクトップの検証ではない。wheelビルド来歴、Alma8 libXau署名、公開版との統合・版決定、アプリ版間移行も残る。
