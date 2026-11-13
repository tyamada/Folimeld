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

DEBのX案内: https://x.com/tyamada22/status/2121043541908689225 （本文と公開表示を確認）。

Snap追加検証: x5の画像変換・保存・終了は0。x6への同一パッケージ更新後、Documents/設定のハッシュ保持と保存PDFの再読込は成功。次の画像再変換中にapt-daily-upgrade.serviceによるシステムサービス/Xorg再起動が起き、XIO error/終了1となった。これは合格として集計せず、ログを保存して自動更新完了後に再試験する。Snapはこの段階では未公開。

## ARM64候補の最終分類と次工程

| 対象 | 分類 | 根拠・次工程 |
|---|---|---|
| Linux 0.3.3 / 0.3.4 ARM64 DEB・Snap | 既存公開済み・保持 | 既存タグ/添付/対応ソースを確認。今回の試験版で置換・削除しない |
| 0.3.4+fix1 再現性修正版DEB | 公開済み | Ubuntu新規回帰、Debian同一DEBの保存受入、210ネイティブの対応ソース、全16公開後添付照合済み |
| 0.3.4+fix1 再現性修正版strict Snap | 公開済み | 専用ブランチ56de426、固有X11/制限/画像変換/再導入、更新中断と再試験を別記。全16添付の公開後再ダウンロード照合済み |
| crashfix1、初期fix1、再現性修正前の再ビルド候補 | 保管・公開候補から除外 | より後の再現可能候補に集約。候補・ログ・ソースの削除なし |
| main 0.3.5 ARM64 DEB/Snap | 未ビルド・未検証 | amd64 0.3.5の公開をARM64の合格とはしない。次の実装優先候補は既存Ubuntu/Debian環境を再利用できるARM64 DEBの0.3.5同期 |
| Fedora 44/45、AlmaLinux9、Leap16.1、Tumbleweed ARM64 | 未検証・未公開 | 梱包ヘルパーのaarch64許容を確認。ただしARM64での実ビルド・固有依存ソース監査・導入・GUI受入が必要。新RPM環境を作る場合は固定版Fedora44を先行候補とする |
| Kali ARM64 | 未検証・未公開 | 共通DEBが動作すると推測して合格扱いにしない。ARM64の専用環境を別途用意する |
| FreeBSD/NetBSD/OpenBSD ARM64 0.3.3 | 既存公開済み（BSDとして区別） | 専用ARM64タグとパッケージ・対応ソースあり。Linuxの合格件数へ混ぜない |

VM運用: 今回は3台を内蔵に復元し、圧縮/展開後の照合後に起動。使用後はすべて正常停止。更新された内蔵VMは次回用に保持し、外付け保管庫は元スナップショットとして不変。VM/ISO削除0件。内蔵残量は終了確認時約109GiB。再度外付けに退避する場合は元保管物を上書きせず新しい版としてコピー・照合・復旧確認後に原本整理を判断する。

## Snap公開完了

linux-snap-arm64-v0.3.4-fix1をprerelease/latest=falseで公開し、全16添付の公開後再ダウンロード・サイズ・SHA-256を照合した。[照合JSON](linux-arm64-snap-fix1-publication-result-2026-11-13.json)。専用ブランチrelease/linux-arm64-snap-0.3.4-fix1とタグは56de426。DEB→Snapの順で各公開後照合を完了。既存latestはlinux-v0.3.4を保持。
