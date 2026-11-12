# AlmaLinux9の0.3.5未公開統合案ビルド・更新・設定保持

実施日: 2026-11-12（日本時間）。[統合レビュー案](linux-public-integration-review_ja.md)を基に、新しい専用コピーで実ビルドした。0.3.5/build1は未公開案であり、元のWindows作業ツリーは0.3.3/build1のまま。公開Linux0.3.4・他OSの配布物・旧候補は保持した。

## 候補とソース対応

```text
WSL: Folimeld-AlmaLinux9-Amd64-Build
/home/folimeld-build/folimeld-candidates/alma9-integration-035-20261112/
  source/
  dependency-materials/
  packages/folimeld-0.3.5-1.alma9_8.x86_64.rpm

RPM SHA-256: 156e65018c06233878ebb315fdf371ff63392c78a9a5544f533f020599fa9dfe
ELF SHA-256: 2abe33953f482b723bbd9c15a132bd7bad114ae1e998d3ee6105c96bfd096c98
```

元作業ツリーの入力に、専用レビューコピーの版と日英CHANGELOGだけを反映し、既存の画像取込後処理・サムネイル修正・告知収集・ソースZIP処理・梱包処理をバイト一致で保持した。READMEの公開案内は変更していない。

Linux暗号化告知・OS告知を新コピーへ反映し、別添149ファイル・1,680,455,895バイトをコピーして照合した。目録の候補識別を0.3.5案へ更新し、Alma8 libXau署名・wheelビルド来歴等の未完了状態を維持した。旧候補の告知・目録は変更していない。

告知反映後に29テスト・35サブテスト、ruff、Qt/PyMuPDF import、アイコン生成、PyInstaller、Alma専用RPM梱包が成功した。機能コードを保持した統合案の全409テスト・9スキップ・67サブテストは先行レビューで確認済みで、今回その全件を再実行したという意味ではない。ビルドには既存固定依存venvを再利用し、依存を更新していない。

実行ファイル内のBuild-source、対応ZIPの全678入力、RPM/ELF対応、別添149ファイルのハッシュを確認した。PyInstaller COPYING全文、Linux固有暗号化ネイティブの一致、OS告知、別添目録を確認し、Qt Virtual Keyboardは0件だった。依存ソースは別添であり、FolimeldソースZIP内に含めない状態を保持した。

## 版更新と起動

許可済み`Folimeld-AlmaLinux9-Amd64-Test`内で試験アプリが起動していないことを確認し、weak dependencies無効のdnf upgradeで次を更新した。

```text
folimeld-0.3.3-3.alma9_8.x86_64
  → folimeld-0.3.5-1.alma9_8.x86_64
```

導入済みELFが新候補と一致し、rpm -Vとdnf checkが成功した。一般ユーザーでoffscreen/xcb各12秒の起動が成功した。旧RPMはTest側の検証ディレクトリにも保持した。Alma向け公開0.3.4 RPMからの更新ではなく、非公開0.3.3候補からの版更新試験である。

## 設定保持とGUI

更新前の0.3.3候補で使った合成試験プロフィールを、新規`/home/folimeld-test/verification/version035-upgrade-20261112`へ複製した。元プロフィールは使用せず保持した。確認対象のGeneral設定は次の3件。

- language=ja
- last_open_directory: 前回のrevision3回帰用PDFフォルダ
- last_image_directory: 同じ回帰用imagesフォルダ

更新後にその設定コピーを使ってGUIを起動した。[日本語UI・PDF表示](linux-almalinux9-035-integration/01-japanese-settings-loaded.png)、[実際のバージョン0.3.5表示](linux-almalinux9-035-integration/02-version035.png)、[PDFフォルダ履歴](linux-almalinux9-035-integration/03-open-directory-restored.png)、[画像フォルダ履歴](linux-almalinux9-035-integration/04-image-directory-restored.png)を確認した。各選択ダイアログはキャンセルし、編集・画像取込は行っていない。

3設定値は実行前後で一致し、元プロフィールのSHA-256も不変だった。元PDFはSHA-256`c82a9b0bb388a2120fe570fd4a603e9038868cfc046b2164a301690e99c01610`で不変。所有者と専用プロフィールを確認した試験GUIを終了した。バージョン情報をEscapeで閉じる際のBadWindowは、閉じたウィンドウへのキー解放イベントによるもので、後続の主画面・履歴ダイアログ表示は成功した。

コマンド、終了コード、対応ソース、告知・資料ハッシュ、更新結果、設定の前後値、ログ、4画面のハッシュは[検証JSON](linux-almalinux9-035-integration-verification-2026-11-12.json)に保存した。

## 残る工程

0.3.5新ELFの[GIO・削除再導入・最小依存起動](linux-almalinux9-035-lifecycle_ja.md)も後続で確認した。通常デスクトップ・他OS再ビルド等は残る。

後続で0.3.5新ELFの[編集・保存・暗号化PDF・画像・IME回帰](linux-almalinux9-035-regression_ja.md)を確認した。前項のGIO・導入回帰と合わせ、列挙した主要項目は新ELFで確認済み。旧0.3.3 revision3の結果とは区別する。設定保持は上記3項目の合成コピーの確認であり、任意の既存設定や公開Ubuntu/Debian0.3.4からの移行の合格ではない。

他ディストリビューションの0.3.5案再ビルド、通常デスクトップ、wheelビルド来歴・Alma8 libXau署名、公開版・公開先の最終決定も残る。新規コミット・タグ・公開は行っていない。
