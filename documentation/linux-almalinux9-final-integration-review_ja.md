# AlmaLinux 9公開用ソースの統合レビュー案

2026-11-12。検証済みrevision4の対応ソースZIPを基に、専用コピー内で日英README・CHANGELOGと公開説明案を揃えた。元作業ツリーの版・README・CHANGELOG、公開物・旧候補は変更していない。

```text
/home/folimeld-build/folimeld-candidates/alma9-final-integration-review-20261112-02/source/
```

## 変更した内容

- README日英へ、AlmaLinux9.8のWSL2/WSLgで確認した0.3.5/build1、RPM revision4の未公開候補の説明を追加。
- 対象外の通常デスクトップ・ARM64・AlmaLinux10・他RPM OSを明記。ダウンロード済み・公開済みという表記や架空の公開リンクは追加しない。
- CHANGELOG日英の一般的なLinux統合案を、Alma先行候補の実検証と告知・ソース修正の説明へ更新。既存の他OS項目は保持。
- 日英公開説明案をコピー内のdocumentationへ収録し、READMEからリンク。

既存変更はREADME/CHANGELOGの4ファイル、追加は日英公開稿2ファイル。機能コードはrevision4とバイト一致。日英の版・CPU・検証範囲・公開状態・制約を対照確認し、言語切替を保持した。4文書の相対リンクはすべて解決し、RPM --checkとgit diff --checkも成功した。

[文書提案パッチ](linux-almalinux9-final-documentation-proposal.patch)はrevision4ソースを基準にした4文書の差分であり、元作業ツリーへ単独適用してLinux実装全体が揃うパッチではない。[統合検証JSON](linux-almalinux9-final-integration-review-2026-11-12.json)に基準ZIP・変更範囲・相対リンクを記録した。

最初の入力一覧検査は文字列リストにPathを比較して停止した。試行を保持し、新規コピーで型を合わせて検証した。元ソースの欠落ではない。

## 固定したレビュー用ソース

文書を含む686入力を新しい単独レビュー用ZIPへ収録し、全入力ハッシュと日英6文書の内容を照合した。

```text
Folimeld-source-578f68cdc6caf09dd56a22a32f7db05fcec989200ceafed01433c3002d636b14.zip
SHA-256: 578f68cdc6caf09dd56a22a32f7db05fcec989200ceafed01433c3002d636b14
```

実パスと確認範囲は[レビューソースJSON](linux-almalinux9-final-integration-source-2026-11-12.json)を参照。ZIP生成・照合自体は成功したが、生成ログをJSONと一括解釈したWindows側の収集処理が失敗した。既存の成功記録を回収し、ZIPを再生成せず収集を修正した。

## 既存RPMとの関係と次工程

この文書更新後のZIPをrevision4 RPMの対応ソースとして付け替えていない。revision4の埋め込みBuild-sourceと旧ZIP・stagingはそのまま保持した。レビュー案から実配布用候補を作る際は、新しいソーススナップショットでビルドし、そのRPM・ELFとの対応記録とチェックサムを再生成する。

元リポジトリへの反映・コミット・タグ・公開は未実施。0.3.5/build1の最終採用と公開先は引き続き案として扱い、元の公開禁止指示を保持する。変更は専用コピー内で具体的にレビュー可能な状態になった。
