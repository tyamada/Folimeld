# AlmaLinux9 revision3の削除再導入・GIO関連付け確認

実施日: 2026-11-12（日本時間）。[告知入り新候補](linux-almalinux9-notices-candidate_ja.md)と[GUI回帰](linux-almalinux9-revision3-regression_ja.md)の続き。許可済み専用`Folimeld-AlmaLinux9-Amd64-Test`内で実施した。旧候補・元素材・既存配布物を保持し、公開していない。

対象は`folimeld-0.3.3-3.alma9_8.x86_64`。RPM SHA-256は`3f1da813afaedad6aa6d47fa8b5d4d1cd0e2bba429e86b1f34b9c1590433be28`、導入済みELFは`b0915988edbfcea48704cf013f5961b5c496d7b6689a888f019cff9034f46455`で新候補と一致した。

## 削除・再導入

専用WSL登録名、導入版、候補RPMのハッシュ、試験アプリ未起動を確認してから実施した。

1. `rpm -V folimeld`と`dnf check`が成功。
2. `dnf -y --setopt=clean_requirements_on_remove=False remove folimeld`で削除。実行ファイル・desktop項目・アイコン・ライセンスの4ファイルが消失し、RPMの未導入を確認。
3. `dnf -y --setopt=install_weak_deps=False install <revision3 RPM>`で再導入。4ファイルのハッシュが削除前と一致。
4. 再導入後も`rpm -V folimeld`と`dnf check`が成功。

前回GUI回帰で作成したPDFと設定6ファイルのハッシュは削除直後・再導入後とも保持された。依存は意図的に自動削除しなかった。GUIツール/EPEL追加済みの環境内でのパッケージ動作確認であり、新規最小環境への導入試験とは区別する。

## GIO関連付けと日本語パス

新規試験設定`/home/folimeld-test/verification/revision3-gio-20261112`へXDG各設定を分離し、専用設定内だけでapplication/pdfの既定をfolimeld.desktopへ設定した。独立dbus-run-session内で、標準出力をログファイルへ分離してGIOを実行した。

```text
日本語 パス/関連付け 試験.pdf
```

`gio info`はapplication/pdf、`gio mime`はfolimeld.desktopを返し、`gio open`は終了コード0。WSLg GUIに正しいファイル名と日本語を含む3ページが表示された。[画面証拠](linux-almalinux9-revision3-lifecycle/01-gio-nonascii-opened.png)。元素材・関連付け用コピーともSHA-256`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。

今回の独立D-Bus条件のGIOログはfitzの非推奨警告のみ、セッションログは空だった。旧候補で記録した明示セッションなしのGIO警告・待機を、今回解消したとは扱わない。通常ファイルマネージャーのダブルクリックや、利用者の既定関連付け変更は試していない。

## 再起動と記録

続いて[新規DNF installrootの最小依存導入・offscreen起動](linux-almalinux9-revision3-minroot_ja.md)を確認した。独立WSLのブートや通常デスクトップとは区別する。

GIO試験後、所有者・試験環境を照合したGUIと専用D-Busを終了。再導入済み候補を一般ユーザーでoffscreen/xcb各12秒起動し、試験終了のため停止した。最後にFolimeldプロセスが残っていないことも確認した。Windows/OS設定は変更していない。

削除・再導入ログ、4ファイルとユーザー作成物のハッシュ、GIO各コマンド・終了コード・ログ、再起動結果、画面ハッシュは[検証JSON](linux-almalinux9-revision3-lifecycle-verification-2026-11-12.json)に保存した。

revision3では編集・保存・暗号化PDF・画像・IMEに続いて、この限定条件のGIOと削除再導入を確認できた。残る主な工程は新規最小環境の導入、通常デスクトップとアプリ版間/設定移行、wheelビルド来歴・Alma8 libXau署名、公開版との統合・版決定。公開準備が完了したとは扱わない。
