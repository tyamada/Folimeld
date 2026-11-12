# Fedora 45 revision2の技術検証と配布資料準備

後続の[公開結果](linux-fedora45-publication-result_ja.md)：ユーザーの明示許可を受けてFedora試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。Fedora45 amd64向け0.3.5 revision2の技術検証を完了し、配布候補のRPM・対応アプリソース・依存ソース別添を新規ディレクトリへ準備した。Fedora版の公開、push、タグ作成は行っていない。

## 検証の到達点

- [ビルド](linux-fedora45-035-r2_ja.md)：409テスト・67サブテスト成功、9件スキップ。固定依存でRPM生成、208ネイティブ実体不変。
- [PDF回帰](linux-fedora45-035-r2-regression_ja.md)：編集・日本語名保存・再読込・暗号化PDFの再認証・画像PDF生成とデータ照合、元入力不変。
- [デスクトップ連携](linux-fedora45-035-r2-desktop_ja.md)：IME変換・確定、GIOの日本語・空白入りパス起動、追加告知のライセンス画面表示。
- [導入回帰](linux-fedora45-035-r2-installation_ja.md)：削除・再導入で4ファイル復元、ユーザー作成物6件保持、再導入後offscreen/xcb起動。新規installrootでもPython・ビルド依存なしで一般ユーザーのoffscreen起動と整合性確認が成功。
- [配布実体・OSソース](linux-fedora45-035-r2-source-audit_ja.md)：wheel由来105 ELFの一致、OS由来103 ELFと署名検証済み38 SRPMの対応付け。

PyInstaller6.22.2の公式PyPI wheelとインストール済みブートローダーも完全一致した。LinuxではPyInstallerがobjcopyで`pydata`セクションを追加するため、完成ELFの単純な先頭比較は一致しなかった。候補を変更せず新規監査出力から`pydata`だけを除くと、公式wheelの`run`へバイト単位で復元できた。公式sdistにはブートローダーソース45件があり、COPYINGの同梱も照合した。[ブートローダー記録](linux-fedora45-035-r2-bootloader-2026-11-13.json)を参照。Python3.14.10はFedora RPM由来で、上記OSソース対応表に含まれる。

## 新規の配布準備ディレクトリ

```text
/home/folimeld-build/folimeld-candidates/fedora45-r2-readiness-20261113/
  packet/                          RPM・対応ソースZIP・関連付けJSON
  Folimeld-fedora45-0.3.5-r2-dependency-sources.tar
  supplemental-source-manifest.json
  verification.json
  final-check.json
```

別添は1,788,856,320バイト、目録を含む180項目。元の118資料に、検証済み38 SRPM・Fedora監査記録・Python3.14用Pillow/cffi公式wheel・PyInstaller公式wheel/sdist・Fedora鍵を加えた。失敗ダウンロードの一時ファイルと監査用rpmdbは含めていない。全項目をアーカイブから再読込してSHA-256を照合した。

| 対象 | SHA-256 |
| --- | --- |
| RPM `folimeld-0.3.5-2.fc45.x86_64.rpm` | `03c273625477385a8c92d246c7d7f44b50ed622afe656750f6b94a1b107c539b` |
| 対応アプリソースZIP | `76b4a7c37f071399d602965e1d348ab35cda3277d2ecf2c0b4ffad2392830836` |
| 依存ソース別添tar | `daebd0d729661dad6c40e57e0f9dd8f4cb8965d074c5c71858343a371e3c768c` |

候補のELF・RPM・埋め込み118資料目録は変更していない。追加資料は外部の別添として明示した。元のビルド記録とELF内目録の一致、対応ソース785入力、準備済みRPM・ZIP・別添のハッシュを最後に再確認した。[資料統合記録](linux-fedora45-035-r2-material-staging-2026-11-13.json)と[最終照合](linux-fedora45-035-r2-final-check-2026-11-13.json)を参照。

## 公開前に残る作業

後続の[公開前レビュー](linux-fedora45-publication-review_ja.md)で、785入力と一致する専用Gitコミット、日英案内、11添付の公開パケットとチェックサム検証まで完了した。Fedora版の公開許可はまだ受けていないため、mainへの実装統合・push・タグ・GitHub Release公開は実施していない。

検証対象はFedora45 x86_64の専用WSL2/WSLg環境。新規installrootはchroot/offscreenの試験であり、完全なデスクトップの検証とは区別する。他のFedora版やARM64には結果を拡張しない。公式配布実体・対応ソースの照合と、過去コンパイラー設定の完全再構成・再現ビルド・ライセンス適合認定は別の範囲である。共通上流資料の過去Alma監査記録はその履歴を保持し、Fedora実行結果と混同しない。
