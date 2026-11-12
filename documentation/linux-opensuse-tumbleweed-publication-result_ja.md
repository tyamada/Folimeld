# Tumbleweed 20261110 amd64試験版の公開結果

2026-11-13（日本時間）。ユーザーが確定済み11添付と専用ソースブランチ・タグの公開を承認した後、[Folimeld 0.3.5 revision1を公開した](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.5)。11添付を公開後にサイズ・SHA-256で照合し、既存Releaseの添付ID・サイズ・ハッシュとlatestが不変であることを確認した。

| 項目 | 結果 |
| --- | --- |
| 専用ブランチ | `release/opensuse-tumbleweed20261110-amd64-0.3.5`、push済み |
| タグ | `opensuse-tumbleweed20261110-amd64-v0.3.5`、push済み |
| コミット | `2f479d4cfa224be3aa8c25d51b8ec8583eecd073` |
| RPM | `folimeld-0.3.5-1.tw20261110.x86_64.rpm` |
| RPM SHA-256 | `7c0bc1b2301783acdf349d62fa1c18ae49c3c8bba6fb2963a3aefab3df6f8eea` |
| 対応ソース | 864入力のZIP・埋込記録・コミットのバイト一致 |
| ネイティブ実体 | 206件＝公式wheel105件＋OS101件、35 SRPM署名確認済み |
| 検証 | 409テスト・67サブテスト成功、9件スキップ |
| 公開添付 | 11件、合計1,825,967,363バイト |

主要GUI、更新・削除再導入・設定/PDF保持、新規最小installroot、正確なwheel/OSソース・ブートローダーの確認は[公開前確認](linux-opensuse-tumbleweed-publication-review_ja.md)に記録した。ビルド時の文書と「監査待ち」の埋込記録は凍結時点の履歴として保持し、完了した監査は外部添付で示している。

最小rootは通常のローリングリポジトリから作成したchroot/offscreen試験であり、20261110固定の独立WSLブートではない。通常デスクトップ・他スナップショット・ARM64・公開Ubuntu/Debian 0.3.4からの移行や広い入力条件は未検証。RPM・チェックサム・コミットは未署名。再現ビルドやライセンス適合認定ではない。

[日英公開案内](linux-opensuse-tumbleweed-publication-body_ja.md)、[検証JSON](linux-opensuse-tumbleweed-035-r1-verification-2026-11-13.json)、[公開計画](linux-opensuse-tumbleweed-publication-plan-2026-11-13.json)、[公開結果JSON](linux-opensuse-tumbleweed-publication-result-2026-11-13.json)を参照。

公開後、[X `tyamada22`への案内](https://x.com/tyamada22/status/2121020656238420066)も投稿し、タイムライン本文とURLで確認した。[各版のpush・案内確認記録](linux-amd64-publication-announcements_ja.md)を参照。
