# Ubuntu／Debian ARM64 DEB 0.3.5の検証

実施日: 2026-11-13。公開用の候補を固定し、既存のmain・作業候補・公開済みパッケージを保持した。

本体のビルド元は `7890a67ef893799ff614646646733b376dd43613`（差分なし）。正確なソースZIPのSHA-256は `b3bd9a9b25703c1573b34255d4f0ed514c6fa6b004a33dc203ba3e5458642a4b`。961入力をGit・ZIP・埋込記録で全件照合。タグには本記録等の追加資料が含まれるので、ソースZIPとタグの資料追加を区別する。

候補 `folimeld_0.3.5_arm64.deb` のSHA-256は `8be1d43bc227c9e7a38c346357670025925dcc6a6cd30d5b1f2155a59b158e18`、ELFは `4230a0fd5a919f3ea41bc3cc1d3fbfca0a10dc9a87b3fb4d2f1aa48d6f34f549`。同一Ubuntu ARM64 VMの別の未使用ビルド先2件でDEBバイト一致。独立VM2台の試験とは主張しない。

Ubuntu 24.04.5／Debian 13.7 ARM64の一般ユーザーXorg/Openboxで、回転の即時表示、Undo/Redo、ページ移動、白紙挿入・削除、別名保存、日本語名コピーの再読込、画像変換・保存・正常終了を今回実行。削除再導入・既存文書/設定の全件ハッシュ保持・再導入後の画像PDF再読込・正常終了も成功。GUI計6回すべて終了0、後刻のプロセス確認で残存なし。PDFは順序2→1→3、回転0→90→0、画像画素は元PNGと一致。日本語名のコピーはシェルで作成し、IME入力試験には数えない。

Ubuntu ARM64のpytestは409 passed、9 skipped、67 subtests passed、ruff成功。新規Ubuntu minbaseへ推奨依存なしで導入し、開発用PythonのないUID1000環境でoffscreen起動。15秒の意図した打切り124はGUI正常終了0と区別する。ビルドの最初の依存事前検査でlibEGL不足を検出し、公式libegl1/libgl1導入後に再実行した。

同梱210ネイティブファイルは全件AArch64で、対応資料確認済みARM64 fix1とバイト一致。175件の旧共通資料と更新35件/11公式Ubuntuバイナリ/8ソースの補足を継承し、今回の実行物から告知を抽出した。ブートローダー元セクションも公式wheelと全件バイト一致。履歴の埋込NOT INCLUDEDは外部の対応表・ソース一式で解決。amd64の合格結果をARM64受入に流用していない。

今回未再試験: 完全なGNOME/Wayland、実機ARM、IME、ファイルマネージャー関連付け、暗号化/フォームGUI、拡張ズーム等。PyMuPDF fitz警告は残る。glibc >=2.39が必要でUbuntu22.04には使用しない。

VMはMac内蔵ストレージ上でのみ実行。外付けChatGPT-Test上のアーカイブを直接起動せず、VM/ISOの削除もしていない。ビルド手順・証跡・既存公開物は保持。

[検証JSON](linux-deb-arm64-035-verification-2026-11-13.json) / [ネイティブ対応](linux-deb-arm64-035-native-provenance-2026-11-13.json) / [公開対象16点](linux-deb-arm64-035-release-assets-2026-11-13.json)。公開と再ダウンロードの結果はmain側の公開記録に追記する。
