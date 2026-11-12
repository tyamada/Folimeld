# Linux amd64実装のmain統合

2026-11-13。ユーザーの明示依頼に従い、[公開案内PR #1](https://github.com/tyamada/Folimeld/pull/1)をCI成功確認後にmainへマージした。元作業ツリーで保持していた実装を、関連するRPMテンプレート・ヘルパー・テスト・LibTIFF告知とともに統合する。

ソース版は公開済みLinux試験版と同じ0.3.5へ同期する。既存Release・タグ・バイナリは変更しない。非同期サムネイルの配置修正、Qt Virtual Keyboard除外、PyInstaller全文告知、Fedora/Leap16.1/Tumbleweed/AlmaLinux9固有のRPM出力と上書き拒否を含む。

[検証結果JSON](linux-amd64-main-integration-2026-11-13.json): 専用コピーの0.3.5で409テスト・67サブテスト成功（9スキップ）、ruff・mypy・シェル構文検査成功。既存7ファイルの差分は統合前にハッシュ確認とパッチ保存を行った。LibTIFF告知の余分な末尾空行だけを整理し、過去監査へのリンクは公開済み不変コミットへ向けた。

[DEB追加GUI検証](linux-deb-amd64-extended-verification_ja.md)はUbuntu24.04.4で実施。Debian/KaliのIME等や通常デスクトップへの拡大は未実施。公開時の添付記録はその時点の履歴として保持する。
