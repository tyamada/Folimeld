# Folimeld 0.3.5 — openSUSE Leap 16.1 amd64 試験版

[English](linux-opensuse-leap161-publication-body.md)

openSUSE Leap 16.1の専用WSL2/WSLgで検証したx86_64 RPMです。通常デスクトップ、ARM64、他のディストリビューションへの対応確認ではありません。既存のLinux 0.3.4、AlmaLinux9、Fedora44/45の配布物は保持します。

RPMとSHA256SUMS.txtを同じフォルダーへ取得し、照合後に導入します。

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo zypper install --allow-unsigned-rpm --no-recommends ./folimeld-0.3.5-1.lp161.x86_64.rpm
folimeld
```

指定したローカルRPMは未署名です。上記オプションはそのローカルRPMを許可するもので、標準リポジトリの署名検証は無効にしません。

409テスト・67サブテスト成功、9件スキップ。新しい実行ファイルでPDF回転、Undo/Redo、ページ移動、白紙挿入削除、日本語・空白入り名での保存とGIO経由の再読込、IBus/Mozcの「にほんご→日本語」変換・確定、ライセンス画面を確認しました。暗号化PDFの認証・回転・保存後の再認証と本文保持、PNGからのPDF生成・保存と画像画素の一致も確認しました。

専用Testの0.3.3 revision3から0.3.5 revision1への更新、offscreen/xcb起動、削除再導入、既存試験PDF・設定のハッシュ保持、rpm整合性・依存整合性を確認しました。新規最小installrootでも、開発依存や推奨CJKフォントなしでUID/GID1000のoffscreen起動を確認しました。chroot内の試験であり、独立WSLブートや最小環境でのIMEの確認ではありません。

対応ソースはコミット`44f76e77c05c0c097be9dc1e8f1de9f8449e6aaa`の858入力と一致します。添付するソースZIP・RPM対応記録・第三者告知・依存ソース別添・検証資料がビルドを識別します。ビルド時のREADME、CHANGELOG、準備中の告知記録は履歴として保持しています。

配布実行ファイルの209ネイティブ実体を、公式wheel由来105実体とOS由来104実体へ照合しました。OS実体は署名検証済み36ソースRPMへ対応します。PyInstallerブートローダーも公式wheelと一致します。解析時に存在したVirtual Keyboard 3実体は配布物から除外されています。

通常ファイルマネージャーの操作、公開Ubuntu/Debian 0.3.4からの移行、幅広い入力・設定、過去wheelの全ビルド設定の再構成は未検証です。RPM・チェックサム・コミットは未署名です。再現ビルドやライセンス適合認定ではありません。合成GUI入力での反復文字・ダイアログ増加・長すぎる保存名の失敗を記録し、単独GUIのマウス確定で画像取込・保存を再検証しました。詳細は検証JSONとKNOWN-LIMITATIONS.txtを参照してください。

LibTIFFのLZW実装には、カリフォルニア大学バークレー校で開発されたソフトウェアが含まれます。同梱のLibTIFF-LZW告知を参照してください。
