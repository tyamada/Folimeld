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

専用Python3.12.16環境を使用。ランタイム依存版はpackaging/windows/desktop-runtime.jsonの14件と同じ値を検査しますが、uv自体は導入にも実行にも使いません。
PyInstaller6.22.2、hooks-contrib2026.7を検査します。バイナリ収集元は専用PythonとWindowsに限定し、UPX無効・DPI manifestを維持します。
収録順を明示ソートしますが、異環境でのバイト再現性は未保証です。Store向けFolimeld.specは変更しません。

ビルド前に新しい版専用のファイルバージョン情報と、別途点検済みのlegalフォルダーを用意します。
legalのreviewed-files.jsonにはdistribution=windows-desktop-x64とfilesの相対パス→SHA256を記録し、少なくともInstalled-packages.txt、THIRD-PARTY-NOTICES.txt、DEPENDENCY-SOURCES.jsonを含めます。
これはハッシュ固定のガードであり、ライセンス確認を自動で代替しません。旧cp314由来のlicenses資料やuvの未同梱前提の資料を、実物対応を調べずに転用しません。
Qt等の対応ソース・パッチ・収録物を点検するまで、このガードを通す架空の資料は作らないでください。

承認後のビルド入口はpython -m tools.desktop_build --output <新規絶対パス> --legal-root <点検済み資料> --version-info <専用版情報> --input-root <照合済み取得物フォルダー> --crt-root <照合済みCRT専用フォルダー>です。
既存出力先があれば停止。制限PATHと依存版、資料ハッシュを検査し、build-inputs.jsonとpyinstaller.logを保存します。
アプリの対応ソースZIP・Gitコミット・全入力/全ペイロード・最終setupの対応台帳はビルド段階で別途確定し、公開ゲートで照合します。

## Inno Setup候補

公式Inno Setup7.1.1 x64配布EXEのハッシュを固定し、署名を確認しました。導入・実行は行っておらず、導入後のISCC版・実体の確認は残件です。
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


## Desktop専用固定入力とQt収録方針

packaging/windows/desktop-runtime.jsonにPython配布ハッシュ、依存14件の版・wheel URL/SHA256、PyInstaller/hooks版を独立保持します。uv設定は参照しません。入力自体のハッシュをbuild-inputs.jsonへ記録します。
Desktop specだけにtools/desktop_qt.pyを適用。Core/Gui/Widgetsと任意のSVG/OpenGL支援を許可し、VirtualKeyboard・Charts・Graphs・QML/Quick・WebEngine・Pdf・Multimedia等の未使用モジュール、DLL/プラグイン/QMLデータを除外します。保持コードが除外Qtや解決不能Qtに依存する場合、またCore/Gui/Widgets/qwindows欠落時には停止します。除外一覧は将来のworkpath/desktop-qt-exclusions.jsonに記録します。
動的読込・日本語IME・GPU・実ペイロード受入は未確認。Store/uv specとランチャーは変更しません。ビルド補助は依存取得・環境作成を行いません。工具wheel7件とInno配布EXEのハッシュを固定しました。独立環境構築と導入後の工具の実体対応は残件です。wheelハッシュは再配布許諾やインストール済み全ファイル一致の証明ではありません。告知承認ガードを維持します。


## 配布入力のハッシュ確認（2026-11-15）

固定台帳に工具7件の版/wheelとInno7.1.1 x64配布EXEを追加。読み取り専用の事前検査は--input-rootを必須とし、Python・依存14wheel・工具7wheel・Innoの計23入力を、ビルド出力作成前にハッシュ照合します。欠落・改変・指定領域外への参照は停止します。この照合は入力を導入・実行しません。
専用desktop-runtime-requirements.txt/desktop-tools-requirements.txtは直接wheel URL、--require-hashes、--only-binary=:all:を指定。インストールには未使用です。wheelメタデータでWindows x64/Python3.12.16の有効な依存19条件（任意extraなし）が固定版で満たされることを確認。取得物は照合済みですが環境は新規作成していません。導入後の全ファイル対応とInno工具内部の確定は残件です。ハッシュ照合は再配布承認を意味しません。ソース/ライセンス審査は未完了です。点検済み資料の承認前に、第三者告知・対応ソース、CRT再配布条件、導入後Innoコンパイラ/スタブとの対応を確定してください。取得物ハッシュだけでこれらの点検を完了扱いにはしません。


## Desktop専用CRT収録

packaging/windows/desktop-crt.jsonに正規Desktop x64 CRT14.44.35211.0の7件だけをSHA256/サイズで固定。--crt-rootはその7ファイルのみを含む専用フォルダーを指定します。事前検査で領域内参照・内容・x64 PEを確認し、specの収録直前にも再照合します。導入・実行はしません。
Analysis入力に対する従来のPython/Windows由来ガードを維持し、その後に個別照合したCRTだけを追加します。Program Filesや作業領域全体を許可しません。binaries/datas両TOCの承認名CRT重複を正規7件へ統一し、未知CRT・OSのUCRT/API-set収録・名前変更したCRTは停止します。入力ファイルは削除・変更しません。
Desktop specは_internalを明示。COLLECT後に7件の正確な配置/ハッシュを再検査し、配下/EXE隣への重複、追加CRT、欠落/改変、領域外参照は失敗とします。workにdesktop-crt-inputs.jsonとdesktop-crt-collected.jsonを保存。検査失敗時はビルド失敗とし、途中出力を受入済み候補にしません。
入力検査・模擬TOC/単体検査は、実凍結アプリのDLL読込・ワーカー・互換性確認の代替ではありません。再配布条件/告知/対応ソースの審査とreviewed-files.jsonは別の必須条件で、CRTハッシュ一致を法的承認にしません。Store/uv specとデータを維持します。


## 固定入力の形式・requirements同期検査

台帳読込時にruntime/工具wheelへ同じ規則を適用します。SHA-256は小文字16進64文字、URLはHTTPSかつホストが正確にfiles.pythonhosted.orgであることを要求。資格情報・ポート・query/fragment・空白・領域移動指定を拒否し、安全な.whl名とURLの復号後末尾名が一致することも確認します。
requirements2件は--require-hashesと--only-binary=:all:を各1回だけ必須とし、直接wheel指定のみ許可。名前・URL・SHA-256を対応するJSON区分と一致させ、欠落/追加/重複・追加pipオプション・版だけの指定をビルド出力作成前に拒否します。空行/コメントは許可し、配布名はPythonパッケージの名前規則で正規化します。両requirements自体のハッシュもbuild-inputs.jsonへ記録します。
ローカルファイルの検査のみで、導入・インデックス照会・uv実行・法的承認を行いません。導入後実体との対応、Inno内部工具、ライセンス/対応ソースの点検は残件です。
