# Windows x64／ARM64 ソース＋uv版プレビュー

公開済みプレビューの導入手順は以下を参照してください。後半の過去の確認用ZIP・未公開時点の記録は履歴であり、現在の公開ZIPのハッシュとは区別します。

Microsoft Storeを標準配布として維持する。これは上級者向けの追加経路であり、
Windows 11 x64およびWindows 11 ARM64（Surface Pro 11等のCopilot+ PC）を対象とする。開発PCで正規ランチャーの起動・文書操作・3ワーカー・再起動後の設定保持を確認済み。
本番Store版との併存と、別版への更新・旧版復帰は未確認。

## 固定する入力

### Windows 11 x64版
- CPython 3.12.16、python-build-standalone配布ビルド20261110。
- uv 0.13.8。取得URLと公開SHA-256は`../windows-uv-runtime.json`を参照。
- 実行依存14件は`../requirements-windows-uv.in`に固定。
- `../requirements-windows-uv.lock`はWindows x64／CPython 3.12用のwheelハッシュのみを許可。

### Windows 11 ARM64版
- CPython 3.12.10、Python Software Foundation公式署名済みARM64 NuGetパッケージ（`pythonarm64.3.12.10.nupkg`）。すべてのバイナリがAuthenticode署名されており、Windows 11のSmart App Control（スマート アプリ コントロール）有効環境でもブロック通知を誘発しません。
- uv 0.13.8（ARM64 Windows ネイティブバイナリ）。取得URLと公開SHA-256は`../windows-arm64-uv-runtime.json`を参照。
- `../requirements-windows-arm64-uv.lock`はWindows ARM64／CPython 3.12用のwheelハッシュのみを許可。
- インストール時は固定Python配布物の実物ハッシュを照合し、私有の版別runtimeへ展開する。
  Python版番号だけでは配布ビルドの証明にならない。導入台帳に取得物ハッシュを記録する。
- 本体ソースのコミット・ZIPハッシュ・対応記録は配布候補作成時に確定する。
  このJSONはソースZIP全体の真正性を証明する署名ではない。

## 導入・起動契約

以下は利用者向けの導入手順。PowerShell 7.2以降とWindows標準のtarが必要。
開発PCの隔離環境で行った導入確認は別の確認記録に残し、実機GUI受入とは区別する。

ソースZIP全体のSHA-256を公開台帳と照合し、新しい専用フォルダーへ展開してから実行する。

```powershell
pwsh -NoProfile -File .\install_uv.ps1
```

#### 公開ZIPの照合と未署名スクリプトのブロック解除

この手順は公開済みのx64プレビュー`windows-uv-v0.3.5-preview.1`専用です。他のZIPにこの期待ハッシュを流用しないでください。
通常権限のPowerShell 7.2以降で実行します。ZIPをDownloadsへ保存した場合の例です。保存先が異なる場合は`$zip`を変更してください。
既存の導入先を再利用せず、`$destination`には存在しない専用フォルダーを指定します。

```powershell
$ErrorActionPreference = 'Stop'
$zip = Join-Path $HOME 'Downloads\Folimeld-0.3.5-windows-x64-uv-source-1475b48-candidate1.zip'
$expected = '8B651224221505B4CA6F0F48ECC13989C33573DE4501ACE3A9BA960C2EBB86BA'
if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne $expected) {
    throw 'ZIP SHA-256 mismatch. Stop without extracting or running it.'
}

$destination = Join-Path $HOME 'Folimeld-uv-0.3.5'
if (Test-Path -LiteralPath $destination) {
    throw 'Destination already exists. Choose a new dedicated folder.'
}
Expand-Archive -LiteralPath $zip -DestinationPath $destination

$scripts = @(Get-ChildItem -LiteralPath $destination -Recurse -File -Filter 'install_uv.ps1')
if ($scripts.Count -ne 1) {
    throw 'Expected exactly one install_uv.ps1. Stop without running it.'
}
$installer = $scripts[0].FullName
Unblock-File -LiteralPath $installer
Push-Location -LiteralPath $scripts[0].DirectoryName
try {
    pwsh -NoProfile -File $installer
    if ($LASTEXITCODE -ne 0) { throw 'Installation failed. Retain the error and installation records.' }
}
finally {
    Pop-Location
}
```

SHA-256不一致では展開・実行せず停止します。照合したZIPを新規展開し、見つかった`install_uv.ps1`が1件であることを確認して、その1ファイルだけを`Unblock-File`でブロック解除します。ZIPやフォルダー全体の一括ブロック解除は行いません。

この操作はダウンロード元情報によるブロックを外すもので、デジタル署名を付ける操作ではありません。`RemoteSigned`でダウンロード由来の未署名スクリプトが拒否されている場合の対処です。`AllSigned`・`Restricted`・組織ポリシーなどでは引き続き拒否されることがあります。その場合は`Get-ExecutionPolicy -List`の結果とエラー全文を保存して確認してください。`Set-ExecutionPolicy`や`-ExecutionPolicy Bypass`は使用せず、PC全体・ユーザー・プロセスの実行ポリシーは変更しません。

導入後は`install_uv.ps1`と同じフォルダーに作成される「Folimeld UV」ショートカットから起動します。`main.py`は直接起動しません。導入後のフォルダーは移動・改名しないでください。

`install_uv.ps1`は固定URLからuvとPythonを取得・ハッシュ照合し、ソースフォルダー内の
`.uv-runtime`と`.venv`にだけ展開・導入する。専用の`uv pip check`とランチャー事前検査後、
同じフォルダーに通常起動・調査用ショートカットを作る。アプリ自体は起動しない。
既存`.uv-runtime`・`.venv`・同名ショートカットがあれば停止し、上書きや自動削除をしない。
失敗時は状態と作成物を残して調査できる。管理者権限、PATH変更、実行ポリシー変更、
Store登録変更は行わない。

導入記録は既定で`%LOCALAPPDATA%\Folimeld-UV\install-records\<版>\<実行ID>\`。
隔離検査用には`-RecordRoot <絶対パス>`で記録先を指定できる。取得物のハッシュ・サイズ・
実行結果・インストール依存版・作成したショートカットを記録し、資格情報や環境変数全体は収集しない。

固定Pythonの絶対パスを指定して版フォルダー直下の`.venv`を作成する。
uvの自動Pythonダウンロードを禁止し、既存Pythonや共有環境を使用しない。
依存導入では`uv pip sync`に専用Python、`--require-hashes`、`--only-binary :all:`を指定する。
利用者の外部uv設定を混入させないため`--no-config`も指定する。
確認済みバージョンのuv実行ファイルを明示して使い、PATHやグローバル設定を変更しない。
wheelがなければ停止し、ソースビルドへ切り替えない。

通常起動は`.venv\Scripts\pythonw.exe`に`launch_uv.py`の絶対パスを渡す。
調査時は同じ環境の`python.exe`を使う。ショートカットは導入工程で作成する。
uvの起動時同期、依存更新、関連付け登録はしない。
uv版は必ず`launch_uv.py`を使用し、従来の`main.py`を直接起動しない。

ランチャーはWindows x64、CPython 3.12.16、版フォルダー専用`.venv`、
MSIX識別情報なし、非凍結、ロックハッシュ、依存14件の実インストール版を確認する。
不一致はメッセージを表示して終了し、自動修復・インストールは行わない。
`freeze_support()`と`__main__`ガードを維持し、spawn子でGUIを再生成しない。
開発PCでPDF保存・画像変換・画像PDF保存の3ワーカーの親PID・実行パス・起動終了を確認した。

## 保存先とStoreとの分離

- 設定：`%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini`
- ログ：`%LOCALAPPDATA%\Folimeld-UV\logs\<アプリ版>\<起動ID>\`
- 導入台帳：`%LOCALAPPDATA%\Folimeld-UV\install-records\<版>\`

uv入口は`run(source_uv=True)`を使い、設定を読むI18n・MainWindowの構築前に
専用プロファイルを選ぶ。全アプリ設定は共通ファクトリを通し、uvではINIを明示し、
Qtのフォールバックを無効化する。Storeの通常起動は従来のQSettingsとログ経路を保つ。
専用保存先の初期化失敗時にStoreの領域へ切り替えない。
ログの初期化失敗もuvでは起動失敗として扱う。

1セッションのログは既存の1MiB×3本ローテーション。古いセッションの自動削除はしない。
Store設定の自動移行、既定PDFアプリ変更、レジストリ関連付け、Store購入処理は行わない。
利用者文書は指定した保存先へ保存し、版フォルダーへ自動移動しない。

## ライセンス告知と対応ソース

uvプロファイルでは画面のライセンス一覧に固定依存14件・Python・uvの専用告知と、
実インストール版・版別ソース台帳を表示する。typing-extensionsを含め、PyInstallerは実行依存に数えない。
Store版は従来の同梱告知を使い、uv用の画面分岐を使わない。

[版別ソースと確認限界](windows-uv-sources_ja.md)／
[告知全文](windows-uv-licenses/notices.txt)／[由来台帳](windows-uv-licenses/sources.json)

## 更新・残る確認

新版は別フォルダーと別`.venv`に導入する。設定はuv用の共通INIに保持する。
旧ソース・環境は残し、確認後にショートカットを切り替える。設定形式を変更する場合は
事前バックアップと旧版復帰を別途実装・検証する。現段階でスキーマ移行は実装していない。

### 確認用ZIPからの新規導入・受入（2026-11-15）

未コミットの0.3.5ソース＋uv実装を収録した確認用ZIPを使い、開発PCで次を確認した。
これは正式リリースや異なる版への更新の試験ではない。

- ZIP：`Folimeld-0.3.5-windows-uv-source-preview.zip`、26,569,868 bytes。
- SHA-256：`EB48FF341C90AA9323CBB32EC0D98A16CB94442B3C2BB4D037964B6FC6336924`。
- ZIP内台帳に記録されたソース1031件を展開前・展開後にサイズとSHA-256で照合。
  日本語と空白を含む新しい専用フォルダーへ展開し、受入後も全件不変を確認した。
- ZIP内の`install_uv.ps1`で固定uv・Python・依存14件を新規導入。
  配布物・wheelのハッシュ、導入版、依存整合、ランチャー事前検査が成功した。
- 専用`.venv`の`pythonw.exe`と`launch_uv.py`を使う正規入口から起動。
  合成PDF3ページの表示・別名保存、画像2件の変換・PDF保存、再起動後の両PDF再読込を確認した。
- PDF保存・画像変換・画像PDF保存の3ワーカーで、親PID・実行パス・起動終了を確認した。
- サムネイルサイズを144pxから288pxへ変更し、再起動後の288px表示と前回PDFフォルダーの保持を確認。
  初回・再起動後とも通常終了コード0で、観測した全対象プロセスが終了した。
- 合成入力3件のハッシュ、既存の開発用Folimeld登録・設定・既定PDF関連付けは前後一致した。

新しいのはソース・ランタイム・依存の配置であり、uvの共通設定INIは既存のものを継承した。
この新規導入試験とは別に、以下の追加確認を行った。本番Store版との実機併存、別版への更新・旧版復帰は未確認。
通常操作の単回受入であり、画像変換後クラッシュへの修正効果を証明するものではない。
このハッシュは確認済みの既存ZIPを指す。今回の手順書更新後やコミット後に再作成するZIPには、
別の版識別・台帳・SHA-256を付け、必要な確認を行う。

### 空設定・DPI・エラー復帰・対象Pythonの追加確認（2026-11-15）

- 既存のuv設定INIをハッシュ照合して一時退避し、INIが存在しない状態で正規起動に成功。
  終了コード0を確認し、生成INIを別途保存してから元INIを復元した。復元前後のSHA-256は一致した。
  ログ・導入履歴は保持しており、完全な新規Windowsユーザーの試験ではない。
- メインウィンドウの`GetWindowDpiAwarenessContext`を取得し、
  `AreDpiAwarenessContextsEqual`で`DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2`（-4）と一致した。
  プロセス認識値2だけでV2と判断していない。現在の`GetDpiForWindow`は144（150%相当）。
  倍率変更・複数モニター移動の描画試験は未実施で、旧WACK警告の原因や個別判定は未確認。
- 専用の不正PNGによる変換警告を閉じると、画像取込ダイアログが再表示された。
  キャンセルしてメイン画面へ戻り、その後に合成3ページPDFを開けた。
  想定された読取エラーの確認であり、クラッシュ再現試験ではない。
- アプリ環境を変更せず、同じCPython 3.12.16・固定依存14件の別検査環境でpytest 9.1.1を使用。
  Qt設定を検査専用INIへ分離し、関連10モジュールで61テスト＋16サブテストが成功した。
  リポジトリ全体の試験完了を意味しない。
- 初回は54成功・3失敗だった。設定共通化前の`folimeld.app.QSettings`をモックする古い参照が原因。
  `tests/test_file_dialog.py`と`tests/test_button_display.py`の計5箇所を
  `folimeld.app.application_settings`へ合わせ、期待値・判定・ケースを変えずに再検査した。
  初回の失敗記録も保持した。アプリ本体は変更していない。
- 固定依存14件、従来のFolimeld登録・設定・既定PDF関連付けは不変。
  テスト2ファイルの静的検査と差分検査も成功した。

追加確認のGUI対象は既存の照合済みZIPから導入した環境、自動検査対象は作業ツリーである。
テスト2ファイルの修正と本手順書の追記は未コミットで、上記ZIPには含まれない。
既存ZIPのハッシュを更新後の成果物のハッシュとして流用しない。

### GitHub公開前の残件

- 本番Store版との併存、別版更新・旧版復帰、複数倍率・モニター移動での描画を確認する。
  実施する環境と範囲は事前に確定し、試験PC更新は別途承認を受ける。
- uv専用告知・台帳と版別ソース案内を整備した。残る内包物のビルド由来・ソース照合を区別し、
  最終配布形態に合う告知を確認する。runtime・wheelを同梱する場合は別途点検する。
- 対象Pythonで確認済みの関連検査の範囲を維持し、最終変更に必要な追加検査と日英差分レビューを行う。
- 承認後のコミットに結び付くZIP・内部台帳・SHA-256を確定し、内容変更に応じた受入を行う。
  日英READMEの配布リンク案とReleaseのファイル一覧・説明を提示してから公開する。

画像変換後クラッシュの修正効果は未検証のままとし、公開可否を判断する際の制限事項として明記する。
公開・試験PC更新・WACK・Hosted API比較はこの実装に含めない。

[English](windows-uv-source.md)
