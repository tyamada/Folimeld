# Qt・Pillow・MuPDF：初回ビルド前資料の追加点検

2026-11-16。資料のみを整備。PREBUILD-DRAFT-NOT-APPROVEDを維持し、reviewed-files.jsonは作成していません。

| 依存 | 今回確認・補完したこと | 初回onedirビルド前に必要な不足 | 再現性の未確認事項 |
|---|---|---|---|
| Qt6.11.2 / PySide6 | 公式期待SHA一致のQt全ソースを再照合。許可候補のqtbase/qtsvgにあるattribution79エントリーと、そのLicenseFile参照43ファイルをすべて解決。元の著作権/ライセンス式/QtPartsを索引化。 | LicenseFile未指定10件は本文内告知/著作権の適用範囲を確認。実wheel固有の追加変更・必要な告知/ソースを結び付け、PySide/Shibokenを含む最終案内を整える。候補モジュール内には工具・テスト・他OS向け成分もあり、79件全てのruntime収録を意味しない。 | wheelの全ビルド入力・追加パッチ・工具環境とバイト再生成一致。公式ソースに存在するだけでwheelへの適用を断定しない。 |
| Pillow12.3.0 | 取得済み13依存の宣言告知16件は全て実在。libjpeg-turbo3.1.4.1・xz5.8.3・harfbuzz14.2.1は今回公式Release assetの独立SHA256と一致。Windows置換17パターンの元ソース/出現数を再照合（適用なし）。 | その他10依存の独立した由来/期待ハッシュの根拠、AOM/dav1d/libyuv等の推移的内包範囲、条件・原文告知・対応ソース/パッチの提供集合を確定。libimagequantは取得404の任意項目で、Windows定義--no-imagequantと実入力非対応の既存根拠を維持し、必要依存の欠落と混同しない。 | 各置換が実wheelへ適用された完全証明、compiler/生成設定、取得不能なWindowsジョブログ、バイト再生成。17は置換パターン数で、17ファイルや17回の単一置換ではない。 |
| PyMuPDF/MuPDF1.28.2 | 18サブモジュール全てに、実ソースファイルとコミット固定を対応。従来索引で抜けたleptonica-license.txtとlibjpegのLEGAL ISSUESを含むREADMEを補完し、18/18に告知25件を対応。COPYING/Make等の原本も保持。 | 有効機能・追加変更と対応ソース提供集合を確定し、18実サブモジュール・生成ラッパー/ヘッダー入力・必要手順・告知を統合。元ソースに部品があることだけでWindows DLLへのリンクを断定しない。 | 実pipcl/packaging/libclang/SWIG実体、全compiler/SDK/環境変数、生成物の再生成一致。pipcl12は候補のみ。 |

QtのLicenseFile未指定10件: emoji-segmenter、libjpeg、md4、md5、sha1、siphash、sqlite、wintab、tlexpected、tika-mimetypes。未指定は直ちにライセンス欠落を意味しません。標準ライセンス原文候補とattributionは保存し、ソース内の著作権/許諾本文や適用条件の確認を残します。親QtをLGPLと記すだけで第三者条件を代替しません。

Pillowで今回独立digestを新しく確認したのは13件中3件です。残る10件やAOM/dav1d/libyuvの過去のローカルSHA/コミット特定を、独立digest一致へ読み替えません。ソースを取得したことと、実バイナリの由来を完全確定したことも区別します。

## 次の順序

1. Qtの10エントリーを本文内告知まで点検し、Pillowの未照合ソース・推移的成分、MuPDFの機能/生成入力の不足を個別に閉じる。
2. 各依存について「保持する原文・変更・ソース・必要な生成/ビルド手順・版別提供先」を統合。対応ソースに必要な不足を再現性調査へ棚上げしない。
3. CRT等の別依存に残る条件提示とあわせ、告知/Installed-packages/ソース台帳を点検し、完了後のみreviewed-files.jsonを作成。
4. 別途承認後のonedir生成で実payloadへ突合し、Inno前のpayload台帳を作成。初回ビルド前に未生成payloadの照合を要求しない。

生のLicenseFile参照や原本ファイルの在庫は最終配布範囲の確定ではありません。独立期待ハッシュがないことだけで配布条件違反とは判断せず、公式Git本文対応等の根拠も個別に評価します。ライセンス条件の最終充足・公開承認は未完です。

[追加点検台帳](windows-desktop-licenses/QT-PILLOW-MUPDF-REVIEW.draft.json)にソース・パッチ前テキスト・告知のパスとハッシュを記録しました。原本は変更せず、コピーと索引のみ追加。uv開発中止を維持。新規課金・モデル呼出・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。

公式参照（一般説明であり、今回の6.11.2ソースの個別証拠を置き換えない）：
- https://doc.qt.io/qt-6/licensing.html （取得時はQt6.12の説明）
- https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright
- 各Pillow取得物の公式Release API/asset URLは点検台帳に保存。


## Qt本文内告知とwheelの追加点検（2026-11-16）

前回のlibjpeg LicenseFiles/ CopyrightFile読落しを訂正。9件の本文内告知＋libjpeg指定原文3件を点検し、合計参照数を43→46（著作権含む）へ補完。emoji定数表4組とQtGui、SQLite完全ソースIDとqsqliteの一致を確認。5ネイティブはx64/Qt6.11.2.0。Tikaの固定上流NOTICEにPRONOM/OGL3.0・IPTC記載があり適用範囲/必要表示はビルド前残件。全機械語・全生成環境/バイト再生成は別の未確認事項。

[詳細](windows-desktop-qt-inline-wheel-review_ja.md)。資料は未承認、点検済み台帳未作成。uv中止/禁止事項を維持。
