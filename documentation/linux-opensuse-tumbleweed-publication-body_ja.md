# Folimeld 0.3.5 — openSUSE Tumbleweed 20261110 amd64 試験版

[English](linux-opensuse-tumbleweed-publication-body.md)

VERSION_ID=20261110の専用WSL2/WSLg Build/Testで検証したx86_64 RPMです。Tumbleweedの全スナップショット、通常デスクトップ、ARM64、他ディストリビューションへ結果を拡張しません。既存のLinux 0.3.4・AlmaLinux9・Fedora44/45・Leap16.1の配布物は保持します。

RPMとSHA256SUMS.txtを同じフォルダーへ取得し、照合後に導入します。

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo zypper install --allow-unsigned-rpm --no-recommends ./folimeld-0.3.5-1.tw20261110.x86_64.rpm
folimeld
```

RPMは未署名です。上記オプションは指定したローカルRPMだけを許可し、標準リポジトリの署名検証は維持します。

409テスト・67サブテスト成功、9件スキップ。新ELFで回転・Undo/Redo・ページ移動・白紙挿入削除、日本語・空白入り名での保存とGIO再読込、Mozcの「にほんご→日本語」変換・確定、ライセンス画面を確認しました。暗号化PDFの認証・回転・保存と保存後の誤パスワード拒否・再認証・本文保持、画像PDF生成・保存も確認しました。

専用Testの0.3.3 revision3から0.3.5 revision1への更新、offscreen/xcb起動、削除再導入、既存試験PDF/設定のハッシュ保持、RPM/依存整合性を確認しました。新規最小installrootでも、開発依存・推奨CJKフォントなしでUID/GID1000のoffscreen起動を確認しました。最小rootは通常のローリングリポジトリから組み立てたchrootであり、20261110固定の独立WSLブートや最小環境のGUI/IMEを検証したものではありません。

配布物の206ネイティブ実体を公式wheelまたはOS所有パッケージへ照合し、対応する35ソースRPMの署名を確認しました。PyInstallerブートローダーも公式wheelと一致します。対応ソースZIP、RPMとの対応記録、第三者告知、依存ソース別添、検証資料を添付します。ソースコミットと全入力の照合結果は検証JSONに記録しています。凍結済みのビルド時文書・準備中の告知は履歴として保持しています。

通常ファイルマネージャー操作、他スナップショット、公開Ubuntu/Debian 0.3.4からの移行、幅広い入力・設定、過去wheelの全ビルド設定の再構成は未検証です。IBus切替コマンドは終了コード1でしたが、エンジン照会と実際の変換・確定で動作を確認しました。WSLのsystemdユーザーセッション警告は記録し、グローバル設定は変更していません。RPM・チェックサム・コミットは未署名です。再現ビルドやライセンス適合認定ではありません。詳細は検証JSONとKNOWN-LIMITATIONS.txtを参照してください。

LibTIFFのLZW実装には、カリフォルニア大学バークレー校で開発されたソフトウェアが含まれます。同梱のLibTIFF-LZW告知を参照してください。
