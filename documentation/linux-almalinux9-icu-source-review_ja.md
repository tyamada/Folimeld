# AlmaLinux 9候補のQt同梱ICUソース補完

2026-11-12。[revision2公開準備](linux-almalinux9-release-readiness_ja.md)に続き、Qt側の外部ランタイムを調べた。

## 見つかった不足

候補にはPySide6のQtディレクトリ由来の`libicudata.so.73`、`libicui18n.so.73`、`libicuuc.so.73`がある。3実体は固定ビルド環境とバイト一致し、`u_getVersion_73`による実ランタイム版は73.2.0.0だった。これまでの別添149ファイルには、独立したICU 73.2ソースがなかった。QtWebEngine内の別版ICUソースを代用しない。

## 追加取得と照合

[Unicode公式ICU 73.2リリース](https://github.com/unicode-org/icu/releases/tag/release-73-2)から`icu4c-73_2-src.tgz`、`SHASUM512.txt`と両者の署名ファイルを新規専用資料ディレクトリへ取得した。

```text
/home/folimeld-build/folimeld-candidates/alma9-release-readiness-20261112/icu73-source-review/
```

ソースのSHA-512は公式チェックサムと一致し、ソース内`uvernum.h`の版は73.2。アーカイブの`icu/LICENSE`全文を補足告知`ICU-73.2.txt`として保存した。現revision2の全`licenses/*.txt`には、このLICENSE全文と空白正規化後に一致するものは見つからなかった。

ソース版、実体ハッシュ、取得先、サイズ、SHA-256/SHA-512、告知ハッシュは[検証JSON](linux-almalinux9-icu-source-review-2026-11-12.json)へ記録した。公式HTTPSで取得したチェックサムとの一致であり、独立した署名検証ではない。署名ファイルは保存済みだが、OpenPGP署名は未検証。

## 次候補への反映

現revision2とその配布準備物は変更していない。Qt/MuPDFの追加告知確認をまとめてから、ICUソース・告知を次候補と別添目録へ反映する。実ランタイムとソースの版一致は、wheelの過去のコンパイラー・パッチ・ビルドフラグの完全な証明とは区別する。
