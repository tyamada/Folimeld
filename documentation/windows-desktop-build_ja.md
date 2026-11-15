# Windows x64 Desktop版：ビルド前の実装・確認事項

[English](windows-desktop-build.md)

未ビルド・未公開の候補設定です。Store版・uv版とは別の配布方式です。
Python/uv/PowerShellを利用者へ要求しないPyInstaller onedir＋Inno Setupを使います。

## 実装

- launch_desktop.pyはfreeze_supportを維持し、Windows x64・凍結・非MSIXを確認して専用入口を呼びます。
- 設定：%LOCALAPPDATA%/Folimeld-Desktop/settings/settings.ini。INIのfallbackなし。
- ログ：%LOCALAPPDATA%/Folimeld-Desktop/logs/<版>/<起動ID>。初期化失敗時は停止。
- uvとの同時プロファイル有効化を拒否し、既存設定の自動移行・既定PDF変更・Open With登録はしません。
- SponsorsはDesktop専用プロファイルが有効な場合に表示。Storeでは非表示を維持。
- Local\Folimeld-Desktop mutexを通常起動の存続中に保持。Inno Setupは同じmutexを確認し、実行中の更新・削除を拒否します。ワーカーを強制終了しません。

## onedir候補の前提

専用Python3.12.16環境を使用。ランタイム依存版はwindows-uv-runtime.jsonの14件と同じ値を検査しますが、uv自体は導入にも実行にも使いません。
PyInstaller6.22.2、hooks-contrib2026.7を検査します。バイナリ収集元は専用PythonとWindowsに限定し、UPX無効・DPI manifestを維持します。
収録順を明示ソートしますが、異環境でのバイト再現性は未保証です。Store向けFolimeld.specは変更しません。

ビルド前に新しい版専用のファイルバージョン情報と、別途点検済みのlegalフォルダーを用意します。
legalのreviewed-files.jsonにはdistribution=windows-desktop-x64とfilesの相対パス→SHA256を記録し、少なくともInstalled-packages.txt、THIRD-PARTY-NOTICES.txt、DEPENDENCY-SOURCES.jsonを含めます。
これはハッシュ固定のガードであり、ライセンス確認を自動で代替しません。旧cp314由来のlicenses資料やuvの未同梱前提の資料を、実物対応を調べずに転用しません。
Qt等の対応ソース・パッチ・収録物を点検するまで、このガードを通す架空の資料は作らないでください。

承認後のビルド入口はpython -m tools.desktop_build --output <新規絶対パス> --legal-root <点検済み資料> --version-info <専用版情報>です。
既存出力先があれば停止。制限PATHと依存版、資料ハッシュを検査し、build-inputs.jsonとpyinstaller.logを保存します。
アプリの対応ソースZIP・Gitコミット・全入力/全ペイロード・最終setupの対応台帳はビルド段階で別途確定し、公開ゲートで照合します。

## Inno Setup候補

公式Inno Setup7.1.1を固定候補とします。導入物の署名・ハッシュとISCC版の実確認は未実施です。
packaging/windows/Folimeld-desktop.issにDesktopVersion（数値版）、PayloadRoot（確認済みonedir）、OutputRoot（新規専用出力）、PayloadReviewed=1を明示してコンパイルします。
版の命名、全入力ハッシュ、EXE/インストーラー/アンインストーラー署名方針はビルド前に確定します。

- 通常ユーザー単位、Windows11 x64のみ。ARM64は受け付けません。
- 固定Desktop専用AppId。%LOCALAPPDATA%/Programs/Folimeld-Desktop/versions/<版>に配置。
- スタートメニューFolimeld Desktop。インストール直後に自動起動しません。
- 同版フォルダーがあれば上書きせず停止。旧版は残し、異版更新時にショートカットを新しい版へ向けます。
- Inno管理のアプリファイル・ショートカットを削除対象とし、%LOCALAPPDATA%/Folimeld-Desktopの文書/設定/ログ、Store/uv領域は削除対象にしません。再帰的な一括削除は定義しません。

設定バックアップ・形式移行・完全な失敗時復旧/旧版復帰は未実装・未試験です。部分導入失敗時の動作と合わせて、公開前の受入で確認します。
現候補をそのまま一般公開可能とは扱いません。

## 今回の検査と残件

対象Pythonでプロファイル分離・不正環境拒否・Sponsors条件・既存Store/uv経路・資料ハッシュ検査を自動試験します。
QtのOS条件は模擬し、実インストーラー/実Frozenの受入を代替しません。
ISCCでのコンパイル・Inno Setup構文のコンパイラ検証・実EXE生成はまだ行いません。
起動速度、PDF/画像操作、3ワーカー、Per-Monitor V2、実画面の支援リンク、併存、更新/削除/復旧、法的資料・署名は今後の受入です。
試験PC更新・WACK・Hosted API比較は行いません。
