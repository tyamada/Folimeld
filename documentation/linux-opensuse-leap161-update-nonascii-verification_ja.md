# Leap 16.1の関連付け・日本語名保存・RPM更新検証

実施日: 2026-11-12（日本時間）。許可済みの新規Leap16.1 Build/Test環境だけで実施した。[基礎検証](linux-opensuse-leap161-rpm_ja.md)、[PDF編集GUI](linux-opensuse-leap161-gui-verification_ja.md)、[追加GUI](linux-opensuse-leap161-extended-gui-verification_ja.md)の続きである。

## 関連付けと日本語名保存

専用XDG設定を`/home/folimeld-test/verification/mime-gui-20261112`へ分離し、同ディレクトリの`日本語 パス/関連付け 試験.pdf`へ合成原本をコピーした。この専用設定だけで`gio mime application/pdf folimeld.desktop`を指定した。

セッションバスなしの`gio open`は終了コード0でもGUIが現れず、合格としなかった。独立したdbus-run-sessionでは、導入済みdesktopエントリ経由で通常候補が起動し、日本語・空白入りパスを引数として3ページを表示した。[関連付け画面](linux-opensuse-leap161-extended-gui-verification/08-mime-nonascii-loaded.png)、[関連付けJSON](linux-opensuse-leap161-mime-verification-2026-11-12.json)。

1ページ目を右回転し、同じ日本語フォルダへ日本語・空白入り名で別名保存した。合成キー入力では意図した「保存 結果.pdf」の一文字が欠け、実際の名前は`保 結果.pdf`となった。実際の入力欄・タイトル・一覧を観測し、そのファイルを一覧から選択して開き直した。この入力欠落をアプリ固有の障害と断定しない。[保存後](linux-opensuse-leap161-extended-gui-verification/09-nonascii-saved.png)、[再読込](linux-opensuse-leap161-extended-gui-verification/10-nonascii-reopened.png)。

保存データは3ページ・回転[90,0,0]・各ページの文字保持。保存PDF SHA-256は`3e0ea27dd544045888a79989c28f507987a5b3cb672ac5c58f8f542d05c33a04`。原本と関連付けコピーは`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。所有者と起動引数を照合したGUIと専用D-Busセッションを終了した。

## RPM更新

同じ検証済みELFをrevision3として別名梱包し、revision1/2とログを保持した。アプリの再ビルド・版変更は行っていない。

```text
/home/folimeld-build/folimeld-candidates/suse161-20261112/packages/folimeld-0.3.3-3.lp161.x86_64.rpm
RPM SHA-256: 0dc2dc75899bc1c6cffe6503e735e690c8c71a25161884c2151df34bf5add004
ELF SHA-256: 53fb285ac9efa231e4abf40d82bb69be0b411c04de21890cfd609fd3366cf567
```

`zypper --non-interactive install --allow-unsigned-rpm --no-recommends <ローカルRPM>`で0.3.3-2.lp161から0.3.3-3.lp161へ更新成功。指定した未署名ローカルRPMだけを許可し、標準リポジトリの署名検証は維持した。ELFは更新前後で一致し、rpm -Vとzypper verify --dry-runが成功した。

更新後の一般ユーザー起動をoffscreen/xcbで各12秒確認し、試験プロセスを終了した。更新コマンド・終了コード・対応ソース・起動結果・保存データと追加3画面は[更新・保存検証JSON](linux-opensuse-leap161-update-nonascii-verification-2026-11-12.json)に保存した。基礎検証JSONはrevision2時点の記録として保持する。

関連付けは独立XDG/D-BusのGIO経由であり、通常ファイルマネージャーのダブルクリックは未確認。更新は同じELFの梱包revision変更で、アプリ版間・設定形式の移行試験ではない。追加GUI依存環境での更新であり、最初の最小依存試験とは区別する。完全なLinuxデスクトップ、Tumbleweed、ARM64、幅広い入力条件や公開前確認は残る。既存環境・配布物・アプリ版は保持し、公開は行っていない。
