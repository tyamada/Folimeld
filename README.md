# Folimeld

Windows 11向けの、PySide6とPyMuPDFで作られたPDFページ編集アプリです。

## セットアップ

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## 起動

```bat
.venv\Scripts\python main.py
```

複数ページは Ctrl または Shift を押しながら選択できます。選択ページはツールバーで移動・回転でき、サムネイルのドラッグでも並べ替えられます。

## 単体EXEの作成

```bat
build_exe.bat
```

生成物は `dist\Folimeld.exe` です。PySide6、PyMuPDF、翻訳データを内包するため、配布先にPythonや付属ファイルは不要です。

`Folimeld.exe` を一度起動すると、WindowsエクスプローラーのPDFファイルの
「プログラムから開く」にFolimeldがユーザー単位で登録されます。

## 開発について

このアプリは、OpenAI Codexを使用して作成しました。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

PySide6やPyMuPDFなどの第三者ライブラリには、それぞれのライセンスが適用されます。

## バージョン履歴

- v0.1.0 - 2026/08/29:  最初のリリース
- v0.2.0 - 2026/08/30:  アプリ名をFolimeldに変更
