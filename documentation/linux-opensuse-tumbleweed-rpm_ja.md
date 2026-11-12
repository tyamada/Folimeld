# openSUSE Tumbleweed amd64 RPMの基礎検証

実施日: 2026-11-12（日本時間）。ユーザーの追加許可に基づき、`Folimeld-openSUSE-Tumbleweed-Amd64-Build`と`Folimeld-openSUSE-Tumbleweed-Amd64-Test`を新規WSL2として作成した。配置先は`C:\Users\takum\WSL\`配下の各登録名と同名のディレクトリ。作成前に登録名・配置先が未使用、Cの空き約249.0 GiBを確認した。既存Leap/Fedora/Kali/Ubuntu/Debianと配布物を保持した。

## スナップショットと実装

初期イメージは20261102。初期パッケージ一覧を保存して標準リポジトリをrefreshし、Tumbleweedの`zypper dup --no-recommends`で更新した。両環境の`VERSION_ID`は20261110で一致。ビルドにはPython 3.14.8とglibc 2.44を使用し、固定制約のwheelを取得した。実施日をスナップショット版の代わりには使わない。

`build_linux.sh tumbleweed-rpm`、`tools/package_linux_tumbleweed_rpm.py`、テストを追加した。OSのIDをopensuse-tumbleweedへ限定し、VERSION_IDは8桁の有効な暦日として検査する。出力名は`.tw20261110`とCPU・revision、既定出力先は`releases/opensuse-tumbleweed/<実スナップショット>/<CPU>/`。既存出力と出力リンクを拒否する。

SUSE specと一時梱包処理を共用し、Release識別子を引数化した。Leapモードは引き続き16.1専用でlp161、Fedoraモードも従来のOS制限と出力を維持する。専用コピーの出力・仮想環境・TMPDIR・キャッシュへ分離してビルドした。アプリ版は非公開検証用0.3.3のまま。

## 検証中に修正した点

最初の回帰試験はビルド側のlibdbus-1.so.3不足で開始できなかった。新規ビルド環境へlibdbus-1-3を追加した。SUSE RPMのDBus必須依存宣言は既にあり、試験側はRPMの依存解決で導入する。

PyInstallerはホストのQtライブラリ不足でも完了する場合があるため、共通ビルドスクリプトへQtCore/QtGui/QtWidgetsとPyMuPDFのimport事前検査を追加した。依存補完と事前検査を含めrevision2で再ビルドし、最初のrevision1は導入せず保持した。

## 検証範囲

SUSE/Fedora/TumbleweedのOS拒否・出力名、スナップショット日付、履歴・モデル・サムネイル・画像・ソース対応を含む93件・26サブテストが成功（4.46秒）。追加実装のruffも成功した。

基礎検証の詳細、RPM・ELF・対応ソース、導入・起動・削除再導入の記録は[検証JSON](linux-opensuse-tumbleweed-verification-2026-11-12.json)を参照する。PDF編集・保存再読込は[後続GUI試験で確認し](linux-opensuse-tumbleweed-gui-verification_ja.md)、IME・画像・暗号化PDFも[追加検証した](linux-opensuse-tumbleweed-extended-gui-verification_ja.md)。GIO関連付け・非ASCII保存・梱包revision更新も[確認した](linux-opensuse-tumbleweed-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、他スナップショット、ARM64は未確認。依存ソースとライセンスの公開前確認も残る。既存候補・アプリ版・READMEを保持し、公開は行っていない。

## 生成候補と導入結果

```text
/home/folimeld-build/folimeld-candidates/susetw-20261112/packages/folimeld-0.3.3-2.tw20261110.x86_64.rpm
RPM SHA-256: ef4ff9f2f6de37e224aa449b2bc6ce6275fb5279fddcba8179f2179b11d8296f
ELF SHA-256: d5395dec696d6a001633ec642da8a784ac0220ab02ac1a8973392fdde0a20d43
```

試験側にgcc・rpm-build・Python3.14本体/pip・推奨日本語フォントがないことを確認し、`zypper install --allow-unsigned-rpm --no-recommends <ローカルRPM>`で導入した。未署名許可は指定したローカル候補だけを対象とし、標準リポジトリの署名検証を維持した。DBusやGLibはRPMの依存解決で導入され、手動補完は不要だった。

一般ユーザーのoffscreen/xcb起動を各12秒確認し、timeoutで試験プロセスを終了した。削除時に実行ファイル・desktop項目・アイコン・ライセンスが消失し、再導入で復元、ELFハッシュも一致。削除前と再導入後のrpm -V、zypper verify --dry-runが成功した。起動時のWSL systemdユーザーセッション警告やfitz非推奨警告はログに保持し、OS/Windows設定は変更していない。

対応ソースZIP、RPMとELFの関連記録、主要コードの作業ツリーとのハッシュ一致、Virtual Keyboard同梱0件を確認した。前述のJSONはこのrevision2時点の結果であり、最初のrevision1は未導入・未検証として区別する。
