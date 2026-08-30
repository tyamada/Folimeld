# Folimeld

PySide6 と PyMuPDF を使った PDF ページ編集アプリです。Windows と macOS の両方で起動することを想定して作成しています。

## セットアップ

### Windows

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## 起動

### Windows

```bat
.venv\Scripts\python main.py
```

### macOS / Linux

```bash
. .venv/bin/activate
python main.py
```

複数ページは Ctrl または Shift を押しながら選択できます。選択ページはツールバーで移動・回転でき、サムネイルのドラッグでも並べ替えられます。

## 単体実行ファイルの作成

### Windows

```bat
build_exe.bat
```

生成物は `dist\Folimeld.exe` です。PySide6、PyMuPDF、翻訳データを内包するため、配布先にPythonや付属ファイルは不要です。

### macOS

```bash
chmod +x build_exe.sh
./build_exe.sh
```

生成物は `dist/Folimeld.app` または `dist/Folimeld` 形式になります。macOS では Windows のレジストリ連携は自動的に無効化されます。

## 開発について

このアプリは、OpenAI Codexを使用して作成しました。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

PySide6やPyMuPDFなどの第三者ライブラリには、それぞれのライセンスが適用されます。

## バージョン履歴

- v0.1.0 - 2026/08/29:  最初のリリース
- v0.2.0 - 2026/08/30:  アプリ名をFolimeldに変更
- v0.2.1 - 2026/08/30:  macOS 互換の Windows 依存処理を安全に無効化
