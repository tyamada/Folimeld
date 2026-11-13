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

## X案内と最終引継ぎ

- DEB: https://x.com/tyamada22/status/2121043541908689225
- Snap（DEB案内への追記）: https://x.com/tyamada22/status/2121046814115979650

各パッケージの専用ブランチ・タグ、日英案内のmain反映、全16添付の公開後照合を完了してから投稿し、本文・リンク・公開表示を確認した。Mac元プロジェクトは未コミット差分0の状態を確認してmainへff-only更新。Windows側の未コミット変更やVMにはアクセス・変更していない。今回、既存公開物の削除/置換とVM/ISO原本の削除はいずれも0件。

## 0.3.5 ARM64 DEBへの同期（2026-11-13、追加）

先行0.3.4+fix1 DEB/Snapの公開とX案内完了後、次順位のUbuntu／Debian向け0.3.5 ARM64 DEBを実ビルド・新規検証した。[今回の検証](linux-deb-arm64-035-validation_ja.md)を参照。ソース7890a67（差分なし）、公開専用資料付きタグb5c98e2。ARM64での実行結果のみを受入に数えた。

0.3.5 ARM64 DEBは公開済みへ変更。0.3.5 ARM64 Snapは未ビルド・未検証を維持し、今回のDEB結果をSnap合格にしない。RPM/Kali ARM64も未検証のまま。既存公開物はすべて保持。

Mac内蔵上のビルド・Ubuntu・Debian VMは通常停止済み。更新済み内蔵ディスクと外付けの元アーカイブを保持し、削除・上書きは0件。次の公開には、このDEBの公開後全添付照合・main反映・X案内を完了してから進む。

公開結果: [linux-deb-arm64-v0.3.5](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-arm64-v0.3.5)をprerelease/latest=falseで公開。全16添付（1,686,119,373 bytes）を公開後のURLから全件取得し、サイズとSHA-256が一致した。既存全公開Releaseの添付ID・名前・サイズ・digestが不変、latestはlinux-v0.3.4。[公開後照合JSON](linux-deb-arm64-035-publication-result-2026-11-13.json)。

X案内も完了: https://x.com/tyamada22/status/2121057222788878379 。全16添付の公開後照合とmain e648deeのpush成功後にtyamada22から投稿し、本文・Releaseリンクのカード・公開日時を確認。今回のDEB公開工程は完了。次のパッケージの公開はまだ開始していない。

## 0.3.5 ARM64 strict Snapへの同期（2026-11-13、DEB完了後の追加）

DEB公開・全16添付の公開後照合・main反映・X案内完了後に、Snap固有のビルド・新規受入・制限確認を実施。[検証記録](linux-snap-arm64-035-validation_ja.md)。本体ソースa77ad2f（差分なし）、タグ/専用ブランチは検証資料追加後の3a1a614。0.3.5 ARM64 Snapは公開済みへ変更し、DEB/amd64の実行結果をSnap合格に数えない。

内部210/外側11のAArch64実体と正確な968ソース入力を照合。3回のGUIはすべて終了0。旧x6→0.3.5 x7更新と同一候補x7→x8再導入、文書/common/current設定の保持、再読込・正常終了、AppArmor enforce・Seccomp2、同一プロファイルの限定的な許可/拒否試験を確認。完全削除再導入・revert・snapshot復旧・IME・Wayland・実機ARMは未試験。

ビルドVM cとUbuntu-Snap VMは内蔵で実行し、通常停止。外付けアーカイブ・旧公開Snap・VM/ISOとユーザーデータの退避を保持。VM/ISO削除・外付け起動は0件。RPM/Kali ARM64は未検証のまま。今回のSnapの全添付再取得照合とX案内完了まで、別パッケージの公開は開始しない。

公開完了: [linux-snap-arm64-v0.3.5](https://github.com/tyamada/Folimeld/releases/tag/linux-snap-arm64-v0.3.5)をprerelease/latest=falseで公開。全16添付（1,690,964,765 bytes）を公開後に全件再取得し、サイズとSHA-256が一致。既存公開Releaseの添付ID・名前・サイズ・digestは不変、latestはlinux-v0.3.4を維持。[公開後照合JSON](linux-snap-arm64-035-publication-result-2026-11-13.json)。

X案内完了: https://x.com/tyamada22/status/2121080042847617395 。全16添付の公開後照合とmain 739e489のpush成功後にtyamada22から投稿し、本文・Releaseカード・公開日時を確認。0.3.5 ARM64 strict Snapの公開工程は完了し、次のパッケージ公開は未開始。

## Fedora44 ARM64 RPM 0.3.5への展開（2026-11-13、Snap完了後の追加）

Snap公開・全添付照合・X案内完了後、Fedora44専用ARM64ビルド/実行VMをMac内蔵に準備。公式イメージの署名・SHA256を確認。最終ソース1c04bd2（差分なし）、タグfedora44-arm64-v0.3.5は検証文書追加後43ab1cc。[検証記録](fedora44-arm64-035-validation_ja.md)。Fedora44 ARM64を公開済みへ変更し、他のFedora45/AlmaLinux/openSUSE/Kali ARM64は未検証のまま。amd64/Ubuntuの実行結果をFedora ARM64合格には数えない。

全974ソース入力、同梱200 AArch64実体（公式wheel105/Fedora RPM95）を確認。38署名付きbinary RPMに対応する34exact signed SRPMを添付。別ビルド先ELF一致（RPMヘッダー時刻は異なる）、409テスト成功、3GUI正常終了、完全削除再導入と文書/設定保持、最小依存起動を確認。SELinux維持。実機/Wayland/IME/旧版更新などは未検証。全16公開添付の再ダウンロード照合とX案内を完了してから次へ進む。

専用VM2台を内蔵で通常停止し、QCOW2 overlay・backing image・UEFI vars・seedを保持。外付けChatGPT-Test上での起動0件、VM/ISOの削除・新規外付け退避0件。既存退避計画の削除前コピー/復旧確認条件を変更しない。従来の外付けアーカイブと既存公開物を保持。

## Fedora45 ARM64 RPM 0.3.5への展開（2026-11-13、Fedora44完了後の追加）

Fedora44公開・全添付照合・X案内完了後、Fedora45専用ARM64ビルド/実行VMをMac内蔵に準備。公式イメージの署名・SHA256を確認。最終ソース0b2ee3e（差分なし）、タグfedora45-arm64-v0.3.5は検証文書追加後52b2686。[検証記録](fedora45-arm64-035-validation_ja.md)。Fedora45 ARM64を公開済みへ変更し、AlmaLinux/openSUSE/Kali ARM64は未検証のまま。amd64/Ubuntuの実行結果をFedora ARM64合格には数えない。

全981ソース入力、同梱200 AArch64実体（公式wheel105/Fedora RPM95）を確認。38署名付きbinary RPMに対応する34exact signed SRPMを添付。別ビルド先ELF一致（RPMヘッダー時刻は異なる）、409テスト成功、3GUI正常終了、完全削除再導入と文書/設定保持、最小依存起動を確認。SELinux維持。実機/Wayland/IME/旧版更新などは未検証。全16公開添付の再ダウンロード照合とX案内を完了してから次へ進む。

専用VM2台を内蔵で通常停止し、QCOW2 overlay・backing image・UEFI vars・seedを保持。外付けChatGPT-Test上での起動0件、VM/ISOの削除・新規外付け退避0件。既存退避計画の削除前コピー/復旧確認条件を変更しない。従来の外付けアーカイブと既存公開物を保持。

## AlmaLinux9 ARM64 RPM0.3.5への展開（2026-11-13）

Fedora45の公開・全添付照合・X案内完了後、公式AlmaLinux9.8 ARM64 Cloudイメージの署名・SHA256を確認し、内蔵Macの専用ビルド/実行VMで検証。[公開・検証記録](almalinux9-arm64-035-validation_ja.md)。Alma9 ARM64を公開済みへ変更し、openSUSE/Kali ARM64は未検証のまま。amd64/Ubuntu/Fedoraの結果をAlma合格には数えない。

正確な本体ソース44dee9d0543f5003160284f21aa458acbe13faa9（clean）、タグalmalinux9-arm64-v0.3.5は7e9870f（検証文書追加）。glibc2.34上でQtbase/qtsvg/PySide6.11.2をソースビルド。標準Qt翻訳カタログなし、アプリ翻訳あり、5モジュール限定と任意梱包ガードパッチを記録。994入力、163AArch64実体（公式wheel25/自前Qt41/AlmaRPM由来97）、39exact signed SRPMを確認。RPATH変換は元ファイルへ再現して全バイト一致。410tests/9skips/69subtests、3GUI終了0、完全削除再導入、文書設定保持、最小依存起動。候補1のOpenGL不足をrevision2で修正し新しいrootで合格。同じQt SDKの2ビルド先でELF一致、RPM時刻は異なる。全16公開添付再取得とX案内まで完了してから次へ進む。

VMは内蔵のみで実行。使用済みVMはユーザーの追加指示によりChatGPT-Testへ退避し、コピー/SHA256/内蔵復元/ディスク整合性確認後に内蔵側を整理する。外付け起動は禁止。公式イメージは長期保管HDDまたはNASへの照合保存を別途必要とし、進行状況は作業出力の保管記録を正とする。過去の「退避0件」は当時の記録として保持する。

## Leap16.1 ARM64 RPM0.3.5の公開（2026-11-13、AlmaLinux9完了後）

[Leap16.1 ARM64](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-arm64-v0.3.5)を公開済みへ変更。本体ソースfa0f0f5、検証資料付きタグ56788b0。0.3.5のままARM64で新規ビルド・検証。Tumbleweed/Kali ARM64は未検証のまま。[検証](opensuse-leap161-arm64-035-validation_ja.md)と[全16添付の公開後再取得照合](opensuse-leap161-arm64-035-publication-result-2026-11-13.json)を参照。既存全公開添付のID・名前・容量・digest不変、latestはlinux-v0.3.4を保持。

410テスト成功/9スキップ/69サブテスト、同一VMの別出力先ELF一致、999ソース入力、202AArch64実体（公式wheel105/署名済みOS95/Google Brotli1.1.1ソースビルド2）を照合。47binary RPMと対応32signed SRPM、Brotli公式ソース/14公式テスト/ライセンス/構成を添付。OSの修正版Brotliを保持し、対応ソースが取得できない古い候補へダウングレードしていない。UID1000/Xorg/IceWM・SELinux EnforcingでGUI3回正常終了、完全削除再導入と文書・設定保持、最小依存構成起動を確認。amd64や他OSの合格を流用しない。実機/Wayland/IME/旧版更新等は未検証。

全添付照合後のmain反映とX案内を完了してから次の対象へ進む。保存先の個別運用記録は私的記録として別管理する。

Leap16.1 ARM64のX案内完了: https://x.com/tyamada22/status/2121163624484053498 。全16公開添付の再取得照合とmain791a791のpush後にtyamada22から投稿し、本文・Releaseカード・2026年11月13日17:49の公開表示を確認。今回の公開工程は完了。Tumbleweed/Kali ARM64は未着手・未検証を維持。

## Tumbleweed ARM64 0.3.5の検証とVM運用変更（2026-11-14）

ユーザー指示により専用の新しい外付けSSDでVMを実行する方針へ変更し、内蔵実空き100GBの再開待ちを解除した。大容量作業はSSD、重要更新はNASにも保管し、既存データ・Time Machine履歴を保持。旧ストレージや完了済み移行・削除手順は再実行しない。これは過去の内蔵限定記録の訂正ではなく現行方針の更新。

次順位は既存梱包処理と公式イメージがあるTumbleweed ARM64をKaliより先行。snapshot20261111向け0.3.5 RPMを新規ARM64環境でビルド・検証した。[検証と制約](opensuse-tumbleweed-arm64-035-validation_ja.md)を参照。410tests/69subtests成功、9skips、GUI3回終了0、文書/設定保持、1001ソース入力、201AArch64実体、32signed SRPMを照合。公開後の全添付再取得・main反映・X案内が完了するまでは公開工程未完了。Kali ARM64は未着手・未検証のまま。

Tumbleweed ARM64公開完了: [opensuse-tumbleweed-arm64-v0.3.5](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed-arm64-v0.3.5)、タグ74de136、本体c8fb78a。全16添付の公開後サイズ/SHA256照合と既存公開物/latest保持を確認。次のKali ARM64へ進む前にmain反映とX案内を完了する。
