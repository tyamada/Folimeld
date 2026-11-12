# Fedora 44 amd64試験版の公開前レビュー

後続の[公開結果](linux-fedora44-publication-result_ja.md)：ユーザーの明示許可を受けてFedora44試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。Fedora44向け0.3.5 revision2の技術検証、対応ソース、専用Gitスナップショット、日英案内と公開パケットを準備した。Fedora44の公開許可はまだ受けておらず、push・タグ・Release公開は未実施。

## 固定したソース

| 項目 | 値 |
| --- | --- |
| 専用ローカルブランチ | `release/fedora44-amd64-0.3.5` |
| コミット | `293da8abe0459eba5d2a95609a6c3d630c986033` |
| ツリー | `a42e63b91a2a3629cf4270a9776250942948d0b3` |
| 親main | `ea3f5f13d5c57e70e1d7a912c5eca9361ca0b272` |
| 一致したビルド入力 | 822件 |
| 保持した親の追加パス | 48件 |
| 追跡ファイルの削除 | 0件 |

専用コピーは `/home/folimeld-build/folimeld-candidates/fedora44-release-tree-20261113/source`。内容変更14件・改行のみ46件・追加355件を分類した。日英README本文は親mainと同じで、日英CHANGELOGに同内容のFedora44候補準備行を追加している。生成アイコン・Fedora44固有告知・Linux修正はこのスナップショットに限定し、mainへの一括マージはしない。

全822入力をコミットから読み戻してハッシュ一致を確認し、既存スクリプトの実行属性と親の48パスも保持した。ビルド後のコミットであるため、埋め込みビルドメタデータや凍結したREADME/CHANGELOGの準備時状態は書き換えていない。[ツリー](linux-fedora44-release-tree-2026-11-13.json)、[差分分類](linux-fedora44-release-tree-classification-2026-11-13.json)、[コミット](linux-fedora44-release-commit-2026-11-13.json)を参照。

親mainを必要とする内部転送用bundleは7,062,177バイト、SHA-256は `0c9ea15e3957bb4c8a6ce3428c363c89cc9c5036ac2e6bb4dea769846e41c4a5`。[bundle記録](linux-fedora44-release-bundle-2026-11-13.json)を参照。これは公開添付に含めない。

## 検証と公開候補

[ビルド・更新](linux-fedora44-035-r2_ja.md)、[PDF回帰](linux-fedora44-035-r2-regression_ja.md)、[IME/GIO/ライセンス・導入回帰](linux-fedora44-035-r2-desktop_ja.md)、[配布実体・ソース監査](linux-fedora44-035-r2-source-audit_ja.md)を完了した。409テスト・67サブテスト成功、9件スキップ。207ネイティブ実体はwheel105・OS102へ照合し、Fedora44固有37 SRPMの署名確認と外部別添178項目の統合を完了した。

```text
/home/folimeld-build/folimeld-candidates/fedora44-r2-readiness-20261113/publication-packet-r2/
```

公開候補は11ファイル、合計1,869,377,074バイト。RPM、対応ソースZIP、対応記録JSON、依存ソース別添tarと目録、第三者告知tar.gz、検証要約JSON、検証記録ZIP、日英RELEASE-NOTES、KNOWN-LIMITATIONS、SHA256SUMSを含む。告知と検証記録ZIPは再読込照合し、全添付のチェックサム検査に成功した。検証記録ZIPには54ファイルを含め、初回revision1の告知不足検出記録も保持した。

[日本語公開案内](linux-fedora44-publication-body_ja.md)と[英語公開案内](linux-fedora44-publication-body.md)の導入コマンド・対象・制限・コミットは一致する。通常デスクトップ・ARM64等は対象外で、最小依存試験はchroot/offscreenの範囲。RPM・チェックサム・コミットは未署名。公式配布物との一致は過去ビルド設定の完全再構成やライセンス適合認定ではない。

公開案はタグ `fedora44-amd64-v0.3.5`、prerelease=true、make_latest=false。[公開計画と11添付のハッシュ](linux-fedora44-publication-plan-2026-11-13.json)を参照。既存Linux0.3.4・Fedora45試験版・AlmaLinux試験版と他OSの配布物、元mainと未コミット実装変更7件は保持する。

[公開GitHubの読取確認](linux-fedora44-publication-remote-check-2026-11-13.json)でmainは上記の親と一致し、Fedora44専用ブランチ・タグは存在しなかった。latestはLinux0.3.4。許可後は認証付きでdraft/release・ブランチ・タグの競合と全添付のハッシュを再確認してから公開する。

残る判断は、このFedora44試験版の公開可否である。Fedora45やAlmaLinuxの公開許可を流用せず、明示許可を待つ。
