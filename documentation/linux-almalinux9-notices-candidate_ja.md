# AlmaLinux9の収集告知入りrevision3候補

実施日: 2026-11-12（日本時間）。既存候補を保持し、許可済み専用AlmaLinux9 Build環境へ新しい作業コピーを作成した。アプリ版は非公開検証用0.3.3/build1を維持し、梱包revisionを3とした。公開0.3.4との統合・新しい公開版の決定は未実施。

## 入力と別添資料

```text
/home/folimeld-build/folimeld-candidates/alma9-notices-20261112/
  source/                現作業ツリーから選択した入力とLinux固有告知
  dependency-materials/  収集資料149ファイル、manifest.json
  packages/              新規RPM
```

現在の未コミット修正を含む入力を転送し、Git HEADの識別を維持した。旧`alma9-20261112`候補と、そのBuild/Test環境の既存資料は保持した。新コピーでは次を反映した。

- PyInstallerのCOPYING全文をInstalled-packagesへ収集する修正。
- Linuxで再生成した暗号化告知とネイティブバイナリ照合記録。リポジトリ本体のWindows用記録は変更していない。
- AlmaLinux9のOS告知45文書をまとめたLinux-OS-runtime-notices.txt。
- 候補の範囲、別添ソース、未検証事項を説明するLinux-candidate-audit.txtと資料目録。

別添資料は149ファイル・1,680,455,895バイト。暗号化依存、Qt/PySide/MuPDF、ランタイムSRPM、Pillow依存ソース・パッチ等をコピー前後のハッシュで照合した。Qt等の大きなアーカイブは実行ファイルやFolimeldソースZIPへ入れず、別添として保持する。目録は実行ファイルとソースZIPにも含めた。

別添目録はPARTIAL AUDIT MATERIALSと明記し、Alma8 libXauの署名未検証、可変pillow-depends/mainとwheel来歴、告知網羅性を残した。Build-sourceのdependency_sources=NOT INCLUDEDは「FolimeldソースZIP内には依存ソースを含まない」という状態として維持した。資料を集めたことと、公開準備・ライセンス確認の完了を混同しない。

## ビルド・照合結果

既存の固定依存仮想環境を再利用し、pip更新・依存更新は行わなかった。新コピー内で告知/ソース対応/RPM制限の29テスト・35サブテスト、ruff、Qt/PyMuPDF import、アイコン生成、PyInstaller、Alma専用RPM梱包が成功した。一時ファイル・キャッシュ・出力は新コピー内へ分離した。

```text
packages/folimeld-0.3.3-3.alma9_8.x86_64.rpm
RPM SHA-256: 3f1da813afaedad6aa6d47fa8b5d4d1cd0e2bba429e86b1f34b9c1590433be28
ELF SHA-256: b0915988edbfcea48704cf013f5961b5c496d7b6689a888f019cff9034f46455
```

実行ファイル内Build-sourceと対応ZIPのハッシュ、ZIPの全647入力、RPM/ELFとの対応、別添149ファイルを検証。PyInstaller COPYING全文、Linux暗号化ネイティブのハッシュ一致、OS告知、別添目録を確認した。Qt Virtual Keyboardの項目は0件。

## 導入・画面確認

許可済み専用Test環境で試験アプリが起動していないことを確認し、weak dependenciesを無効にしたdnf更新でrevision2から3へ更新した。導入済みELFが新候補と一致し、rpm -Vとdnf checkが成功。offscreen/xcbを一般ユーザーで各12秒起動できた。

独立設定のWSLg GUIで日本語PDF3ページを表示し、ライセンス画面を開いた。Folimeld、Installed-packages、Linux-OS-runtime-notices、Linux-candidate-auditの表示を確認。PyInstaller全文は埋込データとの照合で検証しており、画面上で全文をスクロール確認したとは扱わない。

画面証拠: [日本語PDF](linux-almalinux9-notices-candidate/01-pdf-loaded.png)、[ライセンス画面](linux-almalinux9-notices-candidate/02-license-opened.png)、[OS告知](linux-almalinux9-notices-candidate/03-linux-candidate-notice.png)、[候補範囲・未検証事項](linux-almalinux9-notices-candidate/04-linux-audit-summary.png)、[パッケージ告知](linux-almalinux9-notices-candidate/05-installed-package-notices.png)。3枚目のファイル名は候補告知となっているが、内容はOS告知タブ。

原本PDFのハッシュは不変。所有者・起動環境を照合した試験GUIを終了した。fitzの非推奨警告やWSLのユーザーセッション警告をログに保持し、Windows/OS設定は変更していない。

コマンド、終了コード、固定依存、対応ソース、告知ハッシュ、更新・起動結果、5画面のハッシュは[検証JSON](linux-almalinux9-notices-candidate-verification-2026-11-12.json)に保存した。

## 残る検証

新規最小依存の[DNF installroot導入・offscreen起動](linux-almalinux9-revision3-minroot_ja.md)も後続で確認した。独立WSLや通常デスクトップの試験ではない。

GIO関連付け・削除再導入・再起動も[後続試験で確認した](linux-almalinux9-revision3-lifecycle_ja.md)。新規最小環境と通常デスクトップの確認は残る。

その後、新ELFで編集・保存再読込、暗号化PDF、画像取込、日本語IMEを[回帰確認した](linux-almalinux9-revision3-regression_ja.md)。以下はビルド直後の範囲を記録したもので、GIO関連付け・削除再導入・新規最小環境などは引き続き残る。

今回の新ELFは告知修正を中心とする再ビルドであり、旧候補で通ったPDF編集・保存、IME、画像・暗号化PDF、関連付け、削除再導入の全項目を再試験したわけではない。Test環境はGUIツール・EPEL追加後で、新規最小環境への導入検証とも区別する。これらの回帰、wheelビルド来歴とlibXau署名、公開版統合・版決定、通常デスクトップ・アプリ版間移行が残る。README/CHANGELOG、既存配布物を保持し、公開は行っていない。
