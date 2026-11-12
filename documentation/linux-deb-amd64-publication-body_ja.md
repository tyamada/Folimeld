# Folimeld 0.3.5 — Linux DEB amd64試験版

[English](linux-deb-amd64-publication-body.md)

Ubuntu 24.04で生成したx86_64 DEBを、専用のUbuntu 24.04.4、Debian 13.6、Kali Rolling 2026.3 WSL2/WSLg環境で確認した試験配布です。従来のLinux 0.3.4および公開済みRPMは保持します。glibc 2.39以上が必要です。

DEBとSHA256SUMS.txtを同じ場所へダウンロードし、検証後に導入してください。Ubuntuでは公式universeリポジトリも必要です。

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo apt install --no-install-recommends ./folimeld_0.3.5_amd64.deb
folimeld
```

409テスト・67サブテスト成功、9スキップ、ruff成功。3環境で既存版（Ubuntu/Debian 0.3.4、Kali 0.3.3）からの更新、一般ユーザーでのoffscreen/xcb起動、削除・再導入、既存試験PDF・設定のハッシュ保持、dpkg整合性・APT依存確認が成功しました。3環境の実画面で日本語PDF表示・回転直後のサムネイル・Undoを確認しました。

UbuntuではさらにRedo、ページ移動、白紙挿入・削除、日本語と空白を含むファイル名での別名保存・再読込を確認しました。保存PDFは3ページ、元の順[2,1,3]、回転[0,90,0]で文字を保持しました。Ubuntu公式noble main/universeだけから作成した最小chrootでは、開発依存・Python・推奨CJKフォントなしでUID/GID1000のoffscreen起動が成功しました。独立WSL起動や最小環境のGUIを検証するものではありません。

実行ファイルに対応する870ソース入力をソースZIP・Gitコミットとバイト照合しました。同梱ネイティブ214項目（公式wheel105、Ubuntu OS109）を照合し、対応するUbuntuソース61件を取得しました。現在の公式インデックスにない旧版は公式Ubuntu Snapshotの署名付きインデックスから取得し、InRelease署名・SourcesのSHA-256・ソースファイルのSHA-256を検証しています。PyInstallerブートローダーも公式wheelと一致します。対応ソース、第三者告知、依存ソース2分冊、検証記録を添付します。

通常のLinuxデスクトップ、ARM64、他のディストリビューション・将来のrolling更新、幅広いPDF・画像・暗号化設定は未検証です。この新DEBではIME変換・GIO関連付け・画像取込・暗号化PDFの実画面試験を再実施していません。RPM版の結果をこのDEBの合格として扱いません。ビルド時の「監査待ち」記載はその時点の記録として残し、完了結果は外部の検証JSONに記載します。パッケージ・チェックサム・コミットは未署名です。再現可能ビルドやライセンス遵守認証ではありません。

LibTIFFのLZW実装にはUniversity of California, Berkeleyが開発したソフトウェアが含まれます。同梱LibTIFF-LZW告知を参照してください。
