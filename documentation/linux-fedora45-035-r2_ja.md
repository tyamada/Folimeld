# Fedora 45の補足告知入り0.3.5 revision2候補

後続の[公開結果](linux-fedora45-publication-result_ja.md)：ユーザーの明示許可を受けてFedora試験版を公開済み。以下の未公開・許可待ち記述は準備時点の履歴。

2026-11-13。AlmaLinux試験版の案内をmainの日英README/CHANGELOGへ反映後、Fedora45の仕上げを再開した。既存の作業変更・公開物・旧候補は保持し、許可済み専用環境の新規コピーだけで実施した。Fedora版はまだ未公開。

## 新規候補と固定依存

```text
/home/folimeld-build/folimeld-candidates/fedora45-notices-035-r2-20261113/
packages/folimeld-0.3.5-2.fc45.x86_64.rpm
RPM SHA-256: 03c273625477385a8c92d246c7d7f44b50ed622afe656750f6b94a1b107c539b
ELF SHA-256: a87ae589b6d5dad22ea7d2a246d0764ec360b2439c47768a17970cc83da5680f
```

元作業ツリーの実装を新規コピーへ収録し、版0.3.5/build1と日英のFedora候補変更履歴をコピー内だけに反映した。既存Fedoraの固定ビルドvenvと専用テストvenvを再利用し、依存を更新していない。元mainのアプリ版は0.3.3のまま。

## Fedora固有情報と共通ソースの区別

- FedoraのOS依存42パッケージから、現在の告知45文書を収集し直した。暗号依存のネイティブ記録は既存Fedoraのものを保持した。
- 共通Qt/Pillow/MuPDF/ICUの上流ソース・告知等65ファイルを、Alma側の収集資料からハッシュ照合付きで再利用した。Alma9のOS SRPMやネイティブELFはコピーしていない。
- Fedora旧候補内のQt/PySide/Shiboken/MuPDF84実体は、先にPyPI配布wheelと照合した実体ハッシュと一致した。
- Fedora Python3.14用PillowのSBOMが記録するfribidi-shim、pythoncapi_compat、raqmの3ファイルは、収集済みPillow sdistとSHA-256一致。Python3.12用Pillow拡張の実体を代用していない。
- Qt同梱ICUは実行時73.2.0.0で、独立した73.2ソースと告知を資料へ含めた。

新コピーへLibTIFF LZW・ICU・Qtソース告知・Qt追加ライセンス・MuPDFソース告知を収録した。別添は118ファイル。共有資料に含む過去のAlma監査JSONはその時の記録であり、Fedoraの合格結果とは扱わない。[Fedora直接照合JSON](linux-fedora45-035-r2-shared-inputs-2026-11-13.json)を参照。

## ビルドと導入

全409テスト・67サブテスト成功、9件スキップ（17.08秒）。ruff、Qt/PyMuPDF import、アイコン生成、PyInstaller、Fedora RPM生成が成功した。対応ソース785入力、別添118ファイル、補足告知のELF内収録、暗号ネイティブ記録、OS所有パッケージの告知カバー範囲を照合した。

208ネイティブ実体は既存Fedora0.3.5 revision1から全件バイト不変で、Virtual Keyboard関連は0件。[ビルドJSON](linux-fedora45-035-r2-build-2026-11-13.json)に記録した。

専用Testで0.3.5 revision1からrevision2へ更新し、ELF一致、rpm -V、dnf checkが成功。一般ユーザーの新規プロフィールでoffscreen・xcb各12秒の起動が成功し、試験終了のため停止した。[更新・起動JSON](linux-fedora45-035-r2-update-2026-11-13.json)を参照。systemdユーザーセッション警告は保持し、WSLのグローバル設定は変更していない。

## PDF回帰の追記（2026-11-13）

[新ELFのPDF回帰確認](linux-fedora45-035-r2-regression_ja.md)で、編集・日本語名保存・再読込・暗号化PDFの再認証・画像PDF生成を確認した。保存データの本文・ページ順・回転と元入力の不変を照合済み。以下の残作業記述のうち、主要PDF編集・暗号化PDF・画像の確認はこの追記で完了とする。

## 残る確認

後続の[配布実体・OSソース監査](linux-fedora45-035-r2-source-audit_ja.md)で、wheel105実体との公式配布物一致と、OS103実体に対応する署名検証済み38 SRPMの収集を完了した。以下は収集前の範囲として保持し、追加資料の最終配布セットへの統合は残る。

Fedora OS由来42パッケージのSOURCERPMは、実際に使うx86_64へ限定した再照会で38種類と特定した。初回は複数アーキテクチャの出力連結で39種類と数えていたが、取得前検査で検出・訂正した。標準sourceリポジトリで正確な版の取得先を確認し、独立したFedora45鍵束で収集・署名確認を進める。現118資料でOSの全対応ソースが揃ったとはしない。

新ELFでの主要PDF編集・暗号化PDF・画像は上記の回帰試験で、IME・GIO・ライセンス画面は[デスクトップ連携確認](linux-fedora45-035-r2-desktop_ja.md)で完了した。[削除再導入・最小依存導入](linux-fedora45-035-r2-installation_ja.md)も成功し、[配布資料の統合・最終照合](linux-fedora45-035-r2-readiness_ja.md)まで完了した。技術検証後に残るのは専用Gitスナップショットと公開案内の準備・レビュー、公開許可の確認である。旧0.3.3やAlmaの実行結果で代用していない。Fedoraの公開許可・コミット・タグ・公開は今回行っていない。
