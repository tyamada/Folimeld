# AlmaLinux 9 amd64試験版の公開判断用一式

後続でユーザーの明示許可を受け、[試験版の公開と公開後検証](linux-almalinux9-publication-result_ja.md)まで完了した。以下は許可前の判断資料として保持する。

2026-11-12。固定候補を変更せず、公開する場合の本文・対象・添付物をローカルに用意した。公開・push・タグ作成はまだ行っていない。

## 公開操作の具体案

| 項目 | 内容 |
| --- | --- |
| リポジトリ | tyamada/Folimeld |
| 専用ブランチ | release/almalinux9-amd64-0.3.5 |
| 対象コミット | 03b14ec8c4410fbc7510aa9bedb27950e78cfc6e |
| タグ | almalinux9-amd64-v0.3.5 |
| リリース | AlmaLinux9 amd64向け0.3.5の試験版（prerelease） |
| latest指定 | しない |
| 添付物 | 12件、チェックサムを含む |

元main、既存Linux0.3.4、他OSの配布物は変更しない。専用コピーのoriginは元Windowsリポジトリを指すため、公開時に無条件の`git push origin`は使わず、承認されたGitHub URLを明示する。

## 本文と添付物

利用者向け本文は[日本語](linux-almalinux9-publication-body_ja.md)と[英語](linux-almalinux9-publication-body.md)。Alma9.8 WSL2/WSLgの限定検証、未検証のデスクトップ等、未署名・過去ビルド来歴の限界を同じ順序で記載した。公開済みと偽る説明は準備状態の記録に使わず、実際に公開する場合の本文として分離した。

```text
/home/folimeld-build/folimeld-candidates/alma9-release-readiness-20261112/publication-packet-r5/
```

RPM、対応ソースと対応JSON、告知、依存ソース資料、libXau追加署名検証、公開用検証要約、日英リリース本文、KNOWN-LIMITATIONS.txt、SHA256SUMS.txtを収録した。内部準備状態JSONと旧版の公開稿はstagingに保持し、この公開予定パケットへは混ぜていない。既知の未検証事項を隠すためではなく、KNOWN-LIMITATIONS.txtと検証要約へ明示して引き継いだ。

全12添付物のファイル名・サイズ・ハッシュ、対象コミット・公開方法は[公開計画JSON](linux-almalinux9-publication-plan-2026-11-12.json)に固定した。チェックサム対象11ファイルは標準sha256sumで全件一致し、チェックサムファイル自身のハッシュも計画JSONへ記録した。

## 公開先の読み取り確認

予定タグに一致する参照は0件、確認したリリース一覧100件以内に同名リリースは0件。親コミット423e594が公開先にあることも確認した。[読み取り確認JSON](linux-almalinux9-publication-remote-check-2026-11-12.json)を参照。これは準備時点の結果のため、許可後に書き込む直前にも再検査する。

## 許可が必要な境界

元のユーザー指示は「ファイル移動・削除・公開はまだ実行しない」。専用環境・コピー内の許可に基づく準備は行ったが、GitHubへのpush、タグ作成、試験版と添付物の公開はまだ許可範囲に入れていない。これらの具体的な公開操作へ進むには、その指示を解除する明示の許可が必要。

公開対象は試験版であり、全ライセンス条件への適合認定や全環境での動作保証を求める確認ではない。過去ビルド設定の独立再構成等は未完了として保持する。候補の技術検査・添付資料とその限界を確認できる形にして、公開の可否を判断する。
