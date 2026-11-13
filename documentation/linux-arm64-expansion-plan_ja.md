# Linux ARM64 0.3.4+fix1 DEB 公開前確認

2026-11-13 JST。GitHub main c3b55caとMac側mainは一致、未コミット差分なし。元作業ツリーは変更していない。Build BSD ARM64 packages、Plan Folimeld Homebrew Cask distribution、Macのストレージ管理の先行記録を参照した。

最優先を画像変換後の終了クラッシュを直すDEB候補、次を同修正のstrict Snapとした。公開済みLinux ARM64は0.3.3/0.3.4のDEB/Snap、BSD ARM64はFreeBSD/NetBSD/OpenBSD 0.3.3の試験版。Fedora44/45・AlmaLinux9・Leap16.1・Tumbleweed・KaliのARM64は未検証で、amd64の公開結果を合格として流用しない。

今回の再ビルドは保存入力から成功。DEB 1212c9b5…、対応ソースZIP f7f69ff3…は独立2VMの保存成果物とバイト一致した。ソースZIP内460入力と、このブランチのアプリケーション入力を照合済み。元コミットは0a4e2366255f2f7096fd73a24a1a69f30019371f、版・PyInstaller設定・再現性処理の差分を別コミットに固定した。タグには追加の検証/再ビルド資料を含めるため、正確な対応ソースはRelease添付ZIPを使用する。

210ネイティブ実体の全件AArch64を確認。175件は公開0.3.4と同一。更新35件は公式署名付き索引に対応する11 ARM64 DEBのファイルと完全一致し、8ソースパッケージと告知を取得。公式索引のSHA-256とUbuntu Archive Automatic Signing Key (2018)の署名を検証した。共通ソースTARとPillow補足を保持し、更新分を別添する。元埋込記録のNOT INCLUDEDは外部対応記録で解決する履歴として保持する。

Ubuntu24.04.5 ARM64/HVFの一般ユーザーXorgで、画像2件の変換・2ページPDF保存・正常終了、再起動後の保存PDF表示・再変換・破棄終了を確認。3回目は削除再導入後の8ページPDF表示・正常終了。3起動すべて終了コード0。既存Documents/.configの全ファイルハッシュは削除再導入の前後で一致。Debian13.7の通常PDF受入は2026-11-11の同一DEBの記録で、今回未再実行。全試験群・フォーム・暗号化・IME等を今回の新合格とはしない。

VM cとUbuntu受入VMはChatGPT-Testの照合済み保管庫から内蔵の元パスへ復元し、圧縮/展開後のSHA-256を検証してから起動した。外付けからのVM起動は0件。元アーカイブと過去ログは保持し、ビルドゲストの元作業は別名で保護した。今回の削除対象は試験VM内のアプリパッケージだけで、VM/ISO原本は削除していない。

公開対象はrelease-assetsの16ファイル、約1.679GB。DEB、正確な対応ソースZIP/記録、依存ソースと補足、告知、再ビルド手順、検証資料、制約、チェックサム。Snapバイナリ、VM/ISO、SSH鍵、Windows/macOSバイナリは添付しない。新規専用ブランチとタグをpushし、prerelease/latest=falseで公開後、全添付を再ダウンロード照合する。その完了後にX tyamada22へ案内する。

## DEB公開完了

2026-11-13 JST、linux-deb-arm64-v0.3.4-fix1をprerelease/latest=falseで公開。専用ブランチrelease/linux-arm64-0.3.4-fix1とタグの参照先は0be2ec8。16添付を公開後に全件再ダウンロードし、サイズ・SHA-256一致を確認。[公開後照合JSON](linux-arm64-fix1-publication-result-2026-11-13.json)を参照。PyInstaller bootloaderも公式wheelの元ELFセクションと一致し、追加pydataとobjcopyによるセクション表の移動を区別した。[照合JSON](linux-arm64-fix1-bootloader-2026-11-13.json)。次順位のSnapは固有の検証・公開を別工程で扱う。
