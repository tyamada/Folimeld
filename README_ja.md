# Folimeld

[English](README.md) | [日本語](README_ja.md)

![Folimeld icon](assets/Folimeld.iconset/icon_128x128.png)

Folimeld は、PDF のページを見ながら並べ替え、回転、挿入、削除できるデスクトップアプリです。Windows、macOS、Ubuntu、Debian、FreeBSD 15.1（amd64）に対応し、編集するファイルを外部サービスへ送信せず、ローカル環境で処理します。

![Folimeld main window](documentation/screenshots/main-window.png)

### 画像フォルダからPDFを作成

「ファイル → 画像フォルダからPDFを作成…」でフォルダ直下のJPEG・PNG・BMP・TIFF・WebPを一覧表示し、名前・作成日時・更新日時の昇順／降順を選択できます。初期値は名前の自然順・昇順です。不要な画像は除外できます。「読み込み」を押すまで画像のデコードは行いません。1画像を1ページ（複数ページTIFFは各フレームを1ページ）に変換し、新規の未保存PDFとして編集・保存できます。ページサイズは画像に合わせるかA4を選択できます。画像の向きを反映し、透明部分は白背景にします。画像サイズはDPI（不明・異常時は300 DPI）から決定します。サブフォルダとアニメーションWebPは対象外です。作成日時を取得できない画像は末尾に配置し、同一日時は名前の昇順です。変換はキャンセルでき、失敗時は現在の文書を保持します。


「ファイル → 終了」でアプリを終了できます。未保存の変更があれば保存を確認します。Windows版の画像フォルダ選択画面では、設定済みの個人用・職場用OneDriveフォルダを左側のショートカットから選択できます。最初のフォルダ選択画面でもすべての種類のファイル名を表示し、選択対象はフォルダに限定します。

## 特長

- 編集メニューまたはツールバーから複数回のUndo（元に戻す）・Redo（やり直す）。ページ操作、プロパティ、閲覧パスワードの変更に対応。保存後も履歴を保持し、別のPDFを開くとリセットします。Undo・Redo履歴のPDFデータは合計128 MiBまでメモリに保持し、超過分は合計1 GiBまでローカルの一時ファイルへ退避します。両方の上限を超えた場合や退避に失敗した場合は古い履歴から削除し、1件がディスク上限を超える場合は保持しません。一時履歴は文書を閉じる際に解放します。編集・保存中の一時データやサムネイルはこの上限に含まれず、文書全体の一時的なメモリ使用量は増える場合があります。
- 保存中は進捗画面を表示し、PDFの圧縮・書き出しを別プロセスで処理します。保存中の編集とキャンセルはできません。別プロセスへ渡す文書の準備と保存完了時の文書切替は同期処理です。
- 履歴の退避、保存処理の一時入力、画像変換中の一時PDFは暗号化し、鍵はファイルや設定へ保存しません。利用者が指定する保存先PDFには、選択したパスワード設定を適用します。
- サムネイルを見ながらPDFページを並べ替え
- 複数ページをまとめて選択・移動・回転・削除
- 別のPDFや、同じサイズの空白ページを挿入
- PDFバージョン、ページレイアウト、綴じ方向を編集
- 閲覧パスワードの設定と解除
- 日本語、英語、ドイツ語、スペイン語、フランス語、韓国語、ポルトガル語、中国語に対応
- Windows（Intel/AMD（x64）版・ARM（arm64）版の両方）、macOS、Ubuntu、Debian、FreeBSD 15.1（amd64）で利用可能

OpenBSD 8.0 / amd64では、1 vCPU・16 GiBのVirtualBox VMでソース実行を確認しています。依存ライブラリのビルドにパッチが必要です。配布パッケージは作成していません。構築方法と確認範囲は[OpenBSDの検証記録](documentation/openbsd-verification_ja.md)を参照してください。

## ダウンロード

公開対象はLinux・FreeBSD用パッケージです。Windows・macOS用バイナリは非公開とし、手元で開発・検証します。Linux 0.3.3のパッケージ、対応ソースZIP、チェックサム、ビルド記録は[Linux版GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)から取得できます。FreeBSD版は下記の専用Releaseで試験配布しています。以下のダウンロードリンクもReleaseを参照しています。[Linux版の移行計画と実施記録](documentation/linux-release-migration_ja.md)を参照してください。互換性のため従来のリポジトリ内のダウンロードURLも維持しています。

| OS | 配布形式 |
| --- | --- |
| Windows 10 / 11（Intel/AMD（x64） / ARM（arm64）） | EXE / MSIX（バイナリ非公開） |
| macOS | `.app`（バイナリ非公開） |
| Ubuntu | `.deb` / `.snap` / 単体実行ファイル（対応バージョンは各リリースを参照） |
| Debian 13 | `.deb`（amd64 / arm64、WSL2で基本動作確認済み） |
| FreeBSD 15.1 / amd64 | ネイティブ `.pkg` と対応ソース（試験配布） |

> [!NOTE]
> Windows・macOSの検証用成果物は、公開リポジトリやGitHub Releasesへ追加しません。

### Ubuntu / Debian版を直接ダウンロード

バージョン **0.3.3 / x86_64（amd64）**：

- [x86_64版debパッケージをダウンロード](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.deb)（Ubuntu 22.04以降 / Debian 13）
- [x86_64版Snapパッケージをダウンロード](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.snap)（snapdが必要）
- [SHA-256チェックサム](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_SHA256SUMS.txt)
- [ビルド時のソースと対応記録](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)

ダウンロード先のフォルダーで、使用するパッケージのインストールコマンドを実行してください。

```bash
# deb版
sudo apt install ./folimeld_0.3.3_amd64.deb

# Snap版
sudo snap install --dangerous ./folimeld_0.3.3_amd64.snap
```

バージョン **0.3.3 / arm64（AArch64）**：

- [arm64版debパッケージをダウンロード](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_arm64.deb)（Ubuntu 22.04以降 / Debian 13）
- [arm64版Snapパッケージをダウンロード](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_arm64.snap)（snapdが必要）
- [SHA-256チェックサム](https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_SHA256SUMS.txt)
- [ビルド時のソースと対応記録](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)

```bash
# arm64 deb版
sudo apt install ./folimeld_0.3.3_arm64.deb

# arm64 Snap版
sudo snap install --dangerous ./folimeld_0.3.3_arm64.snap
```

Debian 13ではUbuntu版と同じdebパッケージを使用します。最小構成の環境で `Fontconfig error: Cannot load default config file` が表示される場合は、`sudo apt install fontconfig-config` を実行してください。Debian 13.6のamd64環境（WSL2 / WSLg、X11）でPDFの表示・ページ移動・回転・保存・再読込を確認しています。詳しくは[Debianでの検証記録](documentation/debian-wsl-verification_ja.md)を参照してください。arm64環境（WSL2）でもdebのインストールとPDFを指定した起動を確認済みです。

### FreeBSD版のソース・パッケージ・インストール

FreeBSD 15.1 / amd64向けの **0.3.3 / パッケージ改訂1** を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.3)で試験配布しています。FreeBSD公式パッケージではありません。導入・GUI起動・保存・削除・再導入を確認済みです。

- [amd64版pkgをダウンロード](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/folimeld-0.3.3_1.pkg)
- [このpkgに対応するソースZIP](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/Folimeld-source-9ceb5ec75dcd3ddb60bb66f0b6996da5e700cf4400bd89b31808f5250b19f23b.zip)
- [SHA-256チェックサム](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/SHA256SUMS.txt)
- [依存ソース・wheel・ビルド記録](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.3)

[インストール・ビルド手順](documentation/freebsd-install_ja.md)と[パッケージ検証記録](documentation/freebsd-package-verification_ja.md)を参照してください。ソースから再構築する場合は、上記の対応ソースZIPを使用してください。

GUIデスクトップが構成されたFreeBSDで、パッケージ入手後は以下をrootで実行します。Python・Qtなどの依存パッケージは公式リポジトリから導入します。

```sh
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./folimeld-0.3.3_1.pkg
```

一般ユーザーで `folimeld` または `folimeld /path/to/file.pdf` を実行します。削除はrootで `pkg delete folimeld`。フォーム読み込みの不具合を修正したPyMuPDF/MuPDF 1.28.2をアプリ専用領域に同梱し、システムのPyMuPDFは置き換えません。別のFreeBSD版・CPUは未検証です。[GUI検証](documentation/freebsd-gui-verification_ja.md)と[画像取り込み・保存失敗・負荷試験](documentation/freebsd-extended-verification_ja.md)の記録も参照してください。

## 基本的な使い方

「ヘルプ → 使い方」またはF1キーで、基本操作・設定・ショートカットを確認できます。ヘルプ画面を開いたままPDFを操作できます。

1. Folimeldを起動し、「ファイル」→「開く」からPDFを選択します。
2. ページをクリックして選択します。複数選択には Ctrl または Shift を使用します。
3. ツールバー、メニュー、またはドラッグ操作でページを編集します。
4. 「保存」または「名前を付けて保存」でPDFを書き出します。

パスワード付きPDFを開くと、閲覧パスワードの入力画面が表示されます。

![Password dialog](documentation/screenshots/password-dialog.png)

### 文書設定

「文書のプロパティ」の「詳細」タブでは、PDFバージョンとページレイアウトを変更できます。`TwoPageLeft` または `TwoPageRight` を選択した場合、必要に応じてPDFバージョンが1.5へ引き上げられます。

### 設定の保存

「設定 > 画像サイズ」からサムネイルの長辺のサイズを144 / 288 / 432 pxから選択できます（初期値288 px）。変更はすぐに反映されます。

表示言語、画像サイズ、最後に開いたフォルダーは端末内に保存されます。PDFは端末内で処理されます。Windows MSIX版の応援購入では、商品情報・購入状態の確認と決済にMicrosoft Storeを利用します。PDFをStoreへ送信することはありません。

Windows MSIX版では「ヘルプ → 開発を応援する…」から、サポーターアイコン付きの買い切り商品を購入できます（Storeでの商品公開後）。購入するとヘルプメニューにサポーターアイコンが追加されます。PDF編集機能は購入の有無で変わりません。開発者向けの設定手順は [Windows応援購入](documentation/windows-store-purchases_ja.md) を参照してください。

Linux版では「ヘルプ → 開発を応援する…」に [GitHub Sponsors](https://github.com/sponsors/tyamada) への案内を表示します。案内画面のボタンからブラウザーで支援ページを開けます。支援は任意であり、利用できる機能は支援の有無で変わりません。

## 開発・コントリビューション

ソースからの実行、テスト、各OS向けパッケージの作成方法は [DEVELOPMENT_ja.md](DEVELOPMENT_ja.md) を参照してください。不具合報告や提案は [Issues](https://github.com/tyamada/Folimeld/issues) で受け付けています。

変更履歴は [CHANGELOG_ja.md](CHANGELOG_ja.md) にまとめています。

## ライセンス

Folimeld は [GNU Affero General Public License v3.0](LICENSE) で公開されています。

PySide6、PyMuPDFなどの第三者ライブラリには、それぞれのライセンスが適用されます。

ライセンス全文と第三者の告知は「ヘルプ → ライセンス」で閲覧できます。
配布時の確認事項は [ライセンスと配布](documentation/license-distribution_ja.md) を参照してください。
