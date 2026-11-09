# NetBSD 11.1での動作確認計画

作成日: 2026-11-09（日本時間）。検証実施を開始した段階の計画であり、NetBSD対応・動作確認済みの宣言ではない。

## 対象と判断基準

- [公式リリース一覧](https://www.netbsd.org/releases/formal.html)で確認した最新正式版NetBSD 11.1、amd64。
- Windows上の専用VirtualBox VM。4 vCPU、8 GiB RAM、80 GiB可変ディスク、NAT。既存FreeBSD VMとは分離する。
- ソースからの実行を対象とし、配布パッケージの作成は別途判断する。
- 検証開始時のコミット: `98de4104c93a525147f9bd39f0944249ff89c8bc`。修正した場合は再検証時の差分も記録する。

## 実施順序

1. 公式ISOとSHA512を取得して照合。専用ディスクへOSを導入し、一般ユーザー、SSH、X11、デスクトップ、日本語フォントを用意する。再起動後の接続とGUIを確認する。
2. Python 3.12を第一候補に依存を調査する。pkgsrcの版とバイナリ配布先を固定し、PySide6、PyMuPDF、Pillow、cryptographyを導入する。バイナリが不足する場合は同じpkgsrcのソースビルドを検討する。
3. `constraints-release.txt` と実導入版の差異を記録する。PyMuPDF/MuPDFはFreeBSDでフォーム不具合を解消した1.28.2を第一候補にする。FreeBSD用パッチはNetBSDの問題を確認するまで流用しない。
4. import、Qtウィンドウ生成、PDF読込・保存を確認し、フォーム回帰テストを先行実行する。その後pytest全件、Ruff、mypyと依存整合性を確認する。skipは件数だけでなく理由も記録する。
5. 実GUIで日本語PDF表示、複数選択、回転、移動、削除、白紙挿入、undo/redo、別名保存・検証用コピーへの上書き・再読込を確認する。日本語・空白を含むパス、フォーム保持、暗号化PDFの正誤パスワードとキャンセル、画像フォルダー取り込み、設定の永続化も確認する。
6. 書込不可の検証用ディレクトリーへの保存失敗後、編集内容と履歴を保持して別の場所へ保存できることを確認する。元サンプルへの上書きは避ける。
7. `tools.benchmark_pdf` の100ページ、画像入り100ページ、1000ページを各3回、新規プロセスで実施する。中央値・ばらつき・RSSと依存版を保存し、1000ページは実GUIでも確認する。
8. 保存PDFのページ数・順序・回転・内容とフォーム値を照合する。再構築に必要な手順と証跡を残す。

## 完了条件と記録

全テストに原因不明の失敗や異常終了がなく、実GUIで編集・保存・再読込ができることを完了条件とする。依存導入で止まった場合は、未導入の依存、エラー、再現手順を記録し、未実施項目を合格扱いしない。

実施記録は [NetBSD検証記録](netbsd-verification_ja.md)、証跡は `documentation/netbsd-verification/`、大容量のISO・VDI・一時ビルドはGit対象外の `build/netbsd-vm/` に保存する。秘密鍵と認証情報は証跡に含めない。

比較資料:

- [FreeBSD構築記録](freebsd-virtualbox-setup_ja.md)
- [FreeBSDのGUI確認](freebsd-gui-verification_ja.md)
- [フォーム異常終了の修正](freebsd-forms-fix_ja.md)
- [画像取り込み・保存失敗・負荷試験](freebsd-extended-verification_ja.md)
