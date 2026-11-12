# Folimeld 0.3.5 — AlmaLinux 9 amd64 試験版

AlmaLinux 9.8のWSL2／WSLgで確認したx86_64向けRPMです。既存のUbuntu／Debian向けLinux 0.3.4や他OSの配布物は保持します。

RPMとSHA256SUMS.txtを同じフォルダへダウンロードし、照合後に導入してください。

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt
sudo dnf install ./folimeld-0.3.5-5.alma9_8.x86_64.rpm
folimeld
```

日本語PDF表示、回転・Undo/Redo・ページ移動・白紙挿入削除、日本語名での別名保存と再読込、暗号化PDF、PNG取込み、IBus/Mozc入力を確認しています。候補間の更新、設定3項目の保持、独立XDG/D-BusでのGIO起動も検証しました。最終revision5では更新、削除再導入、試験PDF・設定の保持、一般ユーザー起動、新規最小依存installrootでのoffscreen起動と整合性を確認しています。

通常デスクトップ、ARM64、AlmaLinux 10、公開Ubuntu/Debian 0.3.4からの移行、任意の既存設定は未検証です。最小依存試験は独立WSLのブートや日本語GUI/IMEの確認を意味しません。

対応するFolimeldソースZIP、パッケージとの対応記録、第三者告知、依存ソース資料を添付しています。ローカルで固定したソースコミットは`03b14ec8c4410fbc7510aa9bedb27950e78cfc6e`で、候補の686入力との一致を確認しています。詳細は添付の検証JSONとKNOWN-LIMITATIONS.txtを参照してください。

RPM・チェックサム・ソースコミットは未署名です。配布wheelとの内容一致は確認しましたが、過去の全ビルド設定・変更パッチの独立再構成や、全ライセンス条件への適合認定ではありません。

LibTIFFのLZW実装には、カリフォルニア大学バークレー校で開発されたソフトウェアが含まれます。詳細は同梱のLibTIFF-LZW告知を参照してください。
