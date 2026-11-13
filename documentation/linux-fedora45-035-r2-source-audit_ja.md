# Fedora 45 revision2の配布実体・OSソース確認

2026-11-13。[補足告知入り候補](linux-fedora45-035-r2_ja.md)の後続確認。ビルド済みRPM・ELF・対応ZIP・埋め込み118資料の目録は変更せず、追加監査ディレクトリに資料を収集した。Fedora版は未公開。

## wheel由来105実体

候補内のQt/PySide/Shiboken・PyMuPDF・cryptographyの85 ELFは、先にPyPI配布wheelへ照合した内容ハッシュと一致した。大きなQt wheelを重複取得していない。

FedoraのPython3.14環境に適合するPillow12.3.0とcffi2.1.1の公式wheelをPyPIから取得し、版別JSONの公開SHA-256と一致を確認した。そのwheelに含まれるPillow19 ELFとcffi1 ELFも、今回のrevision2内とバイト一致した。監査用ダウンロードであり、既存venvへ再インストールしていない。

計105実体の取得先・ハッシュ・対応項目は[公式wheel照合JSON](linux-fedora45-035-r2-official-wheels-2026-11-13.json)へ保存した。Python3.12用Pillow拡張をPython3.14の合格根拠に使っていない。公式HTTPSハッシュ・内容一致の確認と、過去コンパイラー設定・全変更パッチの独立再構成は区別する。

## OS由来103実体と38 SRPM

新AnalysisからOS共有ライブラリ等の実参照元を取得し、実体ハッシュを照合した。103項目すべてについて所有RPMを確認し、そのSOURCERPM名・版・releaseに一致する38種のSRPMを取得した。

```text
/home/folimeld-build/folimeld-candidates/fedora45-notices-035-r2-20261113/fedora-source-audit/
  srpms/              検証済みSRPM38件と、保持した失敗取得の一時ファイル
  isolated-rpmdb/     この監査専用のRPM鍵束
```

38件の合計は353,710,038バイト。各SRPMの名前・版・release、サイズ、SHA-256を記録し、Fedora45のOS鍵を取り込んだ独立RPMデータベースで署名とダイジェストを確認した。全38件が成功した。既存のシステム信頼鍵・暗号ポリシーは変更していない。

Fedora45では公式鍵が`/usr/share/pki/rpm-gpg`、標準repo設定が`/usr/share/dnf5/repos.d`に配置されていた。従来の/etc配下だけを調べた検査は停止し、RPMパッケージの配置情報から正しい場所を確認した。新規の空監査鍵束へ読み込んで再実行した。

初回のSOURCERPM照会は、複数アーキテクチャの同名RPMの出力を区切らず連結したため39種と数えていた。ダウンロード前の集合検査で不正名を検出し、実際に使用するx86_64を指定・改行区切りで再取得して38種へ訂正した。元の失敗記録は保持した。

標準sourceリポジトリは当該コマンドだけで指定し、永続設定を変更していない。一部ミラーのメタデータ・ファイル取得がタイムアウトしたため、公式配布先へのフォールバックで取得した。失敗した一時ファイルは新規監査ディレクトリに保持し、検証済みファイルと区別した。

[SRPM監査JSON](linux-fedora45-035-r2-srpm-audit-2026-11-13.json)へ鍵ハッシュ・全署名結果・照会の訂正・取得履歴を、[OS実体対応表](linux-fedora45-035-r2-os-native-source-map-2026-11-13.json)へ103項目の実体・所有RPM・SRPMを保存した。

## 到達点と次の作業

候補内208ネイティブ実体は、wheel由来105項目とOS由来103項目に対応付けられた。ソースRPMの名前対応と配布物の内容一致であり、ビット再現ビルドや全ライセンス条件への適合認定ではない。外側のPyInstallerブートローダー等は別の確認範囲。

追加したSRPMと監査結果はrevision2の埋め込み118資料目録の外にある。既存目録を黙って書き換えず、最終の配布資料セットへ含める際に明示的に統合する。これ以降は新ELFのGUI/IME・暗号化PDF・画像・GIO、削除再導入・最小依存導入・ライセンス画面・配布資料の最終照合を優先する。
