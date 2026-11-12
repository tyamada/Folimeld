# AlmaLinux 9の文書統合済み0.3.5 revision5候補

2026-11-12。[専用統合レビュー案](linux-almalinux9-final-integration-review_ja.md)を新しいビルド入力として使い、既存RPMのソースを付け替えず、新規候補と対応記録を作成した。元作業ツリー・旧候補・旧staging・レビューZIPは保持した。

## 固定した配布候補

```text
/home/folimeld-build/folimeld-candidates/alma9-035-integration-r5-20261112/
packages/folimeld-0.3.5-5.alma9_8.x86_64.rpm
RPM SHA-256: 0ba2c7dfc397f61b1ca70679838c93589310d116a267249d67dd822b8cb654bc
ELF SHA-256: 82ada5680df8bb74da15b801ce59793b140a4789766d0caf4b7082a120ca470c
対応ソースSHA-256: f9a6add8b239c0da7f563128242023d880077f89e565cd38eb6ff2c51af4c079
```

専用コピー内の版は0.3.5/build1、RPM revision5。日英README・公開稿のrevisionと導入コマンドを5に揃えた。日英CHANGELOGはAlma先行候補の内容を同期し、未公開状態を保持した。元リポジトリの版・README・CHANGELOGは変更していない。

## ビルドと対応検証

関連15テスト・9サブテスト、アイコン生成、PyInstaller、RPM生成が成功。全対応ソース686入力と別添162ファイル、追加告知4文書を照合した。全アプリ機能コードと210ネイティブ実体はrevision4から不変で、Virtual Keyboard関連は0件。

README・CHANGELOG・公開稿の6文書はソースZIP内と一致し、相対リンク・revision表記・導入対象RPM名が解決・一致した。RPMの対応JSONは、この新ELFと新ソースZIPのハッシュを指す。[ビルドJSON](linux-almalinux9-035-integration-r5-verification-2026-11-12.json)を参照。

実際の対応ZIPをGitなしの新規コピーへ展開し、全686入力、SOURCE-MANIFESTによる入力選択、revision5のRPM事前検査、関連15テスト・9サブテストを確認した。[ZIP検証JSON](linux-almalinux9-source-archive-review-r5-2026-11-12.json)を参照。全409テストは機能コード・テストが一致するrevision4の記録を保持し、revision5で全件を再実行したとは表記しない。

## 導入と配布準備

専用Testでrevision4からrevision5へ更新し、ELF一致、rpm -V、dnf checkが成功した。一般ユーザーの新規プロフィールでoffscreen・xcb各12秒の起動を確認し、試験後に終了した。旧RPMは保持した。[更新・起動JSON](linux-almalinux9-035-integration-r5-update-2026-11-12.json)を参照。

新規`alma9-release-readiness-20261112/staging-r5/`へ11添付物とSHA256SUMS.txtを作成した。日英公開稿はホストの古い稿ではなく、この候補のソース内の文書からコピーし、対応ZIPとの食い違いを防いだ。162依存資料のアーカイブ内照合も成功した。[配布準備JSON](linux-almalinux9-release-r5-staging-2026-11-12.json)を参照。

標準`sha256sum -c SHA256SUMS.txt`も全11件成功した。

## 判断に残す条件

後続で[revision5の削除再導入・新規最小依存起動](linux-almalinux9-035-integration-r5-lifecycle_ja.md)も成功した。4パッケージファイル復元、試験PDF/設定6件保持、Pythonやビルドツールなしの数値UID/GID1000起動と整合性を確認した。

統合案からの新候補作成と、バイナリ・対応ソース・日英説明の一致は完了した。元リポジトリへの反映、採用する不変コミット・タグ、公開操作は未実施。現在の「公開はまだ実行しない」という指示は維持する。

QtPdf等の正確な過去ビルド設定・変更パッチの独立再構成は未完了。ただし上流wheelとの105実体の一致、所有RPMと残る105実体の対応、告知文書・ソースの収録という確認済み事項とは分ける。技術的な配布物検査と、全ライセンス条件への適合認定も区別する。
