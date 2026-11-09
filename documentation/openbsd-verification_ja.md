# OpenBSD 8.0の動作確認記録

検証日: 2026-11-09（日本時間）。[検証計画](openbsd-verification-plan_ja.md)に沿い、OpenBSD 8.0 / amd64の専用VirtualBox VMでFolimeldをソースから実行した。

## 結果

保存した証跡のSHA-256は[一覧](openbsd-verification/SHA256SUMS.txt)に記録した。証跡ファイルを更新した場合は一覧も再生成する。

**1 vCPU・16 GiBの下記構成で、機能・保存結果・負荷試験・再起動後の再現を確認した。** 4 vCPUではデバイス初期化が停滞したため、この結果を複数CPU構成へ一般化しない。

| 確認 | 結果 |
| --- | --- |
| pytest全件 | **386 passed、9 skipped、32 subtests passed** |
| フォーム回帰の先行実行 | 12 passed |
| 静的検査・依存整合性 | OpenBSD上のRuff、mypy（3ファイル）、pip checkが成功 |
| 実GUI | 日本語PDF、選択、回転、移動、白紙・PDF挿入、削除、Undo/Redo、保存・再読込を確認 |
| 追加GUI | フォーム、暗号化、画像取り込み、保存失敗からの復旧、日本語・空白パス、1000ページ表示、履歴退避・復元を確認 |
| 保存結果 | GUI保存した11ファイルの内容照合とqpdf構造検査が成功 |
| 設定保持 | 英語・432pxへ変更し、アプリ再起動後も保持。検証後は日本語・288pxへ戻した |
| 負荷試験 | 100ページ、画像入り100ページ、1000ページを各3回、計9回完了 |
| VM移動・OS再起動 | 永続保存した鍵でSSH接続、GUI起動、11出力と原本のハッシュ保持を確認 |

対象ソースは `ab807790f23ff7c3343d724821790699def1d5d3`。Folimeld本体の変更はなく、MuPDFのコード生成工具へLLVM 22対応パッチを適用した。[転送ソースの範囲とハッシュ](openbsd-verification/source-transfer.json)、[実行環境](openbsd-verification/environment.json)、[保存結果の照合](openbsd-verification/gui-results.json)を参照。

## 専用VM

- 名前: `Folimeld-OpenBSD-8.0-amd64`
- UUID: `10afdc1c-e89e-4399-9f8d-f9e5bfc1c24f`
- ホスト: Windows 11、VirtualBox 7.2.16r174877、Intel Core i7-10700K。開始時の空きメモリは約49 GiB。
- 初期構成は4 vCPU・8 GiB RAM。1 vCPUで起動を確認後、公式更新済みの4 vCPU・16 GiBでもデバイス初期化が停滞したため、機能・性能の検証は1 vCPU・16 GiBで実施した。80 GiB可変VDI、BIOS、PIIX4 IDE、VBoxVGA、VRAM 128 MiB、3D無効。
- 初期構築先: リポジトリー内 `build/openbsd-vm/Folimeld-OpenBSD-8.0-amd64/`。
- 最終保管先: `C:\Users\takum\VirtualBox VMs\Folimeld-OpenBSD-8.0-amd64`。正常停止してVirtualBoxのVM移動機能で移動した。
- NAT、SSH転送 `127.0.0.1:2225` → ゲスト22番。構築中だけ使用したシリアルTCPポート2325は、最終構成ではUARTごと無効化した。
- 既存FreeBSD・NetBSD VMのディスクは使用していない。
- 一般ユーザー `folimeld`、タイムゾーン `Asia/Tokyo`、rootと一般ユーザーに専用SSH公開鍵を配置。パスワードログインはアカウントのパスワードを無効化して制限する。
- 専用鍵は `C:\Users\takum\.ssh\folimeld_openbsd_ed25519`、公開鍵は同名の `.pub`、既知ホスト鍵は `folimeld_openbsd_known_hosts` に保管。Gitには含めない。移動後はこの保存先の鍵とホスト鍵の厳密照合で再接続した。

[最終VM設定](openbsd-verification/vm-configuration.txt)と[スナップショット一覧](openbsd-verification/vm-snapshots.txt)を保存した。最終状態は正常停止済み。`04-verified-after-reboot`（UUID `b1e4d926-5a57-45af-8c2b-dfd9feff06c2`）が再起動確認後の復旧点。

## インストール資材と検証

[公式サイト](https://www.openbsd.org/)で最新正式版OpenBSD 8.0（2026-10-20公開）を確認した。

- ISO: `https://cdn.openbsd.org/pub/OpenBSD/8.0/amd64/install80.iso`
- SHA-256: `bc85d747c6ee4354d14fbfeee38087500386a2e9d86fa7b5ab13d840d902aa33`
- 公式 `SHA256.sig` のEd25519署名を、OpenBSD公式ソースミラーの `etc/signify/openbsd-80-base.pub` で検証。署名とISOのハッシュ一致を確認した。
- [検証結果JSON](openbsd-verification/media-verification.json)、[検証コード](openbsd-verification/verify_media.py)、[署名付きチェックサム](openbsd-verification/SHA256.sig)、[公開鍵](openbsd-verification/openbsd-80-base.pub)を保存した。検証コードはリポジトリールートから実行し、取得資材を `build/openbsd-vm/` に配置する。

ISO内に `SHA256.sig` がなかったため、初回のCDセット導入は署名を省略せず停止した。導入元を公式HTTP配布へ変更し、インストーラーの `Signature Verified` を確認してから各セットを検証・展開した。基本・開発・マニュアル・X11セットを導入した。

## 構築中の問題

1. AHCIコントローラーのデバイス初期化で `device on port 0 didn't come ready` が発生した。専用ディスクとISOをPIIX4 IDEへ変更し、空のAHCIコントローラーも外したところインストーラーが起動した。Windowsホストのハイパーバイザー設定は変更していない。
2. VM起動直後のキー入力でBIOSの `FATAL: Keyboard error:995` が出た。リセット後、BIOS中の入力を避けて復旧した。
3. インストーラーから `halt -p` を実行してもVMの仮想電源は切れなかった。画面で `syncing disks... done` と `The operating system has halted` を確認してからVirtualBox側で電源を切った。
4. `py3-llvm` は21系と22系の複数候補があり、版指定が必要だったため `py3-llvm%22` を指定した。FreeBSDと異なり `pkgconf` パッケージは使わず、基本システムの `pkg-config` を使用する。
5. LLVMのPythonバインディングは標準site-packagesではなく `/usr/local/llvm22/lib/python3.14/site-packages` に配置される。ビルド時に `PYTHONPATH` と `LIBCLANG_LIBRARY_FILE=/usr/local/llvm22/lib/libclang.so.0.0` を指定し、`clang.cindex.Index.create()` まで成功した。
6. MuPDFのフォント生成でBashがなく停止した。Bashを追加し、失敗時に作られた空の生成ファイルだけを削除して再開した。[初回失敗ログ](openbsd-verification/pymupdf-initial-failure.txt)を保存した。
7. Xorgは `_x11` へ権限を下げるため、一般ユーザー専用の `.Xauthority` は読めなかった。Xサーバー用にroot所有・グループ `_x11`・640の認証ファイルを `/var/run/` に分け、ユーザー側は600のコピーを保持して修正した。TCP経由のX11待受は無効にしている。
8. LLVM 22では型の宣言カーソルが前方宣言を指し、匿名unionにも名前が付くため、MuPDFの参照カウント・イテレーター生成が停止した。実定義を解決し、レコードの実フィールドを列挙する[パッチ](openbsd-verification/mupdf-llvm22-definition.patch)を適用した。機能を無効化する回避策は追加していない。[型解析の最小再現](openbsd-verification/clang-type-probe.json)、[匿名unionの修正前](openbsd-verification/clang-iterator-probe-before.json)・[修正後](openbsd-verification/clang-iterator-probe-after.json)、[生成時の初回失敗](openbsd-verification/pymupdf-wrapper-failure.txt)を保存した。
9. 初回の全件テストでは、転送対象から `locales/` を漏らしたため35 failed、351 passedになった。翻訳データを同じコミットから追加し、全件を再実行して成功した。[初回結果](openbsd-verification/pytest-before-locales.txt)も保持している。
10. 長いビルド中にスクリーンセーバーがGUIを覆った。未編集のセッションを起動し直し、検証用ユーザーの自動起動設定で停止した。最終の起動手順は画面ブランクを止め、Xサーバーとウィンドウマネージャーの準備完了を待つ。

ISOを外し、停止状態のスナップショット `01-os-installed`（UUID `830a3636-a224-4434-bd83-e7a1052a6bf0`）を保存した。別途 `00-installer-halted` はhalt済みインストーラーの実行状態を含む比較用復旧点。

## 依存調査

[公式パッケージ一覧](https://cdn.openbsd.org/pub/OpenBSD/8.0/packages/amd64/)でPython 3.14.7、PySide6/Shiboken6 6.11.2、Qt 6.11.2、Pillow 12.3.0、cryptography 49.0.0、pytest 9.0.3、psutil 7.2.2、mypy 1.18.2、Ruff 0.16.7、Xfce 4.20を確認した。これは配布一覧の調査であり、導入・importの成功を示すものではない。

PyMuPDFのパッケージは発見できていないため、PyMuPDF/MuPDF 1.28.2を公式ソースからビルドした。両ソースのSHA-256は既存FreeBSD・NetBSD検証時と一致している。PyMuPDFの公式ビルド定義のOpenBSD分岐と上記パッチを使った。

更新済みの公式パッケージからPython 3.14.9、Pillow 13.0.0が導入された。一般ユーザーでPySide6/Qt 6.11.2、Pillow 13.0.0、cryptography 49.0.0のimportと、Qt Widgetsのoffscreen最小ウィンドウ起動が成功した。これは実X11セッションのGUI操作確認とは区別する。

最終の主要依存はPython 3.14.9、PySide6/Qt 6.11.2、PyMuPDF 1.28.2、Pillow 13.0.0、cryptography 49.0.0、psutil 7.2.2。コンパイラーはOpenBSD Clang 22.1.6、コード解析はLLVM 22.1.8、SWIGは4.4.1。[Python配布一覧](openbsd-verification/python-packages.txt)とimport先を含む[実行環境JSON](openbsd-verification/environment.json)を併用する。

SSH初回接続時はシリアルコンソールに表示されたED25519ホスト鍵の指紋とknown_hostsの指紋が一致することを確認した。SSHで `OpenBSD 8.0 GENERIC.MP#84 amd64`、日本時間、一般ユーザーの実行環境を確認済み。

## OS更新とGUI基盤

`syspatch` で001から009までの9件を適用し、正常停止・再起動後に `OpenBSD 8.0 GENERIC.MP#4 amd64` を確認した。[適用ログ](openbsd-verification/syspatch.txt)と[パッケージ一覧](openbsd-verification/packages.txt)を保存した。

[起動手順](openbsd-verification/start-desktop.sh)で一般ユーザーの日本語Xfceを起動した。自動ログインは設定していない。Xorgは1024×768、VESA表示で動作する。[実X11上のQt確認画面](openbsd-verification/qt-x11-smoke.png)で日本語の描画とウィンドウ表示を確認し、確認プログラムは終了コード0で終了した。終了時にGLibの診断メッセージが出ており、[標準エラー記録](openbsd-verification/qt-x11-smoke.txt)も残した。

## 静的検査

OpenBSDネイティブのRuff 0.16.7で `ruff check --exclude .venv-openbsd .` が成功した。[Ruff結果](openbsd-verification/ruff.txt)、mypy 1.18.2による対象3ファイルの[型検査](openbsd-verification/mypy.txt)、[pip check](openbsd-verification/pip-check.txt)を保存した。

## 全件テスト

pytest 9.0.3で **386 passed、9 skipped、32 subtests passed**。[テキスト結果](openbsd-verification/pytest.txt)、[JUnit XML](openbsd-verification/pytest.xml)を参照。9スキップはWindowsレジストリとPowerShellのビルド・パッケージ処理に関する既存条件によるもの。失敗ケースの除外は行っていない。

フォーム処理を先行実行し、12 passedだった。[先行結果](openbsd-verification/forms-early.txt)と[JUnit XML](openbsd-verification/forms-early.xml)を参照。[実行手順](openbsd-verification/run-tests.sh)も保存した。

## 実GUIと保存内容

一般ユーザーの実X11上で通常の `main.py` を起動し、マウス、メニュー、ツールバー、ショートカット、ファイルダイアログを操作した。マウス入力はゲストのxdotool、キー入力はVirtualBoxの `keyboardputscancode` と `keyboardputstring` を使った。GUI編集・保存をアプリ内部APIで代行していない。計測工具によるモデルAPIの試験は次節に分ける。

| 分類 | 確認した内容 |
| --- | --- |
| 基本操作 | [日本語PDFの8ページ表示](openbsd-verification/gui-open.png)、ページ選択、左右回転、移動、Undo/Redo |
| 挿入・削除 | [白紙挿入](openbsd-verification/gui-blank-inserted.png)、[別PDF挿入](openbsd-verification/gui-pdf-inserted.png)、[ページ削除](openbsd-verification/gui-page-deleted.png)、それぞれのUndo |
| 別名保存・再読込 | 8ページ、順序 `2, 1, 3, 4, 5, 6, 7, 8`、2ページ目だけ90度回転。内容ストリームが原本と対応し、[GUI再読込](openbsd-verification/gui-reopened.png)でも維持 |
| 文書設定 | PDF 1.7、SinglePage、Left to rightへ変更し、保存後の辞書値が一致 |
| フォーム | テキスト、チェックボックス、選択肢のないコンボボックスの値・型・フラグ・矩形を、回転・保存・[再読込](openbsd-verification/gui-forms-reopened.png)後も維持 |
| パスワード | 入力キャンセルで元文書を保持、[誤入力の再入力要求](openbsd-verification/gui-wrong-password.png)、正しい入力、暗号化保存、変更、解除。旧パスワード拒否と新パスワード認証を独立読込で確認 |
| 画像取り込み | [自然順の一覧](openbsd-verification/gui-image-list.png)、キャンセル、[不正画像エラー](openbsd-verification/gui-invalid-image.png)、複数選択による除外、JPEG/PNG/TIFF/WebP/BMPからA4 PDFを作成 |
| 画像の保存内容 | 5ファイルから[6ページ](openbsd-verification/gui-images.png)。TIFFの2フレーム、ページ順、A4寸法、透明部分の白背景合成色が一致。画像のEXIF向き等は既存テストでも検証 |
| 保存エラー | [読み取り専用コピーへの保存拒否](openbsd-verification/gui-save-error.png)後も文書を保持し、別の場所へ保存できた。既存ファイルのSHA-256は不変 |
| 日本語・空白パス | `日本語 sample.pdf` をダイアログから選択し、編集後に上書き保存できた。8ページ・先頭90度回転・元の内容を維持 |
| 1000ページ | [最終ページの表示](openbsd-verification/gui-1000-last.png)、最終ページの90度回転、保存・再読込、ページ数と最終ページのテキスト一致 |
| 履歴退避・復元 | 画像入り100ページで9回編集し、約19.7 MBの一時ファイル3件をfstatで確認。Undo後は全100ページの回転・内容が元に戻り、別文書を開くと大きな一時ファイルは解放された |
| 設定・終了 | 英語・432pxが[アプリ再起動後も保持](openbsd-verification/gui-settings-persisted.png)。[未保存終了の確認](openbsd-verification/gui-unsaved-confirmation.png)でキャンセルすると編集を保持し、再度の終了で検証用変更を破棄できた |

保存済み11ファイルを[読み取り専用の照合スクリプト](openbsd-verification/verify_gui_results.py)で検査し、[結果JSON](openbsd-verification/gui-results.json)と[qpdf検査ログ](openbsd-verification/qpdf-checks.txt)へ保存した。履歴の[fstat比較前](openbsd-verification/history-fstat-before.txt)・[退避後](openbsd-verification/history-fstat-after.txt)・[文書切替後](openbsd-verification/history-fstat-cleared.txt)も残した。

ゲスト内の出力先は `/home/folimeld/Folimeld/build/openbsd-verification/`。大きな検証PDFはVM内に保持し、リポジトリーにはハッシュ・照合結果・画面を保存した。原本 `testdata/tameshibu_episode3_ja.pdf` のSHA-256は `4abfe0f4a028bbac280c7629cd64c72e5df1faac8348695e0277dfc5a9154558` のまま。

暗号化サンプルのパスワードはテスト専用の `OpenBSD-test-only`、変更後は `OpenBSD-changed-only`。実データや実用パスワードは使っていない。

## 負荷試験

アプリを閉じ、既存の `tools.benchmark_pdf` を各ケース3回、新規プロセスで実行した。[実行手順](openbsd-verification/run-benchmarks.sh)、[実行ログ](openbsd-verification/benchmarks-run.txt)、[集計JSON](openbsd-verification/performance-summary.json)を保存した。下表は中央値。最小・最大と全指標は集計JSONおよび各回の元JSONにある。

| ケース | 開く ms | 全体スクロール ms | 保存 ms | 標本化した最大RSS MiB |
| --- | ---: | ---: | ---: | ---: |
| 文字100ページ | 0.69 | 699.41 | 29.50 | 155.59 |
| 画像入り100ページ（256px画像） | 0.68 | 683.25 | 226.82 | 273.73 |
| 文字1000ページ | 0.79 | 6785.88 | 343.61 | 159.88 |

全9回で入力ファイルが不変であり、Undo/Redoが実行された。最大保持サムネイル数は全回24枚。RSSは5ms間隔の標本値で短いピークを取り逃す可能性がある。保存時間は同期のモデルAPIを測定し、実GUIの保存プロセス起動時間を含めない。値は1 vCPU・16 GiBのこのVM構成に限定し、他BSDとの単純な速度比較には使わない。

## 移動・再起動後の確認と起動方法

VMを通常保管先へ移動後にディスクから起動し、`.ssh` に保存した鍵と既知ホスト鍵の厳密照合で再接続した。[OS確認](openbsd-verification/reboot-os.txt)、[再起動後JSON](openbsd-verification/reboot-confirmation.json)、[保存済みPDFのGUI表示](openbsd-verification/gui-after-reboot.png)を保存した。11出力と原本のハッシュ、日本語・288px設定、PyMuPDF 1.28.2とPySide6 6.11.2の保持を確認した。

デスクトップは自動ログインにせず、SSHから起動する。VM起動後、SSHが使用可能になってから実行する例（PowerShell）:

```powershell
VBoxManage startvm Folimeld-OpenBSD-8.0-amd64 --type gui
ssh -i "$env:USERPROFILE/.ssh/folimeld_openbsd_ed25519" -o "UserKnownHostsFile=$env:USERPROFILE/.ssh/folimeld_openbsd_known_hosts" -o StrictHostKeyChecking=yes -p 2225 root@127.0.0.1 "sh /home/folimeld/start-desktop.sh"
ssh -i "$env:USERPROFILE/.ssh/folimeld_openbsd_ed25519" -o "UserKnownHostsFile=$env:USERPROFILE/.ssh/folimeld_openbsd_known_hosts" -o StrictHostKeyChecking=yes -p 2225 folimeld@127.0.0.1 "sh /home/folimeld/launch-folimeld.sh /home/folimeld/Folimeld/build/openbsd-verification/gui-manual-after.pdf"
```

## 確認範囲と残る制約

- 確認対象は上記のamd64 VM・依存構成・ソース実行。OpenBSD向け単体実行ファイルの作成、実機、他アーキテクチャは未検証。
- このホストの4 vCPU構成では正常起動を確認できていない。機能・性能の合格結果は1 vCPUでのもの。
- Qtのダイアログや終了時に `g_main_context_pop_thread_default` のGLib診断が出る。[GUIログ](openbsd-verification/folimeld-gui-session1.txt)に保持した。編集・保存の確認区間でアプリの異常終了はなく、テストの終了コードも成功している。

## ビルド手順

[初期ビルド](openbsd-verification/build-pymupdf.sh)と[再開手順](openbsd-verification/resume-pymupdf.sh)を保存した。初期ビルドの前にBash、SWIG、GNU make、LLVM 22とそのPythonバインディングを導入し、パッチを `/home/folimeld/mupdf-llvm22-definition.patch` に配置する。[成功ログ](openbsd-verification/pymupdf-build.txt)と[ビルド識別情報](openbsd-verification/build-manifest.json)を参照。

生成wheelは `pymupdf-1.28.2-cp314-abi3-openbsd_8_0_amd64.whl`、SHA-256は `25932378ff47c85f5ef308120ff839472a261c3579bf77b3c370423f674c40b1`。別のPython・OS版・アーキテクチャでは、その環境で再ビルド・再検証する。

PyInstaller 6.22.2は既存のソース同梱テスト用に導入した。[導入ログ](openbsd-verification/pyinstaller-install.txt)を参照。wheelは検証VM内の `native-build/wheels/` に保持している。
