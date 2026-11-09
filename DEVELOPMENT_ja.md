# Folimeld 開発ガイド

[日本語](DEVELOPMENT_ja.md) | [English](DEVELOPMENT.md)

この文書では、開発環境の構築、テスト、ビルド、リリース用パッケージの作成方法を説明します。

## 技術構成

- Python 3
- PySide6 / Qt Widgets
- PyMuPDF
- Pillow（アイコン生成）
- PyInstaller（実行ファイル生成）
- pytest（テスト）

## 開発環境のセットアップ

### Windows

Windows版はIntel/AMD（x64）とARM（ARM64）の両方に対応しています。

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

### macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

### Ubuntu

Ubuntu 22.04以降を想定しています。

```bash
sudo apt update
sudo apt install python3-venv libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 fonts-noto-cjk
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt -c constraints-release.txt
```

`fonts-noto-cjk` は日本語、中国語、韓国語の表示に使用します。

### NetBSD（検証済み構成）

NetBSD 11.1 / amd64で、Python 3.12.14、PySide6 / Qt 6.11.2、PyMuPDF / MuPDF 1.28.2を使ったソース実行を確認しました。PySide6・PyMuPDFとビルド工具にはNetBSD向けの修正が必要です。構築方法、パッチ、全件テスト・GUI操作の結果は[検証記録](documentation/netbsd-verification_ja.md)を参照してください。NetBSD用の配布パッケージは作成していません。

検証記録に従って依存と `.venv-netbsd` を構築した後、リポジトリーのルートからX11セッション内で起動します。

```sh
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
.venv-netbsd/bin/python main.py
```

## 公開・非公開の配布方針

Windows・macOSのバイナリは非公開とし、ビルド・検証は手元で行います。Linuxのdeb/Snapは公開します。Linuxパッケージ、SHA-256一覧、対応ソースZIP、ビルド記録を同じReleaseにまとめる移行案は[こちら](documentation/linux-release-migration_ja.md)です。公開前の資材検査は以下で行えます。アップロードやタグ作成は行いません。

```bash
python -m tools.prepare_linux_release --version 0.3.3
```

CIの基準はPython 3.12です。今回のmacOS確認ではPython 3.14.6と制約ファイルの版で依存導入・テスト・ビルドを確認しました。新しい環境でもまず制約付きで導入してください。

## ソースから起動

Windows：

```bat
.venv\Scripts\python main.py
```

macOS / Ubuntu：

```bash
. .venv/bin/activate
python main.py
```

## テスト

```bash
python -m pytest -q
```

Windowsで仮想環境を直接指定する場合：

```bat
.venv\Scripts\python -m pytest -q
```

## 品質チェックと性能計測

GitHub Actions の [Checks](.github/workflows/checks.yml) は Python 3.12 を使い、Windows・Ubuntu 22.04・macOSで Ruff・mypy・pytest を実行します。Ruff は構文エラー・未定義名・未使用コードなどを検査し、mypy はモデル・履歴層を検査します。配布ビルドとCIは `constraints-release.txt` の主要依存バージョン制約を使用します。これはWindowsで確認したバージョンの記録で、他OS固有の依存や配布物の動作を保証するものではありません。依存更新時は制約ファイルも更新し、3 OSのCIと配布前の確認を行ってください。各ジョブのテスト結果と `pip freeze` を成果物として保存します。CIの追加・変更自体は、各OSでの成功や配布物の動作確認を意味しません。

```bash
python -m pip install -r requirements-dev.txt -c constraints-release.txt
python -m ruff check .
python -m mypy
python -m pytest -q -p no:cacheprovider
python -m tools.benchmark_pdf --pages 100 --output build/benchmarks/text-100.json
python -m tools.benchmark_pdf --pages 100 --image-size 256 --output build/benchmarks/images-100.json
python -m tools.benchmark_pdf --pages 1000 --output build/benchmarks/text-1000.json
```

計測はケースごとに新しいプロセスで行います。既存PDFは `--input path/to/document.pdf` で指定でき、保存先は一時ディレクトリになります。暗号化PDFはこのツールの対象外です。ページ数・画像量・ファイルサイズの異なる入力で各ケースを3回以上実行し、中央値とばらつきを比較してください。JSONには操作時間、サムネイル1バッチの最大時間、5ms間隔で標本化したプロセスRSS、依存バージョンを記録します。RSSはネイティブ領域を含みますが、短いピークを取り逃す可能性があります。画像生成とウィンドウ初期化は操作時間の対象外です。

初回の測定値と配布前の確認項目は [性能と配布検証](documentation/performance-and-release_ja.md) を参照してください。
Windows負荷テストの事前確認は [確認記録](documentation/windows-load-test_ja.md) にあります（当時は負荷テスト自体を未実施）。

計測ツールは初期表示に加えて文書全体をスクロールし、最大保持サムネイル数も記録します。大きなPDFでは表示範囲と前後のみ描画するため、`initial_thumbnails` は全ページの描画時間ではありません。`scroll_thumbnails` とメモリ使用量を合わせて比較してください。通常は最大64枚を保持しますが、非常に大きな画面で64枚を超えるページが見える場合は表示中の全ページを優先します。

## 保存・履歴・診断

通常保存は `garbage=3` を使い、ストリームの重複検査を省きます。GUIでは独立した文書を所有する別プロセスが一時出力を書き、成功後にモデルが保存先を置き換えます。準備・最終切替は同期処理で、保存中の編集・キャンセルはできません。性能計測ツールの保存時間は同期のモデルAPIを測定し、GUIのプロセス起動時間を含みません。

履歴はメモリ128 MiBと一時ファイル1 GiBを上限に保持します。`history_bytes` はメモリ内のPDFデータ量、`history_disk_bytes` は認証情報などを含むディスク上の暗号コンテナのバイト数です。スナップショットの生成・復元はPDF全体を扱い、一時メモリ使用量や編集待ち時間はこの上限では制限されません。履歴の退避、保存プロセス用の一時入力、画像変換の中間PDFは `folimeld/temporary_data.py` でAES-256-GCM暗号化し、読み込み時に全体の認証を完了してから平文を返します。ファイルごとにランダムな鍵とnonceを作り、鍵はファイルや設定には保存せず、履歴ではメモリ内、保存・画像変換ワーカーではプロセス間通信で渡します。大きなデータの暗号化は分割処理し、復号結果は認証完了までメモリ内に留めます。不要になった履歴は明示的に閉じて鍵への参照も解放し、保存・画像変換用の一時ディレクトリは処理終了時に削除します。

本体の強制終了やOS停止などで残留した暗号コンテナの自動回収、メモリ・ページファイル・クラッシュダンプからの完全消去は保証しません。画像変換は暗号文を直接書き出し、親プロセスで認証してメモリからPDFを開いた後に現在の文書を置き換えます。シリアライズと復号にはPDF全体分のメモリが必要です。保存先PDFには利用者が指定した暗号化設定を適用します。これらの範囲を混同して「すべての一時データが暗号化される」と説明しないでください。暗号化依存 `cryptography` と `cffi`・`pycparser` の版とライセンスも配布時に収集します。

エラーのスタックトレースはQtの `AppLocalDataLocation` 配下の `logs/folimeld.log` に記録します（1 MiB×最大3ファイル）。Windowsでは通常 `%LOCALAPPDATA%/Folimeld/Folimeld/logs/` です。PDF本文やパスワードを明示的に記録する処理はありませんが、例外メッセージにはファイル名などが含まれる場合があります。ログの初期化に失敗しても起動を継続します。

## バージョン管理

アプリの表示バージョンは `folimeld/__init__.py` の `__version__`、App Store用のビルド番号は `__build__` で管理しています。新しいApp Store提出ごとに、表示バージョンまたはビルド番号を更新してください。特に同じ表示バージョンで再提出する場合は、ビルド番号を増やします。

Windowsの実行ファイル用バージョン情報は `tools/write_version_info.py` によりビルド時に生成されます。UbuntuパッケージとmacOS App Bundleもアプリの表示バージョンを参照します。Store提出用MSIXの版番号は専用の設定ファイルで分けて管理します。

ライセンス文書は各specの `tools/license_bundle.py` 呼び出しで同梱します。
配布前に [ライセンスと配布](documentation/license-distribution_ja.md) を確認してください。

## アイコン

`assets/Folimeld-icon-source.png` を元に、次のコマンドで透過PNG、ICO、ICNS、MSIX用画像を生成します。

```bash
python tools/make_app_icon.py
```

生成先：

- `assets/Folimeld-icon-master.png`
- `assets/Folimeld.iconset/`
- `assets/Folimeld.ico`
- `assets/Folimeld.icns`
- `packaging/msix/Assets/`

## Windowsビルド

```bat
build_exe.bat
```

生成物は `dist\Folimeld.exe` です。Python、PySide6、PyMuPDF、翻訳データを含む単体実行ファイルとして生成されます。

非パッケージ版は起動時にWindowsの「プログラムから開く」へFolimeldを登録します。MSIX版ではレジストリ登録を行わず、パッケージマニフェストのファイル関連付けを使用します。

## Microsoft Store向けMSIX

ユーザーによる確認では既存のFolimeld登録は「EXE または MSI アプリ」です。公開方式はMSIXを選択していますが、MSIX登録への移行・名前の扱いとIdentity情報は確認待ちです。[公開計画](documentation/windows-store-release-plan_ja.md) に状況と提出方式ごとの要件を記録しています。

### Intel/AMD（x64）

開発用の未署名MSIX：

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1
```

生成物は `dist\Folimeld_<バージョン>_x64.msix` です。

Store提出用は `packaging/msix/store-config.example.json` を `build/store-config.json` へコピーし、MSIX登録のIdentity・Publisher・公開者表示名と提出版番号を設定します。EXE/MSI側のアプリケーションIDは使いません。空欄・開発用Identity・不正な版番号はEXEの再ビルド前に拒否します。まず設定だけを検証してください。

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json -ValidateOnly

powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 `
  -Store -StoreConfig .\build\store-config.json
```

`-Store` を省略すると開発用モードです。従来の `-IdentityName`・`-Publisher`・`-PublisherDisplayName` は開発用で利用でき、Storeモードでは設定ファイルのみを使用します。生成後のMSIXはIdentity・版番号・CPU種類・同梱画像などを静的検査し、結果を `build/msix-preflight/` に保存します。更新版では `-PreviousPackage` で前回の同じStore製品のMSIXを指定すると、版番号の増加も検証します。静的検査はWACK・実機試験・Partner Centerの検証の代わりにはなりません。Store外でインストールする場合は、マニフェストのPublisherと一致する証明書で署名してください。

### ARM（ARM64）

ARM64版は、Windows on ARM実機またはARM64 Windows仮想環境で作成します。PyInstallerはx64からARM64へのクロスビルドを行わないため、ARM64版Pythonで仮想環境を作り直し、PySide6、PyMuPDF、Pillow、PyInstallerのARM64対応パッケージをインストールしてください。

```powershell
powershell -ExecutionPolicy Bypass -File .\build_msix.ps1 -Architecture arm64 `
  -Store -StoreConfig .\build\store-config.json
```

ビルドスクリプトはPython/PyInstaller環境のアーキテクチャを検査し、指定と一致しない場合は処理を停止します。

## macOSビルド

```bash
./build_exe.sh
```

生成物は `dist/Folimeld.app` です。スクリプトは必要に応じて仮想環境を作成し、依存関係をインストールします。

```bash
open dist/Folimeld.app
```

ローカル確認用としてad-hoc署名を行います。正式配布ではApple Developer証明書による署名と、公証の手続きを行ってください。

### Mac App Store向けビルド

Apple Developerで、Bundle ID `com.folimeld.Folimeld` に対応するApp Store用アプリ署名証明書、インストーラ署名証明書、App Sandboxを有効にしたプロビジョニングプロファイルを用意してください。

```bash
./build_appstore.sh \
  --application-identity "アプリ署名証明書のCommon Name" \
  --installer-identity "インストーラ署名証明書のCommon Name" \
  --provisioning-profile "/path/to/Folimeld.provisionprofile"
```

生成物は `dist/Folimeld_<表示バージョン>.pkg` です。スクリプトはApp Sandbox entitlementsを適用し、アプリとインストーラに署名します。提出前にアプリ署名、Info.plist、Bundle ID、表示バージョンとビルド番号の分離、PDFのドキュメントタイプ、Sandbox entitlements、インストーラ署名を自動検証します。TestFlightで確認した後、TransporterまたはXcodeからApp Store Connectへアップロードしてください。

App Storeへアップロードするたびに、`folimeld/__init__.py` のバージョンを更新してください。ユーザーがファイルダイアログで選択したPDFだけを読み書きするため、現在のentitlementsにはネットワーク権限を含めていません。

## Ubuntuビルド

```bash
bash build_linux.sh
```

次のファイルが生成されます。

- `dist/folimeld`
- `releases/ubuntu/folimeld_<バージョン>_<アーキテクチャ>.deb`

Ubuntu 22.04以降に対応する配布用debは、Ubuntu 22.04上でビルドしてください。新しいUbuntu上でビルドすると、同梱Pythonや共有ライブラリが新しいglibcを要求し、22.04で起動できなくなる場合があります。

```bash
sudo apt install ./releases/ubuntu/folimeld_*.deb
```

DEBパッケージにはデスクトップメニュー、アイコン、PDF関連付けが含まれます。

Linux専用の仮想環境 `.venv-linux` を使用します。`FOLIMELD_LINUX_VENV` で保存先を変更できます。
WSLではLinux側のパス（例：`/tmp/folimeld-build-venv`）を指定すると高速にビルドできます。
debの `libc6` 最低バージョンはビルド環境から設定します。Ubuntu 22.04で作成したdebは `libc6 >= 2.35` が対象です。依存バージョンの表記だけを下げず、必ず22.04上で実行ファイルごとビルドしてください。

WSLから配布用debをビルドする例（必要な依存関係をインストールした後）：

```powershell
wsl -d Ubuntu-22.04 -- bash -lc 'cd /path/to/Folimeld && FOLIMELD_LINUX_VENV=~/.cache/folimeld-build-venv bash build_linux.sh'
```

パスは自分の環境に合わせて変更してください。配布前にUbuntu 22.04・24.04・26.04でdebのインストール、PDFの表示・編集・保存を確認し、パッケージを差し替えたら `releases/ubuntu/folimeld_<バージョン>_SHA256SUMS.txt` も更新してください。

Debian 13（amd64）にも同じdebを配布します。配布前の動作確認にはDebian 13も含めてください。0.3.2はDebian 13.6のWSL2 / WSLg（X11）で基本動作を確認しています。確認範囲と最小構成でのFontconfig設定不足については[検証記録](documentation/debian-wsl-verification_ja.md)を参照してください。

### Snapパッケージ

Ubuntu 24.04で `build_linux.sh` を実行した後、次を実行します。

```bash
sudo snap install snapcraft --classic
bash build_snap.sh
```

生成物は `releases/ubuntu/folimeld_<バージョン>_<アーキテクチャ>.snap` です。
Snapcraftの既定の隔離ビルド環境を使用します。専用のUbuntu 24.04ビルド環境やWSLで、
ホストへビルド依存をインストールしてよい場合は `sudo bash build_snap.sh --destructive-mode` でも作成できます。
`core24` とGNOME拡張を使い、QtのX11ライブラリ、アイコン、PDF関連付けを同梱します。

ローカルパッケージのインストールと起動：

```bash
sudo snap install --dangerous ./releases/ubuntu/folimeld_0.3.2_amd64.snap
snap run folimeld
```

Snapはstrict confinementで動作し、ホームフォルダー内の通常のファイルにアクセスできます。
外付けドライブのPDFを編集する場合は `sudo snap connect folimeld:removable-media` を実行してください。
Snap Storeへの公開は、このローカルビルドとは別の手順です。

## リリース前チェック

1. `folimeld/__init__.py` のバージョンを更新する
2. テストをすべて実行する
3. 対象OSごとにクリーンビルドする
4. Python未導入の環境で起動、ファイルを開く、編集、保存を確認する
5. PDF関連付けとアンインストールを確認する
6. ライセンスおよび第三者ライセンス表示を確認する
7. MSIXはWindows App Certification Kitで検査する

## ライセンス

このプロジェクトへのコントリビューションは、プロジェクト本体と同じ [GNU Affero General Public License v3.0](LICENSE) の条件で提供されます。
