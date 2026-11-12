# Fedora 45 amd64試験版の公開前レビュー

後続の[公開結果](linux-fedora45-publication-result_ja.md)：ユーザーの明示許可を受けてFedora試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。Fedora向け0.3.5 revision2のローカル準備を完了した。初回の「公開はまだ実行しない」という制約は解除されていないため、Fedoraのpush・タグ作成・GitHub Release公開は未実施。

## 固定したソース

専用コピー `/home/folimeld-build/folimeld-candidates/fedora45-release-tree-20261113/source` のローカルブランチ `release/fedora45-amd64-0.3.5` に固定した。

| 項目 | 値 |
| --- | --- |
| ローカルコミット | `74366ba8a74a8efe65773ffd660e0fff42445f38` |
| ツリー | `d22f09c7c27e66b300bca11a39bbf58fc919dbd2` |
| 親main | `d1407b3efec245babfc8d462f2b3aedf966b413f` |
| 一致したビルド入力 | 785件 |
| 保持した親ツリーの追加パス | 48件 |
| 追跡ファイルの削除 | 0件 |

内容変更14件、改行のみ46件、追加318件を分類した。READMEの日英本文は親mainと同じで、CHANGELOGには日英同内容のFedora候補準備行を追加してある。版0.3.5/build1、Linuxビルド・サムネイル・告知修正、Fedora固有の暗号依存記録と生成アイコンは、この専用スナップショットに限定する。mainへの一括マージ案ではない。

Gitへは改行フィルターを通さず候補の生バイトを登録し、全785入力をコミットから読み戻して照合した。既存シェルスクリプトの実行属性も保持した。バイナリ作成後に固定したコミットであり、埋め込みのビルド時メタデータは書き換えていない。[ツリー](linux-fedora45-release-tree-2026-11-13.json)、[差分分類](linux-fedora45-release-tree-classification-2026-11-13.json)、[コミット](linux-fedora45-release-commit-2026-11-13.json)を参照。

親mainを必要とする増分bundleも生成・検証した。6,738,425バイト、SHA-256は `dff1f9f45593902eaebb6c472804bee850b0ebb4cc2f36be8275c8cdf789d52f`。[bundle記録](linux-fedora45-release-bundle-2026-11-13.json)を参照。これは内部転送用で、公開添付11件には含めない。

## 公開候補パケット

```text
/home/folimeld-build/folimeld-candidates/fedora45-r2-readiness-20261113/publication-packet-r2/
```

11ファイル、合計1,922,302,300バイト。RPM、対応ソースZIP、対応記録JSON、依存ソース別添tarと目録、第三者告知tar.gz、検証要約JSON、検証記録ZIP、日英RELEASE-NOTES、KNOWN-LIMITATIONS、SHA256SUMSを含む。検証記録ZIPの68ファイルと告知アーカイブは再読込して元データと一致を確認し、全添付のチェックサム検査も成功した。

[日本語案内](linux-fedora45-publication-body_ja.md)と[英語案内](linux-fedora45-publication-body.md)の検証範囲・制限・導入コマンド・コミットは一致している。RPM・チェックサム・コミットが未署名であること、通常デスクトップ・Fedora44・ARM64等へ結果を拡張しないこと、最小installrootと完全GUI環境の違い、過去ビルド由来を完全再構成したものではないことを案内へ記載した。

公開設定案は `fedora45-amd64-v0.3.5`、prerelease=true、make_latest=false。既存Linux0.3.4・AlmaLinux試験版と他OSの配布物、元mainの作業ツリー・index・refsは保持する。[全11添付のハッシュと公開計画](linux-fedora45-publication-plan-2026-11-13.json)を参照。

## 公開直前の確認

[公開GitHubの読取確認](linux-fedora45-publication-remote-check-2026-11-13.json)では、mainは上記の親と一致し、Fedora用ブランチ・タグは存在しなかった。latestは既存Linux0.3.4だった。これは公開情報の事前確認である。実行許可後、認証付きでdraft/release・ブランチ・タグの競合と全パケットハッシュを再確認してから、専用ブランチとタグ、11添付の試験版だけを公開する。

技術検証は[到達点記録](linux-fedora45-035-r2-readiness_ja.md)を参照。公開案内・Gitスナップショットの準備まで完了し、残る判断はこのFedora試験版の公開可否である。
