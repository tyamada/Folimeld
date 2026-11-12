# AlmaLinux 9.8の関連付け・日本語名保存・RPM更新検証

実施日: 2026-11-12（日本時間）。許可済みの専用AlmaLinux9 Build/Test環境内で実施した。アプリ版は非公開検証用0.3.3を維持した。[基礎検証](linux-almalinux9-rpm_ja.md)と[追加GUI検証](linux-almalinux9-extended-gui-verification_ja.md)の続きであり、GUIツール・EPEL追加後の環境での結果である。

## 関連付けと日本語パス

専用XDG設定だけでapplication/pdfの既定をfolimeld.desktopに指定し、`日本語 パス/関連付け 試験.pdf`をGIO経由で開いた。日本語を含む3ページの表示を確認し、1ページ目を右回転して`保存 結果.pdf`へGUI別名保存・再読込した。PyMuPDF照合で3ページ・回転[90,0,0]・各ページの文字保持を確認。原本と関連付け用コピーのSHA-256は元の`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`と一致した。

保存PDF SHA-256: `50984c86dcfdcad339f26a133cc449d4a5745832137f218174e6a5264705fd5b`。

初回は明示的D-BusセッションなしでもGUIが現れたが、GLibのGDBus警告があり、アプリ終了後もGIOが待機したため、試験用GIOだけを終了した。初回を正常終了の合格とは扱わない。準備記録の完成前に開始した別セッションはFileNotFoundErrorで失敗した。その後、独立D-Busセッションで再試験した。標準出力パイプを使った取得は子アプリの出力継承によりタイムアウトしたため、ログファイルへ分離してGIO自体の終了コード0とPDF表示を確認した。これらの失敗・警告・限定条件は[関連付けJSON](linux-almalinux9-mime-verification-2026-11-12.json)に保持した。

画面: [関連付け起動](linux-almalinux9-extended-gui-verification/08-mime-nonascii-loaded.png)、[日本語名保存](linux-almalinux9-extended-gui-verification/09-nonascii-saved.png)、[再読込](linux-almalinux9-extended-gui-verification/10-nonascii-reopened.png)、[独立D-Bus再試験](linux-almalinux9-extended-gui-verification/11-mime-isolated-dbus.png)。所有者と試験環境を照合したGUI・セッションは終了した。

## 梱包revision更新

同一ELFをrevision2として別名梱包し、既存revision1を保持した。新規Test環境内でweak dependenciesを無効にしたdnf upgradeにより`0.3.3-1.alma9_8`から`0.3.3-2.alma9_8`へ更新成功。導入前後のELF一致、`rpm -V folimeld`、`dnf check`が成功した。更新後、一般ユーザーでoffscreen/xcbを各12秒起動し、試験プロセスを終了した。

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/packages/folimeld-0.3.3-2.alma9_8.x86_64.rpm
RPM SHA-256: bd93161bca6ed6cd45f0b23a1591dc4f5d0f356608a26eaa679536ad6fa772f9
ELF SHA-256: e7df5b946593a785d5d2c68ba15caa110903ee86b70b30eea784ba8a56f34914
```

対応ソースZIPのハッシュとELFの関連、更新ログ、起動結果、保存PDFデータ、追加3画面のハッシュは[保存・更新JSON](linux-almalinux9-update-nonascii-verification-2026-11-12.json)へ記録した。独立D-Bus画面のハッシュは関連付けJSONに含む。

## 残る制約

WSLg X11・専用XDG/D-Bus条件での限定試験であり、通常デスクトップでのファイルマネージャーのダブルクリックは未確認。更新は同一実行ファイルの梱包revision間であり、異なるアプリ版や設定の移行試験ではない。他EL系OS、AlmaLinux10、ARM64を合格とは扱わない。公開版との統合・依存ソースとライセンスの公開前確認も残る。既存環境・配布物・README・CHANGELOG・アプリ版を保持し、公開は行っていない。
