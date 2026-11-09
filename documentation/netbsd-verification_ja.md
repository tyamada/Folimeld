# NetBSD 11.1の動作確認記録

検証日: 2026-11-09（日本時間）。[検証計画](netbsd-verification-plan_ja.md)に沿い、NetBSD 11.1 / amd64の専用VirtualBox VMでFolimeldをソースから実行した。

## 結果

| 確認 | 結果 |
| --- | --- |
| pytest全件 | **386 passed、9 skipped、32 subtests passed** |
| フォーム回帰の先行実行 | 8 passed |
| 型検査・依存整合性 | NetBSD上のmypyとpip checkが成功 |
| 実GUI | 日本語PDF、選択、編集、保存・再読込、フォーム、暗号化PDF、画像取り込み、保存失敗後の復旧を確認 |
| 設定保持 | 英語・432pxへ変更し、アプリ再起動後も保持。確認後は日本語・288pxへ戻した |
| 負荷試験 | 100ページ、画像入り100ページ、1000ページを各3回完了。実GUIでも1000ページ目を表示 |

検証対象コミットは `98de4104c93a525147f9bd39f0944249ff89c8bc`。Folimeld本体の変更はなく、必要な移植修正は依存ライブラリとビルド工具へ適用した。この結果は下記の構成に限定する。

## ホストと専用VM

- VirtualBox上に `Folimeld-NetBSD-11.1-amd64` を新設。
- UUID: `e50133d1-0e13-47a3-94de-a5fad6f3ed44`。
- 初期構築は4 vCPU・8 GiB RAM。ネイティブビルド中にホストの空きメモリ約41 GiBを確認し、正常停止後に8 vCPU・16 GiBへ増設した。ゲストで `hw.ncpu=8`、`hw.physmem64=17179406336` を確認。
- VRAM 128 MiB、VBoxSVGA、3D無効。
- 専用の80 GiB可変VDI。既存FreeBSD VMのディスクは使用しない。
- 初期構築先はリポジトリー内の `build/netbsd-vm/Folimeld-NetBSD-11.1-amd64/`。最終保存先は `C:\Users\takum\VirtualBox VMs\Folimeld-NetBSD-11.1-amd64`。VirtualBoxのVM移動機能で移動済み。
- NAT、SSH転送はホストの `127.0.0.1:2224` からゲスト22番。
- 初期構築時はシリアルコンソール用TCPサーバーをポート2324で設定。ディスク起動・SSH接続が成立したため、増設時にUARTを無効化した。
- 構築済みスナップショット: `01-os-and-native-build-prepared`（UUID `0cf43072-504e-42be-90e2-eef7d4dd9709`）。この時点ではライブラリのビルドとアプリ検証は未完了。
- 検証済みスナップショット: `02-folimeld-verified`（UUID `4c40ee32-6dd0-4f13-a4e0-be0b671a5853`）。正常停止して取得したディスクの復旧点。
- 移動・再起動後もSSH鍵認証、8 CPU・16 GiB、日本語デスクトップ、[保存済み日本語PDFの起動](netbsd-verification/gui-after-reboot.png)を確認した。Xorg起動時の解像度はスクリプトで1280×1024へ設定する。

## インストール資材

[公式リリース一覧](https://www.netbsd.org/releases/formal.html)でNetBSD 11.1を確認した。

- ISO: `https://cdn.netbsd.org/pub/NetBSD/NetBSD-11.1/amd64/installation/cdrom/boot.iso`
- チェックサム: 同ディレクトリーの `SHA512`。
- 公式SHA-512: `9f7b50d8cd86ec086016c31bc753051863128a808193357719946d9a42653574ce1b9d89ceea2268cde8a921ae494c9cb00ce11a76a468ba64f92abbc2b4c9f1`

ISOの取得を完了し、実ファイルのSHA-512が公式値と一致した。

## OS導入

- ISOのインストール環境で `uname -a` によりNetBSD 11.1 GENERIC / amd64を確認。
- 新設VDIの `wd0` が空であることと167772160セクターの容量を確認し、MBRのNetBSDパーティション、FFSv2ルート、4 GiBスワップを作成した。
- 起動ISOの基本ファイル配置後、公式 `amd64/binary/sets/` のbase、etc、comp、modules、kern-GENERIC、xbase、xcomp、xetc、xfont、xserverを取得。各セットのSHA-512が公式一覧と一致してから展開した。
- インストール環境はCA検索パスが未構成でHTTPSに失敗した。メディア収録のMozilla証明書を束ねて `SSL_CERT_FILE` に指定し、証明書検証を維持して取得できた。導入先では `certctl rehash` を実行した。
- 起動設定、ホスト名 `folimeld-netbsd`、DHCP、SSH鍵認証、一般ユーザー `folimeld`、日本時間、デバイスノードとブートブロックを設定した。
- ホストのローカルHTTPサーバーへのゲスト接続は `No route to host` で失敗したため、構成スクリプトはシリアル転送で適用した。
- ISOを外し、正常停止後にインストール済みディスクから起動した。SSH鍵認証でrootと一般ユーザーの接続が成功し、FFSルート、日本時間、NetBSD 11.1を確認した。
- [公式配布セットの照合記録](netbsd-verification/os-sets.txt)を保存した。

## 依存調査

[公式バイナリ一覧](https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/x86_64/11.1/All/)にPython 3.12.14、Pillow 12.3.0nb1、cryptography 50.0.1、psutil 7.2.2nb3、pytest 9.1.1、Xfce 4.20.0nb20を確認し、下記の環境へ導入した。

同一覧ではPySide6・PyMuPDFを発見できていない。`py312-qt6` は名前だけを根拠にPySide6の代替とは判断しない。
[pkgsrc-wipのPySide6定義](https://github.com/NetBSD/pkgsrc-wip/blob/master/py-pyside6/Makefile)を参考にソースビルドを進めた。

### 導入した構成

- `11.0_2026Q3/All` をパッケージ配布先として固定した。公式の11.1一覧から調べた候補を使い、依存を含む229パッケージの導入が終了コード0で完了した。
- その後、Qt翻訳関連10パッケージとGUI入力用xdotoolを追加した。最終一覧は [packages.txt](netbsd-verification/packages.txt)。
- Python 3.12.14、Qt 6.11.2、Pillow 12.3.0、cryptography 50.0.1、psutil 7.2.2、pytest 9.1.1、Clang/LLVM 21.1.8、SWIG 4.4.1を導入した。
- 一般ユーザーで[日本語Xfceの実画面](netbsd-verification/desktop.png)を確認。Xorg 1.21.1.25、1280×1024へ変更した。起動はSSHからXorgとユーザーセッションを開始する構成で、自動ログインは設定していない。
- 一般ユーザーの `.venv-netbsd` を `--system-site-packages` で作成した。
- PySide6はQt公式6.11.2ソースを取得し、公式SHA-256 `cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8` と一致。pkgsrc-wipのスレッドIDキャスト・CMake探索パスのパッチを照合して適用し、Folimeldが使用するCore/Gui/Widgetsをネイティブビルドした。公式wheelの全モジュールを構築したものではない。
- PyMuPDF/MuPDF 1.28.2は既存FreeBSD構築手順と同じソースSHA-256を照合した。NetBSD向けwheelを生成し、`LD_LIBRARY_PATH=/usr/pkg/lib` を指定したimportとフォーム回帰8ケースが成功した。[フォーム結果](netbsd-verification/forms-early.txt)、[JUnit XML](netbsd-verification/forms-early.xml)を参照。
- MuPDF内部SHA-256・SHA-512の「abc」の結果はPythonのhashlibと一致した。[照合結果](netbsd-verification/sha2.json)を参照。
- NetBSD上のmypy 1.20.2は対象3ファイルで成功。[結果](netbsd-verification/mypy.txt)。Windowsホスト側のRuff 0.17.1も成功した。Ruffの結果をNetBSDネイティブ実行の結果とは扱わない。

### ビルド中に修正した問題

1. PySide6の `pthread_self()` の戻り値のキャストとCMake探索パスには、pkgsrc-wipの既存パッチを適用した。生成ラッパーのBashパスも `/bin/bash` から `/usr/pkg/bin/bash` へ変更した。
2. MuPDFの `bswap32` / `bswap64` がNetBSDの定義と衝突した。[初回ログ](netbsd-verification/pymupdf-initial-failure.txt)を残し、公式pkgsrcの名前空間衝突回避パッチを適用した。
3. 同梱Tesseractのバイト順判定がNetBSDのGCCを判定できなかった。[ログ](netbsd-verification/pymupdf-endian-failure.txt)を残し、`__BYTE_ORDER__` と `__ORDER_*_ENDIAN__` を使う判定を追加した。
4. `libmupdfcpp.so` のリンクが作られず `-lmupdfcpp` に失敗した。[ログ](netbsd-verification/pymupdf-link-failure.txt)を残し、NetBSDでもリンクを作るようビルド分岐を拡張した。
5. pipcl 13がABI制限ビルドで `EXT_SUFFIX=.so` を空文字にし、wheel内の拡張が `_extra` になった。[import失敗ログ](netbsd-verification/pymupdf-import-failure.txt)を残し、拡張子抽出時に仮のファイル名を付けて `.so` を保持した。修正したwheelではimportとフォーム回帰が成功した。

使用したパッチは [patches/](netbsd-verification/patches/) に保存。Folimeld本体のPDF処理やフォーム機能を無効化する回避策は追加していない。

## 全件テスト

[pytest結果](netbsd-verification/pytest.txt)、[JUnit XML](netbsd-verification/pytest.xml)、[pip check](netbsd-verification/pip-check.txt)を保存した。9スキップはWindowsレジストリとPowerShellのビルド・パッケージ処理に関する既存条件によるもの。

初回全件実行は384 passed、9 skipped、2 failedだった。2件ともPyInstaller未導入によるソース同梱テストのimport失敗で、PyInstaller 6.22.2と既存制約の依存を導入後、全件を再実行して成功した。[初回結果](netbsd-verification/pytest-before-pyinstaller.txt)、[導入ログ](netbsd-verification/pyinstaller-install.txt)を参照。

バージョンは [importによる環境記録](netbsd-verification/environment.json)と [Python配布一覧](netbsd-verification/python-packages.txt)で確認した。CMakeで導入したPySide6はpipの配布メタデータがないため、pip freezeだけでは構成全体を表せない。

## 実GUIと保存結果

VirtualBoxの実画面をcomputer-useで確認した。ホストからの相対マウス入力が不安定だったため、文書操作はゲストのxdotoolによるX11のマウス・キー入力イベントで実施した。アプリ内部APIを呼ぶ編集・保存ではない。保存後の照合だけをPyMuPDFによる読み取りで行った。

| 操作 | 確認結果 |
| --- | --- |
| 日本語PDF・複数選択 | 付属の8ページPDFを表示し、全ページ選択できた |
| 回転・undo/redo・移動 | 先頭ページを右90度回転、取り消し・やり直し後、2ページ目へ移動できた |
| 白紙挿入・削除 | 白紙挿入で8→9、取り消しで8。ページ削除で8→7、取り消しで8へ戻った |
| 日本語名の保存・上書き・再読込 | `日本語 saved.pdf` を保存し、開くダイアログから再読込できた。OS再起動後には同じ検証用コピーへの通常の上書き保存も成功した |
| 保存失敗からの復旧 | 0555の検証用ディレクトリーでPermission deniedを表示。編集と履歴を保持し、別の場所へ保存できた |
| フォーム | テキスト、チェックボックス、選択肢あり／なしのコンボを持つPDFを回転・保存・再読込できた |
| 暗号化 | 誤パスワードでは再入力、キャンセルでは元文書を保持。正しいパスワードで開き、回転・暗号化保存後も同じパスワードで再読込できた |
| 画像取り込み | 日本語・空白を含むフォルダーのPNG・JPEGを一覧表示し、2ページPDFへ保存・再読込できた |
| 設定 | 英語と432pxが再起動後に保持され、さらに日本語へ戻した再起動も成功した |
| 1000ページ | 先頭から末尾へ移動し、999・1000ページのサムネイルを表示できた |

保存先はゲストの `/home/folimeld/Folimeld/build/netbsd-verification/`。元のサンプルPDFは変更していない。検証終了後、保存失敗用ディレクトリーの権限は0755へ戻した。

- [通常PDF・復旧保存の照合](netbsd-verification/gui-verification.json): 順序は操作前基準で `2, 1, 3, 4, 5, 6, 7, 8`。通常保存は2ページ目だけ90度、復旧保存は1・2ページ目が90度。対応するページの内容ストリームが一致。
- [フォーム・暗号化・画像の照合](netbsd-verification/extended-verification.json): フォーム4種の名前・種類・値・選択肢・矩形が一致。画像は取り込み時にPNGへ正規化される仕様のため、元PNG/JPEGを復号したRGB画素と保存PDF内の画素を照合し、2件とも完全一致した。
- 画面証跡: [通常PDF再読込](netbsd-verification/gui-after.png)、[保存エラー](netbsd-verification/save-error.png)、[暗号化PDF再読込](netbsd-verification/gui-encrypted.png)、[画像PDF](netbsd-verification/gui-images.png)、[設定保持](netbsd-verification/settings-restart.png)、[1000ページ目](netbsd-verification/gui-1000-pages.png)。

## 負荷計測

`tools.benchmark_pdf` をoffscreenでケースごとに新規プロセスとして各3回実行した。全9回で入力不変、undo・redoを確認。サムネイルは288px、常駐枚数の最大は各ケースとも24枚だった。

| 合成入力 | 開く ms・中央値 | 初期サムネイル ms・中央値 | 保存 ms・中央値（最小〜最大） | 標本化ピークRSS MiB・中央値（最小〜最大） |
| --- | ---: | ---: | ---: | ---: |
| 文字100ページ | 0.850 | 66.010 | 15.365（13.159〜16.610） | 139.480（139.348〜139.688） |
| 256px画像入り100ページ | 0.769 | 74.229 | 212.270（209.756〜213.643） | 264.543（259.887〜266.465） |
| 文字1000ページ | 1.034 | 71.516 | 314.383（311.547〜420.937） | 143.457（143.449〜143.578） |

[集計JSON](netbsd-verification/benchmark-summary.json)、[実行ログ](netbsd-verification/benchmarks.txt)、[集計スクリプト](netbsd-verification/summarize_benchmarks.py)を保存。元データは同ディレクトリーの `text-100-{1,2,3}.json`、`images-100-{1,2,3}.json`、`text-1000-{1,2,3}.json`。

RSSは5ms間隔の標本化で短いピークを逃す可能性がある。OSキャッシュは消去していない。8 vCPU・16 GiBのNEM実行という今回の構成での値であり、異なるVM構成のFreeBSD結果と直接の速度優劣は比較しない。

## このVMでの再実行

ゲストの作業ディレクトリーは `/home/folimeld/Folimeld`。以下の共有ライブラリ検索パスが必要。

```sh
cd /home/folimeld/Folimeld
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
QT_QPA_PLATFORM=offscreen .venv-netbsd/bin/python -m pytest -q -ra -p no:cacheprovider
```

デスクトップはrootで `sh /root/start-desktop.sh`、Folimeldは一般ユーザーで `sh /home/folimeld/native-build/launch-folimeld.sh` として起動する。[デスクトップ起動](netbsd-verification/start-desktop.sh)・[アプリ起動](netbsd-verification/launch-folimeld.sh)のスクリプトを保存した。

再構築用の [PySide6手順](netbsd-verification/build-pyside.sh)と [PyMuPDF手順](netbsd-verification/build-pymupdf.sh)は、このVMのアカウント・パスを前提に、成功したコマンドとパッチを整理したもの。PySide6は[Qt公式ソース](https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/)から取得・ハッシュ照合・展開したソースを `/home/folimeld/native-build/` に用意する。両スクリプトの横へ `patches/` を配置し、一般ユーザーで実行する。[PySide6ログ](netbsd-verification/pyside-build.txt)・[PyMuPDFログ](netbsd-verification/pymupdf-build.txt)を参照。

PySide6手順は仮想環境へのインストールまで行う。PyMuPDF手順はwheelの生成までなので、再構築後は以下でwheelを導入し、両ライブラリをimportできることを確認する。

```sh
cd /home/folimeld/Folimeld
.venv-netbsd/bin/python -m pip install --no-deps --force-reinstall \
  /home/folimeld/native-build/wheels/pymupdf-1.28.2-*.whl
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
.venv-netbsd/bin/python -c 'import PySide6, pymupdf; from PySide6.QtWidgets import QApplication; print(PySide6.__version__, pymupdf.__version__)'
```

今回確認したのは、amd64での上記依存を使ったソース実行。NetBSD用の配布パッケージ・単一実行ファイル、他アーキテクチャー、長時間連続使用は検証対象に含めていない。
