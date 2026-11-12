# AlmaLinux 9 revision5の最終導入確認

2026-11-12。[文書統合済みrevision5](linux-almalinux9-035-integration-r5_ja.md)そのものを対象に、許可済み専用Test内で実施した。公開・元作業ツリーの変更・旧環境の置換は行っていない。

## 削除再導入

revision5 RPMのSHA-256を確認後、専用Testでdnf remove／installを実行した。削除時の依存自動削除は無効にした。

- 実行ファイル・desktop項目・アイコン・LICENSEの4ファイルが削除時に消失し、再導入後に元のハッシュで復元した。
- 既存の合成試験プロフィールのPDF・設定6ファイルは前後で不変。
- rpm -Vとdnf checkが成功。
- 一般ユーザーの新規プロフィールで、再導入後のoffscreen・xcb各12秒起動が成功し、試験後に終了した。

コマンド・出力・ハッシュは[削除再導入JSON](linux-almalinux9-035-integration-r5-lifecycle-2026-11-12.json)を参照。GUIツール追加済みTestでの試験と、新規最小依存導入は区別する。

## 新規最小依存installroot

```text
/root/folimeld-verification/version035-integration-r5-minroot-20261112/root
```

既存rootを再利用せず、新規ディレクトリと独立RPMデータベースへAlma9の鍵を取り込んだ。標準BaseOS/AppStreamのみ、weak dependencies無効で、ハッシュ照合済みrevision5 RPMを導入した。導入は成功し、RPM一覧は鍵を含め105件。

root内にpython3、python3.12、python3.12-libs、python3-pip、gcc、rpm-build、epel-release、推奨日本語Notoフォントがないことを確認した。最小限の文字デバイスと専用HOME/XDG設定を新規root内に用意し、絶対パスのchrootから数値UID/GID1000でoffscreen起動した。

12秒後も起動し、試験終了のため停止した。root内ELFはrevision5の`82ada5680df8bb74da15b801ce59793b140a4789766d0caf4b7082a120ca470c`と一致し、rpm -Vとdnf checkも成功。導入ログの警告・エラー行はなかった。起動時のfitz非推奨・offscreen警告は記録に保持した。

DNF scriptletが作成した空のdev/nullは、新規root内・非リンク・0バイトを確認して文字デバイスへ置換した。procやWSLgソケットのbind mount、WSLの新規登録、既存Testの信頼鍵・暗号ポリシー・リポジトリ設定の変更は行っていない。

既存Test側のELFと試験PDF・設定も不変で、試験プロセスは残っていない。[最小依存JSON](linux-almalinux9-035-integration-r5-minroot-2026-11-12.json)へRPM一覧・起動環境・コマンド・ログ・保持確認を保存した。

## この確認の範囲

revision5の削除再導入と新規最小依存起動は確認済みとなった。最小root内のGUI/IME・独立WSLブート・通常デスクトップの合格とは扱わない。機能・ネイティブ実体・告知が不変であることは先行の候補対応検査で確認しており、理由なく候補を再生成する必要はない。

次はこの固定候補を基に、採用する版・統合先・不変コミット/タグと公開操作を判断する段階。公開禁止の指示は維持し、過去の正確なビルド設定などの未検証条件も公開前レビューから削除しない。
