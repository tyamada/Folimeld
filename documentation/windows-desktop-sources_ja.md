# Desktop版：版別対応ソースの提供案（未承認）

[English](windows-desktop-sources.md)

Desktopの数値版・最終基点コミット・公開先は未確定です。これは公開済み配布リンクでも最終ライセンス承認でもありません。uv版の開発は中止のまま、Store版の対応ソース案内を置き換えません。

## 版ごとに結び付けるもの

- アプリ対応ソース：確定コミット、AGPL原文、Desktop spec/iss/入口、版情報、固定runtime/tools/CRT/Inno入力台帳と必要な生成/ビルド手順。
- 第三者対応ソース：実採用版のQt/PySide・Python・Pillow・MuPDF等のソース、内包成分、適用変更/パッチ・必要な生成入力/手順と原文告知。親パッケージURLだけで完了としない。
- 対応台帳：Desktop数値版・コミット・各ソース/入力のサイズとSHA-256。生成後には全payload・setupとの対応も記録する。
- 公開時のファイル一覧・SHA256SUMS：未作成。版を確定し、完成した資料を点検してから配布ファイル名とURLを決める。

## Tika/Qt MIMEデータの統合

[Desktop最終告知の下書き](windows-desktop-licenses/THIRD-PARTY-NOTICES.draft.txt)へ[部品告知](windows-desktop-licenses/TIKA-PRONOM-NOTICE.draft.txt)を統合しました。PRONOM/TNA/OGL表示、Tika/ASF・IPTCの範囲説明、MIME情報のIan F. Darwin由来BSD原文を含みます。アプリ全体へ第三者条件を一括適用しません。

[補足集合](windows-desktop-licenses/tika-source-delivery/README.txt)と[19ファイルの台帳](windows-desktop-licenses/tika-source-delivery/SOURCE-SET.draft.json)を本案内へ結び付けました。固定Tika原XML、Qt6.11.2加工XML/補助スクリプト/attribution/REUSE、差分、原文・参照資料・告知を保持しています。補足だけで全Qt対応ソースが完成したとは扱いません。

Qt本体の既存ソース入力:
`qt-everywhere-src-6.11.2.tar.xz`
SHA256: `6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33`

PySide/Shibokenの既存ソース入力:
`pyside-setup-everywhere-src-6.11.2.tar.xz`
SHA256: `cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8`

[由来・ソース台帳](windows-desktop-licenses/DEPENDENCY-SOURCES.draft.json)に、告知ハッシュ・補足manifestハッシュ・wheelとの固定対応と、版/公開先未確定を記録しています。

## Qt wheelとの対応と未確認事項

固定wheel4件のSHA・版6.11.2を静的照合。PySide系3件のconfigは59モジュールを宣言し、Desktop許可7モジュールのQt DLLは入力に存在します。これらは最終payloadの収録数/有効機能ではありません。glueソース27件は配布ソースと改行正規化後一致（生バイト一致0件、本文の差はCRLF/LF）。Qt DLL全体の未変更証明ではありません。

今回の4wheelにSBOM/SPDX/CycloneDX名のファイルは見つかりませんでした。PySideソース内の.patch/.diff名も0件ですが、これだけで上流Qtビルドの追加変更なしとは扱いません。configのbuild_dateは自己記録、Qt6.11.2.0というPE値は版情報として区別します。

## 初回ビルド前と後の境界

初回onedir前：残るQt wheel固有構成・追加変更と提供ソースの根拠、Pillow/MuPDF/CRT等の資料、版・署名方針・最終告知とソース索引を点検。資料が完成してからreviewed-files.jsonを作成します。現在は未作成。
onedir後・Inno前：実payload全件・同梱告知・実版・ソース対応を照合し、payload点検台帳を作成します。未生成payloadを初回onedir前の条件にはしません。
再現性の別調査：上流compiler/SDK/全生成環境、加工データの再生成一致、完全なQt DLL/wheelバイト再現性。必要な変更/ソースの具体的不足は、この別枠へ棚上げしません。

ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較は未実施。新規課金・モデル呼出なし。

許可Qt DLL7件とqwindows/qjpegの合計9ネイティブをPE静的点検し、全件x64・版6.11.2.0、通常/遅延importに許可外Qt依存なしを確認しました。動的読込や実収集の成功は未確認です。
