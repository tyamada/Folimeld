# Fedora 44 revision2の配布実体・ソース監査

後続の[公開結果](linux-fedora44-publication-result_ja.md)：ユーザーの明示許可を受けてFedora44試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。[0.3.5 revision2候補](linux-fedora44-035-r2_ja.md)の追加監査を行った。候補のELF・RPM・対応アプリソースZIP・埋め込み119資料目録は変更していない。Fedora44版は未公開。

## wheelとブートローダー

候補内のQt/PySide/Shiboken・PyMuPDF・cryptographyの85実体は、先に公式PyPI wheelと照合した実体ハッシュに全件一致した。大きなQt wheelを重複取得していない。Fedora44のPython3.14に適合するPillow12.3.0・CFFI2.1.1の公式wheelも取得し、PyPI公開ハッシュと候補内のPillow19実体・CFFI1実体が一致した。合計105実体で、監査用ダウンロードを既存venvへ導入していない。

PyInstaller6.22.2の公式wheel・sdistも取得し、公開SHA-256を照合した。候補を変更せず、新しい監査用出力で`pydata`セクションを除くと公式wheelのブートローダーへ完全一致で復元できた。sdist内のブートローダーソース45件とCOPYINGの同梱も確認した。

[公式wheel記録](linux-fedora44-035-r2-official-wheels-2026-11-13.json)と[ブートローダー記録](linux-fedora44-035-r2-bootloader-2026-11-13.json)を参照。公式配布物との一致を、過去のコンパイラー設定・全パッチの完全再構成や再現ビルドと混同しない。

## Fedora44のOS由来102実体

新Analysisと候補バイトを照合したうえで、実参照ファイルの所有RPM41パッケージを取得した。x86_64の所有情報を改行区切りで照会し、対応する正確な37 SRPMを標準sourceリポジトリへ問い合わせた。Fedora45のSRPMは流用していない。

37件、合計303,269,121バイトを取得し、名前・版・release・SHA-256、Fedora44鍵を取り込んだ独立RPMデータベースでの署名とダイジェストを全件確認した。候補のOS由来102実体すべてに、所有RPMと署名検証済みSRPMを対応付けた。Python3.14.10の対応ソースも含む。システムの信頼鍵・repo設定・暗号ポリシーは変更していない。

[SRPM監査記録](linux-fedora44-035-r2-srpm-audit-2026-11-13.json)と[102実体の対応表](linux-fedora44-035-r2-os-native-source-map-2026-11-13.json)を参照。wheel105＋OS102＝207実体を説明でき、外側のブートローダーは上記で別途確認した。RPM所有と正確なソース版の対応付けは独立再コンパイルの証明ではない。

## 外部の配布資料セット

```text
/home/folimeld-build/folimeld-candidates/fedora44-r2-readiness-20261113/
  packet/  RPM・対応アプリソースZIP・対応記録JSON
  Folimeld-fedora44-0.3.5-r2-dependency-sources.tar
  supplemental-source-manifest.json
  verification.json
  final-check.json
```

依存ソース別添は1,738,352,640バイト、目録を含む178項目。元の119資料に署名検証済み37 SRPM・監査記録・公式wheel・PyInstallerソースと鍵を加え、全項目をアーカイブから再読込してハッシュ照合した。既存の埋め込み目録は元ビルド記録とELF内バイトにも一致する。対応アプリソース822入力、準備済みRPM・ZIP・別添も再照合した。

| 対象 | SHA-256 |
| --- | --- |
| RPM | `d3fc22088af7d4fa08b90bc341e64b24b23d350de98a11d9825a0cafa4416574` |
| 対応アプリソースZIP | `957b144ca26d0b13ff91449b1f98165fff2cfa452409fb540cf2d3bbe3d58e3e` |
| 依存ソース別添tar | `48c688417ffbd46af8dc23a87f6aac2de99d6fba8500998b05de25ae0c34f0cd` |

[資料統合記録](linux-fedora44-035-r2-material-staging-2026-11-13.json)と[最終照合](linux-fedora44-035-r2-final-check-2026-11-13.json)を参照。共通上流資料中の過去Alma/Fedora45記録は、その時点の履歴として保持し、Fedora44のGUI成功記録とは扱わない。全ライセンス条件への適合認定ではない。

PDF/IME/GIO/ライセンス表示・削除再導入・新規最小依存起動まで確認済み。残るのは専用Gitスナップショット・日英案内・公開パケットのレビューとFedora44公開許可の確認である。他OS・ARM64・通常デスクトップへ検証結果を拡張しない。
