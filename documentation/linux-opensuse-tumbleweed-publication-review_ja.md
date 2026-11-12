# Tumbleweed 20261110 amd64試験版の公開前確認

後続の[公開結果](linux-opensuse-tumbleweed-publication-result_ja.md)：ユーザーが11添付・専用ブランチ・タグの公開を承認し、公開・push・公開後照合を完了した。以下の許可待ち記述は準備時点の履歴。

2026-11-13（日本時間）。Leap16.1の公開・push・X案内完了後、次順位の既存Tumbleweed専用Build/Testで0.3.5 revision1を作成した。既存候補・元の未コミット実装・他OS配布物は保持した。

| 項目 | 確認結果 |
| --- | --- |
| 対象 | `VERSION_ID=20261110`、x86_64、専用WSL2/WSLg |
| 専用候補 | `/home/folimeld-build/folimeld-candidates/tw20261110-035-r1-20261113` |
| ソースブランチ | `release/opensuse-tumbleweed20261110-amd64-0.3.5` |
| コミット | `2f479d4cfa224be3aa8c25d51b8ec8583eecd073` |
| ビルド入力 | 864件、ZIP・埋込記録・Gitコミットのバイト一致 |
| ネイティブ | 実配布206件＝公式wheel105件＋OS101件 |
| OSソース | 正確な35 SRPMの取得・署名確認 |
| ブートローダー | 公式PyInstaller wheelと一致、対応ソース取得済み |
| RPM | `folimeld-0.3.5-1.tw20261110.x86_64.rpm` |
| RPM SHA-256 | `7c0bc1b2301783acdf349d62fa1c18ae49c3c8bba6fb2963a3aefab3df6f8eea` |
| ソース検証 | 409テスト・67サブテスト成功、9件スキップ、ruff成功 |
| 固定venv | パッケージ一覧の前後一致 |
| 公開候補 | 11添付、合計1,825,967,363バイト、全チェックサム一致 |

専用Testの0.3.3 revision3から更新し、RPM/依存整合性、offscreen/xcb起動、削除再導入、既存PDF/設定のハッシュ不変を確認した。新規最小installrootは通常のローリングリポジトリから作成し、開発依存・推奨CJKフォントなし、UID/GID1000でoffscreen起動に成功した。これは20261110へ固定した独立WSLのブートや、最小環境でのGUI/IME確認ではない。

新ELFのGUIをWindows CUA経由で操作し、回転・Undo/Redo・ページ移動・白紙挿入削除、日本語・空白名保存とGIO再読込、Mozcの変換・確定、ライセンス画面、暗号化PDFの認証・回転・保存、画像PDFの生成・保存を確認した。保存データは3ページ・回転[90,0,0]・日本語本文保持、暗号化維持・誤パスワード拒否・再認証、画像1ページ/1枚・中央RGB[0,0,255]を照合した。試験GUIは終了した。

IBus切替コマンドは1を返したが、照会で`mozc-on`を確認し、入力欄で「nihongo→にほんご→日本語」の変換・確定を観測した。WSLのsystemdユーザーセッション警告は保持し、グローバル設定を変更していない。ブートローダー照合の最初の呼出しは公式wheelの取得完了前で失敗し、取得後の再実行で成功した。

通常デスクトップ・ファイルマネージャー操作・他スナップショット・ARM64・公開Ubuntu/Debian 0.3.4からの移行・広い入力条件は未検証。wheelの過去ビルド設定の完全再構成、再現ビルド、ライセンス適合認定とは区別する。RPM・チェックサム・コミットは未署名。

詳細：[日英公開案内](linux-opensuse-tumbleweed-publication-body_ja.md)、[検証JSON](linux-opensuse-tumbleweed-035-r1-verification-2026-11-13.json)、[11添付とハッシュの公開計画](linux-opensuse-tumbleweed-publication-plan-2026-11-13.json)。公開ブランチ・タグ・Releaseの作成は、この具体的な一式への承認後に進める。
