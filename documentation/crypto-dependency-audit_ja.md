# 暗号化のネイティブ依存調査

[日本語](crypto-dependency-audit_ja.md) | [English](crypto-dependency-audit.md)

対象はWindows x64の暗号化機能に追加した依存であり、Folimeldの依存全体ではありません。[機械可読の記録](../licenses/crypto-native-sources.json) に実ネイティブバイナリ、ソースアーカイブのハッシュ、Cargo.lockのハッシュ、取得先URL、告知のハッシュを保存しています。依存更新やwheel・対象OSの変更時は再確認します。ライセンス適合の認定や、上流wheelが無改変のソースから作られたことの証明ではありません。

| 構成要素 | 確認した版 | 収集した資料 |
| --- | --- | --- |
| cryptography | 50.0.2 | PyPIのソース配布物とチェックサム、付属Apache/BSDライセンス、導入済みネイティブバインディングのSHA-256 |
| cryptography内のOpenSSL | 4.0.3（バックエンド表示は29 Sep 2026） | 公式配布のSHA-256と照合したリリースアーカイブ、`licenses/OpenSSL.txt` の法的文書 |
| Rust依存 | Cargo.lockのレジストリ依存32件 | lockファイルのチェックサムと各`.crate`を照合、`licenses/Cryptography-Rust.txt` にライセンス文書を収集 |
| CFFI | 2.1.1 | PyPIのソース配布物とチェックサム、導入済みネイティブバインディングのSHA-256、`licenses/CFFI-libffi-x64.txt` に内包x86/x64 libffiの著作権ヘッダーを収集 |
| pycparser | 3.12 | PyPIのソース配布物とチェックサム、既存のパッケージ告知収集でwheelのライセンスを取得 |

Rustの一覧にはビルド用・他プラットフォーム用の依存も含みます。ソース・告知を広めに保存したもので、Windows実行ファイルにリンクされたコードだけの一覧ではありません。OpenSSLの版はPythonの`ssl`モジュールとは別に、cryptographyのバックエンドへ問い合わせました。CFFI本体のライセンスだけで、内包libffiソースの別途保存した著作権告知を代用しません。

## 収集の再実行

配布ビルドの環境と実際に導入した固定版を使用します。取得したコードは実行せず、アーカイブ内のパスをファイルシステムへ展開しません。

```powershell
.venv\Scripts\python.exe tools/fetch_dependency_sources.py cryptography==50.0.2 cffi==2.1.1 pycparser==3.12
.venv\Scripts\python.exe tools/fetch_crypto_sources.py --cryptography-version 50.0.2 --cffi-version 2.1.1 --openssl-version 4.0.3
```

アーカイブは `dist/source/dependencies/`、生成した告知とマニフェストは `build/legal/crypto-native/` に保存します。内容を確認してから3つの`.txt`と`crypto-native-sources.json`を `licenses/` へコピーします。既存のパッケージspecとライセンス画面がテキストを取り込みます。告知を変更したらEXE・MSIXを再生成します。過去の配布物には後から反映されません。確認済みの依存アーカイブは最終アプリの対応ソースと一緒に保管・公開します。

## 残る確認

- 上流wheelのビルド来歴、コンパイラー・Rust標準ライブラリの告知、ビルドフラグ、パッチ、厳密なリンク済みコード一覧は未確認です。ソースの版とチェックサムの一致だけで、バイナリとソースの同等性は証明できません。
- OpenSSLソースの法的文書とCFFIのx86/x64ヘッダーは保存しました。実際のビルド構成・他のネイティブ構成要素に必要な告知の網羅性は最終確認が必要です。ARM64・Linux・macOSは別途確認します。
- Qt/PySide/Shiboken、PyMuPDF/MuPDF、Pillowの画像ライブラリ、Python、PyInstallerは、[ライセンスと配布](license-distribution_ja.md) の全体調査に残ります。今回の暗号化依存の調査で、全体調査やStore配布条件の確認を完了とはしません。

## 一次資料

- [OpenSSL公式のソース・チェックサム](https://www.openssl-library.org/source/)
- [cryptographyの導入とOpenSSLを静的リンクしたwheel](https://cryptography.io/en/latest/installation/)
- 各パッケージのソースと法的文書は、機械可読の記録にURL・SHA-256を記載しています。
