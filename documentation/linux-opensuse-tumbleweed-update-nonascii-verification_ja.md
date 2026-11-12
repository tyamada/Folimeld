# Tumbleweedの関連付け・日本語名保存・RPM更新検証

実施日: 2026-11-12（日本時間）。許可済みの新規Tumbleweed Build/Test環境で、スナップショット20261110の候補を使用した。[基礎検証](linux-opensuse-tumbleweed-rpm_ja.md)、[PDF編集GUI](linux-opensuse-tumbleweed-gui-verification_ja.md)、[追加GUI](linux-opensuse-tumbleweed-extended-gui-verification_ja.md)の続きである。

## 関連付けと日本語名保存

設定を`/home/folimeld-test/verification/mime-gui-20261112`へ分離し、`日本語 パス/関連付け 試験.pdf`に合成原本のコピーを作成。この専用XDG設定だけで`gio mime application/pdf folimeld.desktop`を指定した。

セッションバスなしのgio openは終了コード0でもGUIが現れず、合格としなかった。独立dbus-run-sessionでは導入済みdesktopエントリ経由で通常候補が起動し、日本語・空白入りパスを引数として3ページを表示した。[画面](linux-opensuse-tumbleweed-extended-gui-verification/08-mime-nonascii-loaded.png)、[関連付けJSON](linux-opensuse-tumbleweed-mime-verification-2026-11-12.json)。

1ページ目を右回転し、同じ日本語フォルダへ`保存 結果.pdf`という新規名でGUI保存した。合成キー入力は150ms間隔とし、保存前に入力欄の文字列を確認した。保存後のファイルを一覧から選んでGUI再読込にも成功した。[保存](linux-opensuse-tumbleweed-extended-gui-verification/09-nonascii-saved.png)、[再読込](linux-opensuse-tumbleweed-extended-gui-verification/10-nonascii-reopened.png)。

専用TumbleweedビルドPythonのPyMuPDFで、3ページ・回転[90,0,0]・各ページの文字保持を確認。保存PDF SHA-256は`ba37c6eeba454bdd1001c10717dd17fc2b8c0b2466151cfd9cc828e70d4313d8`。原本と関連付けコピーは`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変。所有者と起動引数を確認したGUIと専用D-Busセッションを終了した。

## RPM更新

同一ELFをrevision3として別名梱包し、revision1/2とログを保持した。アプリ本体の再ビルド・版変更は行っていない。

```text
/home/folimeld-build/folimeld-candidates/susetw-20261112/packages/folimeld-0.3.3-3.tw20261110.x86_64.rpm
RPM SHA-256: 7c7dba88bac92b1c8dcbcab6031f496812ba687a2f5c04eec7c2f77606b3f6bb
ELF SHA-256: d5395dec696d6a001633ec642da8a784ac0220ab02ac1a8973392fdde0a20d43
```

zypper installへローカルRPMだけの未署名許可とno-recommendsを指定し、0.3.3-2.tw20261110から0.3.3-3.tw20261110へ更新成功。標準リポジトリの署名検証を維持した。ELFは更新前後で一致し、rpm -Vとzypper verify --dry-runが成功した。

更新後の一般ユーザー起動をoffscreen/xcbで各12秒確認し、試験プロセスを終了した。対応ソースZIP・RPM/ELF関連、更新コマンド・終了コード・起動結果、保存データ、追加3画面は[更新・保存検証JSON](linux-opensuse-tumbleweed-update-nonascii-verification-2026-11-12.json)に保存した。基礎検証JSONはrevision2時点の記録として保持する。

関連付けは独立XDG/D-BusのGIO経由であり、通常ファイルマネージャーのダブルクリックは未確認。更新は同じELFの梱包revision変更で、アプリ版間や設定形式の移行試験ではない。追加GUI依存を含む環境で、最初の最小依存試験と区別する。完全なLinuxデスクトップ、別スナップショット、ARM64、幅広い入力条件、公開前の依存ソース・ライセンス確認は残る。既存環境・配布物・アプリ版を保持し、公開は行っていない。
