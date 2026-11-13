# Linux amd64候補の公開前入力・依存ソース確認

実施日: 2026-11-12（日本時間）。公開、コミット、既存候補の置換は実施していない。対象は専用WSL2で作成した非公開0.3.3候補であり、ライセンス適合性の認定ではない。

## 対応ソースと埋込文書

Fedora45/44、Leap16.1、Tumbleweed20261110、AlmaLinux9.8の5実行ファイルをPyInstallerのアーカイブリーダーで読み取った。各実行ファイルのBuild-source.txtから指定ZIPのハッシュ、ZIP内マニフェストと全入力ファイルのハッシュ、埋込Installed-packages.txtとZIP内文書の一致を検証した。既存RPMとそのELFの対応は各OSの導入記録で別途確認済み。

| ビルド環境 | 照合した入力ファイル数 | ビルドPython | Qt / PyMuPDF・MuPDF / Pillow |
| --- | ---: | --- | --- |
| Fedora45 | 470 | 3.14.10 | 6.11.2 / 1.28.2 / 12.3.0 |
| Fedora44 | 470 | 3.14.10 | 同上 |
| Leap16.1 | 473 | 3.13.13 | 同上 |
| Tumbleweed20261110 | 475 | 3.14.8 | 同上 |
| AlmaLinux9.8 | 478 | 3.12.15 | 同上 |

すべてQt Virtual Keyboardのアーカイブ項目は0件。AGPL/GPL/LGPL、第三者告知、Python・インストール依存の文書、既存暗号化告知を含む。完全なネイティブ構成要素の一覧や告知の網羅性を証明する結果ではない。各OSの実行ファイルハッシュ、埋込文書ハッシュ、ネイティブ項目、Pillowの機能別版は[入力監査JSON](linux-amd64-release-input-audit-2026-11-12.json)に保存した。Pillowのzlib表示などにOS差があり、同じPythonパッケージ版だけでネイティブ構成を同一と判断しない。

5候補ともdependency_sourcesはNOT INCLUDEDのまま。既存crypto-native-sources.jsonはWindows AMD64の記録であり、Linuxのネイティブバイナリとはハッシュが異なる。バイナリの誤りという意味ではなく、その記録をLinuxのバイナリ照合済み証拠として流用できない。今回Linux側で収集した記録も、過去の候補へ後付けで埋め込んだとは扱わない。

## 公開0.3.4との差分

この比較を基に[専用コピーで0.3.5の未公開統合案](linux-public-integration-review_ja.md)を後続で準備・ソース検証した。元作業ツリーの版と公開物は変更していない。

ローカルに保存済みの公開Linuxコミット`eeacd06a49cda85ddc1d432bd785e507f8006a89`と、現在HEAD`423e59471b576e4732c7d6ec0ad9ab25cbf19582`および未コミット作業を比較した。共通祖先は`110f95a6b98a450d4d47f0128da84ed8039ffa2d`。Gitの取得・マージは行っていない。

| 項目 | 現在の状態と統合時の扱い |
| --- | --- |
| アプリ版 | 公開Linuxは0.3.4、現在の検証入力は0.3.3/build1。次の公開版を決める工程が必要。今回変更なし |
| Qt Virtual Keyboard | 公開側の除外を現在の未コミットspecでも維持 |
| 画像取込後処理 | 現HEADにはダイアログ破棄、タイマー切断、例外時のパイプ解放など公開コミットにない変更がある。公開側への丸ごと置換で失わない |
| サムネイル | 現在の未コミット修正と回帰テストは公開0.3.4にない。保持して統合 |
| ソースZIP | 現HEADにはSOURCE_DATE_EPOCHとZIP属性を正規化する処理がある。公開側の旧処理で置き換えない |
| アイコン | assetsに差がある。公開コミットの資産を一括復元せず、次候補の入力として明示して記録 |
| Linux配布告知・旧スクリプト | 公開側のLinux-distribution.txtとbuild-release-candidate.shは現HEADにない。旧告知は0.3.4・DEB/Snap・依存ソース提供を前提とするため、そのまま新RPM候補へコピーしない |
| 新RPMモード | Fedora/SUSE/Alma別ヘルパー・spec・拒否テストは未コミット。現在の作業を保持 |

具体的な差分と未追跡実装一覧は入力監査JSONに含む。この比較だけでアプリ版統合や全OSの回帰試験を完了とはしない。

## AlmaLinux9の依存ソース収集

許可済み専用Build環境の新規ディレクトリへ、既存収集ツールを使って取得した。ダウンロードしたコードは実行せず、tar内文書はファイルシステムへ展開していない。

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/dependency-audit-20261112/
  sources/   固定版sdist、Rust crates、OpenSSL、取得記録
  notices/   Linux上で再生成した告知・暗号化ネイティブ記録
```

- cryptography50.0.2、CFFI2.1.1、pycparser3.12、PyMuPDF1.28.2、Pillow12.3.0のsdistをPyPIのSHA-256と照合した。
- cryptographyのCargo.lockにあるレジストリ依存32件をlock内チェックサムと照合。OpenSSL4.0.3を上流配布のチェックサムと照合した。Cargo一覧はビルド用依存も含む上位集合である。
- Alma候補内のcryptography/CFFIの2ネイティブバイナリが、Linux収集記録の導入済みバイナリと一致した。cryptographyバックエンド表示は5環境ともOpenSSL4.0.3で、Pythonのssl版とは区別した。
- 再生成したOpenSSL/CFFI告知は改行正規化後に既存文書と一致。Rust告知も空行を除いた行の比較で一致した。バイトハッシュは異なるため、比較条件を記録した。
- PySide6/Essentials/Addons/shiboken6はPyPI sdistなしとしてupstream-source-requiredを記録。その後、Qt/Qt for Python/ShibokenとMuPDFの公式アーカイブを[別工程で収集・照合した](linux-almalinux9-qt-mupdf-source-audit_ja.md)。wheelビルド来歴の確認は残る。

取得・生成した54ファイルの版・URL・サイズ・SHA-256、2コマンドの終了コード0、Linux固有ネイティブ記録と既存告知比較は[Alma依存ソースJSON](linux-almalinux9-dependency-source-audit-2026-11-12.json)に保存した。取得ソース本体は上記WSL内に保持し、この文書やJSONだけにソースが含まれるとは扱わない。既存候補・リポジトリの告知・配布物は変更していない。

## 次に必要な確認

1. Qt/Qt for Python/Shiboken、PyMuPDFが指定するMuPDFと内包第三者コード、Pillowの画像ライブラリ、Python・PyInstallerブートローダー、同梱OS共有ライブラリのソース・パッチ・ビルド条件・告知を対象ごとにそろえる。sdist取得だけを完了条件にしない。
2. wheelと収集ソースのビルド来歴を確認する。Almaの2ネイティブハッシュ照合を他OS全体の来歴証明として流用しない。
3. 収集結果を次のソース入力・配布告知へ反映し、新候補をビルドしてソース対応、導入・GUI・ライセンス表示を再確認する。既存候補の埋込記録は変更しない。
4. 公開版との統合・版決定、通常デスクトップ・アプリ版間移行などの残試験後に、公開用ファイル一覧とリンクを整える。現在は公開しない。

全体方針は[ライセンスと配布](license-distribution_ja.md)、既存Windows暗号化記録の範囲は[暗号化依存調査](crypto-dependency-audit_ja.md)、OS別到達点は[拡張計画](linux-amd64-expansion-plan_ja.md)を参照。
