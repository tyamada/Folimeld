# Folimeld 0.3.5 — Fedora 44 amd64 試験版

[English](linux-fedora44-publication-body.md)

Fedora 44の専用WSL2／WSLg環境で確認したx86_64向けRPMです。通常デスクトップ、ARM64、他ディストリビューションへ検証結果を拡張しません。既存のLinux 0.3.4・Fedora 45試験版・AlmaLinux試験版の配布物は保持します。

RPMとSHA256SUMS.txtを同じフォルダーへダウンロードし、照合後に導入してください。

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo dnf install ./folimeld-0.3.5-2.fc44.x86_64.rpm
folimeld
```

409テスト・67サブテスト成功、9件スキップ。PDF表示、回転・元に戻す・やり直し・ページ移動・白紙挿入削除、日本語名での別名保存と再読込、暗号化PDFの再認証、PNGからのPDF作成、IBus/Mozcの日本語変換・確定を確認しました。独立XDG/D-Busで日本語・空白入りパスのGIO起動と、追加告知のライセンス画面表示も確認しています。

revision2への更新、削除・再導入、試験PDF・設定6件の保持、再導入後の一般ユーザー起動が成功しました。新規の最小依存installrootでも、Python・ビルドツールなしでoffscreen起動と整合性を確認しました。この最小依存試験はchroot内の確認で、独立WSLのブートや日本語GUI/IMEの確認を意味しません。公開Ubuntu/Debian 0.3.4からの移行や、任意の既存設定は未検証です。

対応するFolimeldソースZIP、パッケージとの対応記録、第三者告知、依存ソース別添、検証記録を添付します。ソースコミットは `293da8abe0459eba5d2a95609a6c3d630c986033` で、ビルド時の822入力との一致を確認しました。README・CHANGELOGを含むビルド時ソースは履歴として保持しており、公開時の状況へ書き換えていません。

ネイティブ207実体は、公式wheel由来105実体と、署名検証済み37 SRPMに対応するFedora OS由来102実体へ照合しました。PyInstallerブートローダーも公式wheelと一致します。RPM・チェックサム・ソースコミットは未署名です。過去の全コンパイラー設定・変更パッチの独立再構成、再現ビルド、ライセンス適合認定とは区別してください。詳細は添付のverification JSONとKNOWN-LIMITATIONS.txtを参照してください。

LibTIFFのLZW実装には、カリフォルニア大学バークレー校で開発されたソフトウェアが含まれます。詳細は同梱のLibTIFF-LZW告知を参照してください。
