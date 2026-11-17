# Linux配布のプレリリース方針と公開チェックリスト

[English](linux-prerelease-policy.md)

2026-11-17以降の現行方針です。**FolimeldのLinux向け配布は、旧版を含めすべてプレリリース（試験配布）です。** DEB・RPM・Snap、amd64・ARM64、両CPU共通Releaseに適用します。安定版やGitHub Latestへ昇格させません。Windows・macOS・BSDの分類はこの方針の対象外です。

`linux-v0.3.3`・`linux-v0.3.4`の共通Releaseはプレリリースへ変更済みであり、同じ分類変更を重ねて実施する必要はありません。分類だけを理由に再ビルド・VM再試験・既存資材の上書き/削除/再アップロードを行いません。過去の本文・ビルド記録・添付原本にある「stable／安定版」は当時の記録として残します。Snapの`grade: stable`もビルド時設定であり、GitHub Releaseの安定版分類を意味しません。

## 利用者向け説明と対応OS

READMEの日英両方に、旧版を含むLinux全体が試験配布であることを記載します。各Releaseの本文とCPU別の検証記録を読み、OS版・CPU・形式・パッケージrevision・依存条件・検証範囲を確認してください。amd64の成功をARM64へ流用しません。

Kali amd64 0.3.5は、[Ubuntu/Debian/Kali共通DEB](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5)です。Kali専用タグがないことを未公開の理由にしません。ARM64の[Kali専用Release](https://github.com/tyamada/Folimeld/releases/tag/kali-arm64-v0.3.5)とは別です。

## 今後のLinux公開：すべての経路で指定する条件

以下は、別途公開が許可された場合に使う手順です。この文書の追加だけでは作成・編集・公開を実行しません。

1. 現在のブランチ・未コミット変更・AGENTS.mdを確認し、他作業を保護します。公開タグの対象コミット、本文、CPU別資料、明示的な資材一覧とSHA-256を確定します。
2. 新規Linux Releaseを作る時点から**DraftかつPre-release、Latestにしない**を指定します。タグ名に`preview`がなくても例外にしません。既存タグを自動生成しないよう、CLIでは`--verify-tag`を併用します。
3. CLIは作成時に`gh release create <tag> --verify-tag --draft --prerelease --latest=false ...`、公開時にも`gh release edit <tag> --draft=false --prerelease --latest=false`を明示します。既存公開Releaseへ機械的に再適用するためのコマンドではありません。
4. REST APIで作成/公開する場合も、対応する要求で`prerelease: true`と`make_latest: "false"`を明示します。Draftを公開する時だけ`draft: false`とします。引数の省略・`legacy`・自動Latest判定には依存しません。
5. ブラウザーを使う場合はPre-releaseを選び、Latestを選ばず、保存直前に両設定を確認します。Draftであることだけではプレリリース指定の代わりになりません。
6. 公開直前と直後にAPI等で`prerelease=true`、`draft`の段階別値、対象タグ・資材の名前/サイズ/SHA-256、既存Latestが不変であることを確認します。公開後の実URLからの照合を記録し、それが完了する前にREADMEで公開済みと案内しません。相違は停止・報告し、許可のない設定修正・再アップロードは行いません。
7. 他CPU・他OSのReleaseや既存資材、公開日時、本文、タグを変更しません。履歴上の原本は編集せず、現行方針はこの文書とREADMEで明確にします。

[CLI作成](https://cli.github.com/manual/gh_release_create)・[CLI編集](https://cli.github.com/manual/gh_release_edit)の公式仕様を参照してください。

## ローカル準備ツールの限界

`tools/prepare_linux_release.py`は既存資材を検査してローカルの移行計画を作る工具で、GitHub Releaseを作成しません。出力にはプレリリース/Latestの強制フィールドがないため、出力を利用する将来のAPI・CLI・画面操作側で上記条件を必須にします。過去の公開計画JSONや添付原本を遡って書き換えません。

現行の`.github/workflows/checks.yml`は検査/Actions artifact用で、GitHub Releaseの公開経路ではありません。新しい公開自動化を追加する場合には、Linux限定の判定とプレリリース/Latest不変を検査するガードが必要です。現時点で全ての外部・一時スクリプトを技術的に強制できると保証するものではありません。
