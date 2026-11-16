# Windows 11 x86_64／ARM64 `uv tool install` 版（Pure Python Wheel）仕様・導入手順

[English](windows-uv-tool.md)

Windows 11 x86_64 および Windows 11 ARM64（Surface Pro 11等のCopilot+ PC）向けに GitHub Releases で配布する Pure Python Wheel（`folimeld-<version>-py3-none-any.whl`）を `uv tool install` で導入する配布形態の仕様と手順です。Microsoft Store 版を標準配布として維持し、既存の Desktop 版・ソース＋uv 版とも設定・ログ・起動入口を分離します。

## 1. Windows 各エディションとの区別

| 項目 | 1. Microsoft Store版 | 2. Desktop版 (PyInstaller + Inno Setup) | 3. ソース＋uv版 (`install_uv.ps1`) | 4. `uv tool install` 版 (Pure Python Wheel) |
| --- | --- | --- | --- | --- |
| **起動入口** | `main.py` → `run()` | `launch_desktop.py` → `run(distribution="desktop")` | `launch_uv.py` → `run(source_uv=True)` | `folimeld` / `folimeld-console` → `folimeld.uv_tool_launcher:main` → `run(distribution="uv-tool")` |
| **設定保存先** | MSIX 仮想化レジストリ (`QSettings()`) | `%LOCALAPPDATA%\Folimeld-Desktop\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` |
| **ログ保存先** | `AppLocalDataLocation/logs/folimeld.log` (`strict=False`) | `%LOCALAPPDATA%\Folimeld-Desktop\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV-Tool\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) |
| **Mutex** | なし | `Local\Folimeld-Desktop` | なし | `Local\Folimeld-UV-Tool` |
| **環境検証** | `is_packaged() == True` | `win32` / `x64`または`ARM64` / `frozen` / 非 MSIX | `win32` / `x64`または`ARM64` / CPython 3.12（パッチ一致） / 非 frozen / 非 MSIX / 専用 `.venv` / lock SHA-256 & 依存14件一致 | `win32` / `x64`または`ARM64` / **CPython 3.12.x（マイナー一致）** / 非 frozen / 非 MSIX / 仮想環境 (`sys.prefix != sys.base_prefix`) / **依存14件完全一致** |
| **Sponsors / Store支援** | `StoreSupport` 有効、Sponsors 非表示 | `StoreSupport` 無効、Sponsors 表示 | `StoreSupport` 無効、Sponsors 表示 | `StoreSupport` 無効、Sponsors 表示 |
| **Open With 登録** | MSIX マニフェスト | 非登録 | 非登録 | 非登録 |
| **リソース解決** | `sys._MEIPASS` | `sys._MEIPASS` (`_internal/`) | リポジトリルート | パッケージ内 `folimeld/_resources/` |

## 2. ビルドと配布物のステージング

`tools/uv_tool_build.py` は `pyproject.toml`、`folimeld/__init__.py`、ランタイムプロファイル（`windows-uv-runtime.json` または `windows-arm64-uv-runtime.json`）、ロックファイル（`requirements-windows-uv.lock` または `requirements-windows-arm64-uv.lock`）の整合を検査した上で、決定論的な Pure Python Wheel と配布用ファイルを新しい出力ディレクトリへ生成します。

```powershell
# x64 版ステージング
python -m tools.uv_tool_build --output .\dist\uv-tool-release --arch x64

# ARM64 版ステージング
python -m tools.uv_tool_build --output .\dist\uv-tool-arm64-release --arch arm64
```

生成される配布物（[公開 Release `windows-uv-tool-v0.3.5-preview.1`](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.5-preview.1) / コミット `7aee32a74fe51cf20657f8ff9fd2726790db43a9`）：
- `folimeld-0.3.5-py3-none-any.whl`（2,176,864 bytes、SHA-256: `759b2fe0052f1741427194e40104db0af65184041ad5bad8bb5d2003874dbdaf`、`folimeld/_resources/` に翻訳・アイコン・ライセンス資料を内包）
- `Folimeld-0.3.5-windows-x64-uv-tool-source.zip`（26,715,550 bytes、SHA-256: `7cf388af261a8f9a47a49d1453d87f98d39430bc9cbdf4f2692dd0a0b4756ad7`）
- `source-manifest.json`（138,318 bytes、SHA-256: `9752f792e2f5bf4bcad90b00d1347dddab8d8ce627c7b3b98d1778838a8ad3d3`）
- `SOURCE-ASSOCIATION.txt`（506 bytes、SHA-256: `530bd105a65d8725e8847f1c5a2e54274f57b377fbaa470718684e90c5cd8d17`）
- `requirements-windows-uv.lock`（2,316 bytes、SHA-256: `7e994b4c231536fb5c53d79959761bc426bd9ff9585b578165f1fd67ec19077f`、Windows x64 / CPython 3.12 用 wheel SHA-256 ロック）
- `windows-uv-runtime.json`（1,239 bytes、SHA-256: `49ca2dea68fcc253574d867b9d5ff29524aa50e3b214d7c4687cd441dbdaa1dd`、固定依存バージョン定義）
- `THIRD-PARTY-NOTICES.txt`（622,989 bytes、SHA-256: `21929c232ddf95e158a808561a5cdf21b9cbb9798b2d55f6c577975d5393fd3c`）
- `DEPENDENCY-SOURCES.json`（24,583 bytes、SHA-256: `5ef42613490d2f807cbd0cca13b51e96e1f73716d880db2a5fc8dce844291609`）
- `SHA256SUMS.txt`（759 bytes、SHA-256: `099dad4c384a4c520fc2047ac52213c5147906e772496adee4c3efc215cada7f`）
- `uv-tool-release-manifest.json`（1,381 bytes、SHA-256: `883cd08d59fff23949608cbf133542a880266f7c0adb799947b4d4ec45786ad1`）

## 3. インストールと起動手順

### 1. 事前準備

Windows 11（x64 または ARM64）とuv本体が必要です。通常権限のPowerShellで `uv --version` が動く状態にします。uv未導入の場合は以下で導入し、PowerShellを開き直してください。

```powershell
winget install --id=Astral.uv -e
uv --version
```

- **Python 3.12の事前手動インストールは不要です。** `--python 3.12` は、適合するPythonがない場合に標準設定のuvでCPython 3.12.xを取得します。自動取得が無効の場合や通信制限下では別途準備が必要です。Pythonのパッチ版を固定する指定ではありません。
- **Smart App Control（スマート アプリ コントロール）対応**: uv tool管理下の署名済みPythonインタプリタにより実行されるため、ARM64環境でもブロック通知を誘発することなく安全に動作します。

### 2. GitHubから入手するファイル

次の**2ファイルを同じフォルダー**（例: Downloads）へ保存してください。

1. **folimeld-0.3.5-py3-none-any.whl** — アプリ本体のPure Python Wheel。
   - x64 Release: [folimeld-0.3.5-py3-none-any.whl](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-v0.3.5-preview.1/folimeld-0.3.5-py3-none-any.whl)（SHA-256: `759B2FE0052F1741427194E40104DB0AF65184041AD5BAD8BB5D2003874DBDAF`）
   - ARM64 Release: [folimeld-0.3.5-py3-none-any.whl](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-arm64-v0.3.5-preview.1/folimeld-0.3.5-py3-none-any.whl)（SHA-256: `FF06269C5BFC4A53B7BF5B673B48B3CC267744F757F771E29619785CD1150B4E`）
2. **依存ロックファイル** — 依存14パッケージの版と各アーキテクチャ用wheelのSHA-256を記録した固定入力。
   - x64用: [**requirements-windows-uv.lock**](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-v0.3.5-preview.1/requirements-windows-uv.lock)（SHA-256: `7E994B4C231536FB5C53D79959761BC426BD9FF9585B578165F1FD67EC19077F`）
   - ARM64用: [**requirements-windows-arm64-uv.lock**](https://github.com/tyamada/Folimeld/releases/download/windows-uv-tool-arm64-v0.3.5-preview.1/requirements-windows-arm64-uv.lock)（SHA-256: `B30019EC8BB3DDD9C15CEBB093432CD309566A6792B3EBCCDE821964B5054B67`）

### 3. 実行場所と保存先

コマンドは**2ファイルを保存したフォルダー**で実行します。通常は `C:\Users\<ユーザー名>\Downloads` です。Downloadsを移動している場合や別の保存場所を使う場合は、以下の移動先を変更してください。

ソース＋uv版の `install_uv.ps1` と異なり、カレントフォルダーに `.venv` は作成しません。

- **ツール仮想環境**: `uv tool dir` の返す場所の `folimeld` 配下。既定例は `%APPDATA%\uv\data\tools\folimeld\`。
- **起動コマンド**: `uv tool dir --bin` の返す場所の `folimeld.exe`（GUI）と `folimeld-console.exe`（診断用）。既定例は `%USERPROFILE%\.local\bin\`。
- **設定・ログ**: `%LOCALAPPDATA%\Folimeld-UV-Tool\`。Store版・Desktop版・ソース＋uv版と分離します。

保存先は環境変数等で変わるため、実際の場所を確認してください。

```powershell
uv tool dir
uv tool dir --bin
```

**導入成功後は、ダウンロードしたWheelとlockを移動・削除しても導入済みアプリは動作します。** 再導入用に両ファイルとハッシュを保管することを推奨します。uv管理下の環境や使用中のPythonは削除しないでください。

### 4. SHA-256照合と導入

```powershell
$ErrorActionPreference = 'Stop'

# 保存場所が異なる場合は変更
Set-Location -LiteralPath (Join-Path $HOME 'Downloads')

# アーキテクチャに応じたSHA-256照合と導入
if ([System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture -match 'Arm64') {
    if ((Get-FileHash -LiteralPath .\folimeld-0.3.5-py3-none-any.whl -Algorithm SHA256).Hash -ne 'FF06269C5BFC4A53B7BF5B673B48B3CC267744F757F771E29619785CD1150B4E') {
        throw 'Wheel SHA-256 mismatch.'
    }
    if ((Get-FileHash -LiteralPath .\requirements-windows-arm64-uv.lock -Algorithm SHA256).Hash -ne 'B30019EC8BB3DDD9C15CEBB093432CD309566A6792B3EBCCDE821964B5054B67') {
        throw 'Lock SHA-256 mismatch.'
    }
    uv tool install --python 3.12 --with-requirements .\requirements-windows-arm64-uv.lock --no-build .\folimeld-0.3.5-py3-none-any.whl
} else {
    if ((Get-FileHash -LiteralPath .\folimeld-0.3.5-py3-none-any.whl -Algorithm SHA256).Hash -ne '759B2FE0052F1741427194E40104DB0AF65184041AD5BAD8BB5D2003874DBDAF') {
        throw 'Wheel SHA-256 mismatch.'
    }
    if ((Get-FileHash -LiteralPath .\requirements-windows-uv.lock -Algorithm SHA256).Hash -ne '7E994B4C231536FB5C53D79959761BC426BD9FF9585B578165F1FD67EC19077F') {
        throw 'Lock SHA-256 mismatch.'
    }
    uv tool install --python 3.12 --with-requirements .\requirements-windows-uv.lock --no-build .\folimeld-0.3.5-py3-none-any.whl
}

if ($LASTEXITCODE -ne 0) { throw 'uv tool install failed.' }
```

### 5. 起動

起動コマンドの保存先がPATHに含まれていれば、**どのフォルダーからでも**起動できます。

```powershell
# 通常起動（コンソールなしGUI）
folimeld

# 診断起動（コンソール出力）
folimeld-console
```

> [!TIP]
> `warning: ... is not on your PATH` と表示された場合は、`uv tool update-shell` を1回実行してPowerShellを開き直してください。このコマンドはユーザーのシェル/PATH設定を更新します。PC全体の実行ポリシー変更は不要です。

アンインストールは `uv tool uninstall folimeld`（設定・ログは保持されます）。

保存先とPython取得の詳細: [uv storage](https://docs.astral.sh/uv/reference/storage/) / [Installing Python](https://docs.astral.sh/uv/guides/install-python/).

## 4. 隔離環境での導入・実画面GUI・3ワーカー検証記録（2026-11-16）

- CPython 3.12.16（`python-build-standalone` 20261110）と `uv 0.13.8` を用い、隔離した `UV_TOOL_DIR` / `UV_TOOL_BIN_DIR` / `LOCALAPPDATA` に対して上記 `uv tool install` コマンドを実行。
- `folimeld==0.3.5` と固定依存14件の計15パッケージが導入され、`folimeld.exe`（GUI）と `folimeld-console.exe`（コンソール）の2つのエントリポイントが生成されることを確認。
- 導入された `site-packages/folimeld/_resources` から `resource_root()`、翻訳カタログ、アイコン、4タブのライセンス表示（`Folimeld` / `Windows uv notices` / `Windows uv installed packages` / `Windows uv sources`）が解決されることを確認。
- 実画面GUIで合成3ページPDFの読込・回転・ページ移動・別名保存（ワーカー1：PDF保存ワーカー）、合成PNG 2枚の取込変換（ワーカー2：画像変換ワーカー）・PDF保存（ワーカー3：画像PDF保存ワーカー）、保存した両PDFの再読込・ページ数/回転角一致を確認。
- メインウィンドウの `GetWindowDpiAwarenessContext` が `DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2`（-4）と一致すること（`GetDpiForWindow` = 144）、Sponsors メニュー表示有効・`StoreSupport` 無効を確認。
- `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` への設定保存（サムネイルサイズ `144`・ボタン表示 `icon_text`）と再起動後の保持、セッションごとの独立ログディレクトリ生成を確認。
- `Local\Folimeld-UV-Tool` Mutex 保持中に `folimeld-console.exe` を重複起動し、エラーダイアログ（`Folimeld uv tool`）と標準エラー出力を表示して終了コード `1` で拒否されることを確認。
- 既存の `Folimeld-UV`・`Folimeld-Desktop` 設定ファイルおよび `HKCU\Software\Classes\Applications\Folimeld.exe` レジストリが前後で不変であることを確認。
- 公開後の GitHub Release（`windows-uv-tool-v0.3.5-preview.1`）から全10添付ファイルを未認証 HTTPS で再ダウンロードしてサイズ・SHA-256 一致を確認し、再取得した `.whl` と `requirements-windows-uv.lock` を用いた `uv tool install` 導入、`uv tool uninstall folimeld` 実行時の実行ファイル削除と `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` 保持を確認。
