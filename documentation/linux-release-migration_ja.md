# Linux配布物のGitHub Releases移行計画と実施記録

[日本語](linux-release-migration_ja.md) | [English](linux-release-migration.md)

実施日: 2026-11-04。[linux-v0.3.3](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)を公開し、検証済みの17資材を添付しました。全資材をダウンロードし直してSHA-256とサイズが一致することを確認済みです。Windows・macOSバイナリは含めていません。既存ファイルの削除と履歴の書き換えは行っていません。

## 配布方針

- WindowsのEXE/MSIXとmacOSのapp/PKG/DMGは非公開。手元の開発・検証に使用します。
- 公開対象はLinuxパッケージと、それに対応するソース・チェックサム・ビルド記録です。
- 移行前のGitHub Releasesはv0.3.0以前の4件で、添付資産はありませんでした。現在のREADMEはlinux-v0.3.3へリンクし、旧`releases/ubuntu/`も互換性のため維持しています。

## 技術的な移行可否

移行可能です。GitHub Releasesは1ファイル2 GiB未満を扱えます（[公式資料](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)）。現在の0.3.3用資材17件はいずれもこの範囲です。

```bash
python -m tools.prepare_linux_release --version 0.3.3
```

このコマンドは`build/linux-release-plan.json`へ、公開候補の正確なパス、名前、サイズ、SHA-256、役割を書き出します。4パッケージとチェックサム一覧、4対応ソースZIP、4ビルド記録、4配布物との対応記録を検証します。ZIP内のソースのハッシュも確認します。Windows/macOSバイナリや`dist/`は候補に含みません。ワイルドカードで`dist/*`を公開しないでください。

## 移行手順と今後の運用

1. 検証済みの0.3.3資材をそのまま移すReleaseを準備します。使用したタグ名は`linux-v0.3.3`、タイトルは「Linux packages 0.3.3 — existing artifacts」です。現在のmainから再ビルドした成果物と混ぜません。
2. 元の配布記録は、amd64では`ca33994f8ea7dada7996f8902d3ab703dfae88e5`、arm64では`9102573dc45b70393bed716dd5c9f9f7f9e5a35f`と未コミット差分の存在を記録しています。単一のタグだけでは両ビルドのソースを表せないため、各ZIPと記録を基準にします。タグの参照先を現在のmainへ機械的に置き換えず、元の記録と照合します。GitHubが自動生成するSource code ZIPだけで対応ソースを置き換えません。
3. Draftへマニフェストに列挙した17件だけを添付し、パッケージごとに対応ソース・記録へのリンクをRelease本文に記載します。GitHubの添付ファイル名は平坦になるため、重複名がないことも確認します。
4. ダウンロードし直してハッシュと対応関係を確認後に公開し、英日READMEを固定タグのURLへ同時に更新します。URL案は`https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.deb`です。このURLは公開済みです（[公式リンク仕様](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)）。
5. 移行の間は現在の`releases/ubuntu/`を残し、外部からの旧URLを壊さないようにします。削除する場合も別の変更として影響を確認します。過去のGit履歴には大きなファイルが残るため、HEADから削除しただけで通常cloneの履歴容量が消えるわけではありません。別PC開発への影響が大きい履歴書き換えは、この移行に含めません。
6. 以後のLinux新バージョンはReleasesへ直接公開し、リポジトリ内に新しい大容量パッケージを積み増さない運用にします。

## 既存記録の残課題

元の配布記録は`dependency_sources`に「NOT INCLUDED」を記載しています。Folimeld本体のソースZIPは検証できましたが、これだけで全依存の対応ソース・告知確認が完了したとは判定しません。[既存の配布確認事項](license-distribution_ja.md)と[0.3.2調査](source-audit-0.3.2_ja.md)の未完了項目を維持します。移動によってこの課題が解決したように記載しません。

0.3.2は同じソース対応記録が揃っていないため、0.3.3の記録を流用せず、既存のまま保管して扱いを別途決めます。今回Linuxパッケージのインストール・実行は未検証です。

## 公開記録

Releaseタグは`ccb92e5f7d419f4210bc3c23a56e3cb7882f5840`を参照し、移行方針と準備ツールの版を示しています。過去の両アーキテクチャの厳密なビルド元を表すものではありません。各配布物の対応ソースは添付したZIPとビルド記録を使用してください。17資材の合計は414,717,064 bytesです。

以下の手順説明で述べるDraft準備、添付、再ダウンロード検証、公開、README更新は実施済みです。0.3.2の扱い、既存URLの将来的な整理、新バージョンの公開は別途扱います。依存ソースに関する既存記録の残課題も維持しています。
