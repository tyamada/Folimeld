# FreeBSDパッケージの作成・導入確認

検証日: 2026-11-09（日本時間）。パッケージはローカル配布候補で、GitHub Releasesへの公開は未実施。

## 成果物

`dist/freebsd/` に以下を用意した。ビルド出力のためGit管理には含めない。

- `folimeld-0.3.3_1.pkg`: FreeBSD 15.1 / amd64向け、約25 MB。
- `Folimeld-source-9ceb5ec75dcd3ddb60bb66f0b6996da5e700cf4400bd89b31808f5250b19f23b.zip`: ビルド時の対応ソース。作業ツリーの変更を含むことをマニフェストに記録。
- `pymupdf-1.28.2-cp312-abi3-freebsd_15_1_release_p5_amd64.whl`: 再構築用のネイティブwheel。
- `dependency-sources/`: PyMuPDF 1.28.2とMuPDF 1.28.2のソースアーカイブ、PyPIの取得記録。
- `build-record.json`、`SHA256SUMS.txt`: ソース・wheel・パッケージの対応とチェックサム。

最終pkgのSHA-256:

```text
e44f9519f04164ec7064494c0d7f354fcb778b1fbeeb2404c9f484699c3f4c0e
```

[ビルド記録](freebsd-package-verification/build-record.json)に、ネイティブ実行環境、公式依存の版・origin、対応ソースとwheelのハッシュを保存した。

## 構成

`tools/build_freebsd_package.py` がソースZIPのマニフェストを照合し、標準の `pkg create` で作成する。ファイルはroot:wheel所有、起動スクリプト0755、その他0644。インストール先は `/usr/local`。

Python 3.12、PySide6、Pillow、cryptography、psutil、日本語フォント `noto-sans-jp` は公式パッケージに依存する。PyMuPDF/MuPDF 1.28.2をアプリ専用領域に同梱し、システムの旧版を参照しない。

## 確認結果

| 検証 | 結果 |
| --- | --- |
| 通常VMへのpkg導入 | 成功。`pkg check -d`、`pkg check -s`も成功 |
| 通常VMでの実GUI操作 | 一般ユーザーで起動し、フォームPDFを表示、先頭ページを90度回転、別名保存、再読込。[画面](freebsd-package-verification/gui-saved.png) |
| クリーン環境への導入 | 新規にFreeBSDのbaseを展開したchrootへ、公式依存と候補pkgだけを導入。開発用仮想環境・チェックアウトへの参照なし |
| クリーン環境でのGUI | 非特権ユーザーで起動しフォームPDFを表示。[画面](freebsd-package-verification/clean-gui.png) |
| フォーム・ワーカー | フォームの値、回転、Undo/Redo、保存・再読込、PNGと2フレームTIFFからの3ページ生成、画像PDFの保存・再読込が成功。終了コード0 |
| 削除・再導入 | 成功。起動スクリプトが削除され、検証用ユーザーPDFが残ることを確認して再導入 |
| ソース・wheel・pkgの対応 | ビルド記録のSHA-256と実ファイルが一致 |
| ツール関連テスト | `test_freebsd_package.py` と `test_source_bundle.py` の8件成功。Ruffと既定のmypyも成功 |

クリーン検証は同じVM内のchrootで行い、カーネルとXサーバーを共有した。初回展開後に通常の起動処理に相当する `ldconfig onestart` を実行し、共有ライブラリキャッシュを初期化した。

最初は日本語フォント不足でメニューが四角になったため、`noto-sans-jp` をパッケージの依存とREADMEのインストール手順に追加した。Qt関連の公式依存は約280パッケージに展開された。導入される量は公式リポジトリの構成により変わる。

[自動スモークスクリプト](freebsd-package-verification/smoke.py)はインストール先だけを `PYTHONPATH` に指定して実行し、[出力](freebsd-package-verification/clean-smoke.txt)を保存した。初版スクリプトは処理成功後のQtオブジェクト破棄で異常終了したため、QApplicationの破棄前にウィジェットを明示的に破棄するよう修正した。修正後は終了コード0。

今後の別バージョンからのアップグレード、別のFreeBSD版・CPU、公式Portsでのビルドは未検証。インストール手順は[日本語](freebsd-install_ja.md)／[English](freebsd-install.md)を参照。
