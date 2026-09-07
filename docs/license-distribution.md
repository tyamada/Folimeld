# ライセンスと配布

Folimeld は AGPL-3.0-only です。`LICENSE` はプロジェクトの告知、
`licenses/AGPL-3.0.txt` は GNU から取得したライセンス全文です。
バージョン情報から、これらの文書と第三者ライブラリの告知を閲覧できます。

Windows / Linux / macOS の PyInstaller spec は `tools/license_bundle.py` を使い、
全文・告知・ビルド環境の依存パッケージのバージョンと付属ライセンス・Python の
ライセンスを同梱します。MSIX / deb / Mac App Store パッケージもこの実行物を使います。
ビルド時の文書取得にネットワークは使用しません。

## 配布前に必要な確認

- 実行物に対応する Folimeld のソース、ビルドスクリプト、依存バージョンを保存し、
  バイナリのダウンロード場所から取得できるようにしてください。リポジトリの
  トップへのリンクだけでは、対応するソースを提供したことにはなりません。
- PyMuPDF / MuPDF の AGPL と Qt / PySide6 の LGPL の条件に従い、実際に同梱した
  バージョンの対応ソース（必要な依存コードや変更を含む）を提供してください。
  LGPL ライブラリを変更したものと組み合わせて再ビルド・実行できる手段も維持します。
- Qt、MuPDF、Python などに内包される第三者コードのライセンスを、対象OSと実際に
  梱包したバイナリに照らして確認し、必要な著作権告知を `licenses/` に追加してください。
  wheel の付属文書の自動収集だけで、内包コードの告知が網羅される保証はありません。
- Store の利用条件、DRM、署名・再インストールの制約が AGPL / LGPL に基づく
  利用者の権利と両立するか、配布経路ごとに確認してください。

今回の表示・同梱修正は、対応ソースの公開や、全OSの最終配布物のライセンス監査を
完了するものではありません。依存関係を更新した場合にも上記の確認が必要です。

## 一次資料

- GNU AGPL v3（第4～6条など）: https://www.gnu.org/licenses/agpl-3.0.html
- GNU LGPL v3（第4条）: https://www.gnu.org/licenses/lgpl-3.0.html
- Qt: https://doc.qt.io/qt-6/licensing.html
- Qt 内の第三者コード: https://doc.qt.io/qt-6/licenses-used-in-qt.html
- PyMuPDF: https://pymupdf.readthedocs.io/en/latest/faq/index.html
- PyWinRT: https://github.com/pywinrt/pywinrt

`licenses/` の GNU ライセンス全文は https://www.gnu.org/licenses/ の各 `.txt`、
`PyWinRT.txt` は PyWinRT v3.2.1 の `LICENSE` から取得しました。
