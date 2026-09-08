# Android最小試作

## 現在の状態

既存の `folimeld/model.py` の `PdfDocument` を使った試作画面を実装しています。
デスクトップ版とは別のエントリーポイントです。

- PDFを選択してアプリ内の一時領域にコピー
- 1ページずつプレビューし、前後へ移動
- 表示ページを90度回転
- 別の保存先へPDFを書き出し
- 未保存の変更がある場合、開き直し・終了前に確認

**APKはまだ生成していません。Android実機での動作も未検証です。**
Windows上のテスト成功は、Android向けネイティブライブラリやファイル選択の動作保証にはなりません。

## ローカル起動

リポジトリのルートで実行します。既存の開発用仮想環境を利用できます。

```powershell
.venv\Scripts\python -m folimeld.android_probe
```

Linux / macOSでは、同じ依存をインストールした環境で実行します。

```bash
python -m folimeld.android_probe
```

試作のボタン表記は英語です。パスワード付きPDF、ページ並べ替え、複数選択、課金は対象外です。
プレビューは長辺720px以下で、現在の1ページだけを描画します。
ファイルコピーやPDF処理は同期実行のため、大きなPDFでは画面が一時停止することがあります。
作業コピーは通常終了時に削除しますが、強制終了時の回収や編集状態の復元は未実装です。

## Androidのファイル入出力

Androidのネイティブファイル選択が返す `content://` URIを、Pythonの `open()` や
PyMuPDFへ直接渡さず、Qtの `QFile` で読み書きします。通常のファイルパスも同じ処理を通ります。
読み込み後はアプリの一時領域のPDFを `PdfDocument` で編集します。
書き出し時は文書のコピーを既存モデルで保存してから、選択された保存先へ転送します。
書き出し失敗時は編集中の状態を保持します。

書き出し先に既存ファイルを選んだ場合は、そのファイルを上書きします。
プロバイダーへの書き込み途中で失敗した場合、書き出し先に不完全なファイルが残る可能性があります。
最初の実機テストでは新しい名前で書き出してください。

QtがAndroidのURIに対応することは[QFile公式資料](https://doc.qt.io/qt-6/qfile.html)で確認しています。
この試作でのDocuments Provider、ダウンロード、Google Drive経由の選択・保存は実機確認が必要です。

## ビルド調査結果

2026-09-08に確認した内容：

- ローカル環境：Python 3.14、PySide6 6.11.2、PyMuPDF 1.28.2。
- WSL Ubuntu 24.04：Python 3.12.3あり。`java`、`adb`、`pyside6-android-deploy` はPATH上になし。
  標準候補の `~/Android/Sdk`、`~/.pyside6-android-deploy`、`/opt/android-sdk` も見つかりませんでした。
- PyMuPDF 1.28.2の[公式PyPIメタデータ](https://pypi.org/pypi/PyMuPDF/1.28.2/json)にAndroid用wheelはありません。
- [python-for-androidのdevelopブランチ](https://github.com/kivy/python-for-android/tree/develop/pythonforandroid/recipes)に
  名前に `mupdf` を含むビルドレシピはありませんでした。

これはAndroidでの動作が不可能という意味ではありません。
通常の `pip install` とQtのパッケージ化だけでは足りず、PyMuPDFとMuPDFの
Android向けクロスビルド・組み込みを別途検証する必要があります。
Linux用wheelをAndroid用として流用してはいけません。

## 次のビルド作業

1. PyMuPDF 1.28.2と同版が使用するMuPDFについて、Android NDKでのビルド方法を確立する。
   python-for-androidのカスタムレシピ等でPython拡張と依存共有ライブラリを組み込む。
   最初は `arm64-v8a` または `x86_64` のどちらか一方を選び、対応する実機またはエミュレーターで検証する。
2. Linux環境にJDK、Qt版に対応するSDK／NDK、PySide6／Shiboken6のAndroid wheelを用意する。
   バージョンとPython ABIを揃える。手順は[Qt公式Android配布ガイド](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-android-deploy.html)を参照する。
3. 以下で最小ソースだけをステージングする。ユーザーのPDF、既存ビルド、デスクトップUIを含めない。

   ```powershell
   .venv\Scripts\python tools/stage_android_probe.py
   ```

   出力は `build/android-probe/`。このディレクトリの `main.py` がAndroid用エントリーポイントです。
   ビルド用仮想環境は、このステージングディレクトリの外に作ります。

4. ステージング先で `pyside6-android-deploy --init` により設定を生成し、
   SDK／NDKとAndroid wheelを設定する。PyMuPDFのカスタムレシピ・依存指定も統合する。
   **設定生成だけではPyMuPDFは同梱されません。現段階では完成済みのビルド設定を提供していません。**
5. debug APKを生成し、端末で `import fitz`、PDF読み込み、レンダリング、回転、書き出しを検証する。
   続いて別CPU、署名付きAAB、ストア要件への対応を進める。

## 検証

```powershell
.venv\Scripts\python -m pytest tests/test_android_probe.py -q -p no:cacheprovider
```

ローカルで確認する項目：書き出したPDFのページ数・回転・テキスト保持、入力ファイルの保持、
読み込み／保存失敗時の編集状態保持、分割コピーと切り詰め、画面のページ移動と回転。

実機で残る項目：ネイティブ依存のロード、URIの選択・キャンセル・保存、書き出しPDFの再選択、
オフライン操作、タッチ・マウス操作、ウィンドウ変更、スリープ・強制終了時の挙動。
