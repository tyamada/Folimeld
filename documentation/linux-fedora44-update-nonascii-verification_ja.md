# Fedora 44の関連付け・日本語名保存・RPM更新検証

実施日: 2026-11-12（日本時間）。許可済みの新規Fedora44 Build/Test環境だけを使用した。[基礎検証](linux-fedora44-rpm-verification_ja.md)、[GUI編集](linux-fedora44-gui-verification_ja.md)、[暗号化PDF・画像・IME](linux-fedora44-extended-gui-verification_ja.md)の続きである。

## 関連付けと日本語名での保存

設定・キャッシュを`/home/folimeld-test/verification/mime-gui-20261112`へ分離し、同ディレクトリの`日本語 パス/関連付け 試験.pdf`に原本のコピーを作成した。専用XDG設定で`gio mime application/pdf folimeld.desktop`を指定した。通常ユーザーの既存設定は変更していない。

セッションバスなしの`gio open`は終了コード0でもGUIが現れず、成功として数えていない。独立した`dbus-run-session`で同じ関連付けを使うと、導入済みdesktopエントリから通常候補が起動し、日本語・空白入りパスを引数として3ページを表示した。[画面](linux-fedora44-extended-gui-verification/08-mime-nonascii-loaded.png)、[関連付けJSON](linux-fedora44-mime-verification-2026-11-12.json)。

1ページ目を右回転し、同じ日本語フォルダ内へ`保存 結果.pdf`という新規名でGUI保存した。GUIで開き直して回転表示も確認した。[保存後](linux-fedora44-extended-gui-verification/09-nonascii-saved.png)、[再読込](linux-fedora44-extended-gui-verification/10-nonascii-reopened.png)。ファイル選択の補完確定とダイアログ消失を再観測して完了を判断した。

PyMuPDF照合結果は3ページ・回転[90,0,0]・各ページの文字内容保持。保存PDF SHA-256は`b09127fb42ef54dae28bd26e7df01913bf2b81bec02cdf58f44ad5c59808dbc0`。原本と関連付け用コピーはともに`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。試験GUIと専用D-Busセッションを識別して終了した。

## RPM更新

生成済みの同一ELFをrevision2として別ファイルに梱包し、revision1を保持した。アプリ本体の再ビルドや版変更は行っていない。

```text
/home/folimeld-build/folimeld-candidates/fedora44-20261112/packages/folimeld-0.3.3-2.fc44.x86_64.rpm
RPM SHA-256: 96e44e40cfad831f08b1fecd7d0289a32c23cc535db142429f67b7e86e0f8bdc
ELF SHA-256: 8347c123b1af32f37b98898c3b6e3e9db778798cf09f708ee671ad194bdc15ae
```

`dnf -y --setopt=install_weak_deps=False upgrade <RPM>`で0.3.3-1.fc44から0.3.3-2.fc44へ更新成功。ELFは更新前後で一致し、`rpm -V folimeld`と`dnf check`も成功した。更新後、一般ユーザーのoffscreen/xcb起動を各12秒確認して試験プロセスを終了した。対応ソースZIPとRPM/ELF対応記録も照合した。

コマンド・終了コード・ソース対応・起動ログ・追加3画面のハッシュは[更新・保存検証JSON](linux-fedora44-update-nonascii-verification-2026-11-12.json)へ保存した。基礎検証JSONはrevision1時点の記録として保持する。

## 制約

関連付けは独立XDG/D-Bus環境でのGIO経由であり、通常のファイルマネージャーのダブルクリックは未確認。更新は同一実行ファイルの梱包revision更新で、アプリ版間や設定形式の移行試験ではない。更新後起動はGUI依存追加後の環境で、最初の最小依存試験とは区別する。完全なLinuxデスクトップ、ARM64、幅広い入力条件、公開前の依存ソース・ライセンス確認は残る。既存環境・配布物・アプリ版を保持し、公開は行っていない。
