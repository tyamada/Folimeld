# Windows Desktop版の依存告知・対応ソース点検（未承認）

2026-11-15。ビルド・公開前の資料であり、配布条件の確認完了を示しません。

## 確認済み

- 固定14依存の実インストール版とRECORDのハッシュを照合。ハッシュ付きファイルに不一致なし。生成ファイル等の未ハッシュ項目は台帳へ別記。
- 依存10件のPyPI sdist、PySide/Shiboken共通ソース、PyInstallerとhooksのソースの計13件を公開SHA256で照合し、アーカイブ読取とライセンス文を収集。
- cryptography50.0.2 sdistのCargo.lockにあるregistry依存32件を公式配布から取得し、lockのチェックサムを全件照合。
- Python公式PBS full archiveを公開SHA256で照合。候補Pythonのネイティブ入力55件がfull archive内のinstall領域と全件ハッシュ一致。20件のライセンス文とPYTHON.jsonを保管。
- CPython3.12.16、PBS20261110のソース、MuPDF1.28.2公式ソースも取得し、ローカルSHA256を記録。これら3件の独立した公式期待ハッシュとの照合と、全パッチ対応は未完。
- Pillow12.3.0のWindowsビルドスクリプトが公式タグとsdistで改行正規化後一致。公式依存版一覧とインラインパッチ定義を保管。
- Desktop専用の告知下書き・由来/ソース台帳・AGPL/GPL/LGPL全文を整備。uvの非同梱方式と区別し、uvを配布物に含めない。

## 初回点検時の残件（下記の第2回結果で一部解消）

1. Qt6.11.2の全ソース本体は未取得（公式掲載・チェックサムまで確認）。Qt wheelのパッチ・内包物の正確な対応と、Virtual Keyboard等の不要/GPL対象モジュールの除外可否を確定する。
2. Pillowのcodec依存の全ソース/パッチを取得・照合する。実lcms表示2.19とタグ入力2.19.1の対応など、表示版だけで一致と断定しない。
3. Pythonの内包ライブラリ/パッチとMicrosoft CRTの実再配布範囲、cryptographyのOpenSSL4.0.3と実wheelのRust依存集合、MuPDF内包物・ビルド条件を確定する。
4. onedir実ペイロードが未生成のため、入力環境のネイティブ471件とPython55件をそのまま収録数とは扱わない。実収録台帳を作成し、各実体に必要な告知・ソースを対応させる。
5. LGPLライブラリの置換/改変利用の受入、Inno Setup固定コンパイラの由来/条件、最終setupとアプリソース・工具・版の対応を確認する。
6. uv版は開発中止。Desktopビルド補助が参照するuv名の固定入力は、ビルド前にDesktop専用へ分離する。今回アプリ/ビルドコードは変更していない。

reviewed-files.jsonは作成しません。未完了の資料を「点検済み」としてビルドガードへ通さないため、ファイル名も*.draftとしています。
既存Store用・uv用資料、公開済み成果物は変更していません。取得物は開発PCの専用outputsに保持し、まだ公開していません。

## 提供方法の案

将来のReleaseでアプリ対応ソース、ビルド/インストーラー設定、版/全入力/ペイロード対応台帳、告知、必要な第三者ソース補足アーカイブとSHA256を同時提供します。
単なる上流リンクや親パッケージのライセンス表示だけで全内包物の条件を満たしたと扱いません。ビルドパッチや改変依存の利用手順も対応物に含めます。

- [告知下書き](windows-desktop-licenses/THIRD-PARTY-NOTICES.draft.txt)
- [由来・対応ソース台帳下書き](windows-desktop-licenses/DEPENDENCY-SOURCES.draft.json)


## 第2回点検：Qt・Pillow・OpenSSLのソース/パッチ対応

2026-11-15。uv版の開発は中止のまま。アプリ・ビルドコードの変更、ビルド、コミット、公開は行っていません。

### 今回確認できたこと

- Qt6.11.2の全ソース1,019,661,552 bytesを公式mirrorlistのSHA256（6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33）で照合。140件の第三者attribution、402件のLICENSES内ファイル、45モジュールの版情報を記録。アーカイブ内447件のpatch/diffファイルは上流ソースに含まれるファイルの在庫であり、wheelへ適用されたパッチ数ではありません。
- 入力wheelにQt Virtual Keyboard・Charts・Graphs・DataVisualization等が存在し、対応ソースのGPL-only表記も確認。これらをLGPLだけで一律に扱いません。入力に存在することは最終収録される証明ではなく、除外も未実施です。
- Pillow・cryptographyの公式wheel本体を公開SHA256で照合し、埋込SBOMを取得。cryptographyのOpenSSL4.0.3ソースはSBOMにあるSHA256と完全一致。SBOMのWindows/static等のビルドフラグも保管。
- cryptographyのregistry依存32件が、wheel内SBOM・sdist Cargo.lock・取得crateのチェックサムで全一致。差集合は0件。プロジェクト内等の非registry部品と、最終ビルド操作の完全対応は別途必要。
- Python側OpenSSL3.5.9ソースも公式Release digestおよびPBS20261110のdownloads.jsonにある期待ハッシュと一致。PBSのWindows用ビルド/パッチ11件を保管し、applink/uplink修正とstatic-link設定を確認。Python側OpenSSL3.5.9とcryptography側OpenSSL4.0.3は別系統です。
- Pillow公式Windowsビルド定義から14依存のURL/パッチ/告知指定を抽出し、13件を取得。17か所の置換前テキストを各公式ソースで確認。取得物のローカルSHA256は記録済みですが、各codecソースの独立した期待ハッシュ照合は全件完了していません。
- Pillow SBOM内のfribidi-shim・pythoncapi_compat・raqmの3ソースハッシュがsdist内の実ファイルと一致。SBOM記載パッチ3件（raqm2件・LibTIFF1件）を保管。LibTIFFの4区間は元ソース内で一意に対応し、元パッチの行番号との差は8/10行。指定行番号そのままの一致ではなく、文脈一致として記録。
- Little CMS2.19.1の公式ソースヘッダーはLCMS_VERSION=2190で、Pillowはこれを2.19と表示する処理です。表示差はソースで説明できましたが、それだけで当該バイナリの唯一のビルド元とは証明しません。

### まだ残ること

1. Qt wheelの実コミット・追加パッチ・ビルド設定の完全対応。不要なGPL対象/マルチメディア/ブラウザー等の収録範囲を絞り、最終実体で点検する。
2. Pillowのlibavif配下のcodec等の推移的ソース、compiler/生成設定、全外部パッチの閉包。任意項目libimagequantの上流URLは404。上流Windowsワークフローは--no-imagequant、実ランタイムも非対応ですが、最終収録物で再確認する。
3. MuPDFの内包物・パッチ/構成、Microsoft CRT条件、Python等の残る内包成分、改変ライブラリ置換の受入。
4. 最終onedirが未生成のため、入力471件/55件は最終収録数ではありません。実ペイロードと告知/対応ソースを結び付ける工程が必要。
5. Inno固定コンパイラ/署名/対応ソースの最終記録と、Desktop固定入力のuv名プロファイルからの分離。

告知・由来台帳は引き続き*.draftです。reviewed-files.jsonは作成せず、配布条件の全確認やビルド許可済みとは扱いません。

- [ソース/パッチ対応の根拠](windows-desktop-licenses/BUILD-PATCH-CORRESPONDENCE.draft.json)

## 第3回点検：収録範囲とDesktop固定入力の分離案（2026-11-15）

### Qtの除外方針（未実装）

Folimeldソースの直接importはPySide6.QtCore/QtGui/QtWidgets。PDF処理はPyMuPDF、画像変換はPillow。現在のDesktop specはexcludes=[]で、除外はまだ実施していない。

- 維持する基点：Core/Gui/Widgets、PySide/Shiboken、qwindows.dll、必要な日本語IME・アクセシビリティ・スタイル・画像プラグインとその依存。QtSvg等は直接importがなくても画像プラグインの依存になり得るため、一律に除外しない。
- 除外候補：VirtualKeyboard、Charts、Graphs、DataVisualization、QML/Quick、WebEngine/WebView、Pdf/PdfWidgets、Multimedia/FFmpeg、3D、Designer等の未使用機能。各モジュールとネイティブDLL・プラグイン・QMLデータを一組として扱い、依存解析で必要と判明したものは理由を記録して再審査する。
- PyInstaller6.22.2のQtGui hookはplatforminputcontextsやimageformatsを収集対象にする。Pythonモジュール名だけのexcludesではVirtualKeyboardプラグイン等の除外を保証できない。Python import除外と、Analysis後のDLL/プラグイン/データの明示フィルター、最終収録台帳の禁止項目検査を組み合わせる案とする。
- 機械的な広範囲削除はせず、不明な依存はビルドを止めて確認する。OpenGLソフトウェア描画等はTEST88の表示語だけを理由に除外しない。
- 将来の受入：日本語入力・ファイルダイアログ・サムネイル・PDF表示/保存・画像変換・3ワーカー・DPI・低機能GPU経路、およびLGPLライブラリ置換。今回は実行しない。除外しても残るQt/PySideの条件点検は必要。

### Pillowの追加判明点と残件

公式Windows build_prepare.pyはlibavifでAVIF_LIBSHARPYUV/AVIF_LIBYUV/AVIF_CODEC_AOM/AVIF_CODEC_DAV1D=LOCAL、AOM_DECODE=OFFを指定。libavif1.4.2内のextスクリプトはAOM v3.14.1、dav1d1.5.3、libwebp v1.6.0、libyuv checkout 644251f25を参照する。これらはビルド定義の参照先であり、実wheelの全内包版を確定した結果ではない。テスト用fuzztest/GoogleTest等まで一律に実収録と扱わない。

残件は、上記の推移的ソース/ライセンス/パッチの取得と独立ハッシュ照合、libyuv短縮コミットの完全ID対応、実wheelとの結び付け、compiler/生成設定。PillowのImage hookはImagePluginを広く収集するため、アプリの受付画像形式が少ないことだけでcodecを削除できない。libimagequantはWindows定義--no-imagequantかつ実ランタイム非対応であり、SBOMの任意項目を実収録としない。取得済みcodec13件も独立期待ハッシュ照合は未完。

### MuPDFの追加判明点と残件

PyMuPDF1.28.2のdist-infoには今回の範囲でSBOMを確認できず、親パッケージ版だけから内包物を確定できない。公式MuPDF1.28.2ソースのthirdpartyにbrotli/cmark-gfm/curl/extract/freeglut/freetype/gumbo-parser/harfbuzz/jbig2dec/lcms2/leptonica/libjpeg/mujs/openjpeg/tesseract/zint/zlib/zxing-cpp等を確認した。存在はWindows wheelでの有効化・リンクの証明ではない。

上流thirdparty/READMEはリリースtarがテスト等を省略した構成であることを明記。直ちに不足と断定せず、実ビルドに必要な入力を満たすか確認する。残件はwheelの構成・生成設定・パッチ・サブモジュールの正確な版と全告知、取得済みMuPDF tarの独立期待ハッシュ、AGPL対応ソースの実配布物との対応。Folimeld自身のソース、ビルド設定、必要な生成物/変更も版別に結び付ける。

### Microsoft CRTの実入力と残件

キャッシュを除く入力で17パスのCRT DLLを確認。Python2、PySide6 7、Shiboken6 7、winrt 1。すべてPE Machine=0x8664。Python/Qt系は14.44.35211.0、winrt/msvcp140.dllは14.29.30157.0。入力台帳であり最終収録数ではない。

同名・同じ表示版でもPython/PySide/Shiboken間でSHA256が異なるため、同じ版という理由で重複を置換しない。由来・署名・実依存・互換性を確認し、最終ロード先と収録ハッシュを固定する。Microsoftの再配布条件・該当Visual Studio版のREDIST一覧・利用可能なライセンスを確認する必要がある。wheelに同梱されていることだけで再配布許諾を確認済みとしない。OSのUCRT/system DLLを無差別にコピーしない。

配布案は、許諾を確認した公式再配布入力からのapp-local方式を優先検討し、条件が成立しなければ公式VC Redistributable前提方式を再設計する。後者で管理者操作が必要なら、現在の非管理者インストール方針との違いを事前提示する。現時点で方式・許諾・署名確認は未確定。

Microsoft公式：https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170

### Desktop固定入力のuv版からの分離案（未実装）

1. 新しいpackaging/windows/desktop-runtime.jsonにdistribution=windows-desktop-x64、Python3.12.16の配布URL/期待SHA256、依存14件の版とWindows x64 wheelのURL/期待SHA256、必要な第三者ソース/パッチ/告知の対応を固定する。初期版を同じ値にしても、windows-uv-runtime.jsonを実行時に参照・同期しない。
2. Desktop専用lockは工具としてのuvを必須にせず、ハッシュ検証付きの独立した依存解決結果を保持する。runtime入力とPyInstaller6.22.2/hooks2026.7、Inno固定コンパイラ等のbuild-tools入力を分ける。Innoの版/由来/ハッシュ/条件は別途確認する。
3. tools/desktop_build.pyの参照をDesktop専用へ変更し、Python・全依存・工具・入力ハッシュ・x64・制限PATH・Qt収録方針・承認済み告知を事前検査する。uv環境/キャッシュの自動利用やフォールバックを設けない。
4. 新規のDesktop専用ビルド環境/成果物/ログ/対応ソース台帳を作り、アプリ設定分離は既実装のFolimeld-Desktopを維持する。uv用設定・ランチャー・公開物は変更しない。Store版も維持する。
5. 変更時には差分を提示し、承認前にビルドしない。現状は未承認の告知下書きでありreviewed-files.jsonを作らない。

### 今回の根拠と制限

開発PC outputs/windows-desktop-legal-audit-20261115 のthird-pass-source-inspection.json、static-source-excerpts、crt-input-inventory.jsonに生情報/サイズ/SHA256を保存。収集済み入力と既存ソースを静的に確認したもので、新しいonedirやsetup.exeは生成していない。uv開発中止を維持。ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は実行していない。


## 第4回点検：Pillow・MuPDF・CRTとDesktop工具固定（2026-11-15）

### 今回確認・整備したこと

- Desktop専用の工具をPyInstaller6.22.2、hooks2026.7、altgraph0.17.5、packaging26.3、pefile2024.8.26、pywin32-ctypes0.2.3、setuptools84.0.0に固定。工具wheel7件とsdist7件を公式PyPI公開SHA256で照合し、告知を保管。
- Python3.12.16配布、固定依存14wheelも新たに取得・期待SHA256照合。Python・14runtime・7tools・Innoの23入力を実ファイルで再照合した。wheelメタデータのWindows x64/Python3.12.16に対する有効な依存19条件は全件充足（任意extraなし）。依存解決を再実行して新しい版を採用したものではない。
- Inno Setup7.1.1 x64配布EXE（14,336,568 bytes）は公式GitHub Release digestと一致。SHA256=8a5a6711c3766a6e5fb74f280ba0e3551e719ce94538d901fdbd1f8f9920b3f0。Authenticode Valid、発行元Pyrsys B.V.、ProductVersion7.1.1。実行・導入・展開・コンパイルはしていない。公式タグのソースアーカイブとライセンスも保管（ソースアーカイブのSHAはローカル測定）。取得exeの固定は導入後ISCC/内部スタブのハッシュ確定を意味しない。
- Desktop専用JSONに工具wheelとInno配布物のURL/SHA256等を追加。runtime用・tools用のハッシュ付きrequirementsを分離。Desktop補助に必須--input-rootを追加し、ローカル23入力を読み取り照合してからビルド出力を作成する構成にした。照合関数だけを実23入力で実行しPASS。ビルド入口は実行していない。
- Pillow AVIFのAOM v3.14.1→03087864cf4bea6abb0d28f95cf7843511413d8f、libyuv短縮644251f25→644251f252a84bf8ce91ff0aca86a9b16b069ab8を公式Git情報で解決。dav1d1.5.3と合わせソース3件・LICENSE/COPYING/PATENTS等を取得しSHA256を記録。これらアーカイブはローカル測定ハッシュであり、独立した公開期待ハッシュとの照合済みではない。libsharpyuvは取得済みlibwebp1.6.0内の部品として扱う。上流定義が参照する版と実wheelの内包版の完全対応は別問題。
- MuPDF1.28.2の公式Gitタグはfe374accd98a43174a328fa7980d7675e06d5b0d。18サブモジュールの固定コミットを取得し、取得済みtarの通常ファイル8,009件をGit blobへ照合。7,982件完全一致、27件はcurlのWindows solutionファイルの改行差のみで説明。未説明の本文差0。tar圧縮物の独立公開SHA照合や実wheelとのビルド対応を確定した結果ではない。ソース内の告知/ビルド定義26件を保管。
- キャッシュを除くCRT17入力はすべてAuthenticode Valid。同じ14.44.35211.0で異なるSHAを持つPython/PySide/Shibokenのファイルは、証明書領域とPEチェックサムを除くと同名の残り全バイトが一致。元ファイルは未改変。winrt内msvcp140.dllは別版14.29.30157.0なので別扱い。署名一致や本文一致は再配布許諾の証明ではない。

### 残件

1. Pillow：AOM/dav1d/libyuv等の実wheelとの対応、全内包物/ビルドパッチ/compiler/生成設定の閉包、codec取得物の独立期待ハッシュ確認。不要codec除外の実装/受入は今回行っていない。
2. MuPDF：Windows wheelの実構成・適用変更・ビルドログ/証明との対応、実収録物の第三者告知とAGPL対応ソース一式。18サブモジュールはArtifex forkを含み、一般的な上流版名で置き換えない。公式タグとtar本文の対応は前進したが、wheelの完全な由来確定ではない。
3. CRT：該当Visual Studio等の有効な再配布権限、正規Redist実体との対応、採用する配布方式・最終配置/読込先。署名を除去したファイルを配布する案ではない。正規入力を未改変のまま扱う。管理者不要インストール方針を変える前に提示する。
4. 工具：新規Desktop環境への導入とその全実体/RECORD対応は未確認。Inno導入後のISCC/スタブ/内包成分の固定、インストーラー第三者告知と署名方針は残件。取得物23件のハッシュ一致だけで環境や最終バイナリの同一性・再現性を保証しない。
5. Qt wheelの完全なビルド元/パッチ、実onedirの収録台帳、LGPL置換の受入、最終setupとアプリ/第三者ソースの対応も従来どおり残る。

### 確認と制限

自動検査43 PASS（入力改変・領域外参照の拒否を追加）、ruff PASS。git diff --check PASS。現在の8ファイル反映済みコミットfb39c5eに対し、今回の工具固定等は未コミット。
資料は引き続きPREBUILD-DRAFT-NOT-APPROVED。reviewed-files.jsonは作成せず、告知承認ガードを維持。Store用/uv用設定と共通アプリは変更していない。uv開発中止を維持。
ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。

根拠：desktop-fixed-inputs/{archive-gate-verification.json,tools-download-verification.json,runtime-wheel-verification.json,tool-source-verification.json,dependency-closure.json,pillow-transitive-source-verification.json,mupdf-source-git-correspondence.json}、input-authenticode-fourth-pass.json、crt-pe-normalized-comparison.json。
公式条件：
https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution
https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170
https://jrsoftware.org/files/is/license.txt
https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright


## 第5回点検：実wheel・ソース/パッチと正規CRT対応（2026-11-15）

### Pillow12.3.0

1. 公式公開SHA256で照合済みのWindows cp312 x64 wheel（a2b55dd6b2a4c4b7d87ffa56bdb33fdc5fdb9a462173861a7bc097f17d91cb09）について、PyPIのpublish attestationを取得。statementのsubject hashが実wheelと一致。証明書にはpython-pillow/Pillow、refs/tags/12.3.0、コミットbb1d8e8ab8d29048624d96e3ee53cecf7c13d13d、wheels.yml、run28508597348/attempt2が記録されている。ただしSigstore署名・透明性証明の独立検証は未実施。publish証明は全ビルド入力のSLSA証明ではない。
2. 同コミットのGit treeと、取得済みsdistのsrc/・winbuild/・setup.py・pyproject.toml・LICENSEを照合。229件完全一致。残る6件はpillow.egg-info生成メタデータ。実装/Windowsビルド入力に未説明の本文差は今回の範囲でない。
3. 実_avif.pyd内でAOMedia Project AV1 Encoder 3.14.1とdav1dの1.5.3-0-gb546257を確認。dav1d公式1.5.3タグのコミットb546257f770768b2c88258c533da38b91a06f737と接頭辞が一致。版/文字列の一致だけで全codecバイトのビルド由来を証明しない。
4. GitHubで同runのWindows AMD64ジョブ成功とPyPI公開ジョブ成功を確認。Windowsジョブログ取得はHTTP410で不可。再実行はしない。既存SBOMのパッチ3件、Windows置換定義17か所の元ソース文脈一致等は前回記録を維持する。

残件：公開証明の独立検証、実適用パッチ/compiler/生成設定とwheel全体の対応、取得codec/推移的ソースの独立期待ハッシュと告知の閉包。libyuv等は上流定義・完全コミットまで特定済みだが実バイナリとの全対応を断定しない。ログを取得できないことだけで配布違反とは扱わず、対応ソースと告知を満たす根拠を別に整理する。

### PyMuPDF/MuPDF1.28.2

1. 実wheelのpymupdf/_build.pyを実行せず読み取り。pymupdf_git_sha=12786d12b2962a1d77fd13b103162eddf749644cは公式PyMuPDF1.28.2タグのコミットと一致。MuPDF取得先は公式mupdf-1.28.2-source.tar.gz、SWIG版は4.4.1と記録。branch/commentはビルド自己申告であり独立したビルド証明ではない。
2. wheel内Pythonファイル14件のうち11件がsdistのsrc/とバイト一致。extra.py・mupdf.py・_build.pyの3件は生成ラッパー/ビルド記録として直接一致対象から分離。
3. wheel内開発用ヘッダー90件のうち84件がMuPDF取得ソースとSHA256一致。classes.h/classes2.h/exceptions.h/extra.h/functions.h/internal.hの6件は元tar内に直接対応物がなく、生成手順/入力との対応を残件とした。生成物の欠落を即座にソース不足や改変と断定しない。
4. DLL内のMuPDF1.28.2文字列も確認。前回のtar本文8,009件対公式Git（7,982件完全一致、27件改行差のみ）、18サブモジュール固定記録と併せて保管。PyPIの当該wheel publish provenanceはHTTP404で取得できず。公式build_wheels.ymlとsdistのscripts/gh_release.pyを保管したが、可変環境変数の実値/最終ビルドを証明するものではない。

残件：生成ラッパー/ヘッダーとSWIG4.4.1等の正確な生成入力、Windows wheelの有効機能・実パッチ/コンパイラ設定、第三者告知と対応ソース一式。AGPLアプリ/依存の対応ソース、ビルド定義と必要な生成物を最終ペイロードへ結び付ける。MuPDF tar圧縮物の独立期待SHA照合は未完だが、通常ファイル本文の公式Git対応は確認済み。

### Microsoft CRT

1. 開発PCのVisual Studio2022 Community正規VC/Redist/MSVC/14.44.35112領域に、実ファイル版14.44.35211.0のx64 CRTを確認。Desktop系のx64/Microsoft.VC143.CRTとonecoreを分けて記録し、一般Desktop向け候補にはonecoreを選ばない。
2. 17入力中2件（Python側vcruntime）は正規Redistと全バイト/SHA256一致。14件（Qt/Shiboken）は証明書領域とPEチェックサムを除いた本文が正規Desktop Redistと一致。元ファイルには変更を加えていない。これは署名を除去して配布する案ではない。
3. 残るwinrt/msvcp140.dll14.29.30157.0はMicrosoft公式https://aka.ms/vs/16/release/VC_redist.x64.exeから取得した正規14.29.30157.0（SHA256=6afae68a783f11292149175844aed0e2ce3f247bc0250f6cb18c931295b3f399）の埋込CABから、EXE/MSIを実行せずに抽出。x64ファイルのSHA256=75872c426555ac8af55b5a7f6d4aea8831af74353b22612850a2bfc40e3b67e1が実wheel内DLLと完全一致。Redist EXEとDLLの署名はいずれもValid。ARM64の別ファイルは混同しない。
4. これで17入力すべての正規Redistとの対応が取れた（全バイト一致3、署名領域等を除く本文一致14）。ただし採用する最終CRTセットやロード互換性は未決定。現在のwheelやDesktop payloadを置換していない。
5. Microsoft公式Community2022利用条件原本を取得。個人の自己アプリ開発等の利用区分、Distributable Listに基づく再配布権、主たる機能の付加、エンドユーザー/再配布先を保護条件へ同意させる要求、名称・商標・改変/Excluded License等の制限を確認した。Communityが存在することは個別利用条件を満たすことの自動証明ではない。CRTをFolimeldのAGPLで再許諾せず、第三者条件を分離する。
6. 公式資料はcentral deploymentを推奨し、管理者不要のapp-localも条件付きで説明する。app-localの保守更新責任を残件にする。Microsoft正規のRedist領域から未改変の現行CRTを採用する案と、正規Redist前提方式を比較する。後者で管理者操作が必要になるなら、現方針の変更を事前提示する。
7. 旧2019 Redistに同梱されたRuntime EULA原本（14言語）も保存した。install/useの許諾と再配布権を同一視しない。旧DLLを採用する場合はその配布根拠も必要。現行CRTへの統一は互換性確認前に確定しない。

### ビルド前に必要な残件

- 配布条件：Pillow/MuPDFの対応ソース・生成入力・パッチと実収録物の対応、必要な第三者告知の閉包、CRTの適用可能な再配布根拠と利用者向け条件、Qt等の従来残件。
- 配布入力：採用CRTの未改変実体/版/配置とその固定、Inno導入後工具/スタブ内部の固定、新規Desktop環境とハッシュ固定済み23取得物の全実体対応。
- 再現性：コンパイラ/生成条件と全wheelバイトの対応は未確認。これはそれだけで配布条件違反を意味せず、配布に必要な対応ソースの充足とは分ける。
- ビルド後の受入：実onedir、DLL動的読込、日本語IME/GPU/PDF/画像/3ワーカー/DPI、LGPL置換等は今回は未実施で、将来の承認済みビルド後に確認する。

今回アプリ/ビルドコードは変更せず、取得済みwheelのZIP/PE・ソースの静的読取と公式資料照合、資料保存のみ。自動検査43 PASSは前回結果であり今回は再実行していない。
uv開発中止を維持。ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。告知資料はPREBUILD-DRAFT-NOT-APPROVEDを維持しreviewed-files.jsonは作成しない。

根拠保管先：fifth-pass内のpillow-provenance/attestation/source/job evidence、pymupdf/mupdf wheel correspondence、crt-official-redist-correspondence、old-crt-exact-match、Microsoft利用条件/署名記録。各元資料と新規記録のSHA256はevidence-sha256.jsonを参照。
公式条件：
https://visualstudio.microsoft.com/license-terms/vs2022-ga-community/
https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution
https://learn.microsoft.com/en-us/cpp/windows/choosing-a-deployment-method?view=msvc-170
https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright


## 第6回点検（2026-11-16）：生成物・パッチの由来とCRT配布案

### 追加で確認できたこと

- PillowがSBOMに宣言するraqmパッチ2件を、公式libraqm0.10.5ソースの対応箇所へメモリ内で反映した結果が、Pillow sdist同梱のraqm-version.h/raqm.cとそれぞれSHA256・全バイト一致した。元アーカイブや元ソースは変更せず、コンパイル/コード生成はしていない。raqm.cの結果は前回の実wheel SBOM記載ハッシュとも一致する。取得raqmアーカイブはローカル測定SHAであり独立期待SHA照合ではない。
- LibTIFF宣言パッチ4区間も各文脈が一意に対応し、メモリ内の反映結果ハッシュを記録。ソース位置は2224→2216、2364→2356、2522→2512、2625→2615。これは実_imaging.pydへの適用を直接証明するものではない。
- MuPDFの生成ヘッダー6件はscripts/wrap/cpp.pyの出力集合と一致し、実wheel全6件にmupdfwrap.py生成マーカーがある。PyMuPDF setup.pyのplatform/c++/includeからの収録処理も確認。
- extra.pyはsrc/extra.iとpipcl.build_extensionから、mupdf.pyはMuPDF scripts/wrap/swig.pyの生成interfaceから作る経路を確認。実wheel両ファイルにSWIG4.4.1のマーカーがあり、_build.pyの記録と整合する。
- _build.pyはsetup.pyがgit情報・MuPDF位置・版・SWIG版・fake-no-gilフラグから作成する処理を確認。生成物9件は生成由来を追跡できた状態に更新する。ただし再生成してバイト一致を確認した状態には更新しない。追加で、PyMuPDF sdistのpyproject.tomlが外部ビルド工具pipclを版指定なしで要求し、その本体は同sdistに含まれないことを確認。呼出位置は分かったが実際に使われたpipclの版・本体の対応は未確定。libclangの実版や上流生成時の全環境も未確定。

### CRTの配布方針案（まだ適用しない）

1. 現行案の管理者不要インストールを維持する場合は、正規Visual Studio2022 RedistのDesktop x64/Microsoft.VC143.CRT由来・未改変14.44.35211.0を候補にする。onecore/debugやSystem32からの収集を行わず、コピー前後のサイズ/SHA256/署名と相対配置を最終台帳に記録する。
2. 現在のQt再署名CRTおよびwinrtの旧14.29を統合・置換するかは、最終依存・ロード先の検査と受入後に決める。本文一致や新旧互換性の一般説明だけで採用済みとしない。現在のwheel・環境・payloadには置換を実施していない。
3. 適用可能なVisual Studio利用条件とDistributable Listを記録し、CRTをアプリのAGPLで再許諾しない。利用者/再配布先へのMicrosoft条件の扱いを、Folimeldの権利を制限しない第三者条件として分離する。インストーラーに表示する最終条件文と同意方法は未確定で、告知だけで契約条件を満たしたと扱わない。
4. Microsoft推奨のcentral deploymentを使う代案では、公式Redist導入に管理者権限が必要になる点を提示してから設計を変更する。現方針を無断で変更しない。
5. app-localを選ぶ場合はCRTの更新提供もアプリ側で管理する。今回保管した14.44.35211.0が将来も最新/安全と保証するものではなく、公開候補時点で保守状況を見直す。

### ビルド前の残件（区別）

配布資料・条件：Pillow内包codecの告知/対応ソースの閉包、MuPDF生成入力と必要なラッパー/ソース・ビルド手順一式、CRT利用/再配布条件と利用者向け条件、Qtの従来残件を整理する。実payloadの確定後に告知/対応ソースと突合する。
入力・工具：新規Desktop環境と固定済み23取得物の対応、Inno導入後の実工具/スタブ、採用するCRTセット/配置を確定する。
検証上の限界：生成物9件の由来は追跡済みだが再生成一致は未確認。実wheelの全コンパイラ設定・パッチの機械語レベル対応やバイト単位再現性も未確認。これらの未確認を直ちに配布条件違反とみなさず、対応ソースの充足に必要な事項と再現性向け事項を分けて判断する。
ビルド後：PDF/画像/3ワーカー/IME/GPU/DPI、動的DLL読込、LGPL置換、更新/削除/復旧等は承認されたビルド後の受入とする。

今回の新規成果は静的照合資料のみ。アプリ・ビルドコードは追加変更せず、既存の未コミット変更は保持。資料はPREBUILD-DRAFT-NOT-APPROVED、reviewed-files.json未作成。
uv開発中止を維持。ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。前回の43 PASSを今回の検査結果として流用しない。

根拠：sixth-pass/pillow-upstream-patch-correspondence.json、generated-file-source-map.json、generated-artifact-correspondence.draft.json、wheel-generated-file-inventory.json、generator-source/、evidence-sha256.json。
Microsoft再配布条件：https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution
配布方式：https://learn.microsoft.com/en-us/cpp/windows/choosing-a-deployment-method?view=msvc-170


## 第7回点検（2026-11-16）：pipclの版・入力とCRT告知案

### pipclの版について

- 対象PyMuPDF Windows x64 wheelのPyPI公開日時は2026-08-06T21:39:00.213102Z（日本時間8月7日06:39）。実wheelのWHEEL記録はGenerator: pipclで版番号を含まない。sdistのpyproject.tomlもrequires=['pipcl']で版未指定。
- PyPI履歴で、公開前の最新版は12（2026-07-09T07:54:54.760307Z）。13は2026-09-01公開で当該wheel公開後。通常のPyPI公開版を使う前提では12が時系列上の有力候補だが、過去版キャッシュ・非PyPI入力等は排除できず、実使用版12と確定しない。
- 候補11/12のwheel・sdist各2件を公式PyPI SHA256で照合して取得。pipcl12 source SHA256=c7545480cfa808500d8b606da73db7f89a872258bcdb293716126e2ccff1a5c6、wheel SHA256=aa34a85e10701758871f439303f6aace94b18ef9cd6bef69d5948b7afc0e125b。これは候補入力の保管であり、Desktop工具へ採用・インストールしたものではない。
- 11と12のgit_info_pyは関数本文まで一致。build_extensionの差は説明文の追加で、docstring/位置情報を除いたASTは一致。両関数の生成結果から11/12を識別できる根拠にはならない。他関数や全工具環境の同一性を証明するものでもない。
- pipcl12はAGPL3のCOPYINGを含み、パッケージメタデータはpackagingを依存に指定（版未固定）。候補ソース/条件も保管する。実使用packaging版も未確定。
- 該当PyMuPDFコミットの公開Actions履歴は5件取得できたが、対象wheelの実ビルドへ結び付く記録は得られなかった。build_wheels.ymlを指定した当該期間のrun照会は404。ワークフローの改名/削除や保持範囲の影響を排除できず、ビルドが存在しなかったとは扱わない。

### 生成入力の整理

確定/自己記録を区別して、PyMuPDF source commit12786d12b2962a1d77fd13b103162eddf749644c・src/extra.i・setup.py、MuPDF公式1.28.2ソースと18サブモジュール、生成ヘッダー/ラッパー経路を保持。SWIG4.4.1は実wheelの2生成ラッパーのマーカーと_build.pyに記録されるが、使用実行ファイルのハッシュは不明。
追加で必要なのは、実pipcl版/配布ハッシュ、packaging/libclangの実版、SWIG実体、コンパイラ/SDK/Python等の版、環境変数・生成コマンドの実値。cp310-abi3タグは最低ABI情報であり、実ビルドPythonが3.10だったことの証明にはしない。
これは上流wheelをソースから再生成する際の入力問題であり、公式wheelを収集するDesktopアプリのPyInstaller工具にpipclを加える理由ではない。新規の第三者再ビルドを行う場合は、その入力固定を別の承認対象として扱う。過去の未知入力を新しい固定値で埋めて確定済みとはしない。

### CRT条件と利用者向け案

- 正規Visual Studio2022のv143/vc_redist.x64.exeを読取取得。ProductVersion14.44.35211.0、署名Valid/Microsoft。EXEの起動・導入は行わず、埋込CABから14言語のRuntime利用条件原文を保存。英語原文の対象名はMicrosoft Visual C++ 2015 - 2022 Runtime。
- 開発者の再配布根拠（適用可能なVisual Studio契約＋Distributable List）と、利用者に適用されるRuntime条件原文は別の資料。Runtimeのinstall/use条項だけから再配布権まで確認したとは扱わない。
- 採用候補は正規Desktop x64 Redistの未改変ファイル。debug/onecoreを一般Desktop用に選ばず、署名を取り除いた比較用バイト列も配布しない。実採用版・ファイル集合・配置は未確定。
- 利用者向けの日英告知案をCRT-USER-NOTICE.draft_ja.txt/.draft.txtに作成。Microsoftコンポーネントは別条件であること、AGPLで再許諾しないこと、原文・版/ハッシュ一覧への案内、Folimeld/他OSSの権利を制限しないことを記載。
- 告知文はMicrosoft原文の代替契約でも、利用者が同意済みである証拠でもない。最終セット確定後、実際のRuntime条件原文と部品台帳を同梱し、開発者側契約が求める利用者/再配布者への条件提示・同意方法を整合させる。アプリ全体にMicrosoftの制限を適用する文面にはしない。Innoの画面や同意処理は未変更。
- app-localは管理者不要方針を維持できる候補だが保守更新責任が残る。中央Redist方式に変更する場合は管理者導入を伴う点を先に提示する。

### 残件

1. pipclの実使用版確定には、上流の当時の依存インストール記録・ビルドログ/固定台帳等が必要。12という推定を確定値にしない。Pillow/MuPDFの従来の対応ソース・パッチ・告知整理も継続。
2. CRT再配布に適用する契約条件、最終CRTセットと配置、Runtime原文・部品台帳・利用者向け条件/同意方法を確定する。告知案はレビュー前の下書き。
3. Qt、独立Desktop環境と固定済み入力の実体対応、Inno内部工具/スタブ、最終payloadと告知/ソース対応は引き続き残る。
4. 過去の上流ビルド再現性が不明であることと、対応ソース提供義務等を満たすかは分けて判断する。未確認事項だけで違反と断定しない。

アプリ・ビルドコードは追加変更しない。資料はPREBUILD-DRAFT-NOT-APPROVED、reviewed-files.json未作成。uv開発中止を維持。
ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。自動検査の再実行もしていない。

根拠：seventh-pass/{pipcl-pypi.json,pymupdf-pypi.json,pymupdf-wheel-WHEEL.txt,pipcl-11/12-downloads.json,pipcl-candidate-function-comparison.json,pipcl-executable-ast-comparison.json,official-vc-redist-14.44-terms.json,official-vc-redist-14.44-signature.json,MICROSOFT-VC-RUNTIME-14.44-EN.original.rtf,CRT-USER-NOTICE.draft*.txt,evidence-sha256.json}。
公式資料：https://pypi.org/project/pipcl/ 、https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution


## 第8回整理（2026-11-16）：pipcl未確定の扱い・ビルド前条件・CRT集合/配置案

### pipcl未確定でも進められる範囲

Desktopは固定済み公式PyMuPDF wheelを収集する方式で、pipclを呼ばずMuPDF/PyMuPDFを再コンパイルしない。そのため過去のpipclの正確な版が不明なことだけを、アプリのパッケージ作成そのものの停止理由にはしない。
進められるのは、固定wheel/工具のハッシュ検証、新規Desktop環境準備の設計、収録制限/重複検査、告知・対応ソース・生成経路の整理、CRT配置/更新/受入手順の設計。今回は実装追加・環境導入・ビルドには進まない。
pipcl不明を理由に、sdistや生成入力・ライセンス条件の確認まで省略してよいわけではない。対応ソースが実依存に対応している根拠は別途審査する。

### 別に残す再現性調査

上流wheelの完全再生成、第三者ライブラリの変更ビルド、バイト単位再現性を行う場合は、pipcl実版と配布ハッシュ、packaging/libclang/SWIG/コンパイラ/SDK/Python・全生成設定を別入力として固定する。候補12を過去の確定値にしない。現行Desktop工具へpipclを追加しない。
従来の「ビルド前残件」に混在していた項目は、対応ソースの充足、Desktopの技術的なビルド条件、上流wheel再現性に分ける。再現性の不明だけで配布条件違反とは扱わない。

### この計画で候補ビルド前に必要な確認

1. 版/対象の確定：Desktop x64・独立設定/ログ・Store非変更・uv開発中止・数値ファイル版を確認。今回のビルド実行は未承認なので行わない。
2. 入力と環境：既存23入力（Python、14runtime、7tools、Inno）のハッシュ固定を維持し、新規Desktop環境の実版/RECORD対応と、導入後Inno/ISCC・スタブ実体を確認。取得物の一致だけで導入後の全実体を確認済みにしない。
3. CRT収録処理：下記7ファイルの正規Desktop x64原本・SHA256・署名を再照合し、TOCの重複除去/正規化と実体記録を実装して差分確認する。既存validate_binary_sourcesはPython/Windows配下のみ許可するため、正規CRTを外部入力から採用する処理には、個別ハッシュで限定した許可を設計する。Program Files等の広範囲許可や黙ったガード解除をしない。
4. 条件と資料：適用可能なMicrosoft再配布根拠、利用者向けRuntime原文と告知/条件提示方法、Pillow/MuPDF/Qt等の対応ソース・パッチ/生成入力・必要告知を審査する。未確認事項を明記しただけの資料をreviewed-files.jsonで「点検済み」にしない。
5. 二段階の資料確認：候補ビルド前には採用入力に対する資料を審査し、候補生成後には実payloadと全件突合する。実payloadが未生成の現在、その照合まで完了したとしない。ビルド前には実payload審査が必要という循環条件を置かない。最終公開承認はこの二段階の後。

これは本プロジェクトの候補ビルド条件であり、一般にライセンス審査完了まで一切のローカルコンパイルが法律上禁止されるという意味ではない。

### CRT集合案：14.44.35211.0 x64の正規未改変7件

- vcruntime140.dll
- vcruntime140_1.dll
- msvcp140.dll
- msvcp140_1.dll
- msvcp140_2.dll
- concrt140.dll
- msvcp140_codecvt_ids.dll

保守的な7件案であり、最小集合を証明したものではない。既存入力の静的依存ではCore/Gui/Widgetsがmsvcp140_1を、Guiがmsvcp140_2を参照。concrtは入力にあるvcamp140経由で参照されるが、そのvcamp自体の最終収録は未確定。codecvt_idsへの静的参照は今回0で、動的利用を否定する証拠にはしない。将来減らす場合は実収録物・動的経路・受入の根拠を必要とする。
7件外のCRT/AMP等が収集された場合は未承認として止め、理由と条件を追加審査する。勝手に許可集合を広げない。System32のUCRT/API-set DLL、debug/onecore、旧14.29やQt再署名の同名CRTを最終案に混在させない。現時点で実ファイル削除や置換はしていない。

### 配置案

%LOCALAPPDATA%/Programs/Folimeld-Desktop/versions/<version>/
  FolimeldDesktop.exe
  _internal/
    vcruntime140.dll
    vcruntime140_1.dll
    msvcp140.dll
    msvcp140_1.dll
    msvcp140_2.dll
    concrt140.dll
    msvcp140_codecvt_ids.dll
    python312.dll
    PySide6/... (同名CRTは重複収録しない)
    shiboken6/... (同名CRTは重複収録しない)
    winrt/... (旧msvcp140.dllを混在させない)
    licenses/... (確定したRuntime原文・告知・部品/ソース台帳)

PyInstaller6.22.2の既定contents_directory=_internalと起動時SetDllDirectoryW処理を取得済み公式ソースで確認。現specはこの既定値を使う。既存runw.exeが公式ハッシュ照合済みPyInstaller wheel内の実体と完全一致し、通常/遅延インポートに上記VC Runtimeの直接参照はないことを確認した。したがって現在案ではEXE隣への同名CRT二重コピーを提案しない。ブートローダーを変更する場合は再検討する。
これは静的根拠に基づく案であり、OSの実ロード経路・フックによるAddDllDirectory等との組合せ・3ワーカーでの成功を確認したものではない。アプリ/ワーカーで全CRTの実パス・ハッシュをビルド後に確認し、System32や別アプリから偶然拾っただけの成功を区別する。

### 今回の確認と残件

既存Python/依存/Qt候補・CRT候補・ブートローダーの通常/遅延PEインポートを静的記録。入力にはアプリ未使用部分も含まれ、記録数は最終収録数ではない。7ファイルの版・サイズ・SHA256・予定相対パスはCRT-PAYLOAD-PROPOSAL.draft.jsonに記載。
今回は資料のみ追加。CRT正規化の実装、環境作成、実ビルド、アプリ/ワーカーのロード確認は未実施。前回43 PASSは再実行していない。uv開発中止を維持。
ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。

根拠：eighth-pass/crt-native-import-map.json、crt-import-summary.json、bootloader-wheel-correspondence.json、internal-layout-source-evidence.json、CRT-PAYLOAD-PROPOSAL.draft.json。
公式説明：https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170



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
