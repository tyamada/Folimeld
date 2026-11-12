# AlmaLinux 9 amd64向け0.3.5試験版の公開結果

2026-11-12、ユーザーの明示許可後に公開した。公開日時は13:10:25 UTC、日本時間22:10:25。

**[Folimeld 0.3.5 — AlmaLinux 9 amd64 preview](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.5)**

## 公開した対象

- 試験版（prerelease）。latestへの指定なし。
- 専用ブランチ`release/almalinux9-amd64-0.3.5`と注釈付きタグ`almalinux9-amd64-v0.3.5`。
- 対象コミット`03b14ec8c4410fbc7510aa9bedb27950e78cfc6e`、ツリー`b6c719a04ab38ec9befb2ec61db7c37851f744bb`。
- RPM`folimeld-0.3.5-5.alma9_8.x86_64.rpm`、対応ソース、依存ソース資料、告知、検証要約、既知の制約、日英本文、チェックサム等12添付物。

RPM SHA-256は`0ba2c7dfc397f61b1ca70679838c93589310d116a267249d67dd822b8cb654bc`、対応ソースSHA-256は`f9a6add8b239c0da7f563128242023d880077f89e565cd38eb6ff2c51af4c079`。AlmaLinux9.8 WSL2/WSLgでの限定検証と、未署名・ビルド来歴等の限界を日英本文とKNOWN-LIMITATIONS.txtへ保持した。

## 実施と公開後確認

GitHub接続ツールにはリリース作成・大容量添付機能がなかったため、既存Git認証とGitHub APIを利用した。認証値は表示・保存していない。専用ブランチとタグを明示したGitHub URLへatomic pushし、元リポジトリを指すoriginへのpushは行わなかった。

下書きリリースに全12件をアップロードし、GitHub側のサイズ・SHA-256が計画と一致した後で公開した。公開後に認証なしでリリースを取得し、12件の状態・サイズ・ハッシュを再照合。SHA256SUMS.txtは実際の公開ダウンロードURLから取得して照合した。タグ・ブランチが同じ対象コミットを指すことと、prereleaseでlatestではないことも確認した。

元Windows側はmain、HEAD423e594のまま、既存の未コミット変更を保持した。既存配布物の移動・削除・置換や、main・既存タグへの書き込みは行っていない。

実行結果と各ダウンロードURLは[公開結果JSON](linux-almalinux9-publication-result-2026-11-12.json)、認証なしの確認は[公開後検証JSON](linux-almalinux9-publication-public-verification-2026-11-12.json)を参照。

準備時点の計画・許可待ち文書にある`published: false`等は当時の履歴。現時点の公開状態は本記録と公開後検証JSONを正とする。
