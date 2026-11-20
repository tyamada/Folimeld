# 実PDFを使う検証入力

利用者向けの漫画サンプルは[集約ページ](https://tyamada.github.io/manga-prompt-kit/samples/ja/)へ接続します。個別PDFをdocs/sampleやPagesへ複製しません。

## 明示的な準備

固定Releaseのpdf-manifest.jsonをtools/data/sample-inputs-v1.jsonとして保存し、SHA-256を検査してから選択した1冊の容量・SHA-256を確認します。アプリの最新版JSON・既存ID・利用者キャッシュには変更を加えません。過去のFilipino別名ep1_tl等はep1_fil等へ解決します。

```sh
python -m tools.sample_inputs --sample-id ep3_ja --cache-dir /absolute/external/sample-cache --download
python documentation/netbsd-verification/prepare_fixtures.py --cache-dir /absolute/external/sample-cache --output build/netbsd-verification
python documentation/openbsd-verification/verify_gui_results.py --cache-dir /absolute/external/sample-cache --results-dir build/openbsd-verification
```

Windowsではキャッシュ引数にリポジトリ外の絶対パスを指定します。取得済みファイルを渡す場合は--input-dirで実際の入力フォルダーを指定します。元のPDF名またはSHA-256.pdf名に対応します。--downloadなしでは通信をせず、欠落・破損は明示的に失敗します。自動スキップで合格にはしません。

NetBSDのフォーム・画像は小さな生成fixtureです。実際の8ページ漫画を使うGUI照合は統合確認として分離しています。OpenBSDの結果検査は保存済みの実GUI出力が必要で、単なる準備処理の成功をOpenBSD実機合格と扱いません。

旧documentation/netbsd-verification/fixtures.jsonや旧検証報告は当時の原記録です。旧testdataパスを含んでも改変しません。今後生成するfixtures.jsonは照合済みの外部入力パスを記録します。

## 公開と整理

[更新手順](https://github.com/tyamada/manga-prompt-kit/blob/main/docs/sample-download-maintenance.md)に従います。Folimeldの利用者向けPagesは日英のみで、対応する集約ページへリンクします。外部集約先の言語別ページ・地域アンカーが案内の正本です。

最新版51冊と異なるSHA-256の旧PDFは用途・保管を確定するまで保持します。一般回帰PDF、SEASIDE_LIVING、同梱JSON、利用者の取得済みPDFは削除対象外です。配信済みアプリが旧URLへ依存する場合は対応版の配信確認まで削除しません。
