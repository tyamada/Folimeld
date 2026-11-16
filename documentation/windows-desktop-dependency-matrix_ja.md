# Desktop版：依存・告知・対応ソースの対応表（未承認）

2026-11-16。基点コミット584484a0f435d26528874bf1951ad432e89d30bb。
既存証拠の整理であり、新規の上流照会・配布条件の最終判断・入力アーカイブ再照合は行っていません。PREBUILD-DRAFT-NOT-APPROVEDを維持し、reviewed-files.jsonは作成しません。

実入力14件のファイル名・固定SHA-256、原文告知のパス/ハッシュ、ソース参照、パッチの確認範囲は[機械可読の対応表](windows-desktop-licenses/DEPENDENCY-CORRESPONDENCE.draft.json)に個別記録しています。宣言ライセンスは親パッケージのメタデータで、内包成分全体の判定ではありません。ソースURLがあることと、対応ソースの提供準備が完了したことは別です。

| 実入力 | 宣言ライセンス・告知 | 対応ソース・パッチの確認範囲 | 初回onedirビルド前の残件 | 再現性調査（別枠） |
|---|---|---|---|---|
| cffi 2.1.1 | MIT-0。原文パス/ハッシュはJSON参照。 | 公式sdistと原文を保管。親パッケージのMIT-0表記を内包libffi等へ一律適用しない。 | libffi等のネイティブ内包成分の実版・告知・ソース対応を最終点検。 | 上流wheelの全コンパイラ/パッチ入力は未確定。 |
| cryptography 50.0.2 | Apache-2.0 OR BSD-3-Clause。原文パス/ハッシュはJSON参照。 | 公式wheelとsdistを照合。Rust registry32件はSBOM/Cargo.lock/取得crateが一致。OpenSSL4.0.3ソースはSBOM SHA-256一致。 | OpenSSL/Rustの原文告知と非registry部品を含む由来台帳を統合。Python側OpenSSLとは別系統として扱う。 | SBOMは全ビルド操作の完全証明ではない。全工具・生成設定の再現性は未確認。 |
| pillow 12.3.0 | MIT-CMU。原文パス/ハッシュはJSON参照。 | 公式wheel/ソース229件の対応を確認。raqmパッチ反映結果は同梱ソース一致。LibTIFF4区間は文脈一致。AOM/dav1d文字列を静的確認。 | codec/推移的依存のソース・独立期待ハッシュ・原文告知の閉包と、実wheelに適用されたパッチの説明を完成させる。libimagequant非対応は最終payloadでも確認。 | publish証明の独立検証、取得不能ジョブログ、全compiler/生成設定とcodec機械語の完全対応は未確認。 |
| pycparser 3.12 | BSD-3-Clause。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |
| pymupdf 1.28.2 | Dual Licensed - GNU AFFERO GPL 3.0 or Artifex Commercial License。原文パス/ハッシュはJSON参照。 | PyMuPDFタグ/自己記録コミット一致。MuPDFソース本文と公式Git、18サブモジュールを照合。生成物9件の由来/経路を追跡。 | AGPL対応ソース一式（実サブモジュール・変更・ラッパー入力・ビルド手順）と第三者告知を整える。MuPDF tarの独立期待ハッシュ未確認はGit本文照合と区別して記録。 | 実pipcl/packaging/libclang/SWIG工具実体・全環境は未確定。pipcl12は候補で確定値ではない。生成経路追跡は再生成一致ではない。 |
| pyside6 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only。原文パス/ハッシュはJSON参照。 | PySide/Shiboken共通ソースとQt6.11.2全ソースを取得。Qt全ソースは公式期待SHA-256一致。Qt attribution/ライセンス原文を保管。 | 採用wheel・Qt各部品・追加パッチ/構成と対応ソース/第三者告知を結び付ける。不要モジュール除外実装済みだが実収録は生成後に確定。 | Qt/PySide wheelの全ビルド環境・正確な追加パッチとバイト再生成は未確認。 |
| pyside6-addons 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only。原文パス/ハッシュはJSON参照。 | PySide/Shiboken共通ソースとQt6.11.2全ソースを取得。Qt全ソースは公式期待SHA-256一致。Qt attribution/ライセンス原文を保管。 | 採用wheel・Qt各部品・追加パッチ/構成と対応ソース/第三者告知を結び付ける。不要モジュール除外実装済みだが実収録は生成後に確定。 | Qt/PySide wheelの全ビルド環境・正確な追加パッチとバイト再生成は未確認。 |
| pyside6-essentials 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only。原文パス/ハッシュはJSON参照。 | PySide/Shiboken共通ソースとQt6.11.2全ソースを取得。Qt全ソースは公式期待SHA-256一致。Qt attribution/ライセンス原文を保管。 | 採用wheel・Qt各部品・追加パッチ/構成と対応ソース/第三者告知を結び付ける。不要モジュール除外実装済みだが実収録は生成後に確定。 | Qt/PySide wheelの全ビルド環境・正確な追加パッチとバイト再生成は未確認。 |
| shiboken6 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only。原文パス/ハッシュはJSON参照。 | PySide/Shiboken共通ソースとQt6.11.2全ソースを取得。Qt全ソースは公式期待SHA-256一致。Qt attribution/ライセンス原文を保管。 | 採用wheel・Qt各部品・追加パッチ/構成と対応ソース/第三者告知を結び付ける。不要モジュール除外実装済みだが実収録は生成後に確定。 | Qt/PySide wheelの全ビルド環境・正確な追加パッチとバイト再生成は未確認。 |
| typing-extensions 4.16.0 | PSF-2.0。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |
| winrt-runtime 3.2.1 | MIT。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |
| winrt-windows-foundation 3.2.1 | MIT。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |
| winrt-windows-foundation-collections 3.2.1 | MIT。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |
| winrt-windows-services-store 3.2.1 | MIT。原文パス/ハッシュはJSON参照。 | sdist参照とライセンス原文を既存台帳に保管。実入力版・RECORD照合の既存記録あり。 | ソース/告知の実保管先・SHA-256を最終一覧へ統合し、内包物を含む不足の有無を点検。 | 上流wheelの全工具・生成条件とバイト一致は未確認。 |

## Python・内包成分・工具・CRT

| 対象/実入力 | 告知・対応ソース/パッチの既存証拠 | 初回ビルド前の残件 | 再現性/ビルド後の別枠 |
|---|---|---|---|
| Python3.12.16 / PBS20261110 | 固定install_only取得物とfull archiveのネイティブ55件が一致。原文20件、PYTHON.json、CPython/PBSソースとWindowsパッチを保管。 | 内包成分とソース/告知の全対応を統合。CPython/PBS取得物の独立期待ハッシュと既存Git等の代替根拠の充足を点検。 | 過去PBSの全工具/生成条件とバイト再生成は別調査。 |
| Python側OpenSSL3.5.9 | 公式digestとPBS downloads.json一致。Windowsパッチ11件とstatic設定を記録。 | 原文/パッチ/ソースをPython側に結び付ける。cryptography側4.0.3と混同しない。 | 最終収録有無、ロード実体はビルド後。 |
| CRT14.44.35211.0 x64、7ファイル | 正規未改変入力と個別ハッシュ固定。Runtime原文・日英告知案あり。_internal配置/重複除去/検査を実装。 | 適用可能なVS契約/Distributable List、利用者/再配布先への条件提示・同意方法を記録し、告知案を確定。 | 実payloadの7件一致、旧CRT混在なし、主/3ワーカーのロードと互換性は生成後。 |
| PyInstaller6.22.2 / hooks2026.7 | 固定wheelとソース/工具告知を保管。ブートローダーrunw.exeのwheel対応あり。 | ブートローダーを含む適用条件・例外・告知を最終資料に対応付ける。 | 実EXEとの対応と起動性能は生成後。 |
| altgraph0.17.5 / packaging26.3 / pefile2024.8.26 / pywin32-ctypes0.2.3 / setuptools84.0.0 | 7工具wheelの一部としてURL/版/SHA固定、専用環境に導入済み。 | 工具告知/由来を確認。工具だけの成分と配布物に入る成分を分離し、必要なソース/条件を記録。 | build-only入力が全てpayloadに入るとは扱わない。 |
| Inno7.1.1 x64 / Setup.e32 / SetupLdr.e32 | 公式配布物の署名/固定SHA、内部133件固定、エンジン版照会、スタブ選択の公式ソース対応、LICENSE原文あり。 | setupに残るスタブ/内包成分の告知と条件を最終資料へ対応付ける。アプリ/インストーラー/アンインストーラーの署名方針を確定。 | .issigの独立検証と最終setupでの実使用/受入は別。工具x64と起動スタブx86を区別。 |
| Folimeld本体 | AGPL原文、Git mainのソース、Desktop専用spec/iss/入口を保持。 | 数値版・基点コミット・版情報ファイル、アプリ対応ソースと第三者補足資料の版別提供方式を決める。 | 最終EXE/setupとソース/全入力の台帳を生成後に結び付ける。 |

## 初回onedirビルド前に必須の残件

1. 上表の実入力に対する告知・対応ソース・変更/生成手順の不足を確認し、証拠パスとハッシュを統合する。配布条件に関わる不明点と、単なるバイト再現性の不明点を個別に評価する。
2. CRT適用条件と利用者向け提示方法、Qt等の条件と改変利用手順、Inno内包成分の告知を確定する。ハッシュ一致だけで再配布承認にしない。
3. Installed-packages.txt、THIRD-PARTY-NOTICES.txt、DEPENDENCY-SOURCES.jsonと必要な原文/ソース案内を点検し、完了した資料だけをreviewed-files.jsonへ登録する。下書きを名前変更するだけで承認にしない。
4. Desktop数値版・コミット・専用版情報・新規出力先・署名方針を確定する。固定23入力・専用環境・CRT7件・Inno133件は準備済みで、実行時に再照合する。現時点でビルド実行は未承認。

## onedir生成後、Innoコンパイル前に必須

実payload全件の版/ハッシュ・禁止Qt除外・CRT正規化・ライセンス資料同梱を点検する。入力に存在する部品を実収録と決め付けない。対応ソース/告知を実payloadに突合し、実アプリ版も確認したpayload点検台帳を作る。コンパイル入口で版・payload全件・ライセンス台帳・工具/CRT/runtime台帳・issを結び付け、直前再照合を行う。未生成payloadを初回onedirビルド前の必須条件にはしない。

## 別枠で残す再現性調査

pipclの実使用版（12は候補のみ）、packaging/libclang/SWIG実行体、上流Python/SDK/compiler・環境変数・生成コマンド、Qt/Pillow/PyMuPDF等の完全ビルド設定、バイト単位の再生成一致は未確認。公式wheelを収集する現方式へpipclを追加しない。上流ログ未取得だけで配布条件違反としない一方、必要な対応ソース/変更/生成入力の不足が見つかった場合は「再現性だけ」として棚上げしない。

## 受入と制限

実ビルド後のPDF/画像操作・3ワーカー・DPI/IME/GPU・CRT実ロード・LGPL置換・Store併存・起動性能・更新/削除/復旧は未実施。既存151テスト合格は入口/ガード等の実装時記録であり、今回の実機受入ではない。
uv版開発中止を維持。ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は行わない。

根拠：[既存ライセンス点検](windows-desktop-license-review_ja.md)、[Desktop手順](windows-desktop-build_ja.md)、windows-desktop-licenses内のDEPENDENCY-SOURCES / BUILD-PATCH-CORRESPONDENCE / FIXED-INPUTS-AND-SOURCE-REVIEW / WHEEL-SOURCE-CRT-REVIEW / PILLOW-SOURCE-PATCH-REVIEW / GENERATED-ARTIFACTS-REVIEW（すべてdraft）。後続の専用環境・工具・CRT・入口の実装記録で旧時点の未実装項目を更新して判断した。


## 2026-11-16 追加点検：実体・原文告知・ソース/パッチの具体化

- runtime14 wheelと既存告知原文を再ハッシュ照合。ソース18アーカイブ、Rust registry32 crate、OpenSSL2系統も保存済み期待ハッシュへ再照合。期待値は従来の公式照合台帳に基づき、今回新たな独立上流証明を取得した意味ではない。
- 原文告知/ソース先頭コメント141件をsource-notices-followupへ収集し、全件の元アーカイブ・member・SHA-256を記録。先頭コメントだけのものや工具/テスト用成分もあり、全件が最終payloadへ必要な独立ライセンス文だとは扱わない。
- CFFI：Windows x64用libffi同梱10ファイルとsetup経路を特定。win64.objと元win64.asmを保持。x64スナップショットのリリース版・asm/objectを含む告知適用範囲・実wheel由来は未確定。ARM64用ヘッダーの3.4.2をx64に転用しない。
- cryptography：registry32件の原文とソース、非registry7件のsdist内Cargo.tomlを対応。ルートworkspace.packageから版0.50.2とライセンス式を解決し、7件のSBOM版と一致。単なるworkspace継承を版不一致として残さない。これは実wheelの再生成証明ではない。
- OpenSSL：Python/PBSの3.5.9とcryptographyの4.0.3を分離し、ソース・原文ライセンス・ハッシュを対応。
- 既存Pillow/PBSパッチ/ビルド入力14ファイルをハッシュ付きで索引化。保存されていることと実wheelへ適用されたことは区別。

### 初回onedirビルド前に残ること

1. CFFIの同梱スナップショット全体の告知範囲、Qt実wheel/採用部品の変更・原文告知/ソース対応、Pillow codec推移的依存のソース/独立期待ハッシュ/告知の不足を点検する。
2. MuPDFの18実サブモジュール・生成ラッパー入力・必要な変更/手順を対応ソース提供集合へ統合。Python/PBS内包成分と工具/スタブも含む提供索引を完成させる。今回の20ソース照合は全推移的依存の閉包完了ではない。
3. CRTの適用契約/再配布根拠と利用者向け条件提示方法を確定。最終告知とソース案内を点検し、完了後のみreviewed-files.jsonを作成する。
4. Desktop版・基点コミット・版情報/署名方針を決める。実payload全件照合はonedir生成後、Inno前に行う。

### 再現性として別に残す事項

pipcl実使用版、上流全工具・compiler/SDK・生成設定とバイト一致、win64.objの再生成一致、Pillow公開証明の独立検証や取得不能な過去ログ。必要な対応ソース・変更・生成入力の不足そのものはこの別枠へ隠さない。新しい固定値で過去の未知入力を埋めない。

根拠：[追加対応台帳](windows-desktop-licenses/SOURCE-NOTICE-FOLLOWUP.draft.json)。点検済み承認ではなくPREBUILD-DRAFT-NOT-APPROVEDを維持。既存の原本アーカイブは未変更。uv開発中止、新規課金・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。モデル呼出なし。


## Qt・Pillow・MuPDFの追加点検（2026-11-16）

Qt候補attribution79件のLicenseFile43件を解決。未指定10件の本文内告知は残件。Pillow13依存の指定告知16件を確認し、公式Release digest3件を新規照合、Windows置換17パターンの元テキスト/出現数を再点検。MuPDF18サブモジュール全件に告知25件を対応（leptonica/libjpegの索引漏れを補完）。実wheel固有の変更/機能と必要資料の充足は未確定。pipcl実版等の再現性事項と分離して継続。

[詳細](windows-desktop-qt-pillow-mupdf-review_ja.md)。資料は未承認、reviewed-files.json未作成。禁止事項・uv中止を維持。


## Qt本文内告知とwheelの追加点検（2026-11-16）

前回のlibjpeg LicenseFiles/ CopyrightFile読落しを訂正。9件の本文内告知＋libjpeg指定原文3件を点検し、合計参照数を43→46（著作権含む）へ補完。emoji定数表4組とQtGui、SQLite完全ソースIDとqsqliteの一致を確認。5ネイティブはx64/Qt6.11.2.0。Tikaの固定上流NOTICEにPRONOM/OGL3.0・IPTC記載があり適用範囲/必要表示はビルド前残件。全機械語・全生成環境/バイト再生成は別の未確認事項。

[詳細](windows-desktop-qt-inline-wheel-review_ja.md)。資料は未承認、点検済み台帳未作成。uv中止/禁止事項を維持。


## Tika/PRONOM/OGL3.0の追加点検（2026-11-16）

公式OGL原文と固定Tika NOTICEを点検。明示出典は元/Qt XMLの5定義・6マーカーで保持（ルールは一部変換/無効化）。保守的にTika由来MIMEデータ全体を対象とするPRONOM/TNA出典、OGL標準文とv3リンク、非推奨表明、元NOTICE抜粋の告知案を作成。未標記部分の由来全件は未確定。最終告知/ソース集合への統合・追加専用表示/IPTC等の点検はビルド前残件。Qt加工の再生成/埋込データの完全一致等は別の未確認事項。

[詳細](windows-desktop-tika-pronom-review_ja.md)。未承認・禁止事項を維持。


## Tika追加指定表示・IPTC範囲・提供集合（2026-11-16）

IPTC2010 Photo Metadata説明文の明示出所を固定Tika Java2クラスに特定。Qt MIME subsetにJavaはなく、IPTC名のMIME10定義と説明文を同一視しない。長文95ブロックの比較は完全一致0件（権利不存在の保証ではない）。追加でMIME情報のIan F. Darwin由来BSD原文を告知へ補完。PRONOMの調査範囲に専用文未検出のため名前付き出典/OGL標準文・リンクを維持。対応ソース補足19ファイル＋台帳を整備し全件サイズ/SHA一致。全Qt/Folimeldソースの承認や公開ではない。

[詳細と残件](windows-desktop-tika-delivery-review_ja.md)。資料は未承認・禁止事項/uv中止を維持。


## Tikaの最終告知・版別ソース案内への統合（2026-11-16）

現行Tika告知をDesktop最終告知下書きへ統合し、日英の版別ソース案内とソース台帳を整備。19補足ファイル/manifestと全Qt/PySide入力に結び付け、版/最終コミット/URLは未確定。固定4wheel、config59モジュール、許可7+plugin2のPE、glue27件（改行のみ差）を静的点検。Qt DLL固有configure/追加変更とソース対応、他依存、版/署名は残件。未承認/禁止事項を維持。

[詳細](windows-desktop-tika-integration-review_ja.md)。
