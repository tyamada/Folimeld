# Tika追加指定表示・IPTC範囲・対応ソース提供集合（未承認）

2026-11-16。Tika固定コミットc29724782854bb5a319f4a1940d0828a58ace3f9を対象とした静的点検。CLI/Pythonによる原本の読取・比較・コピーのみで、AIモデル呼出・生成処理・ビルドはしていません。

## 追加指定表示の点検結果

- 公式OGL3本文、PRONOM aboutのOGLフッター、The National Archivesの出典表示ガイダンスを確認しました。この範囲にPRONOM独自の指定文は見当たらず、提供者名/PRONOM出典＋OGL標準文＋v3リンクを告知案に維持します。ガイダンスの汎用テンプレートを固有の指定文とは扱わず、権利者・年を推定して補いません。
- 現在のPRONOMデータサイト全体のOGL表示は確認しましたが、過去の全レコードに追加表示条件が一切ないことの証明ではありません。新たに具体的な指定が判明した場合は反映します。
- 固定Tika coreのLICENSEに、MIME情報をfile-4.26由来としてIan F. Darwinらへ帰属させる告知を確認。著作権・再配布条件・免責を原文のまま告知案に補いました。OGLやApache親表記だけでこれを代替しません。

## IPTC関連の適用範囲

| 確認対象 | 結果 | 扱い |
|---|---|---|
| 固定TikaのIPTC.java / Photoshop.java | 2010年7月のPhoto Metadata説明文とIPTC著作権を明示。固定Gitツリーのblobとも一致。 | この旧説明文に関連する条件の具体的な出所として記録。新しいIPTC仕様のCC BY4.0へ読み替えない。 |
| Tika core LICENSE / root LICENSE | 2010年Photo Metadataの歴史的条件を含む。 | 原本をreference-onlyに保管。MIMEデータ/アプリ全体へ一括適用しない。 |
| 元XMLのIPTC名を持つMIME10定義 | NewsML/G2/ANPA/NITF等の形式識別情報。Qt版でも10/10保持。 | Photo Metadataの説明文と、名称がIPTCであることだけで同一視しない。 |
| Java内の長い説明文95ブロックと元XML | 正規化した長文全体の一致0件。Qt vendor MIME範囲はXML/加工補助等5ファイルで、Java2クラスを含まない。 | この限定範囲での比較結果。語句検索だけで全権利/来歴の不存在を保証しない。 |

このため、今回のQt MIME補足に2010年Photo Metadata説明文を収録している根拠は得られていません。上流のIPTC謝辞は保守的に保持し、適用範囲の説明を添えました。IPTCの全歴史的条件をFolimeldへ課したり、2025仕様のCC BY条件を2010説明文に遡及適用したりしていません。Javaクラス自体は開発PCの点検証拠で保持し、Qt MIME対応ソース集合には入れていません。

## 整備した告知と提供集合

- [改訂告知案](windows-desktop-licenses/TIKA-PRONOM-NOTICE.draft.txt)：PRONOM/TNA/OGL表示、元NOTICE抜粋、MIME由来BSD告知、IPTCの範囲説明。アプリ画面への反映は未実施。
- [対応ソース補足の手順・範囲](windows-desktop-licenses/tika-source-delivery/README.txt)
- [提供集合台帳](windows-desktop-licenses/tika-source-delivery/SOURCE-SET.draft.json)：19ファイル＋自己参照を避けた台帳。全件サイズ・SHA-256一致を確認。

集合には、固定Tika原XML、Qt6.11.2の加工XML/2補助スクリプト/attribution/REUSE、原文Apache/Qt GPL/LGPL/例外、OGL公式原文HTML、静的差分、改訂告知、MIME情報のBSD原文を含めました。集約LICENSE/NOTICEと旧IPTC条件はreference-onlyへ分離し、そこに列挙されたJava等の全成分がQtに入るという意味にはしていません。

完全なQtソースアーカイブは別の既存入力（qt-everywhere-src-6.11.2.tar.xz、SHA256 6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33）として索引に記載。この19ファイルだけでQt/PySide/Folimeld全体の対応ソースが完成したとは扱いません。公開アーカイブ・タグ・Releaseは作成していません。

## 初回onedirビルド前の残件

1. 改訂したTika/MIME告知と補足集合を、Desktop最終告知・Installed-packages・版別ソース案内に統合し、他依存を含む最終点検を行う。提供先URL/最終版/アプリ対応ソースとの結び付けは未確定。
2. 実wheel固有のQt構成・追加変更と、供給する全Qt/PySideソース/手順の対応を説明する。Tika補足の19ファイルの一致だけでこの審査を完了しない。
3. 新たに具体的な追加指定・第三者権利の不足が判明した場合は告知/範囲へ反映する。限定した調査の未検出を普遍的な免責としない。
4. CRT/Pillow/MuPDF等の別残件も解消し、資料が点検済みになってからのみreviewed-files.jsonを作る。実payload照合は承認後のonedir生成→Inno前の工程へ分ける。

今回、TikaのPhoto Metadata謝辞の出所未特定、MIME固有BSD告知の不足、補足提供集合の未整備は解消しました。資料の最終承認は未完です。

## 再現性として別に残るもの

- 歴史的PRONOMの全レコード/リリース来歴と、未標記ルールの個別由来。
- Qt加工スクリプトの再生成一致。元updateスクリプトは可変upstream/dateを参照するため、そのまま実行して固定再現手順とはしない。原本を変更せず注意事項を付けました。
- QtCoreへ埋め込むデータとの完全一致、上流compiler/SDK/生成環境と全wheelのバイト再生成。これらを確認するためのビルドは実行していません。

必要なソース/パッチ/表示の具体的な欠落を、この再現性の別枠へ移して放置するものではありません。

## 原本と検査

GitHub公式の固定コミットツリーに対し、取得したroot/core LICENSEとJava2件のGit blobを全件照合。coreの個別NOTICEパスは404であり、root NOTICEを使用し、存在しないファイルを補造していません。JSONと文書リンク、提供集合の全ファイルを照合しました。

[点検台帳](windows-desktop-licenses/TIKA-DELIVERY-REVIEW.draft.json)を参照。PREBUILD-DRAFT-NOT-APPROVEDを維持し、reviewed-files.json未作成。uv開発中止を維持。新規課金・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。

公式一次参照：
- https://raw.githubusercontent.com/apache/tika/c29724782854bb5a319f4a1940d0828a58ace3f9/LICENSE.txt
- https://raw.githubusercontent.com/apache/tika/c29724782854bb5a319f4a1940d0828a58ace3f9/tika-core/src/main/java/org/apache/tika/metadata/IPTC.java
- https://pronom.nationalarchives.gov.uk/about
- https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/open-government-licence/copyright-notices-attribution-statements/


## Tikaの最終告知・版別ソース案内への統合（2026-11-16）

現行Tika告知をDesktop最終告知下書きへ統合し、日英の版別ソース案内とソース台帳を整備。19補足ファイル/manifestと全Qt/PySide入力に結び付け、版/最終コミット/URLは未確定。固定4wheel、config59モジュール、許可7+plugin2のPE、glue27件（改行のみ差）を静的点検。Qt DLL固有configure/追加変更とソース対応、他依存、版/署名は残件。未承認/禁止事項を維持。

[詳細](windows-desktop-tika-integration-review_ja.md)。
