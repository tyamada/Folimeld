# AlmaLinux 9.8 amd64公開前レビュー案

2026-11-12。先行対象をAlmaLinux 9.8 amd64に限定したレビュー資料。公開・コミット・タグ作成・元作業ツリーの版変更は行っていない。

## レビュー対象の固定

後続の最新対象は[文書統合済みrevision5](linux-almalinux9-035-integration-r5_ja.md)。以下はrevision4時点の確認を保持した履歴であり、公開時はrevision5のハッシュとstaging-r5を使用する。

候補は[0.3.5 revision4](linux-almalinux9-035-source-r4_ja.md)。RPMのSHA-256は`6440af05b100d283ce48b46dd72d0b9bc690c0bca1ed6c019b6b1a3ba8bc99f8`、対応ソースZIPのSHA-256は`f4d5f3639a43e86f289bb7925476bb0179fe12a5ad8b52381418b055e891233e`。

準備物は専用Build内`alma9-release-readiness-20261112/staging-r4/`。11添付物とSHA256SUMS.txtの実名・ハッシュは[準備物JSON](linux-almalinux9-release-r4-staging-2026-11-12.json)を参照。旧候補や別OSの成果物を混ぜない。

## 上流配布物との一致を追加確認

初回依存検査で保存したwheel8件を読み取り、各wheel内METADATAの名前・版からPyPIの版別JSONを取得した。ファイル名と公開SHA-256が全8件一致した。重いwheel本体を再取得・更新・再インストールしていない。

対象はPySide6 Essentials/Addons、Shiboken6、PyMuPDF、Pillow、cryptography、cffi、PyInstaller。候補内のwheel由来105 ELF項目が、この配布wheel内の同名ファイルと全件バイト一致した。導入済みPyInstallerブートローダーもwheelと一致した。梱包後ELFのヘッダー・pydata変更の扱いは先行ロード領域照合と分ける。

[公式wheel照合JSON](linux-almalinux9-official-wheel-review-2026-11-12.json)には、各wheelのPyPI URL・ファイル名・SHA-256・公開日時、候補内項目ごとのハッシュを保存した。残るOS RPM由来105項目は[所有RPM・ソース対応表](linux-almalinux9-release-native-source-map-2026-11-12.json)と別添SRPMで扱う。これにより210 ELFすべての配布実体の対応を具体化した。

これはHTTPSで公開された配布ハッシュ・内容との一致であり、署名・attestationの検証、過去のGN設定・コンパイラーフラグ・変更パッチの独立再構成ではない。

## 技術検査の状態

| 項目 | 状態 |
| --- | --- |
| 対応ソースZIP | 683入力の全照合。Gitなし・上書きなしで409テスト・67サブテスト成功、9件スキップ |
| 配布物の対応 | RPM/ELF/ソース対応、11添付物とチェックサム、162依存資料のアーカイブ内照合が成功 |
| 実体の由来 | wheel由来105項目をPyPI配布物と一致確認、OS由来105項目は所有RPM・SRPMへ対応付け |
| 告知 | PyInstaller、LibTIFF LZW、ICU、Qt/MuPDF補足を収録。QtPdf公式文書の9成分群の文書存在を確認 |
| 表示・導入 | revision3で補足4タブ・大文書操作・削除再導入を確認。機能不変のrevision4で更新・整合性・起動を確認 |
| 適用範囲 | Alma9.8 WSL2/WSLgの限定検証。全デスクトップ・ARM64・他OS・全設定移行の合格とはしない |

## 公開操作前に決めること

後続で[日英README/CHANGELOGと公開稿を揃えた専用統合案](linux-almalinux9-final-integration-review_ja.md)と、686入力の単独レビュー用ZIPを作成した。既存revision4 RPMへのソースの付け替えは行わず、新入力での候補ビルド・対応付けを次工程とする。

1. 0.3.5/build1とAlma RPM revision4を公開版に採用するかを確定する。現在は専用コピー内の案で、元リポジトリの版と日英CHANGELOGは未変更。
2. 公開ソースの統合先と、対応する不変のコミット・タグを決める。既存の公開Linux0.3.4ブランチや他OS成果物を置換しない。
3. 上記限定検証の記述と、署名・来歴の未検証条件を日英公開説明で保持する。公開後のリンク・タグを未確定のまま既成事実として書かない。
4. 元の「公開はまだ実行しない」という指示を維持し、公開操作は別の明示指示が出るまで実行しない。

過去ビルド設定の再構成は追加調査として残るが、配布wheelとの一致が未確認であるかのように扱わない。一方、全ライセンス条件への適合をこの技術検査だけで認定するものでもない。公開判断を求める前に必要なソース統合案は専用コピー内で準備し、元作業ツリーの既存変更を保持する。
