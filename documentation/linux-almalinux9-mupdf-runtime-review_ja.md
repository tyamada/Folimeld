# AlmaLinux 9候補のMuPDF実体・内蔵フォント確認

2026-11-12。revision2候補と固定ビルド環境のMuPDF実体4件をバイト照合した後、公開シンボルと実行時に取得できるフォントを調べた。候補は変更していない。

## 内蔵フォントとソースの一致

固定PyMuPDF 1.28.2から`Font(fontname='helv').buffer`と`Font(fontname='cjk').buffer`を取得し、収集済みMuPDFソースのフォントデータと照合した。

| 実行時の指定 | ソース内の一致ファイル | バイト数 |
| --- | --- | ---: |
| helv | resources/fonts/urw/NimbusSans-Regular.cff | 33,151 |
| cjk | resources/fonts/droid/DroidSansFallback.ttf | 3,556,308 |

両者のSHA-256が一致した。これにより、先行の[MuPDF告知収集](linux-almalinux9-qt-mupdf-notice-review_ja.md)を、実際の内蔵フォント2件へ対応付けた。全内蔵フォントを網羅する試験ではない。

## 公開シンボルによる補助確認

MuPDF実体の動的定義シンボルから、FreeType、libjpeg、jbig2dec、MuJS、LittleCMS、zlib、Brotli、Tesseract、Leptonicaの各接頭辞に一致するものを確認した。これは実装が含まれる補助的根拠であり、各ライブラリの完全な版・パッチ・ビルドフラグの証明とはしない。

HarfBuzzやOpenJPEGは今回の接頭辞では一致がなかった。非公開・変更されたシンボル等の可能性があるため、これを非同梱の根拠には使わない。配布ヘッダーconfig.hの既定値も、wheelがその設定でビルドされた証明には使わない。

実体・フォントのハッシュ、シンボル数と具体例は[検証JSON](linux-almalinux9-mupdf-runtime-review-2026-11-12.json)を参照。

## QtPdfについて

QtPdfの動的定義シンボルには、今回の検索でPDFiumの公開API名が見つからなかった。一方、実バイナリの文字列にはpdfium名前空間とChromiumのpartition allocatorのソースパスがあった。QtPdfがPDFium/Chromium由来コードを持つ根拠とし、単なるQtバージョンの一致だけでは判断しない。

QtソースにPDFium本体とNotoSansCJK、agg23、bigint、fp16、highway、lcms、libopenjpeg、libtiffのライセンス文書があることを先行目録で確認した。生成告知・実ビルド選択の完全な対応は未完了のため、広いQtソース告知集合を補足資料として保持する。
