# Folimeld

Folimeld は、PySide6 と PyMuPDF を使って作成した PDF ページ編集アプリです。Windows、macOS、Ubuntu Linux で動作し、ページの並べ替え・回転・挿入・削除・パスワード保護などを GUI から操作できます。

## 主要機能

- PDF のページ一覧表示
- 複数ページ選択による並べ替え
- 90° 単位の回転
- ページ挿入と削除
- 空白ページの追加
- PDF のプロパティ閲覧・編集（PDF バージョン、ページレイアウト、綴じ方向）
- パスワード付き PDF の保護/解除
- 公式の言語切替対応（日本語・英語など）

## セットアップ

### Windows

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

### macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### Ubuntu

Ubuntu 22.04以降を想定しています。最初にQtの実行に必要なライブラリとPython環境を用意します。

```bash
sudo apt update
sudo apt install python3-venv libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## 起動

### Windows

```bat
.venv\Scripts\python main.py
```

### macOS / Ubuntu

```bash
. .venv/bin/activate
python main.py
```

## 使い方

- 複数ページは Ctrl または Shift を押しながら選択できます。
- 選択したページはツールバーまたはドラッグ操作で移動・並べ替えできます。
- 選択中のページを回転・削除・挿入できます。
- 文書のプロパティの「詳細」タブでは、PDF バージョンやページレイアウトを変更できます。ページレイアウトに `TwoPageLeft` または `TwoPageRight` を指定した場合、PDF バージョンが 1.5 未満なら、保存時に 1.5 へ自動的に引き上げられます。
- ローカル設定は QSettings に保存され、最後に開いたフォルダが記憶されます。

## 実行ファイルの生成

### Windows

```bat
build_exe.bat
```

生成物は `dist\Folimeld.exe` です。PySide6、PyMuPDF、翻訳データを内包するため、配布先に Python や付属ファイルは不要です。

### macOS

```bash
./build_exe.sh
```

このスクリプトは `.venv` が無い場合でも自動で作成し、依存関係と PyInstaller を入れてからビルドします。生成物は `dist/Folimeld.app` です。`dist/Folimeld` も併せて作成されますが、通常は `.app` を開いて使用します。

生成後は次のように起動できます。

```bash
open dist/Folimeld.app
```

macOS では Windows のレジストリ連携は自動的に無効化されます。

### Ubuntu

```bash
bash build_linux.sh
```

Pythonを含む単体実行ファイル `dist/folimeld` と、デスクトップメニュー・アイコン・PDF関連付けを含むUbuntuパッケージ `dist/folimeld_<バージョン>_<アーキテクチャ>.deb` が生成されます。ビルドは配布先と同じか、それより古いUbuntu上で行ってください。

パッケージは次のようにインストールできます。

```bash
sudo apt install ./dist/folimeld_*.deb
```

インストール後はアプリ一覧から Folimeld を起動でき、ファイルマネージャーの「別のアプリケーションで開く」からPDFを渡せます。インストールせず `./dist/folimeld` を直接起動することもできます。

## 配布時の注意

- 本アプリは Windows、macOS、Ubuntu Linux を想定しており、Windows 専用のレジストリ連携は他OSでは自動的に無効化されます。
- macOS の配布用アプリは ad-hoc 署名を行っているため、ローカル環境ではそのまま起動できます。
- 署名済みの正式配布を行う場合は、Apple 開発者証明書で署名し直す必要があります。

## 開発について

このアプリは、OpenAI Codex を使用して作成しました。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

PySide6 や PyMuPDF などの第三者ライブラリには、それぞれのライセンスが適用されます。

## バージョン履歴

- v0.2.3 - 2026/08/31: PDF バージョンを自動的に変更
- v0.2.2 - 2026/08/30: macOS 向けのビルド手順とアイコン/署名を整備
- v0.2.1 - 2026/08/30: macOS 互換の Windows 依存処理を安全に無効化
- v0.2.0 - 2026/08/30: アプリ名を Folimeld に変更
- v0.1.0 - 2026/08/29: 最初のリリース
