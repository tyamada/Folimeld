# FreeBSDでの画像取り込み・保存失敗・負荷試験

検証日: 2026-11-09（日本時間）。[フォーム修正後の環境](freebsd-forms-fix_ja.md)で追加検証した。

## 結果

| 項目 | 確認結果 |
| --- | --- |
| 画像フォルダー取り込み | PNG、JPEG、2フレームTIFFを自然順で読み込み、計4ページを表示・保存・再読込できた。非画像のTXTは対象外になった |
| 不正画像の取り込み | 正常PNGと壊れたJPEGを選択すると、JPEG名を含むエラーを表示した。ダイアログを閉じて中止すると、読み込み前の4ページ文書が保持された |
| 保存先の書き込み拒否 | 保存先ディレクトリーを0555にして回転後に上書き保存すると、PermissionErrorを表示した。元PDFのバイト列、未保存の編集、Undo/Redoを保持した |
| 保存失敗からの復旧 | 保存先を0755に戻し、同じGUIセッションで再保存できた。再読込後も4ページ、先頭のみ90度回転だった |
| GUIでの多ページ表示 | 合成テキストPDF 1000ページを開き、Ctrl+Endで末尾、Ctrl+Homeで先頭へ移動・再表示できた |
| 自動負荷試験 | テキスト100ページ、画像100ページ、テキスト1000ページを別プロセスで各3回実行し、9回すべて完了した。入力PDFのSHA-256不変、Undo/Redo成功を確認した |

上記操作中の異常終了はなかった。取り込み・保存のアプリ本体に追加修正は必要なかった。

## 環境と操作方法

VirtualBox VM `Folimeld-FreeBSD-15.1-amd64`（8 GiB RAM、4 vCPU、WindowsホストのNEM実行）を使用。FreeBSD 15.1-RELEASE-p5、Python 3.12.15、PyMuPDF/MuPDF 1.28.2、PySide6 6.11.2、Pillow 13.0.0、psutil 7.2.2、cryptography 50.0.1。
アプリと計測は `/home/folimeld/Folimeld/.venv-freebsd/bin/python` を使用した。

computer-useでVirtualBoxのGUIを操作し、キー入力のみVirtualBoxの `keyboardputstring` / `keyboardputscancode` を使用した。画像取り込み・編集・保存・再読込はアプリのGUIから実行した。SSHは検証用素材の生成、専用ディレクトリーの権限変更、保存結果の独立照合、計測に使用した。

検証用ファイルはゲストの `build/freebsd-extended-verification/` 配下。既存のユーザーファイルは使用していない。保存先ディレクトリーの権限は検証後に0755へ戻した。

## 画像と保存失敗の照合

`images-ok/page1.png`、`page2.jpg`、`page10.tiff` を用意した。各画像は640×480、150 DPIで、TIFFは2フレーム。背景色は順に水色・薄緑・薄黄・ピンクとした。GUIの一覧は自然順の1、2、10で、出力PDFの4ページの中央色もこの順に一致した。

画像取り込み後、`save-target/images.pdf` へ保存した時点のSHA-256:

```text
9ab77bfbf3c65f589ea3b65d9d7bfd58f796f7572726b2b6340b01938932fe97
```

専用の `save-target/` を0555にし、先頭ページを右90度回転して「保存」を押した。保存先に一時PDFを作成する段階で書き込み拒否となり、エラー前後で上記SHA-256は一致した。タイトルの未保存表示と回転が残り、元に戻すと横向き、やり直すと縦向きになった。0755へ戻して再保存すると未保存表示が消えた。

再保存後のSHA-256は `0de4de6951f4169cc7bb116378912f1af53d8891d89c2f09a20e71641108c044`。
[独立照合JSON](freebsd-extended-verification/images-verification.json)にページ数、回転、用紙寸法、中央のRGB値を記録した。

- [保存失敗時の画面](freebsd-extended-verification/save-permission-error.png)
- [不正画像のエラー画面](freebsd-extended-verification/image-import-error.png)
- [再保存・再読込後の画像PDF](freebsd-extended-verification/images-reopened.png)
- [1000ページ文書の末尾側表示](freebsd-extended-verification/load-1000-end.png)

容量不足、ディスク切断、電源断はこの試験には含めていない。

## 負荷試験

既存の `tools.benchmark_pdf` を `QT_QPA_PLATFORM=offscreen` で実行した。各条件は1回ごとに新しいPythonプロセスで実行し、計測中はGUIを操作しなかった。各回で生成入力をハッシュ検証し、全ページのサムネイル走査、回転、Undo/Redo、並べ替え、保存を実行した。

```sh
env QT_QPA_PLATFORM=offscreen .venv-freebsd/bin/python -m tools.benchmark_pdf --pages 100 --output build/freebsd-extended-verification/text-100-1.json
env QT_QPA_PLATFORM=offscreen .venv-freebsd/bin/python -m tools.benchmark_pdf --pages 100 --image-size 256 --output build/freebsd-extended-verification/images-100-1.json
env QT_QPA_PLATFORM=offscreen .venv-freebsd/bin/python -m tools.benchmark_pdf --pages 1000 --output build/freebsd-extended-verification/text-1000-1.json
```

末尾番号を1～3にして各3回実行。画像条件は各ページに異なる256×256 RGB画像を埋め込む。入力サイズはテキスト100ページ32,953 bytes、画像100ページ19,728,289 bytes、テキスト1000ページ333,065 bytes。

時間は中央値（最小～最大）、単位ms。読み込みはモデルのopenのみで、初回描画や全ページ走査は別計測。

| 条件 | 読み込み | 初回サムネイル | 全ページ走査 | 回転 | 保存 |
| --- | --- | --- | --- | --- | --- |
| テキスト100ページ | 1.11（0.52～1.15） | 45.14（40.45～54.91） | 269.50（264.41～277.17） | 15.73（14.80～16.60） | 9.92（9.03～10.83） |
| 画像100ページ | 0.69（0.59～0.74） | 44.39（42.51～44.68） | 461.07（460.49～463.03） | 376.67（369.62～378.62） | 118.43（117.30～119.22） |
| テキスト1000ページ | 1.46（0.37～3.13） | 41.32（40.76～57.38） | 2388.31（2360.53～2418.39） | 144.29（108.69～146.83） | 195.21（192.64～195.30） |

| 条件 | サンプリング最大RSSの中央値（最小～最大）、MiB | 常駐サムネイル最大数 |
| --- | --- | --- |
| テキスト100ページ | 142.98（142.87～143.09） | 24 |
| 画像100ページ | 308.88（308.04～309.21） | 24 |
| テキスト1000ページ | 146.08（146.06～146.10） | 24 |

RSSはプロセス全体を5 msごとにサンプリングした値で、短時間のピークを取り逃がし得る。履歴のディスク退避は今回の条件では発生していない。この計測はVM上の合成入力に対する結果で、物理マシンでの性能や長時間連続運用、複雑な実PDF、大容量画像の上限を保証しない。offscreen計測値からGUIの入力応答時間は判断しない。

生データは `freebsd-extended-verification/` の `text-100-{1,2,3}.json`、`images-100-{1,2,3}.json`、`text-1000-{1,2,3}.json`。同名の `.txt` に実行時出力を保存した。

## 計測ツールの修正とチェック

初回実行ではPDF操作完了後、結果出力時の `importlib.metadata.version("PySide6")` が `PackageNotFoundError` になった。FreeBSDのpkgから導入したPySide6はimportできるが、Python配布メタデータが見つからないためだった。
`tools/benchmark_pdf.py` の依存ライブラリの版取得を、実際に読み込んだモジュールの版情報へ変更した。修正後の9回で版情報を含むJSON出力に成功した。

- Windows、FreeBSDとも `tests/test_benchmark_pdf.py`: 3 passed。
- `ruff check tools/benchmark_pdf.py`: 成功。
- リポジトリ既定の `python -m mypy`（指定された3ファイル）: 成功。
- 参考として対象外の計測ツールを直接指定したmypyは、既存の未注釈関数・依存モジュール等で105件のエラーになった。型検査範囲の拡大は行っていない。
- `git diff --check`: 成功。

既存のFreeBSD検証記録が参照する `.log` をGitに含められるよう、`.gitignore` に検証用2ディレクトリーだけの除外例外も追加した。

## 最終確認

追加検証後の差分を含め、全件テストを再実行した（2026-11-09）。

- Windows: 395 passed、32 subtests passed。[JUnit XML](freebsd-extended-verification/final-pytest-windows.xml)
- FreeBSD: 386 passed、9 skipped、32 subtests passed。スキップはWindows固有のテスト。[JUnit XML](freebsd-extended-verification/final-pytest-freebsd.xml)
- リポジトリ全体の `ruff check .` と既定の `python -m mypy`: 成功。
- FreeBSD関連の全検証文書の相対リンクと `git diff --check`: 成功。

修正と検証記録を同じ変更セットにまとめた。リリース公開は行っていない。
