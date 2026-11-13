# Ubuntu ARM64 strict Snap 0.3.5の検証

2026-11-13。先行DEBの公開後全添付照合・main反映・X案内完了後、Snap固有の新規検証を実施。DEBやamd64の合格結果はSnap受入に数えていない。

本体のビルドソースは `a77ad2f426f23f8dd0245e04f94674cccb71694a`（未コミット差分なし）。正確なソースZIPのSHA-256は `6cce8f6ec446a467ef67e099832077894f3236b9579c76703232b76844b7c96a`、968入力をGit・ZIP・埋込マニフェストで照合。タグには後続の検証資料追加も含むので正確な本体ソースは添付ZIPを使用する。

`folimeld_0.3.5_arm64.snap` はSHA-256 `8a7bb4ac42934d038e830935798dce33e238cfde0dea1051dc54cbae9d369f2c`、内部ELFは `637f450800945fc53bb4541c422509689603653ed15e437af6a626407f5f647c`。同一Ubuntu ARM64 VMの未使用ビルド先2件でSnapのバイト一致。独立ホスト2台の結果とはしない。Ubuntu ARM64の単体テスト409 passed、9 skipped、67 subtests、ruff成功。

OS更新・再起動後のUbuntu24.04.5 ARM64/HVF、一般ユーザーXorg/Openboxで回転の即時表示・Undo/Redo・ページ移動・白紙挿入/削除・別名保存・日本語名再読込・画像変換/保存・正常終了を確認。0.3.4+fix1 x6→0.3.5 x7更新、同じ候補x7→x8再導入でDocuments/common/current設定の全件ハッシュ保持。再導入後の画像PDF再読込・正常終了も成功。3起動すべて終了0、後刻の残存プロセスなし。保存PDFの順序2→1→3、回転0→90→0、画像画素と元PNGの一致を検査。

実行中と再導入後にAppArmor `snap.folimeld.folimeld (enforce)`、Seccomp2/2フィルターを記録。removable-mediaは未接続。同一プロファイルのsnap run --shellで通常Documentsの読込成功、合成の隠しホームと/mntファイルは拒否、カーネル監査にDENIEDを記録。GUIプロセスの制限状態は別途確認しており、この限定的な読込試験を包括的な安全性認定に広げない。

内部210ネイティブ実体・外側11実体（symlinkを含む22パス）は全件AArch64で、対応確認済みARM64 fix1とバイト一致。外側差分は本体・版・配布説明、今回の告知追加。元告知とcommand chainは保持し、ブートローダー元ELFセクションも公式wheelと一致。共通第三者ソースTAR・Pillow補足・Ubuntuソース補足・今回の告知TARと対応表を公開する。履歴のNOT INCLUDEDは外部対応資料で解決。core24/gnome-46-2404/mesa-2404/gtk-common-themes等は別のsnapd提供ランタイムとして、検証時の版・ローカルSHA-256・接続を証跡に記録した。

GitHubからローカル導入するSnapでStore署名はない。--dangerousでもstrict制限を実測。完全削除再導入・revert・snapshot復旧、IME、暗号化/フォームGUI、GNOME/Wayland、実機ARM等は今回未試験。日本語名コピーはシェルで作成した再読込試験で、IMEや日本語Save Asではない。portal/compose/fitz警告、cgroup cpu.max読込拒否は残るが、対象の操作は完了した。

更新前と再導入前にユーザーデータTARとsnap saveを作成。snapdの保持規則により古い無効リビジョンは整理されたが、旧公開Snap原本・元外付けVM・試験前の設定退避を保持している。元Git作業ツリーの差分は0、専用ブランチで作業。2台のVMは内蔵ストレージ上でのみ実行し、通常停止。VM/ISOの削除・外付け起動は0件。

[検証JSON](linux-snap-arm64-035-verification-2026-11-13.json) / [対応表](linux-snap-arm64-035-native-provenance-2026-11-13.json) / [公開対象16点](linux-snap-arm64-035-release-assets-2026-11-13.json)。公開・全添付再取得・Xの結果はmainの公開記録へ追記する。
