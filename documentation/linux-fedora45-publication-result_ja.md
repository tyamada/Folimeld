# Fedora 45 amd64試験版の公開結果

2026-11-13の継続作業。ユーザーの明示許可後、[Fedora 45 amd64向けFolimeld 0.3.5試験版](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.5)を公開した。GitHubの公開時刻は `2026-11-12T20:47:02Z`（日本時間 `2026-11-13T05:47:02+09:00`）。

- 専用ブランチ：`release/fedora45-amd64-0.3.5`
- タグ：`fedora45-amd64-v0.3.5`
- コミット：`74366ba8a74a8efe65773ffd660e0fff42445f38`（ビルド入力785件と一致）
- 添付11件のサイズ・GitHub SHA-256 digestが公開計画と全件一致。
- 認証なしで試験版を取得でき、公開SHA256SUMSのダウンロードハッシュも一致。
- prerelease=true、make_latest=false。latestは既存Linux0.3.4のまま。
- 既存Linux0.3.4・AlmaLinux試験版のrelease IDと全asset ID・名前・サイズ・digestを公開前後で照合し、不変。
- 元mainのコミット・追跡変更一覧・差分ハッシュと、GitHub mainを公開前後で照合し、不変。

添付にはRPM、対応アプリソース、関連付けJSON、依存ソース別添と目録、第三者告知、検証要約・記録、日英案内、制限事項、チェックサムを含む。RPM・チェックサム・ソースコミットは未署名。対象はFedora45 x86_64の専用WSL2/WSLgで、他環境へ結果を拡張しない。

[公開許可](linux-fedora45-publication-approval_ja.md)、[公開計画](linux-fedora45-publication-plan-2026-11-13.json)、[公開実行記録](linux-fedora45-publication-result-2026-11-13.json)、[認証なしの公開検証](linux-fedora45-publication-public-verification-2026-11-13.json)を参照。

これ以前の準備資料や添付中のpublished=falseは、各資料を作成した時点の状態として保持する。今回の公開状態は本書と公開結果JSONを優先する。mainへのLinux実装統合・他ディストリビューションの公開は実施していない。
