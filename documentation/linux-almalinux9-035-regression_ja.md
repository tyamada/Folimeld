# AlmaLinux9の0.3.5案 編集・暗号化PDF・画像・IME回帰

実施日: 2026-11-12（日本時間）。[0.3.5案のビルド・更新](linux-almalinux9-035-integration_ja.md)の続き。許可済み専用AlmaLinux9 Test環境の`folimeld-0.3.5-1.alma9_8.x86_64`、ELF SHA-256`2abe33953f482b723bbd9c15a132bd7bad114ae1e998d3ee6105c96bfd096c98`を使用した。元作業ツリーの版は0.3.3のまま、公開物・旧候補を保持した。

新規`/home/folimeld-test/verification/version035-regression-20261112`へ設定・合成素材コピー・ログ・出力を分離した。旧0.3.3 revision3の結果を新ELFの合格として流用せず、実際に操作して確認した。

## 結果

| 項目 | 確認内容 |
| --- | --- |
| 描画・Undo/Redo | 右回転直後のサムネイル、Undoで向き復帰、Redoで回転復帰 |
| ページ編集 | 選択ページを後ろへ移動、白紙挿入で4ページ、挿入白紙を削除して3ページ |
| 日本語名保存 | 「保存 結果.pdf」へ別名保存・GUI再読込。3ページ・元の順[2,1,3]・回転[0,90,0]・ページ文字保持 |
| 暗号化PDF | 自作AES-256 PDFを認証し、1ページ目を回転して別名保存。保存後に再認証・GUI再読込。データ照合でパスワード必須・誤パスワード拒否・試験パスワード受理、3ページ・回転[90,0,0]・文字保持 |
| 画像取込 | 合成青色PNG1枚を既定設定で取込み保存。1ページ・画像1枚・描画中央RGB[0,0,255] |
| 日本語IME | 独立D-Bus内のIBus/Mozcでnihongo→にほんご→日本語の変換・確定。選択ダイアログはキャンセル |
| 整合性 | 新ELFのハッシュ一致、rpm -Vとdnf check成功 |

データ照合には専用Build環境のPyMuPDFを使用した。元の合成素材と今回の元PDFコピーはSHA-256`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変。暗号化入力とPNGも元の素材と一致した。今回は3つの出力を別名保存し、元コピーへの上書きはしていない。

| 出力 | SHA-256 |
| --- | --- |
| 保存 結果.pdf | 4654e184ef48f9d1c955f64b5590bf95f2c6bbd0153d1bfc7b7dceabffa55eb9 |
| encrypted-edited.pdf | 0533528ef63e689631f4144cf193acdcd2297d820912aee557e87f7bbcae8983 |
| image-created.pdf | aa665f5ea0ec838c6c85382bf628ab7b0eaf617e2298044c09abef72164dc19a |

## 画面と操作記録

画面証拠: [回転](linux-almalinux9-035-regression/01-rotated.png)、[Undo](linux-almalinux9-035-regression/02-undo.png)、[Redo](linux-almalinux9-035-regression/03-redo.png)、[白紙挿入](linux-almalinux9-035-regression/04-blank-inserted.png)、[白紙削除](linux-almalinux9-035-regression/05-blank-deleted.png)、[編集PDF再読込](linux-almalinux9-035-regression/06-edited-reopened.png)、[暗号化PDF読込](linux-almalinux9-035-regression/07-encrypted-loaded.png)、[暗号化PDF再読込](linux-almalinux9-035-regression/10-encrypted-reopened.png)、[画像取込](linux-almalinux9-035-regression/13-image-imported.png)、[画像保存](linux-almalinux9-035-regression/14-image-saved.png)、[ひらがな](linux-almalinux9-035-regression/15-ime-hiragana.png)、[漢字](linux-almalinux9-035-regression/16-ime-kanji.png)、[確定](linux-almalinux9-035-regression/17-ime-committed.png)。

別名保存の最初の合成キー入力ではダイアログが開かなかったため、ファイルメニューから選び直した。保存中ダイアログが消えたことと、実際のファイル一覧からの再読込完了を確認して判定した。自動入力の不成立を、ショートカット機能の手動試験の不合格とは扱わない。

UI操作は所有者と専用プロフィールを確認した対象ウィンドウに限定し、各段階のコマンド・終了コードを保存した。保存名の画面、画像設定等も含め全20画面のハッシュを記録。試験後に専用IBusへ終了要求を送り、試験GUIを終了した。

実行ファイル・素材・保存データ・IMEエンジン・整合性コマンド・ログ・操作記録・画面ハッシュは[検証JSON](linux-almalinux9-035-regression-2026-11-12.json)を参照。

## 残る範囲

後続で0.3.5新ELFの[GIO・削除再導入・最小依存確認](linux-almalinux9-035-lifecycle_ja.md)も実施した。以下はGUI回帰時点の範囲であり、通常デスクトップ・他OS・公開版からの移行等は引き続き残る。

既存GUIツール/EPEL入りのTest環境で、単一の合成PDF・AES-256 PDF・PNG・Mozc条件を確認した結果である。新しい0.3.5 ELFでのGIO関連付け・削除再導入・最小依存検証はまだ再実施していない。他ディストリビューションの0.3.5案、公開Ubuntu/Debian0.3.4からの更新、通常デスクトップ、wheelビルド来歴とAlma8 libXau署名の確認も残る。新規コミット・タグ・公開は行っていない。
