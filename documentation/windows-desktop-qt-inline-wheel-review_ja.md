# Qt本文内告知10件と実wheelの静的対応（未承認）

2026-11-16。原本ソース・固定wheelの読取と資料追加のみ。ビルド・DLL読込/実行はしていません。

## 前回分類の訂正

前回の「LicenseFile未指定10件」には、複数形LicenseFilesとCopyrightFileを索引が読み落としたlibjpegが含まれていました。libjpegのLICENSE / ijg-license.txt / COPYRIGHT.txtを補完し、9件の本文内告知＋1件の指定ファイル告知に訂正します。従来の43参照ファイルは単数フィールド分の件数で、補完後は著作権ファイルを含め46件です。前回の完全性の説明をこの範囲で訂正します。

| 対象 | ソース告知の確認 | 実wheelとの対応・限界 |
|---|---|---|
| emoji-segmenter | 生成Cの先頭にGoogle2019/Apache2.0の許諾・免責と元rl名を確認。 | QtGui内で定数表4組（27/85/24/24 bytes）がソースと完全一致。内部データの対応根拠で、全機械語/生成工具の一致ではない。 |
| libjpeg | LicenseFilesのLICENSE/ijg-license.txtとCopyrightFileのCOPYRIGHT.txtを全件取得・ハッシュ化。本文内告知未指定との前回分類を訂正。 | qjpeg.dllに3.2.0文字列が存在し、Qt側attribution版と一致。Pillow側3.1.4.1とは別系統。 |
| md4 | Solar Designer2001のpublic domain/無保証をソース本文で確認。 | QtCoreのQCryptographicHash APIの存在は確認。特定MD4実装の機械語対応は未確定。 |
| md5 | Colin Plumb1993/Ian Jacksonのpublic domain表明をソース本文で確認。 | QtCoreのQCryptographicHash APIの存在は確認。特定MD5実装の機械語対応は未確定。 |
| sha1 | Dominik Reichl/Qt2016の著作権とLicenseRef-SHA1-Public-Domainをソースで確認し、対応するQt原文を追加。 | QtCoreの暗号ハッシュAPIに間接対応。SHA1個別実装/有効設定は未確定。 |
| siphash | Aumasson/Bernstein/Intelの著作権とCC0-1.0をソースで確認。 | QtCoreのQHashというソース側利用経路はattributionに記載。wheelの当該テンプレート/実装の機械語対応は未確定。 |
| sqlite | sqlite3.h/cのcopyright放棄とblessing原文を確認。 | qsqlite.dllの3.53.4に加え、完全なSQLITE_SOURCE_IDがソースと一致。現Desktop方針ではSql/SQLプラグインは除外対象。 |
| wintab | pktdef.h/wintab.hのLCS/Telegraphics1991-1998の許諾本文を確認。対応するQt LicenseRef原文も追加。 | qwindows.dllにWTInfoW/WTOpenWの参照文字列。API利用経路との対応であり、Wintabドライバー自体の同梱/実行を示さない。 |
| tlexpected | qexpected_p.hのSy Brand2017、CC0による権利放棄/無保証とCC0原文への案内を確認。 | QtCore等で使用され得るヘッダーだがインライン化を含み、実wheelの特定機械語対応は未確定。 |
| tika-mimetypes | XML先頭のASF/Apache2.0と上流NOTICE参照を確認。固定コミットのNOTICEと元XMLを取得し、Qt加工版との差分を保存。 | QtCoreにQMimeDatabase APIは存在するが、特定加工XML全体と実wheel埋込データの対応は未確定。 |

## 初回onedirビルド前に必要な不足

- 確認した本文告知、4件の標準/個別LicenseRef原文、libjpegの3原文を最終資料へ統合し、適用範囲を点検する。原文のpublic domain表明をメタデータのCC0表記で置換しない。
- Tikaの固定コミットNOTICEには、mime定義のPRONOM由来/OGL3.0とIPTC記載がある。Qt加工版に該当する範囲と必要な表示・条件を点検する。NOTICE内のJava依存等をすべてQt同梱扱いにするのも避ける。
- Qt加工XMLと元XMLは非同一で、差分と元のprocess_tika_mimetypes.py/updateスクリプトを保持した。必要な変更・生成入力/手順を対応ソースへ含める。スクリプトは実行していない。
- 特定wheelの構成/追加変更とソースの対応説明、最終告知/版別ソース案内は未完。情報不足を単なる再現性調査へ押し出さない。
- 実payloadの収録/禁止Qt除外、CRTロード、通常動作・LGPL置換等はビルド後。入力wheelのqsqliteは現Desktop方針で除外対象だが、生成済みpayloadで確認した意味ではない。

## 再現性として別に残ること

全機械語とソースの対応、上流compiler/SDK/全生成設定、バイト単位再生成は未確認。emoji定数表4組・SQLite完全ソースIDの一致は強い部分的対応根拠だが、変更なしの全体証明ではない。md4/md5/sha1/siphash/tl::expectedやTika加工データについて、API/ソース経路・文字列だけで特定実装の収録を断定しない。マーカー未検出を不在とも扱わない。Qt/PySideの正確な追加パッチは、対応ソース充足に必要な範囲の確認と再現性向け全環境の調査を分ける。

## 証拠と変更

- [本文告知・原文案](windows-desktop-licenses/QT-INLINE-NOTICES.draft.txt)
- [ソース/実wheel対応台帳](windows-desktop-licenses/QT-INLINE-WHEEL-REVIEW.draft.json)
- 固定pyside6-essentials wheelをSHA256再照合し、対象ネイティブ5件の個別ハッシュとPE情報を記録。全5件x64、FileVersion/ProductVersion=6.11.2.0。版情報はバイナリ全体のビルド証明ではない。
- ソース136ファイルを静的証拠として保存。Qt全ソースも固定期待SHAで再照合。親Qtライセンスだけで第三者告知を代替しない。
- 原本は変更なし。reviewed-files.json未作成。PREBUILD-DRAFT-NOT-APPROVEDを維持。
- uv版開発中止を維持。新規課金・モデル要求・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。

公式一次参照：
https://raw.githubusercontent.com/apache/tika/c29724782854bb5a319f4a1940d0828a58ace3f9/NOTICE.txt
Qt6.11.2の固定ソース/attributionは台帳にパス・SHAを記載。可変なWeb版のQt説明を対象ソースの代替にしていません。


## Tika/PRONOM/OGL3.0の追加点検（2026-11-16）

公式OGL原文と固定Tika NOTICEを点検。明示出典は元/Qt XMLの5定義・6マーカーで保持（ルールは一部変換/無効化）。保守的にTika由来MIMEデータ全体を対象とするPRONOM/TNA出典、OGL標準文とv3リンク、非推奨表明、元NOTICE抜粋の告知案を作成。未標記部分の由来全件は未確定。最終告知/ソース集合への統合・追加専用表示/IPTC等の点検はビルド前残件。Qt加工の再生成/埋込データの完全一致等は別の未確認事項。

[詳細](windows-desktop-tika-pronom-review_ja.md)。未承認・禁止事項を維持。
