# Linux配布物のGitHub Releases移行計画

[日本語](linux-release-migration_ja.md) | [English](linux-release-migration.md)

確認日: 2026-11-04。計画・資材検証まで実施。アップロード、タグ作成、公開、既存ファイル削除、履歴書き換えは行っていません。

## 配布方針

- WindowsのEXE/MSIXとmacOSのapp/PKG/DMGは非公開。手元の開発・検証に使用します。
- 公開対象はLinuxパッケージと、それに対応するソース・チェックサム・ビルド記録です。
- 既存のGitHub Releasesはv0.3.0以前の4件で、確認時点では添付資産がありません。READMEの現在のダウンロード先は`releases/ubuntu/`です。

## 技術的な移行可否

移行可能です。GitHub Releasesは1ファイル2 GiB未満を扱えます（[公式資料](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)）。現在の0.3.3用資材17件はいずれもこの範囲です。

```bash
python -m tools.prepare_linux_release --version 0.3.3
```

このコマンドは`build/linux-release-plan.json`へ、公開候補の正確なパス、名前、サイズ、SHA-256、役割を書き出します。4パッケージとチェックサム一覧、4対応ソースZIP、4ビルド記録、4配布物との対応記録を検証します。ZIP内のソースのハッシュも確認します。Windows/macOSバイナリや`dist/`は候補に含みません。ワイルドカードで`dist/*`を公開しないでください。

## 移行手順案

1. 検証済みの0.3.3資材をそのまま移すReleaseを準備します。タグ名候補は`linux-v0.3.3`、タイトルは「Linux packages 0.3.3 — existing artifacts」です。現在のmainから再ビルドした成果物と混ぜません。
2. 元の配布記録は、amd64では`ca33994f8ea7dada7996f8902d3ab703dfae88e5`、arm64では`9102573dc45b70393bed716dd5c9f9f7f9e5a35f`と未コミット差分の存在を記録しています。単一のタグだけでは両ビルドのソースを表せないため、各ZIPと記録を基準にします。タグの参照先を現在のmainへ機械的に置き換えず、元の記録と照合します。GitHubが自動生成するSource code ZIPだけで対応ソースを置き換えません。
3. Draftへマニフェストに列挙した17件だけを添付し、パッケージごとに対応ソース・記録へのリンクをRelease本文に記載します。GitHubの添付ファイル名は平坦になるため、重複名がないことも確認します。
4. ダウンロードし直してハッシュと対応関係を確認後に公開し、英日READMEを固定タグのURLへ同時に更新します。URL案は`https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.deb`です。現在このURLの資産は未作成です（[公式リンク仕様](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)）。
5. 移行の間は現在の`releases/ubuntu/`を残し、外部からの旧URLを壊さないようにします。削除する場合も別の変更として影響を確認します。過去のGit履歴には大きなファイルが残るため、HEADから削除しただけで通常cloneの履歴容量が消えるわけではありません。別PC開発への影響が大きい履歴書き換えは、この移行に含めません。
6. 以後のLinux新バージョンはReleasesへ直接公開し、リポジトリ内に新しい大容量パッケージを積み増さない運用にします。

## 既存記録の残課題

元の配布記録は`dependency_sources`に「NOT INCLUDED」を記載しています。Folimeld本体のソースZIPは検証できましたが、これだけで全依存の対応ソース・告知確認が完了したとは判定しません。[既存の配布確認事項](license-distribution_ja.md)と[0.3.2調査](source-audit-0.3.2_ja.md)の未完了項目を維持します。移動によってこの課題が解決したように記載しません。

0.3.2は同じソース対応記録が揃っていないため、0.3.3の記録を流用せず、既存のまま保管して扱いを別途決めます。今回Linuxパッケージのインストール・実行は未検証です。
