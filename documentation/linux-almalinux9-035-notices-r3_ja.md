# AlmaLinux 9の補足資料入り0.3.5 revision3候補

2026-11-12。[ICUソース補完](linux-almalinux9-icu-source-review_ja.md)、[Qt/MuPDF告知収集](linux-almalinux9-qt-mupdf-notice-review_ja.md)、[MuPDF実体・フォント照合](linux-almalinux9-mupdf-runtime-review_ja.md)をまとめて新規候補へ反映した。未公開の専用コピーであり、元作業ツリーの版は0.3.3のまま。

## 反映とビルド

```text
/home/folimeld-build/folimeld-candidates/alma9-035-notices-r3-20261112/
packages/folimeld-0.3.5-3.alma9_8.x86_64.rpm
RPM SHA-256: 6a79478fb4485de0deaf126bbfed86d9cf003065a2c372e6a825937dbf4c6d69
ELF SHA-256: 026ceba16663ab58d62afed6f5a3fdfec41d0f59841665f05f6420dbf1fb5dbd
```

revision2を保持して新規コピーを作り、ICU-73.2、Qt-source-notices、Qt-additional-referenced-licenses、MuPDF-source-noticesの4文書を追加した。Qtの文書集合は実使用が確定した成分だけの一覧ではなく、広いソース告知資料であることを冒頭に明記した。

別添にはICUソース・チェックサム・署名、Qt/MuPDF告知と参照解消記録、MuPDFランタイム確認記録を追加し、全162ファイルを目録化した。ICUの署名未検証、wheelの完全な過去入力・ビルド選択が未確定であることは保持した。

ライセンス・ソース・Alma RPMの15テストと9サブテスト、アイコン生成、PyInstaller、RPM生成が成功。全対応ソース683入力、追加告知4文書、別添162ファイルを照合した。全`folimeld/`入力と210ネイティブ実体はrevision2からバイト不変で、Virtual Keyboard関連は0件。[ビルド検証JSON](linux-almalinux9-035-notices-r3-verification-2026-11-12.json)を参照。

## 更新・起動と準備物

専用Testでrevision2からrevision3へ更新し、ELF一致、rpm -V、dnf checkが成功した。一般ユーザーの新規プロフィールでoffscreen・xcb各12秒の起動が成功し、試験プロセスを終了した。[更新・起動JSON](linux-almalinux9-035-notices-r3-update-2026-11-12.json)に記録した。主要機能を全件再試験したという結果ではない。

既存stagingとstaging-r2は保持し、新規`alma9-release-readiness-20261112/staging-r3/`へRPM・対応ソース・告知・依存資料等11添付物とSHA256SUMS.txtを用意した。162資料をアーカイブから再照合し、標準sha256sumも11件成功。日英公開稿の導入例をrevision3の実RPM名へ合わせ、チェックサムを再生成して再照合した。[準備物JSON](linux-almalinux9-release-r3-staging-2026-11-12.json)を参照。

## 次の確認

後続で[補足告知4タブの実表示・Qt大文書のスクロール・PDF画面への復帰](linux-almalinux9-035-notices-r3-license_ja.md)を確認した。以下のライセンス画面確認は完了し、残項目は同記録へ整理した。

新候補で4補足文書のライセンス画面表示・操作性を確認する。QtPdf/PDFiumの生成告知と実ビルド選択、全内包成分・必要告知の対応確認は未完了。広いソース告知集合の追加を、これらがすべて証明されたという意味では扱わない。版確定・公開用ソースの最終統合も残る。公開・コミット・タグ作成は行っていない。
