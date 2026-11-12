# 公開Linux0.3.4と追加amd64対応の統合レビュー案

実施日: 2026-11-12（日本時間）。専用WSL作業コピーで、現在の修正を保持するソース統合案を準備した。アプリ版0.3.5/build1はこのコピー内だけの未公開案であり、公開版の決定ではない。元のWindows作業ツリーは0.3.3/build1、専用Testへ導入済みの候補は0.3.3 revision3のまま保持した。

## 公開入力と専用コピー

GitHub接続で[公開Release一覧](https://github.com/tyamada/Folimeld/releases)を読み取り、Linux0.3.4の対応コミットが`eeacd06a49cda85ddc1d432bd785e507f8006a89`であることを再確認した。取得できた公開一覧には0.3.5のReleaseはなかった。非公開Draftや全タグの不存在を保証するものではない。[公開一覧・0.3.4成果物の取得記録](linux-public-integration-inputs-2026-11-12.json)を保存した。ReleaseやGit履歴への書込みはしていない。

```text
WSL: Folimeld-AlmaLinux9-Amd64-Build
/home/folimeld-build/folimeld-candidates/linux-integration-review-20261112/source
branch: linux-amd64-integration-review-20261112
base: 423e59471b576e4732c7d6ec0ad9ab25cbf19582
```

現在の未コミット入力を含むファイルを新コピーへ転送し、そのコピー内だけに専用ブランチを作成した。マージコミットや新規コミットを作ったわけではなく、公開コミットと現入力を比較したレビュー用作業ツリーである。

## 保持・変更した内容

| 項目 | 統合案の扱い |
| --- | --- |
| 版 | 専用コピーの__version__を0.3.3から0.3.5へ変更。build1維持。0.3.4の再利用を避けた未公開案 |
| 日英CHANGELOG | 専用コピーのUnreleasedへ対応する1項目を同時追加。公開済み対応を示す記述にはしない |
| README日英 | 現在の公開案内をそのまま保持。コピー・元作業ツリーとも変更なし |
| Qt Virtual Keyboard | 公開0.3.4の除外3行を保持し、公開側と一致を確認 |
| 画像取込 | 現HEADのダイアログ破棄・タイマー切断・後処理を保持 |
| サムネイル | 未コミット描画修正と回帰テストを保持 |
| 告知 | PyInstaller全文収集修正と回帰テストを保持 |
| ソースZIP | SOURCE_DATE_EPOCHとZIP属性正規化を含む現処理を保持 |
| RPM | Fedora・Leap・Tumbleweed・Alma別ヘルパー/spec/拒否テストを保持 |
| 画像資産 | 現作業ツリーのassetsを全件バイト一致で保持。公開コミットの旧資産へ戻さない |
| 旧Linux専用告知・梱包 | 公開0.3.4の版固定ファイルを復元しない |

主要コード・スクリプト・テスト・assetsは元作業ツリーとハッシュ一致を再確認した。公開0.3.4の旧build-release-candidate.shは、0.3.4の既存DEB/Snapテンプレートと別添告知を前提に再梱包する処理である。新しいRPM群の一般ビルド手順としてそのまま流用しない。旧成果物内の配布告知を、新候補へすべて反映したという主張でもない。

コピー内の版・日英CHANGELOGを確認できる[提案パッチ](linux-public-integration-proposal.patch)を保存した。このパッチは全未コミット実装を含む単独適用用パッチではない。元からある追加対応実装は、専用コピーと[検証JSON](linux-public-integration-review-2026-11-12.json)の入力ハッシュ・差分で識別する。元の版とCHANGELOGは変更していない。

## ソース検証結果

専用コピーの0.3.5入力で、全テスト409件成功・9件スキップ・67サブテスト成功（16.12秒）。変更コードのruff、build_linux.shのbash構文検査、AlmaLinux RPMヘルパーの--checkも成功した。日英CHANGELOGの意味を同期し、相対リンクを確認した。

最初の全テストはpsutil不足で収集に失敗した。既存ビルドvenvは変更せず、新規test-venvから既存パッケージを読み取り参照し、constraints-releaseで固定したpsutil7.2.2だけを追加して再実行した。初回失敗・専用環境・最終結果を記録に保持している。

Alma環境での実際の--check出力は`folimeld-0.3.5-1.alma9_8.x86_64.rpm`。他OSについてはファイル名関数で次を確認しただけで、実ビルドやOS合格ではない。

```text
folimeld-0.3.5-1.fc44.x86_64.rpm
folimeld-0.3.5-1.fc45.x86_64.rpm
folimeld-0.3.5-1.lp161.x86_64.rpm
folimeld-0.3.5-1.tw20261110.x86_64.rpm
```

## 次工程と制約

この統合案からバイナリ・パッケージはまだ作っていない。実ビルド時は、[告知入り候補](linux-almalinux9-notices-candidate_ja.md)で用いたLinux固有告知・別添資料目録の反映を、新コピー内で明示して行う必要がある。Linux用記録をリポジトリ全体のWindows用記録へ上書きしない。

次は0.3.5案の実ビルドと、0.3.3 revision3からのアプリ版更新・設定保持・主要GUI回帰・ソース対応の確認。他ディストリビューションの再ビルド、通常デスクトップ、wheelビルド来歴・Alma8 libXau署名も残る。ソーステストの成功をWindows/macOS/ARM64の実行確認や公開準備の完了とはしない。公開・タグ・コミット・元版変更は行っていない。
