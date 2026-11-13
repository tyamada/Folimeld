# AlmaLinux9候補のQt・PySide・Shiboken・MuPDFソース確認

実施日: 2026-11-12（日本時間）。[公開前入力監査](linux-amd64-release-input-audit_ja.md)の続き。許可済みAlmaLinux9 Build環境の新規監査ディレクトリだけへ資料を追加した。候補の再ビルド、既存告知の上書き、版変更、公開は実施していない。

## 収集したアーカイブ

既存`dist/source/dependencies-0.3.2-linux/`のアーカイブを保持したまま、次の専用WSLディレクトリへコピーした。過去の配布物との対応ではなく、今回の候補が使う版・内容との照合として記録する。

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/qt-mupdf-audit-20261112/
```

| アーカイブ | バイト数 | SHA-256 |
| --- | ---: | --- |
| pyside-setup-everywhere-src-6.11.2.tar.xz | 18,053,248 | cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8 |
| qt-everywhere-src-6.11.2.tar.xz | 1,019,661,552 | 6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33 |
| mupdf-1.28.2-source.tar.gz | 68,898,646 | 44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156 |

QtとPySideは、現在の公式配布先から取得した`.sha256`とコピー前後のファイルを照合した。公式配布一覧は[Qt 6.11.2](https://download.qt.io/archive/qt/6.11/6.11.2/single/)と[Qt for Python 6.11.2](https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/)。PySideのアーカイブに` sources/pyside6/CMakeLists.txt`と`sources/shiboken6/CMakeLists.txt`があることをハッシュ付きで確認した。

MuPDFは[公式ソースURL](https://mupdf.com/downloads/archive/mupdf-1.28.2-source.tar.gz)をHTTPSで再取得し、収集済みファイルとハッシュが一致した。独立した署名付きチェックサム検証とは扱わない。リダイレクト先の一時クエリーはリポジトリの記録に含めていない。

## 候補内の実ライブラリとの照合

Alma候補`dist/folimeld`のQt/PySide/Shiboken/MuPDF関連106項目を、導入済みwheelのファイルと照合した。84件が実体、22件がPyInstallerのリンク項目で、リンク先を解決した全106件のSHA-256が一致した。最初の単純比較はリンク項目を実体として扱って失敗したため、項目種別を確認して再比較した。これをライブラリ改変の検出結果とは扱わない。

対象にはQtCore/Gui/Widgets/DBus/Network/OpenGL、QML/Quick、SVG、Wayland、PDF、XCB/EGL関連、PySide/Shiboken拡張、MuPDF共有ライブラリとPython拡張を含む。Qtソース内に必要なqtbase、qtdeclarative、qtsvg、qtwayland、qtwebengineのディレクトリが存在することも確認した。QtPdfが含まれるためqtwebengineソースも保持しているが、WebEngine機能をアプリが使用したことを意味しない。

この一致は「候補内バイト列と導入済みwheel」の照合であり、「wheelがこの上流ソースからどのパッチ・フラグでビルドされたか」の証明ではない。他OS候補のバイナリ全体についての照合結果でもない。

## ソース構成・告知の一覧

アーカイブを展開・実行せずに全項目を読み取り、LICENSE/LICENCE/COPYING/NOTICE/COPYRIGHTで始まる文書と`qt_attribution.json`のパス・サイズ・SHA-256を記録した。浅い階層の法的文書本文とQt attributionの内容もWSL内のinventory JSONへ保存した。

| ソース | 通常ファイル数 | 名前条件に該当する文書数 | qt_attribution.json数 |
| --- | ---: | ---: | ---: |
| PySide/Shiboken | 4,602 | 21 | 5 |
| Qt | 390,976 | 2,329 | 147 |
| MuPDF | 8,009 | 34 | 0 |

文書数はattributionを含み、重複やサンプルの文書も含む。ファイル名で抽出した一覧であり、必要な告知をすべて抽出したという判定ではない。Qt全体の広いソース集合なので、候補に含まれるコードだけのSBOMでもない。

PyMuPDF sdistの`setup.py`をテキストとして確認し、`version_p`と`version_mupdf`はともに1.28.2、既定取得先はmupdf.comの上記URLだった。sdist内にはMuPDFの入れ子アーカイブやMuPDFソースディレクトリは見つからず、独立したMuPDFアーカイブを保持した。

MuPDFにはfreetype、harfbuzz、libjpeg、openjpeg、jbig2dec、mujs、lcms2、zlib、brotli、leptonica、tesseractなどのthirdpartyディレクトリがあることを記録した。存在だけで、全構成要素がwheelへリンクされたとは扱わない。

版・取得先・全ライブラリハッシュ・文書一覧・attribution・PyMuPDF指定版・監査ファイルハッシュは[検証JSON](linux-almalinux9-qt-mupdf-source-audit-2026-11-12.json)に保存した。大きなソース本体と選択文書本文はWSL内に保持しており、JSONだけが対応ソース一式ではない。

## 残る工程

Python・PyInstaller・OS共有ライブラリとPillow実体は[後続調査](linux-almalinux9-native-runtime-source-audit_ja.md)で確認し、ソースRPM42個を収集した。PyInstaller告知の収集漏れは次回ビルド向けに修正・テスト済み。下記のうちPillow画像ライブラリのソース、ビルド来歴、新候補への反映は引き続き残る。

- wheelのビルド来歴、パッチ、コンパイラー、フラグ、実際の内包第三者コードと告知の確認。
- Pillowの画像ライブラリ、Python、PyInstallerブートローダー、同梱OS共有ライブラリのソース・告知収集と照合。
- 確認済み資料を次のビルド入力と配布告知へ反映し、新候補でソース対応・導入・GUI・ライセンス表示を再確認。
- 公開版との差分統合、版決定、通常デスクトップ・アプリ版間移行の残試験と公開前ファイル整理。

今回の追加はソース収集と技術的照合であり、ライセンス適合性の認定や公開準備の完了ではない。既存変更・配布物・README/CHANGELOGを保持した。
