# Tika統合とQt wheel固有構成・変更の静的点検

2026-11-16。最終配布用資料の下書きへ統合した段階で、ライセンス承認・初回ビルド許可・公開ではありません。

## 統合結果

- [Desktop最終告知下書き](windows-desktop-licenses/THIRD-PARTY-NOTICES.draft.txt)へ、現行Tika部品告知を原文のまま1回統合しました。PRONOM/OGL、元Tika/ASF謝辞、MIME固有BSD、IPTC範囲説明を保持。
- 版別ソース案内を[日本語](windows-desktop-sources_ja.md)と[English](windows-desktop-sources.md)で整備。Tika補足19ファイルの台帳、完全なQt/PySideソース入力の版/ハッシュ、アプリ/第三者/生成後payloadとの対応工程を案内。
- [由来・ソース台帳](windows-desktop-licenses/DEPENDENCY-SOURCES.draft.json)に告知ハッシュ、補足manifestハッシュと全件サイズ/SHA一致、固定4wheelとの対応を記録。Desktop版・最終コミット・公開先は未確定としてnullを維持し、既存Store/uv版を転用しません。
- ソース台帳に残った古い「uv名入力を分離する」「工具未準備」等は歴史記録へ残し、最新の実装済み状態と実際の残件へ更新しました。設定や工具は追加変更していません。

## Qt wheelとの具体的対応

| 対象 | 確認結果 | 限界 |
|---|---|---|
| PySide/PySide Essentials/Addons/Shiboken4wheel | 固定SHA256再照合、config版6.11.2とsoversion6.11を確認。 | 版一致は全ソース/パッチの証明ではない。 |
| config | PySide系3件は59モジュールを宣言。生成テンプレートの元ソースを保管。build_dateは2026-08-14、Shibokenと他は秒部分が異なる自己記録。 | 59はwrapper側宣言で、Qt configure全フラグでもDesktop収録数でもない。 |
| Desktop許可7モジュール | 対応DLLは入力に存在。qwindows/qjpegも含む9ネイティブの通常/遅延PE importは許可外Qt依存なし。全件x64・版6.11.2.0。 | 静的import検査は動的機能・実COLLECT・実ロードの検証ではない。 |
| wheel内glueソース27件 | PySide6.11.2ソースの全27件と改行正規化後一致。生バイト一致は0で、CRLF/LF差を記録。 | Qt DLL実装の差分/未変更証明へ拡張しない。 |
| ソース内patch/diffとwheel SBOM | PySideソースの.patch/.diff名は0、4wheelのSBOM/SPDX/CycloneDX名も0。 | 名前による探索範囲。追加変更が存在しない証明ではない。Qt全ソース内のpatch在庫とは別。 |
| Tikaの変更 | 固定元XML・Qt加工版・加工原本・差分が補足集合に統合済み。 | 実QtCore埋込データの完全同一性は未確認。 |

configはASTの定数/文字列だけを読み、DLLやPython設定をimport実行していません。静的解析の実行にFolimeldのビルド入口は使っていません。

## 初回onedirビルド前の残件

1. Qt wheel固有の有効configure設定・追加変更と、提供するQt/PySideソース・必要手順の根拠を補う。今回の27glue/版/PE情報だけで未変更と確定しない。
2. Pillow/MuPDF/CRT/Python等の未完資料を含め、最終告知・全対応ソース索引の点検を終える。Tikaの補足19件が全依存/全Qtの代替になるわけではない。
3. Desktop数値版・最終基点コミット・版情報・署名方針を確定し、アプリ対応ソース/第三者資料の提供計画へ結び付ける。URLや公開済みZIPを捏造しない。
4. 完了後にのみ点検済みライセンス台帳を作る。現時点はreviewed-files.json未作成。実payloadの一致確認は別途承認後のonedir生成→Inno前の工程。

## 再現性として別に残すもの

上流compiler/SDK/全生成環境、Qt加工処理の再生成一致、最終DLL/全wheelのバイト再生成。未確定の具体的なパッチ/ソース不足そのものはこの別枠へ棚上げしません。初回ビルド前の資料点検と上流全バイト再現の達成を同一条件にしません。

uv開発中止を維持。新規課金・モデル要求・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。PREBUILD-DRAFT-NOT-APPROVEDを維持。変更は資料のみ。
