# AlmaLinux 9 amd64 RPMの基礎検証

実施日: 2026-11-12（日本時間）。ユーザーの追加許可に基づき、`Folimeld-AlmaLinux9-Amd64-Build`と`Folimeld-AlmaLinux9-Amd64-Test`を新規WSL2として作成した。配置は`C:\Users\takum\WSL\`配下の各登録名と同名のディレクトリ。作成前に未使用であることとCの空き約241.6 GiBを確認した。既存環境・配布物は保持した。

## 固定依存と実装

初期OSはAlmaLinux 9.8、glibc 2.34、Python3.9。両環境の初期パッケージ一覧を保存して標準リポジトリを更新した。ビルド側だけへ標準のPython3.12本体/pipを追加し、専用仮想環境で現requirementsとconstraints-releaseを変更せず、only-binary指定でwheel取得を確認した。

PySide6 6.11.2とcryptography 50.0.2はmanylinux_2_34、PyMuPDF 1.28.2はmanylinux_2_28のwheelを取得できた。これは取得可否の結果であり、実行互換性は後段のテスト・導入起動と分ける。追加リポジトリや制約緩和は行っていない。

`build_linux.sh alma-rpm`、`tools/package_linux_alma_rpm.py`、`packaging/linux/folimeld-alma.spec.in`と拒否テストを追加した。ID=almalinuxかつ9系へ限定し、他EL系OSやAlmaLinux10を拒否する。小版・CPU・revisionを出力へ含め、9.8は`.alma9_8`、既定配置は`releases/almalinux/9.8/<CPU>/`。既存出力とリンクを拒否する。

QtのGL/DBus/GLib/XCB能力依存を明示し、日本語推奨フォントは標準リポジトリで実在するgoogle-noto-sans-cjk-ttc-fontsを指定した。共通の一時梱包・ELF無改変・対応ソース記録を使用し、既存Fedora/Leap/Tumbleweedモードの制限を維持した。新規コピーに未コミット修正を取り込み、出力・仮想環境・TMPDIR・キャッシュを専用ディレクトリへ分離した。

## 検証範囲

Qt/PyMuPDFのimport事前検査、Alma/SUSE/Tumbleweed/FedoraのOS拒否・出力名、PDFモデル・履歴・サムネイル・画像・ソース対応を含む97件・35サブテストが成功（3.73秒）。ruffとシェル構文検査も成功した。

OS・Python・固定依存取得ログ・対応ソース・RPM/ELF、導入・起動・削除再導入の結果は[検証JSON](linux-almalinux9-verification-2026-11-12.json)に保存した。アプリは非公開検証用0.3.3のまま。PDF編集・保存再読込は[後続GUI試験で確認し](linux-almalinux9-gui-verification_ja.md)、IME・画像・暗号化PDFも[追加検証した](linux-almalinux9-extended-gui-verification_ja.md)。非ASCII保存・専用D-BusでのGIO関連付け・梱包revision更新は[保存・更新記録](linux-almalinux9-update-nonascii-verification_ja.md)にまとめた。GUIツール取得のため試験側だけへEPELを追加した段階とは区別する。完全なLinuxデスクトップ、アプリ版間移行、ARM64は未確認。他EL系OSやAlmaLinux10の対応済み根拠にはしない。依存ソース・ライセンスの公開前確認も残る。README・版・既存配布物を保持し、公開は行っていない。

## 成果物と導入結果

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/packages/folimeld-0.3.3-1.alma9_8.x86_64.rpm
RPM SHA-256: e8f7564c95f1a4692de9555c2b37e20eae22ee27e72a21eb802777153becf970
ELF SHA-256: e7df5b946593a785d5d2c68ba15caa110903ee86b70b30eea784ba8a56f34914
```

試験側のgcc・rpm-build・Python3.12本体/pip・推奨フォント未導入を確認し、`dnf --setopt=install_weak_deps=False install <RPM>`で導入成功。OS既定のPython3.9は保持し、検証スクリプトに使用した。凍結アプリの実行にPython3.12の追加導入は不要だった。

一般ユーザーでoffscreen/xcbを各12秒起動し、試験プロセスを終了した。削除時は実行ファイル・desktop項目・アイコン・ライセンスが消失し、再導入で復元、ELFハッシュも一致。削除前・再導入後のrpm -Vとdnf checkが成功した。

対応ソースZIP、RPM/ELF関連、導入済みELF、主要コードの作業ツリーとの一致とVirtual Keyboard同梱0件を確認。glibc下限は2.34。WSLのsystemdユーザーセッション警告とfitz非推奨警告はログに保持し、Windows/OS設定は変更していない。
