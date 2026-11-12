# サムネイル修正入りDEBの検証

実施日: 2026-11-12（日本時間）。Ubuntu 24.04の専用作業コピーで再ビルドし、許可済みの新規Kali環境だけへ再導入した。非公開の検証用バージョン0.3.3であり、公開済み成果物とはハッシュで区別する。

## 成果物とソース

```text
/home/tyamada22/folimeld-candidates/script-validation-20261112/packages-thumbnail-fix/folimeld_0.3.3_amd64.deb
DEB SHA-256: bb531236e78c9195245a88d6620e840f232b505b97d82968719528f415573875
ELF SHA-256: 752d4f389a671196aa15a1b673b08b88d8ebbcc26b67f04822a58fe05102bbc6
Source SHA-256: fcbf135aaf1b5ce6cc628f73716f31751cbc4ac876369ef18e56fca61deefd9d
```

Python 3.12.3で生成し、DEBのglibc下限は2.39。対応ソースZIP、パッケージ内ELF、Kali導入済みELF、Ubuntuで展開したELFのハッシュを照合した。ソースの`main.py`と`folimeld/thumbnails.py`は現在の作業ツリーと一致し、Qt Virtual Keyboard関連の同梱項目は0件。専用コピーには未コミット変更を含むため、HEADだけで成果物を再現できるとは扱わない。ビルド用コピー全体が現在の作業ツリーと同一であることは保証しない。

## 確認結果

| 対象 | 結果 |
| --- | --- |
| Ubuntuのソース試験 | サムネイル関連9件成功（1.29秒） |
| Kali Rolling 2026.3 | `apt-get --reinstall --no-install-recommends`による同一版の再導入成功。導入ELF一致、`dpkg --audit`の出力なし |
| Kaliの通常GUI | 初期配置、回転直後のプレビュー、Undo/Redo、別名保存、保存PDFの再読込を確認 |
| 保存データ | 3ページ、回転角度[90,0,0]、各ページの文字内容を保持。原本SHA-256不変 |
| Ubuntuの既存試験環境 | DEBを新しい専用ディレクトリへ展開し、offscreenで12秒間の起動を確認。導入済み0.3.4と既存ELFは保持 |

画面証拠: [初期表示](linux-deb-thumbnail-fix-verification/01-kali-loaded.png)、[回転直後](linux-deb-thumbnail-fix-verification/02-kali-rotated.png)、[Undo](linux-deb-thumbnail-fix-verification/03-kali-undo.png)、[Redo](linux-deb-thumbnail-fix-verification/04-kali-redo.png)、[別名保存](linux-deb-thumbnail-fix-verification/05-kali-saved.png)、[再読込](linux-deb-thumbnail-fix-verification/06-kali-reopened.png)。回転表示は追加編集や保存を挟まず確認した。保存と証拠取得後、所有者と引数を照合した検証用GUIだけを終了した。

バージョン・依存関係・ソース対応・ログ・画面ハッシュは[検証JSON](linux-deb-thumbnail-fix-verification-2026-11-12.json)に保存した。原因と修正は[描画修正記録](linux-thumbnail-redraw-verification_ja.md)を参照。

## 検証範囲

今回の修正入りDEBでは、新規クリーン環境の依存解決・削除再導入、IME、画像取込、暗号化PDFのGUI試験は繰り返していない。[以前のKali GUI試験](linux-amd64-kali-gui-verification_ja.md)と区別する。Ubuntuは展開起動だけであり、導入試験ではない。完全なLinuxデスクトップと他アーキテクチャも未検証。既存配布物・アプリ版・READMEの対応済み表記を変更せず、公開も実施していない。
