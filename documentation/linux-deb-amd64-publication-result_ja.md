# Linux DEB amd64試験版の公開結果

2026-11-13（日本時間）。確定12添付と専用ブランチ・タグへのユーザーの明示承認後、[Folimeld 0.3.5 DEB試験版](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5)を公開した。公開後も12添付のサイズ・SHA-256を照合し、既存Releaseと安定版latestが不変であることを確認した。

| 項目 | 結果 |
| --- | --- |
| ソースブランチ | `release/deb-amd64-0.3.5`、push済み |
| タグ | `linux-deb-amd64-v0.3.5`、push済み |
| コミット | `24265ed9bb9c312921faac4b952ce27729639ad3` |
| DEB | `folimeld_0.3.5_amd64.deb` |
| DEB SHA-256 | `573f72f323097d398d245218eda454037fdc5e74a4d6865bd085bd5955ecc3f7` |
| 対応入力 | 870件、ZIP・埋込記録・Git内容のバイト一致 |
| ネイティブ | 214項目（公式wheel105、Ubuntu OS109）、対応Ubuntuソース61件 |
| 署名付きインデックス | Sources 53件のInRelease署名・SHA-256確認 |
| テスト | 409テスト・67サブテスト成功、9スキップ、ruff成功 |
| 公開添付 | 12件、合計2,218,206,851バイト |

Ubuntu24.04.4・Debian13.6・KaliRolling2026.3で更新・削除再導入・一般ユーザー起動・既存試験PDF/設定保持と日本語PDFの回転/Undoを確認。Ubuntuでは追加編集・日本語/空白名保存と再読込、最小chroot起動を確認した。このDEBではIME/GIO/画像/暗号化PDFの実画面を再試験していない。通常デスクトップ・ARM64・将来のrolling更新は未検証。パッケージ・チェックサム・コミットは未署名であり、再現可能ビルドや遵守認定ではない。

詳細は[公開前レビュー](linux-deb-amd64-publication-review_ja.md)、[日英案内](linux-deb-amd64-publication-body_ja.md)、[検証JSON](linux-deb-amd64-035-r1-verification-2026-11-13.json)、[確定計画](linux-deb-amd64-publication-plan-2026-11-13.json)、[公開結果JSON](linux-deb-amd64-publication-result-2026-11-13.json)を参照。

公開後、[X tyamada22への案内](https://x.com/tyamada22/status/2121026291403256241)を投稿し、タイムライン本文と投稿URLで確認した。
