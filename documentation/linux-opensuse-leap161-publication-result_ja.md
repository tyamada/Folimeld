# openSUSE Leap 16.1 amd64試験版の公開結果

2026-11-13（日本時間）。ユーザーの依頼と11添付・専用ブランチ・タグの具体的な公開承認を受け、[Folimeld 0.3.5 revision1を公開した](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.5)。公開後の11添付のサイズ・SHA-256、既存Releaseの添付ID・サイズ・SHA-256、latestの保持を確認した。

| 項目 | 結果 |
| --- | --- |
| 専用ソースブランチ | `release/opensuse-leap161-amd64-0.3.5`、push済み |
| ソースコミット | `44f76e77c05c0c097be9dc1e8f1de9f8449e6aaa` |
| タグ | `opensuse-leap161-amd64-v0.3.5`、push済み |
| RPM | `folimeld-0.3.5-1.lp161.x86_64.rpm` |
| RPM SHA-256 | `ae7517737f6011a145161e3f56a1776d910ed172f12aa807999b64144d06066f` |
| ビルド入力一致 | 858ファイル、埋込記録・ZIP・専用コミットのバイト一致 |
| ネイティブ実体 | 実配布209件＝公式wheel105件＋OS104件、36 SRPM署名検証済み |
| テスト | 409件・67サブテスト成功、9件スキップ |
| 公開添付 | 11ファイル、合計1,822,380,407バイト |

専用Buildの新規候補は`/home/folimeld-build/folimeld-candidates/leap161-035-r1-20261113`。既存固定venvのパッケージ一覧は前後一致し、元作業ツリー・旧候補・他OS配布物を保持した。専用Testで0.3.3 revision3から更新し、offscreen/xcb起動・削除再導入・既存PDF/設定のハッシュ保持・RPM/依存整合性、新規最小installrootの一般ユーザー起動を確認した。

新GUIではPDF編集、日本語・空白入り保存名、GIO再読込、ライセンス画面、Mozc変換・確定、暗号化PDF認証・回転・保存、画像PDF生成・保存を確認した。保存データは3ページ・回転[90,0,0]・日本語本文保持、暗号化の維持・誤パスワード拒否・正パスワード再認証、画像1ページ/1枚・中央RGB[0,0,255]を照合した。

合成キー操作ではIME切替コマンドの失敗、反復文字・ダイアログの増加、長すぎる名前による保存失敗があった。試験GUIを停止し、単独GUIとマウス確定操作で画像取込・保存を再検証した。これを全デスクトップ環境での障害判定や完全解消とは扱わない。GIOは日本語・空白パスのGUI表示後に試験アプリを明示終了し、呼出し終了コード0を記録した。出力パイプの継承により取得完了がアプリ終了まで待たされていた。

最初の全体ruff呼出しは試験venvからバイナリを見つけられず失敗したが、固定venvのruffを直接指定して成功した。最初のGitスナップショットは改行正規化でビルド入力と不一致となり、専用インデックスにフィルターを通さない実バイトを登録して再照合した。最初の公開処理はpush後にWindowsの文字コードで案内読込に失敗し、UTF-8を明示して再開した。既存タグ・ブランチを再作成せず、一致を検証した。

通常デスクトップ・通常ファイルマネージャー操作・ARM64・他ディストリビューション・公開Ubuntu/Debian 0.3.4からの移行・幅広い入力条件は未検証。wheelの過去ビルド設定の完全再構成、再現ビルド、ライセンス適合認定とは区別する。詳細は[日英案内](linux-opensuse-leap161-publication-body_ja.md)、[検証JSON](linux-opensuse-leap161-035-r1-verification-2026-11-13.json)、[公開計画](linux-opensuse-leap161-publication-plan-2026-11-13.json)、[公開結果JSON](linux-opensuse-leap161-publication-result-2026-11-13.json)を参照。

公開後の[push・X案内の確認記録](linux-amd64-publication-announcements_ja.md)：[Leap試験版の案内投稿](https://x.com/tyamada22/status/2121013348489986500)を`tyamada22`のタイムラインで確認した。Fedora44/45のpush確認と案内投稿も完了した。
