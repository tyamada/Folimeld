# AlmaLinux9のPython・PyInstaller・Pillow・OS共有ライブラリ確認

実施日: 2026-11-12（日本時間）。[Qt/MuPDF調査](linux-almalinux9-qt-mupdf-source-audit_ja.md)の続き。許可済み専用Build環境内に`native-runtime-audit-20261112`を作成した。既存候補・配布物・アプリ版は保持し、公開していない。

## 同梱ELFとソースRPM

Alma候補のPyInstallerアーカイブと`Analysis-00.toc`を読み取り、ELF実体210件すべてのSHA-256がビルド時の参照ファイルと一致した。OSパス由来のファイルはRPMの所有者・正確な版・SOURCERPMを記録した。これらはPythonを含め42種類のソースRPMに対応した。

BaseOS/AppStream/CRBのソースリポジトリを当該取得処理だけで参照し、42個・合計291,092,006バイトを取得。各SRPMのDNFメタデータ内チェックサム、導入済み信頼鍵を使った`rpmkeys --checksig`、保存後のSHA-256を検証した。恒久リポジトリ設定変更、SRPMのインストール、ソースのビルドは行っていない。

最初の`dnf download`は正確な`.src`指定を解決できず2回失敗した。その後のrepoqueryには必要版が存在したため、DNF APIでファイル名・URL・チェックサムを直接照合して取得した。初期エラーをソース消失と判断せず、失敗コマンドも保存した。

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/native-runtime-audit-20261112/
  srpms/           PythonとOS共有ライブラリのソースRPM42個
  pypi-sources/    PyInstallerのsdistとPyPI取得記録
  origins.json    ELF実体とAnalysis参照元・RPM所有者
```

Pythonは`python3.12-3.12.15-1.el9_8.src.rpm`。他にgcc/libstdc++、glib2、fontconfig、freetype、harfbuzz、libX11/XCB、DBus、OpenSSL、libffi、zlib、xzなどを含む。Pythonパッケージの版だけで代用せず、Almaのディストリビューション版・パッチを含むSRPMを保持した。SRPM内のファイル名・サイズ・ダイジェストも記録したが、全specのビルドフラグやリンク結果の再現検証は未実施。

導入済み所有パッケージの`/usr/share/licenses/`から45文書の本文とハッシュを保存した。これはOSパッケージ側の文書収集であり、現在の候補へ追加同梱したことを意味しない。

## PyInstallerと告知修正

PyInstaller6.22.2のsdistをPyPIのSHA-256`89b65a3ad07d9dd5832253e37bc45f31872d10d7f9d5c9fd0fdd6088a83829dd`と照合して保存した。sdistには今回比較対象としたLinux用ビルド済みbootloader項目はなく、ソース・告知の収集とビルド済みwheelの来歴確認は区別する。

Linux候補には導入済み`run`が使用されている。`console=False`だからLinuxでも`runw`になるとは判断しない。単純な実行ファイル先頭ハッシュは不一致だったが、導入済みPyInstallerの`building/api.py`ではobjcopyでpydataセクションを追加していることを確認した。

ELF64のセクションヘッダー参照`e_shoff/e_shnum/e_shstrndx`だけを正規化すると、2つのPT_LOAD領域が一致した。プログラムヘッダーも一致。これは明示した正規化条件でのロード領域照合であり、コンパイラー来歴の証明ではない。初期の単純先頭比較と後続の照合を記録に分けて保持した。

既存候補のInstalled-packagesにはPyInstaller版の項目がなく、既存の告知収集対象から外れていた。`folimeld/license_info.py`へPyInstallerを追加し、インストール済み`COPYING.txt`の全文を次回ビルドのInstalled-packagesへ取り込むよう修正した。全文収集の回帰テストを追加し、ライセンス・ソース対応の既存テストと合わせて11件成功、変更ファイルのruffも成功した。実際のビルド環境のCOPYING全文が生成告知に含まれることも検証した。

この修正はWindows/Linux/macOS共通の次回ビルドへ適用される。過去の候補の告知・対応ソースZIPを変更せず保持しているため、反映には新しい候補の再ビルド・検証が必要。

## Pillowと残る範囲

Pillowの画像ライブラリは[後続SBOM・ソース調査](linux-almalinux9-pillow-native-source-audit_ja.md)でアーカイブ21件・パッチ3件を収集し、wheel告知22件を照合した。下記はこの調査時点の範囲であり、wheel来歴とAlma8由来libXauの署名確認、新候補への反映は引き続き残る。

Pillow由来のネイティブ19件はAnalysis参照元と一致した。wheel付属のライセンス文書1件は既存候補のInstalled-packagesに含まれていた。Pillow12.3.0のsdistには依存取得スクリプトと内包raqmなどがあるが、これだけでwheel内画像ライブラリの対応ソース一式とは扱わない。

FreeType、LittleCMS、WebP、libavif、libjpeg-turbo、OpenJPEG、libtiff、zlib-ng等の版表示は[先行監査JSON](linux-amd64-release-input-audit-2026-11-12.json)に記録済み。これらのwheel側のソース・パッチ・ビルド条件の確認は残る。OSのfreetype等のSRPMがあることを、wheel内の別版ライブラリのソース収集済み根拠にはしない。

全210件の由来、SRPM42個の取得先・署名・ハッシュとpayload一覧、OS告知45文書、PyInstaller/Pillow、ヘッダー正規化条件、テスト・ruff結果は[検証JSON](linux-almalinux9-native-runtime-source-audit-2026-11-12.json)へ保存した。大きなソース本体は専用WSL内に保持している。今回の調査は対応付けと資料収集であり、完全なビルド来歴やライセンス適合性の認定ではない。

次はPillow画像ライブラリとwheelビルド来歴の確認、収集告知の次候補への反映、再ビルド・導入・GUI・ライセンス画面の確認。公開版との統合・版決定、通常デスクトップ・アプリ版間移行も残る。
