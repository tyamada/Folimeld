# Linux DEB amd64 0.3.5 公開前レビュー

2026-11-13。公開前の確認記録。後続の明示承認を受けて公開済み。公開確定内容は[計画JSON](linux-deb-amd64-publication-plan-2026-11-13.json)、検証結果は[JSON](linux-deb-amd64-035-r1-verification-2026-11-13.json)、案内は[日本語](linux-deb-amd64-publication-body_ja.md) / [English](linux-deb-amd64-publication-body.md)。

- 優先順位はLeap16.1、Tumbleweed20261110、共通DEB。前2件は公開・ソースpush・X案内まで完了した。次の対象が本DEB。
- 専用Ubuntuビルドコピーのみ0.3.5へ更新。固定ビルドvenvは前後一致。409テスト・67サブテスト成功、9スキップ、ruff成功。
- コミット24265ed9bb9c312921faac4b952ce27729639ad3、ソース870入力をZIP・組込み記録・Git内容でバイト照合。元作業ツリーの版と既存7実装変更は保持した。
- DEB SHA-256: 573f72f323097d398d245218eda454037fdc5e74a4d6865bd085bd5955ecc3f7。
- 実ネイティブ214項目（wheel105/OS109）、Ubuntu対応ソース61件、PyInstaller公式ブートローダーを確認。公式現行/Snapshotの署名付き53 SourcesインデックスをInReleaseからSHA-256照合。依存ソースは1,421,547,520バイトと659,783,680バイトの2分冊。
- Ubuntu24.04.4・Debian13.6・KaliRolling2026.3の専用Testで更新、削除再導入、offscreen/xcb一般ユーザー各12秒、dpkg/APT整合性、既存試験PDF/設定保持が成功。3環境の実画面で日本語PDF・回転・Undoを確認。
- Ubuntu実画面でRedo・移動・白紙挿入削除・日本語/空白名保存・再読込を確認。保存データは3ページ・順[2,1,3]・回転[0,90,0]・日本語保持。
- 公式noble main/universeから作成した最小chrootで、Python/開発依存/推奨CJKフォントなし、UID/GID1000 offscreen15秒が成功。初回はuniverse未設定でlibxcb-cursor0を解決できず、専用root内だけへ公式universeを加えた再試験が成功。ログを保持。
- 最初の共有パス転送はアクセス拒否、転送完了前のAPT試験は未対応ファイルとして失敗した。転送完了後に独立の再試験先で成功。シェル引用不備・試験用システムPythonのfitz不足も失敗ログとして区別し、保存PDFのデータ照合は固定ビルドPythonで成功した。
- 今回のDEBではIME/GIO/暗号化PDF/画像取込の実画面再試験を実施していない。RPMの合格を流用せず、日英案内・制約に明記した。通常デスクトップ/ARM64/将来rolling更新は対象外。
- 12添付の合計は2,218,206,851バイト。各添付は2GiB未満。ソースブランチrelease/deb-amd64-0.3.5、タグlinux-deb-amd64-v0.3.5。安定版latestは維持する。

自動承認レビューは、DEB固有の確定12添付・ブランチ・タグに対するユーザーの明示承認が未確認であることを理由に公開実行を拒否した。公開処理は実行されておらず、具体的な内容への承認を依頼済み。承認後に公開・全添付照合・X案内へ進む。

2026-11-13追記: ユーザーが確定12添付・約2.22GBと専用ソースブランチ・タグの公開を明示承認した。確定payloadを変更せず公開処理を再開した。

[公開結果](linux-deb-amd64-publication-result_ja.md): 12添付・ブランチ・タグを公開後照合済み。既存Release・latestは不変。
