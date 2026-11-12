# AlmaLinux9の0.3.5案 GIO・削除再導入・最小依存確認

実施日: 2026-11-12（日本時間）。[0.3.5案のGUI回帰](linux-almalinux9-035-regression_ja.md)の続き。許可済み専用AlmaLinux9 Test内で実施した。元作業ツリーの0.3.3、公開Linux0.3.4、旧候補、旧installroot、設定・素材は保持し、公開していない。

対象は`folimeld-0.3.5-1.alma9_8.x86_64`、RPM SHA-256`156e65018c06233878ebb315fdf371ff63392c78a9a5544f533f020599fa9dfe`、ELF SHA-256`2abe33953f482b723bbd9c15a132bd7bad114ae1e998d3ee6105c96bfd096c98`。

## 削除・再導入と再起動

専用WSL名、導入版、RPMハッシュ、試験アプリ未起動を確認し、rpm -V/dnf checkの成功後に削除した。依存の自動削除を抑止し、次の4ファイルが消失、RPM未導入となることを確認した。

- /usr/bin/folimeld
- /usr/share/applications/folimeld.desktop
- /usr/share/icons/hicolor/256x256/apps/folimeld.png
- /usr/share/licenses/folimeld/LICENSE

weak dependencies無効で同じ候補RPMを再導入し、4ファイルが削除前と同じハッシュで復元した。前回の0.3.5回帰で作成したPDF・設定6件も、削除直後と再導入後にハッシュ不変。rpm -V/dnf checkは再導入後も成功した。

一般ユーザーによるoffscreen/xcb各12秒の起動が成功し、試験終了のため停止した。これはGUIツール/EPEL追加済みの既存Test環境での削除再導入試験で、新規最小導入とは次項で分ける。

## GIO関連付けと日本語パス

専用`version035-gio-20261112`のXDG設定だけでapplication/pdfの既定をfolimeld.desktopへ指定し、独立D-Bus内で`gio open`を実行した。対象は`日本語 パス/関連付け 試験.pdf`。GIO終了コード0で、日本語を含むPDF3ページが表示された。[画面証拠](linux-almalinux9-035-lifecycle/01-gio-nonascii-opened.png)。

元の合成PDFと関連付け用コピーはSHA-256`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変だった。GIOログはfitzの非推奨警告のみ、専用セッションログは空。所有者・試験設定を照合したGUIとD-Busを終了した。

利用者の既定関連付けは変更していない。通常ファイルマネージャーのダブルクリックや、明示D-Busなしの条件を合格とする結果ではない。ログ・各終了コード・ハッシュ・再起動結果は[削除再導入/GIO JSON](linux-almalinux9-035-lifecycle-verification-2026-11-12.json)へ保存した。

## 新規最小依存installroot

既存rootを再利用せず、専用Test内に新規DNFインストール先を作成した。

```text
/root/folimeld-verification/version035-minroot-20261112/root
```

AlmaLinux9の鍵を独立RPMデータベースへ取り込み、当該コマンドだけで標準BaseOS/AppStreamを指定、weak dependencies無効で0.3.5案を導入した。トランザクションは104パッケージ、鍵を含むRPM一覧は105件。基本DejaVu・英語フォントは必須依存として含む。

root内にpython3、python3.12、python3.12-libs、python3-pip、gcc、rpm-build、epel-release、推奨google-noto-sans-cjk-ttc-fontsがないことを確認した。最小限の文字デバイス・専用HOME/XDG設定を用意し、絶対パスのchrootから数値UID/GID1000でoffscreen起動した。DNF scriptletが作成した空のdev/nullは、新規root内・非リンク・0バイトと確認してから文字デバイスへ置換した。

12秒後も起動しており、試験終了のため停止。root内のELFは新候補と一致し、rpm -Vとdnf checkが成功した。既存Test側の候補ELFと試験ファイルも保持された。導入ログの警告/エラー行はなし。起動ログのfitz/offscreen警告は保持した。

全コマンド、RPM一覧、未導入項目、起動環境・出力・終了コード、ハッシュ、保持確認は[最小依存JSON](linux-almalinux9-035-minroot-verification-2026-11-12.json)に保存した。proc/WSLgソケットのbind mountや新しいWSL登録は行っていない。独立WSLのブート・通常デスクトップ・root内のGUI/IME検証とは区別する。

## 到達点と残る範囲

AlmaLinux9の0.3.5未公開案では、実ビルド・ソース対応・非公開0.3.3からの版更新・3設定保持、主要GUI/IME、GIO、削除再導入、最小依存offscreen起動を確認できた。試験プロセスは終了済み。

他ディストリビューションの0.3.5案再ビルド、公開Ubuntu/Debian0.3.4からの移行、通常デスクトップ・広い設定条件、wheelビルド来歴・Alma8 libXau署名、公開版の最終決定は残る。ライセンス適合性や公開準備の完了を認定する結果ではない。
