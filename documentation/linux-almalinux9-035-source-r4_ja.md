# AlmaLinux 9のソース修正反映済み0.3.5 revision4候補

2026-11-12。revision3で見つかった配布ソース内テストの前提依存を修正し、新規専用コピーで反映した。元作業ツリーのアプリ版0.3.3と旧候補・旧stagingは保持した。

## 候補と変更範囲

```text
/home/folimeld-build/folimeld-candidates/alma9-035-source-r4-20261112/
packages/folimeld-0.3.5-4.alma9_8.x86_64.rpm
RPM SHA-256: 6440af05b100d283ce48b46dd72d0b9bc690c0bca1ed6c019b6b1a3ba8bc99f8
ELF SHA-256: bed5def2772161ca1c9a33cffa6aa0684b1944d3d5176bcbefa9c20f0c3e6ee6
```

revision3からの入力変更は`tests/test_license_info.py`と監査・別添目録のrevision表記だけ。アプリ機能コード、210ネイティブ実体、追加告知4文書は不変。ビルド前に変更がこの3入力に限定されることを検査した。

ライセンス・ソース・Alma RPMの15テスト・9サブテスト、ruff、アイコン生成、PyInstaller、RPM生成が成功。対応ソース683入力、別添162ファイル、ELF内の補足告知と対応ソースのハッシュを確認した。[ビルドJSON](linux-almalinux9-035-source-r4-verification-2026-11-12.json)を参照。

## 配布ソースそのものでの確認

対応ZIPを新規ディレクトリへ展開し、Gitなし・テスト上書きなしで全683入力を照合した。SOURCE-MANIFEST.jsonによる入力選択、Alma RPMのrevision4出力名の事前検査、関連15テスト・9サブテストが成功した。[ZIP検証JSON](linux-almalinux9-source-archive-review-r4-2026-11-12.json)を参照。

さらに、既存の専用テストvenvを変更せず同じ展開ソースから全テストを実行し、409件成功・9件スキップ・67サブテスト成功（16.79秒）。前回のテスト修正オーバーレイは不要となった。[全テストJSON](linux-almalinux9-source-r4-full-tests-2026-11-12.json)を参照。これは別のバイナリ再ビルドやビット再現性の証明ではない。

## 導入と配布準備

専用Testでrevision3からrevision4へ更新し、ELF一致、rpm -V、dnf checkが成功した。一般ユーザーでoffscreen・xcb各12秒の起動を確認して試験プロセスを終了した。旧RPMは保持した。[更新・起動JSON](linux-almalinux9-035-source-r4-update-2026-11-12.json)を参照。

新規`alma9-release-readiness-20261112/staging-r4/`へ11添付物とSHA256SUMS.txtを用意し、162資料をアーカイブ内で再照合した。日英公開稿の導入コマンドもrevision4のRPM名へ同期。[準備物JSON](linux-almalinux9-release-r4-staging-2026-11-12.json)を参照。

## 公開前の判断項目

| 項目 | 状態 |
| --- | --- |
| 修正テストと対応ZIP | 反映・検証済み。修正前テストを含むZIPから差し替わった新候補として識別 |
| アプリ機能とネイティブ実体 | revision3と不変。新候補で主要GUI全操作を再試験したとは扱わない |
| QtPdf告知9群 | 候補内の対応文書を確認済み。正確な過去のGN設定・生成creditsとの一致は未証明 |
| 版と最終統合 | 0.3.5は専用コピー内の案。元リポジトリの版・日英変更履歴の最終反映は未実施 |
| 公開 | 未実施。公開を認定する最終チェックではなく、レビュー可能な候補一式の準備 |

残る来歴確認は「QtPdf等の正確なビルド選択・変更パッチの証拠」に限定して区別し、既に確認した告知の存在・ソースZIP・導入を再び未確認として扱わない。広いソース告知集合の収録を完全な来歴の証明とはしない。
