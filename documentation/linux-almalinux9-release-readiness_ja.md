# AlmaLinux 9先行公開の準備状況

**最新状態: 2026-11-12 22:10:25 JST、ユーザー許可後に[AlmaLinux9 amd64向け0.3.5試験版を公開](linux-almalinux9-publication-result_ja.md)。添付12件・公開後の認証なし取得を検証済み。以下の未公開・許可待ち記述は準備時点の履歴として保持する。**

2026-11-12。AlmaLinux 9.8 amd64を先行対象とし、検証済み0.3.5候補を変更せず、新規専用ディレクトリに配布準備物を作成した。公開・タグ・コミット・元作業ツリーの版変更は行っていない。

## libXau SRPMの追加署名検証

Alma9のRPMが古い鍵の取り込みを拒否した先行結果は保持した。今回は新規GNUPGHOMEへ保存済み公式Alma8鍵を取り込み、SRPMのOpenPGP署名を独立検証した。システムの信頼鍵・暗号ポリシー・GPG設定は変更していない。

対象は`libXau-1.0.9-3.el8.src.rpm`、SHA-256は`f9e5775417473caa6b5699171eec64253ef90473f36f0efe81d020b52a5de49a`。RPM署名ヘッダーのタグ268（主ヘッダー）と1002（主ヘッダー＋payload）を取り出し、それぞれの対象バイト列に対してGPG検証が終了コード0・VALIDSIGとなった。

主鍵fingerprintは`5E9B8F5617B5066CE92057C3488FCF7C3ABB34F8`、署名副鍵は`E53CF5EF91CEB0AD1812ECB851D6647EC21AD6EA`。[AlmaLinux公式8.3文書](https://wiki.almalinux.org/release-notes/8.3.html)の両fingerprintと一致する。

署名日時は2021-01-14、鍵の期限は2024-01-12で、GPGはGood signatureとともにEXPKEYSIG／KEYEXPIREDを報告した。したがって「保存済み公式鍵と署名バイト列の一致を確認、現在は鍵期限切れ」と記録する。現行の有効鍵による署名、RPMの既定ポリシーでの成功、Pillow wheelのビルド来歴やソース対応の確定とは扱わない。

## 配布準備物

```text
/home/folimeld-build/folimeld-candidates/alma9-release-readiness-20261112/staging/
```

- 検証済みRPM、対応FolimeldソースZIPと対応JSONをコピー。
- 既存の別添149ファイルを全件再ハッシュし、依存資料tarへ収録。tarを読み直して全149ファイルのハッシュを再照合。
- 実際のELF内の`licenses/`全項目から告知tar.gzを作成。
- 追加署名検証JSON、日英公開説明の準備稿、未完了状態JSON、SHA256SUMS.txtを作成。
- 全添付ファイルのチェックサムを再照合。元RPM・ELF・対応ソース・埋め込み目録は変更していない。

既存の埋め込み目録にある「libXau署名未確認」は当時の状態として残す。追加JSONはその項目だけを補足し、依存資料全体を完全と認定するものではない。候補RPMは未署名で、SHA256SUMS.txtも認証署名ではない。

実パス・ファイル名・サイズ・ハッシュ・署名出力は[準備検証JSON](linux-almalinux9-release-readiness-2026-11-12.json)、利用者向け文章は[日本語稿](linux-almalinux9-release-draft_ja.md)と[英語稿](linux-almalinux9-release-draft.md)を参照。

## 公開判断までの残項目

[公開判断用一式](linux-almalinux9-publication-approval_ja.md)を準備済み。試験版の対象コミット・タグ・日英本文と添付12件を固定し、チェックサム一致、公開先に予定タグ等がないことを読み取り確認した。公開操作は元の禁止指示を解除する明示の許可待ちで、まだ実行していない。

専用コピーで[ローカルコミット03b14ec](linux-almalinux9-release-commit_ja.md)を作成し、revision5の686入力と全件一致を確認した。親を前提とする検証済み増分bundleも保存済み。元リポジトリへの反映・タグ・push・公開は行っていない。

[版・専用releaseブランチ・コミット前ツリー案](linux-almalinux9-release-tree_ja.md)を新規完全コピーで具体化した。候補686入力をGit blobまで一致させ、候補外の既存48パスを保持、削除0件。コミット・タグ・公開はまだ作成していない。

最新revision5の[削除再導入・新規最小依存起動](linux-almalinux9-035-integration-r5-lifecycle_ja.md)まで確認済み。これで固定候補の最終導入検査を揃えた。以後は新しい不具合・入力変更がなければ候補を作り直さず、版・統合先・不変コミット/タグ・公開操作の判断へ進む。公開は禁止指示のまま未実施。

最新は[文書統合済みrevision5候補](linux-almalinux9-035-integration-r5_ja.md)。統合案から新規ビルドし、RPM・ELF・686入力の対応ソース・候補内日英稿を同じ入力に揃えた。旧RPMのソース付け替えは行わず、新しい対応JSONとstaging-r5を作成した。

[公開用ソース統合案](linux-almalinux9-final-integration-review_ja.md)を専用コピーで準備した。日英README/CHANGELOG・公開稿を同期し、相対リンクと686入力のレビューZIPを照合。元作業ツリーは未反映で、既存RPMへの誤ったソース再対応付けは行っていない。

[公開前レビュー案](linux-almalinux9-release-review_ja.md)に候補・検査結果・公開前の判断項目を集約した。保存済みwheel8件はPyPI公開SHA-256と一致し、候補内のwheel由来105実体も全件一致。配布物の由来確認と、過去ビルド設定の再構成を分けて記録した。

最新の[revision4候補](linux-almalinux9-035-source-r4_ja.md)へテスト修正を反映済み。対応ZIPそのもので、Gitなし・上書きなしの409テスト成功・9件スキップ・67サブテスト成功を確認した。修正テストのZIP未反映は解消し、残るのは過去ビルド選択の証拠整理と版・最終統合の判断。旧revision3以前の記録は履歴として保持する。

[QtPdf告知・配布ソース確認](linux-almalinux9-qtpdf-source-final-review_ja.md)で、公式文書の9成分群に対するrevision3内告知の存在を確認。ソースZIPの683入力・Gitなし入力選択・RPM事前検査も確認した。配布ソース内の同梱告知に依存して失敗したテスト1件を独立した入力へ修正し、15テスト・9サブテスト成功。修正テストは既存ZIPへ未反映のため、最終ソースへの同期が残る。

revision3で[補足告知4タブの表示と大文書の操作](linux-almalinux9-035-notices-r3-license_ja.md)を確認済み。約9MBのQt文書の表示・スクロールとPDF画面への復帰が成功した。本文の存在だけで表示を合格扱いにせず、実アプリの証跡を追加した。

最新候補は[補足資料入りrevision3](linux-almalinux9-035-notices-r3_ja.md)。ICUソース・Qt/MuPDF告知を反映し、対応ソース683入力・別添162ファイル・不変の210ネイティブ実体を照合した。専用Testで更新・起動・整合性が成功し、新規staging-r3の11添付物も照合済み。以下のrevision1/2時点の記録と区別し、旧準備物は保持する。

[Qt/MuPDF告知参照確認](linux-almalinux9-qt-mupdf-notice-review_ja.md)で、Qt対象6モジュールの広い告知集合2,080文書、MuPDFのフォント等を含む34文書を収集した。未解析Qt attribution5文書を解消し、追加の明示参照3文書も確保。実ビルド選択との対応確認と、ICUを含む次候補への反映は残る。

[Qt同梱ICU 73.2のソース補完](linux-almalinux9-icu-source-review_ja.md)で、別添149ファイルには独立したICUソースがないことを確認した。実ランタイム版と3実体を照合し、公式ソース・チェックサム・告知を新規資料へ取得。公式SHA-512は一致したが、候補・別添目録への反映は未実施。revision2の準備物を最終版とは扱わない。

[Pillow構成要素の追加確認](linux-almalinux9-pillow-component-review_ja.md)で、vendored 3ファイルのSBOMハッシュ一致とraqmの2パッチによる内容再現を確認した。一方、revision1でLibTIFF LZWのBerkeley告知全文が不足していることを検出し、補足告知を追加した新規revision2を準備している。上記stagingはrevision1時点の履歴であり、そのまま公開しない。

新0.3.5 ELF内の210 ELF項目を、先行監査の実体ハッシュへ全件再照合した。内訳はOS RPM由来105、Qt/PySide/Shiboken80、Pillow19、PyMuPDF4、cryptography/cffi2。OS由来105項目は所有RPMのSOURCERPM名に一致する別添SRPMが存在し、ハッシュも一致した。[実体・ソース対応表](linux-almalinux9-release-native-source-map-2026-11-12.json)に項目別で保存した。

これにより旧候補の実体監査を新候補へバイト単位で対応付けた。ただし、wheel実体の一致は上流ソース・パッチの完全性の証明ではない。ブートローダー、Pythonバイトコード、フォント等の非ELFデータはこの210件の集計外で、別の告知・資料確認と合わせて扱う。

| 項目 | 状態と次の確認 |
| --- | --- |
| 候補の主要機能・導入 | 新0.3.5 ELFで確認済み。[導入回帰](linux-almalinux9-035-lifecycle_ja.md)と[GUI回帰](linux-almalinux9-035-regression_ja.md)の範囲を採用 |
| libXau SRPM署名 | 独立GPGで一致を確認。期限切れ鍵の条件を明示。wheel内ELFとの来歴は別項目 |
| 依存ソース・告知 | 資料の収集・ハッシュ照合とアーカイブ化を完了。実際の内包コードごとのソース・パッチ・必要告知の対応確認は継続 |
| wheel入力の可変参照 | Pillowのpillow-depends/main等から過去の取得物を推定しない。SBOM・レシピ・固定コミットの対応を追加確認 |
| 版とリポジトリ | 0.3.5は専用コピー内の案。変更履歴・最終ソース・公開版の確定は未完了 |
| デスクトップ全般 | 全面対応とは表記せず、Alma9.8 WSL2/WSLgの確認範囲を公開稿に明記。全デスクトップ検証を必須の待機条件にはしない |

## revision2の画面確認・資料再作成

補足告知入りrevision2を導入した専用Testで、ライセンス画面の`LibTIFF-LZW`タブとBerkeley告知全文を実際に表示した。[タブ先頭](linux-almalinux9-035-lzw-r2-license/01-notice.png)と[Berkeley本文](linux-almalinux9-035-lzw-r2-license/03-berkeley-bottom.png)、[GUI検証JSON](linux-almalinux9-035-lzw-r2-license-2026-11-12.json)を保存した。Ctrl+Endではスクロールしなかったため、ホイールで末尾を表示した。原本PDFは不変、所有者と専用環境変数を確認した試験アプリだけを終了した。

配布準備物は既存`staging/`を保持し、同じ親の新規`staging-r2/`へ作成した。RPM・ソース・対応JSON・告知・依存資料・追加署名検証・日英稿・準備状態の11ファイルとSHA256SUMS.txtを収録。149依存ファイルをアーカイブから再照合し、標準`sha256sum -c SHA256SUMS.txt`も全11件成功した。告知アーカイブ内の補足文書はrevision2内の文書とハッシュ一致し、依存目録のrevision2表記も確認した。

実パスと全添付物のハッシュは[revision2配布準備JSON](linux-almalinux9-release-r2-staging-2026-11-12.json)を参照。これは旧revision1準備物の公開許可や、新候補の全機能再試験を意味しない。

現時点の準備状態は`publication_ready: false`。次は対象OSを増やさず、Qt/MuPDF等の内包第三者コードと配布資料の対応を確認する。公開先への書き込みはまだ実施しない。
