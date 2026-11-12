# Fedora 45の0.3.5未公開候補検証

2026-11-12、許可済み専用Build/Test WSL2内で実施した。0.3.5/build1は専用コピー内だけの案で、公開版の決定ではない。元作業ツリーは0.3.3/build1のまま、既存候補・配布物を保持した。

## ビルドと対応ソース

新規コピーは`/home/folimeld-build/folimeld-candidates/fedora45-integration-035-20261112`。固定ビルド環境（Python 3.14.10、glibc 2.44）を変更せず利用した。版と日英CHANGELOGの提案パッチは`git apply --check`で適用できなかったため、実適用せず、Alma専用統合レビューコピーの検証済み3ファイルを新規コピーへ転送した。Gitの統合成功を意味しない。

- 全409テスト・67サブテスト成功、9件スキップ（17.76秒）。ruff、Qt/PyMuPDF import、アイコン生成、PyInstaller、RPM生成も成功。
- 対応ソース703入力と実行ファイルの関連を照合。PyInstallerの完全なCOPYINGを収録し、Virtual Keyboard関連は0件。
- Fedora固有のOS依存42パッケージ・ライセンス45ファイルを収集し、新Analysisの所有パッケージが対象内にあることを確認。AlmaのELF・OS通知は流用していない。
- 暗号依存の共通上流ソースを再利用し、Fedoraのネイティブ実体から記録を再生成。別添素材52ファイルを照合した。ただしQt/Pillowの全ソース、Fedoraの全SRPM、wheelの完全な来歴を揃えた記録ではない。Almaの別添149ファイルとは範囲が異なる。

```text
packages/folimeld-0.3.5-1.fc45.x86_64.rpm
RPM SHA-256: ec3cc83e24de97c11b661d0286f7d48f0b32bea66a88e9d0bb93229eb70e5ffb
ELF SHA-256: b59faa51dbdc16580eb93c2b978ea85b53b727f6d843067fa37bdd53a4729cf9
```

## 更新・設定の確認

専用Testで非公開0.3.3 revision4から0.3.5 revision1へ更新できた。導入後のELF一致、`rpm -V folimeld`、`dnf check`が成功。一般ユーザーでoffscreen・xcbそれぞれ12秒の生存を確認した。

既存試験プロフィールを新規ディレクトリへ複製し、`language`、`last_open_directory`、`last_image_directory`の3項目を確認。日本語UI、実際の0.3.5表示、PDF・画像選択ダイアログの初期フォルダが旧設定と一致した。元設定・コピー設定・原本PDFのハッシュは不変。画像取込みと保存は行わず、所有ユーザーと専用環境変数を確認した試験アプリだけを終了した。

証跡: [日本語PDF](linux-fedora45-035-integration/01-loaded.png)、[版](linux-fedora45-035-integration/02-version.png)、[PDF履歴](linux-fedora45-035-integration/03-pdf-history.png)、[画像履歴](linux-fedora45-035-integration/04-image-history.png)。コマンド結果・ハッシュ・素材範囲は[検証JSON](linux-fedora45-035-integration-verification-2026-11-12.json)を参照。

## 残る確認

今回の新ELFでは、編集・IME・画像変換・暗号化PDF・GIO・削除再導入・新規installrootをまだ再試験していない。旧0.3.3の結果やAlmaの結果で代用しない。公開Ubuntu/Debian 0.3.4からの移行、任意の設定スキーマ、完全なデスクトップ、他OS・ARM64、依存ソースの完全性も今回の合格範囲に含まない。公開・コミット・タグ作成は行っていない。
