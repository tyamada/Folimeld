# Folimeld

Folimeld は、PySide6 と PyMuPDF を使って作成した PDF ページ編集アプリです。Windows と macOS の両方で動くことを想定しており、ページの並べ替え・回転・挿入・削除・パスワード保護などを GUI から操作できます。

## 主要機能

- PDF のページ一覧表示
- 複数ページ選択による並べ替え
- 90° 単位の回転
- ページ挿入と削除
- 空白ページの追加
- PDF のプロパティ閲覧
- パスワード付き PDF の保護/解除
- 公式の言語切替対応（日本語・英語など）

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

## 使い方

- 複数ページは Ctrl または Shift を押しながら選択できます。
- 選択したページはツールバーまたはドラッグ操作で移動・並べ替えできます。
- 選択中のページを回転・削除・挿入できます。
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

## 配布時の注意

- 本アプリは Windows と macOS の両方を想定しており、Windows 専用のレジストリ連携は macOS では自動的に無効化されます。
- macOS の配布用アプリは ad-hoc 署名を行っているため、ローカル環境ではそのまま起動できます。
- 署名済みの正式配布を行う場合は、Apple 開発者証明書で署名し直す必要があります。

## 開発について

このアプリは、OpenAI Codex を使用して作成しました。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

PySide6 や PyMuPDF などの第三者ライブラリには、それぞれのライセンスが適用されます。

## リリースページ見出し

### 何ができるアプリか

Folimeld は、PDF のページ整理をスムーズに行えるシンプルな編集ツールです。ページの並べ替え、挿入、削除、回転、パスワード保護の管理を GUI で行えます。

### 対応環境

- Windows 11
- macOS 13 以降

### ダウンロード方法

リリース版の配布物をダウンロードするには、GitHub の Releases ページから最新のアセットを取得してください。

#### macOS

- `Folimeld.app` をダウンロードして、Finder から開きます。
- もし Gatekeeper により起動がブロックされた場合は、以下を実行してローカルで許可してください。

```bash
xattr -dr com.apple.quarantine "dist/Folimeld.app"
```

#### Windows

- `Folimeld.exe` をダウンロードして実行してください。
- 実行時に Windows Defender などの警告が出る場合は、ローカルの安全性確認を行ってください。

## スクリーンショット

以下は、GitHub のリリースページや README で表示するための実際のスクリーンショットです。

![Folimeld main window](docs/screenshots/main-window.png)

PDF の一覧を見ながら、ページの並べ替えや回転を直感的に行えます。

![Folimeld password dialog](docs/screenshots/password-dialog.png)

パスワード付き PDF の保護と解除を、ダイアログの操作だけで完結できます。

## リリースノート形式

```markdown
## v0.2.2

### 変更点
- macOS 向けのビルド手順を整理
- Windows 専用依存処理の安全な無効化を追加
- 配布用アプリのアイコンと ad-hoc 署名を追加

### 修正点
- macOS の典型的なロケール `C` / `posix` で言語選択が失敗する問題を修正
- `.venv` 未作成時のビルド失敗を自動回復するよう修正

### 対応環境
- Windows 11
- macOS 13 以降
```

## バージョン履歴

- v0.2.2 - 2026/08/30: macOS 向けのビルド手順とアイコン/署名を整備
- v0.2.1 - 2026/08/30: macOS 互換の Windows 依存処理を安全に無効化
- v0.2.0 - 2026/08/30: アプリ名を Folimeld に変更
- v0.1.0 - 2026/08/29: 最初のリリース
