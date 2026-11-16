# Windows 11 x86_64 `uv tool install` 版（Pure Python Wheel）仕様・導入手順

[English](windows-uv-tool.md)

Windows 11 x86_64 向けに GitHub Releases で配布する Pure Python Wheel（`folimeld-<version>-py3-none-any.whl`）を `uv tool install` で導入する配布形態の仕様と手順です。Microsoft Store 版を標準配布として維持し、既存の Desktop 版・ソース＋uv 版とも設定・ログ・起動入口を分離します。

## 1. Windows 各エディションとの区別

| 項目 | 1. Microsoft Store版 | 2. Desktop版 (PyInstaller + Inno Setup) | 3. ソース＋uv版 (`install_uv.ps1`) | 4. `uv tool install` 版 (Pure Python Wheel) |
| --- | --- | --- | --- | --- |
| **起動入口** | `main.py` → `run()` | `launch_desktop.py` → `run(distribution="desktop")` | `launch_uv.py` → `run(source_uv=True)` | `folimeld` / `folimeld-console` → `folimeld.uv_tool_launcher:main` → `run(distribution="uv-tool")` |
| **設定保存先** | MSIX 仮想化レジストリ (`QSettings()`) | `%LOCALAPPDATA%\Folimeld-Desktop\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV\settings\settings.ini` | `%LOCALAPPDATA%\Folimeld-UV-Tool\settings\settings.ini` |
| **ログ保存先** | `AppLocalDataLocation/logs/folimeld.log` (`strict=False`) | `%LOCALAPPDATA%\Folimeld-Desktop\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) | `%LOCALAPPDATA%\Folimeld-UV-Tool\logs\<版>\<起動ID>\folimeld.log` (`strict=True`) |
| **Mutex** | なし | `Local\Folimeld-Desktop` | なし | `Local\Folimeld-UV-Tool` |
| **環境検証** | `is_packaged() == True` | `win32` / `x64` / `frozen` / 非 MSIX | `win32` / `x64` / CPython 3.12.16（パッチ一致） / 非 frozen / 非 MSIX / 専用 `.venv` / lock SHA-256 & 依存14件一致 | `win32` / `x64` / **CPython 3.12.x（マイナー一致）** / 非 frozen / 非 MSIX / 仮想環境 (`sys.prefix != sys.base_prefix`) / **依存14件完全一致** |
| **Sponsors / Store支援** | `StoreSupport` 有効、Sponsors 非表示 | `StoreSupport` 無効、Sponsors 表示 | `StoreSupport` 無効、Sponsors 表示 | `StoreSupport` 無効、Sponsors 表示 |
| **Open With 登録** | MSIX マニフェスト | 非登録 | 非登録 | 非登録 |
| **リソース解決** | `sys._MEIPASS` | `sys._MEIPASS` (`_internal/`) | リポジトリルート | パッケージ内 `folimeld/_resources/` |

## 2. ビルドと配布物のステージング

`tools/uv_tool_build.py` は `pyproject.toml`、`folimeld/__init__.py`、`windows-uv-runtime.json`、`requirements-windows-uv.lock` の整合を検査した上で、決定論的な Pure Python Wheel と配布用ファイルを新しい出力ディレクトリへ生成します。

```powershell
python -m tools.uv_tool_build --output .\dist\uv-tool-release
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

GitHub Release から `.whl`、`requirements-windows-uv.lock`、`SHA256SUMS.txt` を取得し、SHA-256 を照合してから `uv tool install` を実行します。

```powershell
$ErrorActionPreference = 'Stop'
# 1. SHA-256 の確認
Get-FileHash .\folimeld-0.3.5-py3-none-any.whl, .\requirements-windows-uv.lock -Algorithm SHA256

# 2. uv tool install（CPython 3.12.x・ハッシュ付きロック指定・ソースビルド禁止）
uv tool install --python 3.12 --with-requirements .\requirements-windows-uv.lock --no-build .\folimeld-0.3.5-py3-none-any.whl
```

- **通常起動（GUI・コンソールなし）**: `folimeld`
- **診断起動（標準エラー出力確認用）**: `folimeld-console`
- **アンインストール**: `uv tool uninstall folimeld`（`%LOCALAPPDATA%\Folimeld-UV-Tool` の設定・ログは削除されません）

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
