# Fedora 44 amd64 RPMの基礎検証

実施日: 2026-11-12（日本時間）。ユーザーの追加許可に基づき、新しいビルド用・試験用WSL2を作成した。既存Fedora45、Ubuntu、Debian、Kaliと既存配布物は保持した。

## 環境と成果物

登録名は`Folimeld-Fedora44-Amd64-Build`と`Folimeld-Fedora44-Amd64-Test`。配置先は`C:\Users\takum\WSL\`配下の各登録名と同名のディレクトリ。作成前に両配置先が未使用であることと、Cドライブの空き約259.7 GiBを確認した。`wsl --install FedoraLinux-44 --name <登録名> --location <配置先> --no-launch`で導入した。

両環境の初期パッケージ一覧を保存して更新後、ビルド側だけへPython・RPMビルド・Qt実行依存を追加した。一般ユーザーはビルド側`folimeld-build`、試験側`folimeld-test`。glibc 2.43を基準とし、glibc 2.44以上を要求するFedora45候補とは別に生成した。

```text
/home/folimeld-build/folimeld-candidates/fedora44-20261112/packages/folimeld-0.3.3-1.fc44.x86_64.rpm
RPM SHA-256: a2dd4769bb8030c2b28a0c98568a89311bbc91982aab05c49e77dcef3b2254d8
ELF SHA-256: 8347c123b1af32f37b98898c3b6e3e9db778798cf09f708ee671ad194bdc15ae
```

これは非公開の検証用0.3.3/revision1であり、既存公開版の再現物とは呼ばない。現在の未コミット修正を専用コピーへ転送し、`build_linux.sh rpm`、Python 3.14、固定制約でビルドした。`FOLIMELD_LINUX_VENV`、`FOLIMELD_LINUX_OUTPUT`、`TMPDIR`とキャッシュを専用コピー配下へ設定した。

## 確認結果

| 項目 | 結果 |
| --- | --- |
| 実ビルド | 既存のFedora用RPM実装をそのまま使用して成功。OS版を44として出力し、glibc下限2.43を宣言 |
| ソース対応 | 埋め込みソースZIPのSHA-256、RPM対応記録、生成ELF・導入ELFの一致を確認。Virtual Keyboard同梱0件 |
| 現在のコードとの一致 | main.py、サムネイル、ビルドスクリプト、RPMヘルパー、specテンプレートのハッシュを照合 |
| 最小依存導入 | 試験側のgcc・rpm-build・python3-pip・推奨日本語フォント未導入を確認後、`install_weak_deps=False`で導入成功 |
| 通常ユーザー起動 | offscreenとxcbでそれぞれ12秒間の生存を確認し、試験プロセスを終了 |
| 削除・再導入 | 実行ファイル・desktop項目・アイコン・ライセンスの消失を確認。再導入で復元、ELFハッシュ一致 |
| 整合性 | 削除前・再導入後の`rpm -V folimeld`と`dnf check`が成功 |
| 回帰テスト | RPM、サムネイル、履歴、モデル検証、画像取込、ソース対応の85件・8サブテスト成功（3.83秒） |

OS・Python・実依存版、ソースZIP、初期/導入後パッケージ一覧、実コマンドと終了コード、起動・テストログは[検証JSON](linux-amd64-fedora44-verification-2026-11-12.json)に保存した。

## 検証中の問題と未確認事項

最初のソース試験はビルド側の`libdbus-1.so.3`不足で開始できなかった。ビルド側へ`dbus-libs`を追加して成功した。失敗ログも保持した。RPMにはDBusの必須依存宣言が既にあり、試験側は手動補完せずRPMの依存解決だけで導入・起動できた。

RPMの`%changelog`未設定警告とWSLのsystemdユーザーセッション警告は残る。Windowsの既存`.wslconfig`項目に関する警告も導入時に表示されたが、設定は変更していない。

起動生存は実画面の操作合格を意味しない。続いてFedora44でPDF編集・保存・再読込を[実画面で確認し](linux-fedora44-gui-verification_ja.md)、IME・画像取込・暗号化PDFも[追加検証した](linux-fedora44-extended-gui-verification_ja.md)。非ASCIIパスの別名保存・GIO関連付け・梱包revision更新も[後続試験で確認した](linux-fedora44-update-nonascii-verification_ja.md)。完全なLinuxデスクトップとアプリ版間移行は未実施。[Fedora45の結果](linux-fedora-rpm_ja.md)は44の合格として流用しない。他OSやARM64、公開前の依存ソース・ライセンス確認も残る。版・README・既存配布物を変更せず、公開も行っていない。
