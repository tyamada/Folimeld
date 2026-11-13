# openSUSE Leap 16.1 amd64 RPMの基礎検証

実施日: 2026-11-12（日本時間）。ユーザーの追加許可に基づき、`Folimeld-openSUSE-Leap16.1-Amd64-Build`と`Folimeld-openSUSE-Leap16.1-Amd64-Test`を新規WSL2として作成した。配置先は`C:\Users\takum\WSL\`配下の同名ディレクトリ。既存環境・配布物は保持した。

## 実装とビルド

`build_linux.sh suse-rpm`、`tools/package_linux_suse_rpm.py`、`packaging/linux/folimeld-suse.spec.in`を追加した。既存の`rpm`はFedora専用のまま維持し、SUSEモードは`ID=opensuse-leap`かつ`VERSION_ID=16.1`に限定した。TumbleweedやSLES、他版を合格扱いしない。

一時RPMツリーへの入力コピー・実行ファイル無改変・排他的な出力作成・対応ソース記録は既存ヘルパーと共有する。共通処理にspecテンプレートの選択引数を加えたが、既定は従来のFedora用。Leap出力は`.lp161`とCPU・revisionで区別し、同名上書きと出力リンクを拒否する。

標準リポジトリでPython 3.13.13、glibc 2.40、Qtの実行依存と推奨フォント`google-noto-sans-cjk-fonts`を確認した。専用コピーに現在の未コミット修正を取り込み、固定制約で実ビルドした。ビルド仮想環境、出力、TMPDIRとキャッシュは専用コピー配下へ分離した。

```text
/home/folimeld-build/folimeld-candidates/suse161-20261112/packages/folimeld-0.3.3-2.lp161.x86_64.rpm
RPM SHA-256: a1eb907c59bbe82f553e97e1cd374c693b4860d6574f2a422f872504d3819ebd
ELF SHA-256: 53fb285ac9efa231e4abf40d82bb69be0b411c04de21890cfd609fd3366cf567
```

非公開の検証用0.3.3/revision2であり、既存公開版の再現物ではない。最初のrevision1と失敗ログは保持している。

## 依存と検証中の問題

最初のソース試験は`libgthread-2.0.so.0`不足で開始できなかった。ビルド側に`libgthread-2_0-0`を導入し、SUSE specへ同ライブラリ能力の必須依存を追加、revision2として再ビルドした。試験側はライブラリを手動補完せず、RPMの依存解決だけで導入する。

ローカルRPMは未署名で、最初のzypper導入は署名確認で中断した。`zypper install --allow-unsigned-rpm --no-recommends <ローカルRPM>`で再試行した。このオプションはコマンド引数に指定した未署名RPMだけを許可する。標準リポジトリの署名確認を無効化せず、システム全体の設定も変えていない。

GUI試験用スクリプトの最初の起動準備では、シェル経由の変数展開でディレクトリ作成が失敗した。アプリを起動する前の失敗であり、展開を使わない絶対パス指定へ修正した。

## 検証記録

RPM・対応ソース・依存一覧・初期試験環境・回帰試験・起動・削除再導入の結果は[検証JSON](linux-opensuse-leap161-verification-2026-11-12.json)に保存した。ソース試験はSUSE/FedoraのOS拒否・出力ガード、PDFモデル・サムネイル・履歴・画像・ソース対応を含む89件・17サブテストが成功（3.98秒）。追加実装のruffとビルドシェル構文検査も成功した。

開発依存（gcc、rpm-build、Python本体/pip）と推奨フォントがない試験環境で導入し、一般ユーザーのoffscreen/xcb起動を各12秒確認した。削除時は実行ファイル・desktop項目・アイコン・ライセンスの消失、再導入時は全ファイル復元とELFハッシュ一致を確認。削除前と再導入後の`rpm -V folimeld`、`zypper verify --dry-run`が成功した。対応ソースZIP・梱包記録・導入ELF、主要コードの作業ツリーとのハッシュ一致、Virtual Keyboard同梱0件も確認した。起動試験プロセスはtimeoutで終了した。

今回の結果はLeap16.1 x86_64限定。PDF編集・保存再読込は[後続GUI試験で確認し](linux-opensuse-leap161-gui-verification_ja.md)、IME・画像取込・暗号化PDFも[追加検証した](linux-opensuse-leap161-extended-gui-verification_ja.md)。GIO関連付け・非ASCII保存・梱包revision更新も[確認した](linux-opensuse-leap161-update-nonascii-verification_ja.md)。通常ファイルマネージャー、完全なLinuxデスクトップ、Tumbleweed、ARM64は未確認。依存ソースとライセンスの公開前確認も残る。READMEの対応済み表記・アプリ版・既存配布物を変更せず、公開は行っていない。
