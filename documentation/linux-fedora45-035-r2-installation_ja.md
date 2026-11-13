# Fedora 45 revision2の再導入・最小依存確認

2026-11-13。許可済み専用 `Folimeld-Fedora45-Amd64-Test` 内だけで実施した。[revision2候補](linux-fedora45-035-r2_ja.md)は未公開。

## 削除・再導入

インストール済みRPMの検証と `dnf check` の成功後、依存の自動削除を抑止してFolimeldだけを削除した。実行ファイル・desktop entry・アイコン・LICENSEの4ファイルと、RPM登録が消えたことを確認し、保持した同一RPMを再導入した。

4ファイルはすべて削除前と同じSHA-256に復元された。前回GUI試験のPDFと設定ファイル6件は削除前・削除後・再導入後の全段階で不変だった。最後の `rpm -V` と `dnf check` も成功した。

再導入後は一般ユーザーの新規プロファイルでoffscreen・xcbを各12秒起動し、試験のため停止した。実行ELFは `a87ae589b6d5dad22ea7d2a246d0764ec360b2439c47768a17970cc83da5680f`。既存GUIツール入り環境での再導入結果であり、次の最小依存試験とは区別する。

[ライフサイクル記録](linux-fedora45-035-r2-lifecycle-2026-11-13.json)にコマンド・ログ・保持ファイルのハッシュを収録した。

## 新規installroot

専用Test内の新規 `/root/folimeld-verification/version035-r2-minroot-20261113/root` に、DNF5の `--installroot`・`--use-host-config`・`--releasever=45` を使って導入した。標準fedora/updatesリポジトリとFedora45鍵による署名確認を使用し、weak dependenciesは無効化した。鍵とRPMデータベースはこの新規root内に用意し、既存のグローバル設定・信頼鍵は変更していない。

Python、pip、GCC、rpm-build、EPEL、追加CJKフォントが入っていないことをパッケージ一覧で確認した。UID/GID1000の一般ユーザーとしてoffscreenで12秒起動し、試験のため停止した。ELFハッシュ一致、`rpm -V`、`dnf check` も成功した。

デバイスノードとユーザー用ディレクトリは新規root内だけに作成した。マウントや新規WSL登録はしていない。この確認はchroot/offscreenであり、完全なWSLブート・GUIデスクトップ・最小環境の日本語描画を保証する試験ではない。

[最小依存記録](linux-fedora45-035-r2-minroot-2026-11-13.json)に全パッケージ・導入ログ・起動環境・終了結果を保存した。既存のWSL設定警告とPyMuPDFの非推奨警告は隠さず保持した。
