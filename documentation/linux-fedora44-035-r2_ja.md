# Fedora 44の0.3.5 revision2候補

後続の[公開結果](linux-fedora44-publication-result_ja.md)：ユーザーの明示許可を受けてFedora44試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。Fedora45試験版の公開とmainの日英案内統合後、許可済みFedora44専用Build/Testで0.3.5候補を作成した。既存の作業変更・旧候補・公開物は保持し、Fedora44版は未公開。

## 新規候補

```text
/home/folimeld-build/folimeld-candidates/fedora44-integration-035-r2-20261113/
packages/folimeld-0.3.5-2.fc44.x86_64.rpm
RPM SHA-256: d3fc22088af7d4fa08b90bc341e64b24b23d350de98a11d9825a0cafa4416574
ELF SHA-256: c5fea766f7f508255a1c1bfdd68e1e59230d448b564f818d7a4150f0876da7f8
```

main `ea3f5f13d5c57e70e1d7a912c5eca9361ca0b272` と既存の未コミット実装を新しい専用コピーへ収録した。アプリ版0.3.5/build1と日英のFedora44候補変更履歴はコピー内だけで設定し、mainの版は0.3.3のまま。既存のPython3.14固定ビルドvenvは更新せず、全パッケージ一覧の前後一致を確認した。psutil・ruffは新規試験venvだけへ固定版で導入した。

## 告知とネイティブ実体

検証済み共通上流資料113ファイルをFedora45の資料からハッシュ照合付きで再利用した。Fedora45のOS告知・ネイティブ記録・ELF・OS SRPMは転送していない。Fedora44上で暗号化依存のネイティブ記録と告知を再生成し、OS所有パッケージから告知を収集した。LibTIFF LZW・ICU・Qt・MuPDFの補足告知を含む。別添目録は119ファイル。

最初のrevision1はビルドと全409テストが成功したが、新Analysisの所有パッケージ照合で`dbus-libs`・`systemd-libs`の告知不足を検出した。旧候補を基準にした収集範囲が不十分だったため、この候補は合格扱いにせず保持し、revision2を新規作成した。実際のrevision1 Analysisから所有パッケージを再収集し、revision2の新Analysisが全件カバーされることを確認した。[失敗・対処記録](linux-fedora44-035-r1-verification-failure-2026-11-13.json)を参照。

revision2の207ネイティブ実体はrevision1と全件バイト一致。旧0.3.3の205実体も全件不変で、追加は`libdbus-1.so.3`・`libsystemd.so.0`の2件だけ。Fedora45の結果やバイナリで代用していない。RPMはFedora44用のglibc下限2.43を宣言し、Fedora45用の2.44ではない。

## ビルド・更新・起動

revision2で409テスト・67サブテスト成功、9件スキップ（17.39秒）。ruff・Qt/PyMuPDF import・アイコン生成・PyInstaller・RPM生成が成功した。ELF埋め込みソース822入力、RPM対応記録、別添119ファイル、補足告知とPyInstaller COPYING、暗号化依存の実体を照合した。Qt Virtual Keyboardは0項目。

専用Testを0.3.3 revision2から0.3.5 revision2へ更新し、ELF一致・`rpm -V`・`dnf check`が成功した。既存の試験PDF・設定10ファイルはハッシュ不変で保持。新規一般ユーザープロファイルでoffscreen/xcbを各12秒起動し、試験後に終了した。

[ビルド・ソース照合JSON](linux-fedora44-035-r2-build-2026-11-13.json)と[更新・起動JSON](linux-fedora44-035-r2-update-2026-11-13.json)に実行コマンド・ログ・依存一覧・ハッシュを保存した。WSL設定とsystemdユーザーセッションの警告は保持し、グローバル設定は変更していない。

## 残る確認

後続の[新ELFのPDF回帰](linux-fedora44-035-r2-regression_ja.md)で編集・日本語名保存再読込・暗号化PDF・画像PDFを確認し、保存データと元入力不変も照合した。[デスクトップ連携・導入回帰](linux-fedora44-035-r2-desktop_ja.md)でIME・GIO・ライセンス表示、削除再導入と新規最小依存起動も確認した。[配布実体・ソース監査](linux-fedora44-035-r2-source-audit_ja.md)で公式wheel105実体・OS102実体と署名検証済み37 SRPM、外部別添178項目・対応ソース822入力の最終照合も完了した。専用Gitスナップショットと公開パケットのレビュー、Fedora44公開許可確認が残る。共通資料の過去Alma/Fedora45監査記録をFedora44の実行成功として扱わない。通常デスクトップやARM64、他ディストリビューションへ検証結果を拡張しない。

後続の[公開前レビュー](linux-fedora44-publication-review_ja.md)で専用Gitスナップショット・日英案内・11添付のパケットとチェックサム確認まで完了した。タグ・push・Release公開は行っていない。Fedora45試験版の公開許可はFedora44版の公開許可として流用しない。
