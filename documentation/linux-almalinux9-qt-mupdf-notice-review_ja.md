# AlmaLinux 9候補のQt/MuPDF告知参照確認

2026-11-12。[公開準備](linux-almalinux9-release-readiness_ja.md)の続き。候補を再ビルドせず、専用資料ディレクトリへ追加収集した。

## 対象モジュールとソースの区別

実候補のQtライブラリ・プラグインに対応して、qtbase、qtdeclarative、qtsvg、qtwayland、qtwebengineに加え、qtimageformatsを確認対象とした。QtPdfがあるためqtwebengineも含めるが、WebEngine機能の利用を意味しない。

Qt画像プラグインのソースattributionはLibTIFF 4.7.2とlibwebp 1.6.0を示す。Pillow由来LibTIFF 4.7.1の資料だけで代用しない。またQtディレクトリのICU 73.2ランタイムは[独立したソース補完](linux-almalinux9-icu-source-review_ja.md)で扱い、Chromium内の別版ソースとは区別した。ソースattributionの版はビルド時の内包・システム利用選択の証明とはしない。

## 収集した告知

収集済みQt 6.11.2アーカイブを読み、対象6モジュールのファイル名条件に該当する法的文書とattribution、明示的なLicenseFile参照先を集めた。計2,080文書を`Qt-source-notices.txt`（8,946,735バイト）に保存した。これはサンプルやChromium側の広い文書集合も含む資料で、実際のリンク対象だけの告知一覧ではない。

MuPDF 1.28.2ソースからは34文書を`MuPDF-source-notices.txt`（337,722バイト）に保存した。Droid/Han/Noto等のフォント文書も含め、ELF以外のデータに関する確認資料を確保した。全フォントが候補へ含まれるという主張ではない。

```text
/home/folimeld-build/folimeld-candidates/alma9-release-readiness-20261112/qt-mupdf-notice-review-02/
```

ソース内パス・サイズ・ハッシュは[収集JSON](linux-almalinux9-qt-mupdf-notice-review-2026-11-12.json)へ記録した。

## 未解析attributionの解消

先行目録のQt attributionには、文字列中の直接の改行によって通常のJSON解析が失敗したものがあった。対象モジュール内の5文書を`json.loads(strict=False)`で再解析し、8構成要素を取り出した。元の本文・目録は保持した。

これにより、当初の解析成功分には現れなかった次の参照先3件を特定した。

- `qtbase/src/3rdparty/libpsl/PSL-LICENSE.txt`
- `qtbase/src/3rdparty/sha3/BRG_ENDIAN_LICENSE`
- `qtbase/src/3rdparty/sha3/CC0_LICENSE`

3文書を同じQtソースアーカイブから追加抽出し、`Qt-additional-referenced-licenses.txt`へ保存した。選択したモジュールの、今回解析したattribution内の明示的LicenseFile参照は未収集0件となった。[再解析JSON](linux-almalinux9-qt-attribution-resolution-2026-11-12.json)と[追加3文書JSON](linux-almalinux9-qt-extra-licenses-2026-11-12.json)を参照。

元の収集JSONの`qt_runtime_attribution_records: 87`には、当時未解析だった5文書のプレースホルダーも含まれる。87件の実ランタイム使用が確認されたという意味ではない。最初の抽出は`data`キーのない項目で停止したため、新規ディレクトリで未解析状態を保持して再実行し、後続で解消した。

## 残る反映と確認

現revision2とそのstagingは保持したまま。追加資料はまだ候補・別添目録へ反映していない。次はQtPdf/PDFium・Chromiumの実ビルド選択と生成告知、MuPDFの実内包コード・フォントと告知の対応を確認し、ICUも含めて次候補へまとめて反映する。

明示参照の収集完了は、すべての内包第三者コード、変更パッチ、必要告知を網羅したという認定ではない。Qt/MuPDFのソース・告知が存在することと、wheelの過去ビルド来歴の証明を区別する。公開は行っていない。
