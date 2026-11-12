# Linux amd64追加対応とWindowsストレージ運用計画

## 2026-11-13の最新引継ぎ・公開順

`wsl --list --verbose`と`wsl --list --online`はサンドボックス外で取得成功。既存の専用Build/Test環境を維持した。GitHubのRelease・リモート参照を照合し、Linux 0.3.4 DEB/Snap、AlmaLinux9 0.3.5、Fedora44/45 0.3.5が公開済みであることを確認した。以下の過去記録にあるFedora44「未公開」は履歴であり、現在の状態ではない。

未公開候補の優先順位は、固定版で既存検証がまとまったLeap16.1、Tumbleweed 20261110、Kali、Ubuntu/Debian更新候補の順とした。最優先の[Leap16.1 0.3.5 revision1を公開済み](linux-opensuse-leap161-publication-result_ja.md)。専用ブランチ・タグをpushし、858入力・実配布209ネイティブ実体・署名検証済み36 SRPMと11添付を照合した。409テスト・67サブテスト成功、9件スキップ。新GUI・更新・削除再導入・新規最小installrootも検証し、制約と合成入力での失敗を公開資料へ明記した。

次順位のTumbleweed Build/Testでも0.3.5 revision1のビルド・全409テスト・主要GUI・導入回帰・新規最小installrootを完了し、[公開前確認](linux-opensuse-tumbleweed-publication-review_ja.md)と11添付を準備した。864入力を`2f479d4`へ固定し、実配布206実体と35 SRPMの署名を照合。具体的な11添付とブランチ・タグの公開承認を確認中。

ユーザーは公開後のpushとX `tyamada22`での案内も依頼している。Fedora44/45の専用ブランチ・タグはpush済みを再確認し、[Fedora44/45の案内](https://x.com/tyamada22/status/2121012269358448657)と[Leap16.1の案内](https://x.com/tyamada22/status/2121013348489986500)を投稿・表示確認した。[案内確認記録](linux-amd64-publication-announcements_ja.md)を保存。日英README/CHANGELOGとLeap検証記録は専用文書ブランチへpushし、[draft PR #1](https://github.com/tyamada/Folimeld/pull/1)としてmainへの統合をレビュー可能にした。mainへは直接pushしていない。

既存の未コミット実装7ファイルは変更・破棄していない。差分全体のSHA-256は引継ぎ時の`72c52043f70243ef73d9098d9e86596858d8346875677081f0cf014e5e1bc283`と一致する。

## 以下は過去の計画・実施履歴

作成日: 2026-11-12（日本時間）。本書は計画であり、インストール、移動、削除、公開の実施記録ではない。

## 現在の到達点（2026-11-13続行後）

Fedora44最新：[公開前レビュー](linux-fedora44-publication-review_ja.md)まで完了。wheel105実体・OS102実体と署名検証済み37 SRPM、外部別添178項目を照合。822入力を専用コミット293da8aへ固定し、日英案内と11添付（約1.87GB）のチェックサムを確認した。後続でユーザーの明示許可を受け、[Fedora44試験版を公開](linux-fedora44-publication-result_ja.md)した。11添付を公開後に照合し、latest・既存配布物・mainの変更は保持した。

Fedora44の追加確認：[デスクトップ連携・導入回帰](linux-fedora44-035-r2-desktop_ja.md)でIME変換・確定、GIO日本語/空白パス、ライセンス表示、削除再導入・PDF/設定6件保持・再起動、新規最小依存installroot起動が成功。固有wheel/SRPM監査と最終配布資料統合を残し、未公開。

Fedora44の後続：[新ELFのPDF回帰](linux-fedora44-035-r2-regression_ja.md)で回転・Undo/Redo・ページ移動・白紙挿入削除、日本語名保存再読込、暗号化PDFの再認証、画像PDF生成が成功。ページ順・回転・本文・暗号化と元入力不変を照合した。IME/GIO/ライセンス画面・導入回帰・固有ソース監査を残し、未公開。

2026-11-13最新: [Fedora44 0.3.5 revision2候補](linux-fedora44-035-r2_ja.md)を新規専用コピーで生成。409テスト・67サブテスト成功（9件スキップ）、ソース822入力・別添119ファイルを照合し、専用Testの0.3.3からの更新・PDF/設定10件保持・offscreen/xcb起動を確認した。初回のOS告知不足を検出し、新revisionで修正した。Fedora44版は未公開で、新ELFのGUI/導入回帰と固有SRPM・wheel監査を次に進める。Fedora45公開案内の日英README/CHANGELOGはmainのea3f5f1として公開済み。

2026-11-13続行: [Fedora45 revision2の公開前レビュー](linux-fedora45-publication-review_ja.md)まで完了。409テスト・67サブテスト成功（9件スキップ）、PDF/IME/GIO/ライセンス画面・削除再導入・新規最小installrootを確認。署名検証済み38 SRPMと追加監査資料を別添へ統合し、対応ソース785入力を専用Gitコミット74366baへ固定した。日英案内と11添付・チェックサム検証も完了。後続でユーザーの明示許可を受け、[Fedora試験版を公開](linux-fedora45-publication-result_ja.md)した。11添付を公開後に照合し、latest・既存配布物・mainの変更は保持した。

公開済みの追加試験版は[Fedora45 amd64 0.3.5 revision2](linux-fedora45-publication-result_ja.md)（11添付）と[AlmaLinux9.8 amd64 0.3.5 revision5](linux-almalinux9-publication-result_ja.md)（12添付）。ユーザーの明示許可後に公開し、既存配布物を保持した。以下の公開前記述は履歴として区別する。

以前の[AlmaLinux 9先行公開の準備](linux-almalinux9-release-readiness_ja.md)から、依存ソース・告知確認と版確定を経て公開へ進んだ。検証済み候補と準備物は保持している。現在の作業対象は上記Fedora44候補。

以下の実施記録を追記しているため、前半の開始時点の状況と区別する。VM/ISO移動は実施していない。

| 対象 | 到達点 | 主な未確認事項 |
| --- | --- | --- |
| Ubuntu / Debian | 既存0.3.4を保持。Ubuntuで修正入りDEBを生成し、既存試験環境では展開起動のみ確認 | 修正入り候補の新規クリーン導入・削除再導入 |
| Kali Rolling | 専用環境でDEB導入、GUI・IME・画像・暗号化PDFを確認。描画修正候補で回転・Undo/Redo・保存再読込を確認 | 修正後候補でのIME等の全項目再試験、完全なデスクトップ |
| Fedora 45 | 0.3.5 revision2を試験公開。PDF/IME/GIO/ライセンス表示・更新・削除再導入・最小依存起動・対応ソースを確認。11添付を公開後照合、案内をmainへ統合 | 完全なデスクトップ、通常ファイルマネージャー操作、幅広い入力データ。依存来歴等の制約は公開一覧に保持 |
| Fedora 44 | 旧0.3.3の主要GUI/導入回帰に続き、新0.3.5 revision2をビルド。409テスト・ソース822入力・別添119件照合、専用Test更新・PDF/設定10件保持・起動を確認。未公開 | 新ELFのGUI/IME/GIO/ライセンス・削除再導入・最小依存、固有SRPM/wheel監査・配布資料統合、完全なデスクトップ |
| openSUSE Leap 16.1 | 専用2環境作成、SUSE用RPM実装・実ビルド・最小依存導入・起動・削除再導入・回帰テスト、GUI編集・保存再読込・IME・画像・暗号化PDF・GIO関連付け・日本語名保存・梱包revision更新を確認 | 通常ファイルマネージャー、アプリ版間移行、完全なデスクトップ |
| openSUSE Tumbleweed 20261110 | 専用2環境作成、スナップショット識別付きRPM実装・実ビルド・最小依存導入・起動・削除再導入・回帰テスト、GUI編集・保存再読込・IME・画像・暗号化PDF・GIO関連付け・日本語名保存・梱包revision更新を確認 | 通常ファイルマネージャー、アプリ版間移行、完全なデスクトップ |
| AlmaLinux 9.8 | 0.3.5 revision5を試験版公開。実ビルド・ソース対応・版更新・設定3項目保持・主要GUI/IME・GIO・削除再導入・再起動・最小依存起動を確認し、公開12添付物を照合 | 公開Ubuntu/Debian0.3.4からの移行、通常ファイルマネージャー、独立WSLブート・完全なデスクトップ、広い設定条件。依存来歴等は公開した制約一覧に保持 |
| 他ディストリビューション | 未着手 | 各OS別の環境・依存・実ビルド・導入検証 |

いずれも対象を限定した結果であり、全面的な対応済み表記ではない。公開済みFedora45/AlmaLinux9と非公開候補を区別する。新規環境の変更許可はKali、Fedora45、Fedora44、openSUSE Leap16.1、Tumbleweed、追加許可されたAlmaLinux9の専用環境に限定される。他OS環境の作成は今回の許可に含めない。通常デスクトップ固有の操作等は残る。次の候補は既存許可環境の残項目と公開版との差分・依存ソース/ライセンスの確認。AlmaLinux10等への拡大は別途許可範囲を確認する。既存環境・配布物は保持する。

## 作業分担と配置

直近の[Fedora45 0.3.5案検証](linux-fedora45-035-integration_ja.md)では、全409テスト・67サブテスト成功（9件スキップ）、RPM生成、非公開0.3.3 revision4からの更新、整合性・起動・設定3項目保持を確認した。元作業ツリーの版は変更せず、新ELFの編集・IME・GIO・導入回帰等を次の確認に残す。

[0.3.5案のGIO・導入回帰](linux-almalinux9-035-lifecycle_ja.md)を確認した。4パッケージファイルが復元し、PDF/設定6件保持、GIO終了コード0で日本語パス表示、再導入後起動が成功。新規installrootでもPython等の追加なし・UID/GID1000で12秒offscreen起動と整合性が成功した。独立WSL・通常デスクトップとは区別し、他OSの0.3.5案再ビルド等を残す。

[0.3.5案のGUI回帰](linux-almalinux9-035-regression_ja.md)で編集・日本語名保存・再読込、暗号化PDF、画像、IMEを確認した。データ照合も成功し、今回の素材コピー3件は不変。0.3.5新ELFのGIO・導入回帰・他OS再ビルドを残す。

[AlmaLinux9の0.3.5未公開案](linux-almalinux9-035-integration_ja.md)を新規専用コピーで実ビルドし、対応ソース678入力・別添149ファイルを照合した。専用Testは0.3.3 revision3から0.3.5案へ更新、整合性・起動・旧設定3項目の保持を確認。元作業ツリーは0.3.3のままで公開物は保持し、新ELFの全回帰・他OS再ビルド等を残す。

[公開版との統合レビュー案](linux-public-integration-review_ja.md)を専用コピーで準備した。0.3.5/build1はコピー内だけの未公開案で、元作業ツリーは0.3.3のまま。既存コード・資産・RPM処理を保持し、日英CHANGELOGをコピー内で同期。全409テスト・67サブテスト成功、9件スキップ、ruff/シェル構文/Alma出力名検査が成功した。バイナリ作成・版移行・公開は未実施。

[revision3の新規最小依存確認](linux-almalinux9-revision3-minroot_ja.md)として、許可済みTest内にDNF installrootを作成した。標準リポジトリ・weak dependencies無効で導入し、Python/ビルド依存/EPEL/推奨CJKフォントなし、UID/GID1000のoffscreen各12秒起動と整合性を確認。独立WSLやGUI試験とは区別し、既存Test候補・設定・素材は保持した。

[revision3の削除再導入・GIO](linux-almalinux9-revision3-lifecycle_ja.md)を確認した。パッケージ4ファイルが復元、ユーザー作成物6件を保持。専用XDG/D-Busで日本語・空白入りパスをGIO終了コード0で開き、再導入後のoffscreen/xcb各12秒も成功。依存自動削除は抑止した既存GUI試験環境の結果で、新規最小導入とは区別する。

[revision3のGUI回帰](linux-almalinux9-revision3-regression_ja.md)で編集・保存再読込・暗号化PDF・画像・IMEを確認し、保存データを照合した。今回作成した試験用PDFコピーへの保存と、キー入力の失敗を記録して元素材不変と区別した。新ELFのGIO・削除再導入等を残す。

[収集告知入り新候補](linux-almalinux9-notices-candidate_ja.md)を新規専用コピーで作成した。PyInstaller全文・Linux暗号化記録・OS告知を反映し、別添149ファイルを目録化。revision3への更新・起動・PDF/ライセンス画面を確認した。旧候補は保持。新ELFの全GUI・導入回帰はまだ再実施しておらず、公開はしていない。

[Pillow画像ライブラリ調査](linux-almalinux9-pillow-native-source-audit_ja.md)で、公式タグの依存版・ビルドスクリプト、ソース21件・パッチ3件、wheel告知22文書の一致を記録した。Alma8由来libXauは正確なソース版を取得したが鍵のSHA1拒否で署名未検証。システムポリシーは変更せず、可変main取得を含むwheel来歴と新候補への反映を残す。

[Python・PyInstaller・OS共有ライブラリ調査](linux-almalinux9-native-runtime-source-audit_ja.md)では、Alma候補のELF実体210件の一致、正確なSRPM42個の取得・チェックサム/署名、OS告知45文書を確認した。PyInstaller告知を次回ビルドで収集する修正と関連テスト11件・ruffが成功。既存候補は保持し、Pillow画像ライブラリのソース・wheel来歴・新候補への反映を残す。

続いて[Qt・PySide・Shiboken・MuPDFソース確認](linux-almalinux9-qt-mupdf-source-audit_ja.md)を実施した。公式Qtチェックサム、MuPDF再取得、Alma候補の実体84件・リンク22件のwheel照合とアーカイブ構成・告知一覧を記録した。wheelビルド来歴・他ネイティブ依存の確認と新候補への反映は残る。

公開版との差分と5つのRPM候補の埋込ソース・告知は[公開前入力監査](linux-amd64-release-input-audit_ja.md)で照合した。AlmaLinux9専用環境へsdist5件・Rust依存32件・OpenSSLを収集し、Linux固有の暗号化バイナリ照合記録を保存した。Qt等の依存ソース全体とwheel来歴の確認は残る。既存候補・告知・版は保持している。

- amd64はこのWindows PCのWSL2でビルド・検証する。ARM64はMacで別途実施する。
- 稼働中のWSL2、ビルド用ソース、仮想環境、キャッシュはCドライブのSSDに置く。
- EドライブはHDD。停止済みVM、ISO、WSLエクスポート、配布成果物の保管に使う。
- OneDrive配下は調査・集計・移動・削除の対象外とする。
- Macのファイル操作は本計画の実施対象に含めない。

## 現状と開始条件

- 実際の対象: `C:\Users\takum\Downloads\source\Folimeld`。`Downloads\Folimeld`は存在しない。
- 調査開始時のGit作業ツリーに変更なし。
- 空き容量: C約271.0 GiB、E約2166.5 GiB。実施時に再測定する。
- READMEのLinux最新案内は0.3.4だが、このチェックアウトの`folimeld/__init__.py`は0.3.3/build 1。調査により公開タグと対応ソースは0.3.4/build 1と確認した（下記）。新規配布では現mainをそのまま基準にせず、Linux公開ソースとの差分を整理してから版を決める。
- `build_linux.sh`は現在、共通ビルドと梱包を分離し、`binary`/`deb`/Fedora用`rpm`/Leap16.1用`suse-rpm`/Tumbleweed用`tumbleweed-rpm`/AlmaLinux9用`alma-rpm`を選択できる。Arch用梱包は未実装。
- 初回のサンドボックス内実行は`Wsl/E_ACCESSDENIED`だったが、現在はサンドボックス外の実行でWSL2へアクセスできる。新規KaliとFedora 45の専用環境での実施結果は後段を参照する。

## 実施順序

### 1. WSLとソースの確認

通常のPowerShellで次を取得し、失敗した場合はエラーを記録する。権限・WSL設定を一括変更しない。

```powershell
wsl --version
wsl --status
wsl --list --verbose
wsl --list --online
```

既存のUbuntu/Debian検証環境を識別し、名前だけで削除・再利用しない。配布一覧は取得日付きで保存し、以下の候補と照合する。公開ソースに合わせたコミットを選び、無関係な作業ツリーを変更せず専用のブランチまたは独立した作業コピーを使う。

### 2. 対象マトリクスを確定

以下は2026-11-11に確認したMicrosoft公開一覧に基づく候補。開始時のオンライン一覧と各OSの保守状況で確定する。

| 順序 | ディストリビューション | 形式・方針 |
| --- | --- | --- |
| 基準 | Ubuntu 24.04 / Debian 13 | 既存DEBの回帰確認 |
| 1 | Kali Rolling | 既存DEBを先に評価し、必要なら専用ビルド |
| 2 | Fedora 44 / 45 | 各版でRPM作成・クリーン検証 |
| 3 | openSUSE Leap 16.1 / Tumbleweed | SUSE用RPM。Fedora用RPMの無条件流用はしない |
| 4 | AlmaLinux 9 / 10 | Enterprise Linux用RPMの基準 |
| 5 | Arch Linux | PKGBUILDとpkg.tar.zst。AUR登録は別工程 |
| 6 | RLCPlus 9 / 10、Oracle Linux 9.5 | EL用成果物を個別検証。互換性だけで対応済みにしない |
| 7 | eLxr、Azure Linux 4、SUSE Linux Enterprise | Python/Qt/GUI依存パッケージの取得可否から評価 |
| 別枠 | Ubuntuの他版、AlmaLinux 8、Oracle Linux 7/8、Kitten 10 | 古いABI・Pythonと開発版の保守負担を評価し、対応可否を明記 |

同時に全環境を増やさず、原則として1ディストリビューションずつ完了させる。ビルド用と、開発依存を持たないインストール検証用を分ける。

### 3. ビルド実装

1. 固定したPython・依存制約でwheel取得可否、glibc、CPU要件を確認する。
2. 共通の実行ファイル生成、DEB/RPM/Archの梱包、対応ソース生成を分離する。
3. 既存DEB生成の互換性を維持する。出力先とファイル名にOS、版、アーキテクチャを含め、成果物の衝突を防ぐ。
4. 共有ライブラリ・Qtプラグイン・フォント・デスクトップエントリ・MIME登録の依存を確認する。
5. 実際に使った依存一覧、OS情報、コミット、コマンド、終了コード、SHA-256を保存する。

### 4. 検証の合格条件

- クリーン環境への導入、通常ユーザー起動、更新、削除が成功する。
- PDF表示、ページ移動・回転・白紙挿入・削除、Undo/Redo、別名保存、再読込が成功し、原本が保持される。
- 画像からPDF、日本語表示、パスワードPDF、非ASCIIパス、ファイル関連付けを確認する。
- offscreenの自動テストだけでGUI合格とはしない。WSLgの画面で操作を確認する。
- 通常のLinuxデスクトップ固有の操作はWSLgの結果と分け、未確認項目を明記する。必要なら既存VMを使い、追加VMは必要な場合だけ用意する。
- 同一形式でもディストリビューションごとに合否を記録する。

### 5. 公開

パッケージ、対応ソース、必要な依存ソース・ライセンス、SHA-256、ビルド記録、検証結果、導入手順をそろえる。既存ソース対応付け処理を新形式にも適用する。

GitHub ReleasesのDraftに正確なファイル一覧で添付し、再ダウンロードしてハッシュと導入を確認する。日英READMEを同期し、合格した組み合わせだけを対応済みとする。既存配布物を上書きしない。公式リポジトリ・Snap Store・AURへの登録は個別工程とする。今回は公開しない。

## Eドライブへの退避

### 現在確認できた候補

次はフォルダー内のファイル長合計。実際の占有容量・回収量ではない。不要と確定した一覧ではない。

| 対象 | 概算GiB | 次の確認 |
| --- | ---: | --- |
| FreeBSD forms-debug | 13.95 | デバッグ再開予定、他VMとのディスク共有 |
| FreeBSD 15.1 | 22.82 | スナップショット、SSH、再検証予定 |
| NetBSD 11.1 | 13.33 | 同上 |
| OpenBSD 8.0 | 23.23 | 同上。保存状態等も含むフォルダー合計 |
| VirtualBox VMs内ISO | 2.53 | 装着中か、スクリプトが参照するか |

さらにプロジェクトbuild内のISO、およびDocuments内に登録されたUbuntu検証VMを調査する。上の合計に重複加算しない。

### 配置と台帳

一般ファイルの整理と統合しやすいよう、保管ルートを `E:\PC_Archive\<実際のPC名>\2026-11-12\` とする。

- `VirtualBox\<VM名>\`: VM全体
- `ISO\<OS>\<版>\`: ISO
- `WSL\<登録名>\`: WSLエクスポート
- `Releases\<版>\amd64\`: 公開済み成果物の控え
- `_管理\移動台帳.csv`: 元パス、退避先、サイズ、SHA-256、参照修正、検証結果、元ファイルの残存、復元方法

実施前に移動先の絶対パスがこの保管ルート内であること、空き容量、書き込み可否を確認する。本セッションではEの書き込み権限を検証していない。

### 安全な手順

1. ISOから始め、使用終了を確認したforms-debug、低頻度のBSD VMへ進む。使用中WSLはCに残す。
2. VMを正常終了し、設定・ディスク・スナップショット・共有/外部参照を一覧化する。
3. VirtualBoxの「移動」または`VBoxManage movevm`でVM全体を移す。ディスクや差分スナップショットを手動で切り離さない。再構築困難なVMは先にバックアップを作る。
4. ISOはコピーしてSHA-256照合後、VMとスクリプトの参照を更新する。参照変更前の設定をバックアップする。
5. VM起動、SSH、PDF操作、スナップショット一覧、外部ISO参照を確認し、台帳に記録する。
6. コピー方式では確認完了後に限って元ファイルを削除する。移動機能で既に移ったファイルを追加削除しない。最終的にCの空き容量を再測定する。
7. 復旧時はVM移動機能で元の配置へ戻し、ISO参照とスクリプトを台帳に従って復元する。

## 次に着手する単位

開始時の順序はWSLアクセス回復とソース対応確認 → ISO参照調査 → Kali DEB検証 → Fedora RPM実装だった。現在の到達点と次の単位は冒頭の一覧を参照。ストレージ退避は未実施であり、移動・削除の許可を追加せずに実行しない。

### 公開ソース比較後の更新

ローカルに残る公開用checkoutのHEADは`eeacd06`で、作業ツリーはクリーン。共通基点`110f95a`からの公開用コミット差分を確認した。

| 差分 | 扱い |
| --- | --- |
| Linux specのQt Virtual Keyboard除外5行 | 現mainのspecへ同じ処理を反映した |
| アプリ版0.3.4/build 1 | 公開版の正しい値。現mainの版を機械的にこれへ合わせない |
| Linux-distribution.txt | 0.3.4、固定依存版、専用ビルドスクリプトを参照するため、そのまま転記しない。次回の実依存・梱包手順で生成する |
| build-release-candidate.sh | 既存0.3.4 DEB/Snapをテンプレートとする再梱包スクリプト。新OS用の汎用ビルドとしてそのまま採用しない |
| アイコンとMSIX画像の変更 | Linux追加対応への一括取り込み対象外。既存mainを保持 |
| main側の画像取込ダイアログ・タイマーの後始末修正 | 公開版の後に追加された修正として保持 |
| main側のsource_bundle改善・ARM64再現手順 | 現状を保持し、次回ソース対応付けへ利用 |

従って次回は既存0.3.4の再現物とは呼ばず、後続修正を含む新しい版として扱う。推奨候補は0.3.5。ただし版ファイルは今は変更せず、Windows/macOS/BSDと共有する版の影響を確認したリリース準備時に、日英変更履歴・パッケージ版・内部版を同時に更新する。パッケージ梱包のみの変更は各形式のrevisionで区別する。

公開済み0.3.4の再現が必要な場合は、公開タグと対応ソースを独立した作業コピーで使い、mainの後続修正を混ぜない。

今回のspec変更は構文確認まで。WSLのアクセス拒否は継続しており、PyInstallerでの実ビルド、収録一覧の検査、日本語IMEのGUI回帰確認は未実施。

## 参考

- [Microsoft WSL配布一覧](https://github.com/microsoft/WSL/blob/master/distributions/DistributionInfo.json)
- [WSL基本コマンド](https://learn.microsoft.com/windows/wsl/basic-commands)
- [VirtualBox VM移動](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html)
- [既存Linux配布記録](linux-release-migration_ja.md)

## 今回の実施記録

- 2026-11-12: Git状態、ビルド処理、依存制約、空き容量、VMフォルダー容量を読み取り確認し、本計画を作成した。
- WSL導入・起動、VM/ISO移動、削除、ビルド、公開は未実施。
- 続行時: WSL 2.7.3.0のバージョン取得は成功。一覧取得は引き続きアクセス拒否。Git Bashも`NtCreateDirectoryObject ... 0xC0000022`で起動できず、シェル実行による確認は未完了。OS/WSL設定は変更していない。
- 追加切り分け: コマンド実行プロセスは`S-1-16-4096`（Low Mandatory Level）で動作。WSL登録キーの読み取りとService Control Managerへのアクセスも拒否された。これらの結果は本セッションの制限と整合し、通常のWindows/WSLが壊れている証拠にはならない。ACL変更、WSL再インストール、サービス変更は行わない。
- 実ビルド再開には通常のPowerShellで`wsl --list --verbose`と`wsl --list --online`の結果を確認する必要がある。通常ユーザーで実行し、まず管理者権限は不要。サンドボックス外実行の承認経路は本セッションでは利用不可。シェルの構文・動作検証を完了するまでRPM実装の追加や候補配布を進めない。
- `build_linux.sh`へ`binary`モードを追加し、RPM系の共通実行ファイル生成をDEB梱包から分離した。引数なしは従来のDEB。DEBツールの事前確認、既存同名パッケージの上書き拒否、`FOLIMELD_LINUX_OUTPUT`による候補出力先指定を追加した。版は0.3.3のままなので、リリース用と扱わない。Linuxでの実行検証は未実施。

```bash
# 実行可能なLinux環境でのみ実施。いずれも現状は未検証。
bash build_linux.sh binary
FOLIMELD_LINUX_OUTPUT="$HOME/folimeld-candidates/$(date +%Y%m%d-%H%M%S)" bash build_linux.sh deb
```

## 0.3.3 / 0.3.4の事実確認（2026-11-12）

### WSLアクセス再確認と引継ぎ検証（2026-11-12）

- 今回はサンドボックス内の一覧取得が`Wsl/EnumerateDistros/Service/E_ACCESSDENIED`となったが、承認経路によるサンドボックス外実行で`wsl --list --verbose`と`wsl --list --online`が成功した。以前の「承認経路は利用不可」という記録は前セッションの状況であり、今回はWSLにアクセスできる。
- 登録済みはUbuntu-24.04（既定）、Ubuntu-26.04、Ubuntu-22.04、docker-desktop、Folimeld-Ubuntu-24.04-Amd64-034-Test、Debian、Folimeld-Debian-Amd64-034-Test。取得時は全てStopped、VERSION 2。検証専用環境は再利用・変更していない。
- オンライン一覧ではKali、FedoraLinux-45、openSUSE Leap 16.1/Tumbleweed、AlmaLinux 8/9/10、RLCPlus 9/10等を確認。今回の一覧にFedora 44とArchはなく、これらの導入方法・保守状況は別途確認が必要。
- 既定Ubuntuを起動し、Ubuntu 24.04.4 LTS、x86_64、通常ユーザー`tyamada22`、Python 3.12.3を確認。Linuxルートの空きは約940 GiB（仮想ディスク内の値で、Windows Cの実空きとは異なる）。DISPLAY=:0、WAYLAND_DISPLAY=wayland-0を確認したが、GUI操作は未検証。
- 起動時に`.wslconfig`の`wsl2.autoMemoryReclaim`と`wsl2.sparseVhd`が不明なキーとの警告が出た。設定は変更していない。
- 既存未コミット差分を保持し、WSL上で`bash -n build_linux.sh`（終了0）、`--help`（0）、不正形式（2）、`binary extra`（2）、Linux specのPython構文確認（成功）を実施した。ビルド本体・DEB梱包の動作確認は未実施。
- ビルド処理にはPyInstallerの`--clean`と一時ディレクトリ削除が含まれるため、今回の移動・削除禁止の範囲では実ビルドを実行していない。インストール、ファイル移動・削除、公開は行っていない。

GitHub APIの公開リリース、公開タグのファイル、ローカルの最終配布記録と対応ソースZIPを照合した。

- `linux-v0.3.3`は2026-11-04 12:20:42 JSTに公開。リリース本文は、既存の`releases/ubuntu/`のバイト列を変更せず移設し、再ビルドしていないと明記する。旧版は残っている。
- `linux-v0.3.4`は2026-11-10 18:44:39 JSTに公開。対象コミットは`eeacd06a49cda85ddc1d432bd785e507f8006a89`。同タグの`folimeld/__init__.py`は0.3.4/build 1であり、ファイル名だけの変更ではない。
- ローカルの最終配布用ソースZIPについて、amd64のSHA-256 `5483477427254f56e4a82232bab0585d633abe0d5aac73eeb4be0234da197a4a`、ARM64のSHA-256 `281132ee8d40b75c0233b603bcb04e6132a0dcc856b45419d679ade7a2e51c90`を実計算し、GitHubの公開asset digestと一致した。両ZIP内のアプリ版も0.3.4/build 1。
- 公開記録はQt Virtual Keyboard除外、IBus/Mozcで日本語ファイル名の保存・再読込、6環境の検証、依存ソース・告知の補足を記載する。
- amd64 Snapの梱包スクリプトは旧0.3.3 Snapをステージ入力に使用し、0.3.4 DEBのアプリ実行ファイルを使用してSnap版を0.3.4に設定する。これは旧パッケージの単純改名とは異なる。
- mainには`6478317`でダウンロード案内、`00c630d`で変更履歴が追加された一方、アプリ版ファイルの履歴は0.3.3への更新で止まっている。公開用作業コピーとmainで版が分かれている。
- 公開コミットは現チェックアウトのローカルGitオブジェクトに存在しない。祖先関係や全差分の統合状況は、この事実だけでは断定しない。
- 0.3.4を採用した直接の指示・理由（旧版との衝突回避等）は、今回確認した記録だけでは確定していない。

対応案: 公開済み0.3.3/0.3.4は変更せず保持する。次工程で公開コミットとmainの差分を取得し、版・梱包・ソース対応付けを専用ブランチで統合する。その後、追加OS向けのアプリ版とパッケージリビジョンの運用を決める。今回アプリ版・公開物は変更していない。

参照: [0.3.3公開記録](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.3)、[0.3.4公開記録](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.4)、[公開タグのアプリ版](https://github.com/tyamada/Folimeld/blob/linux-v0.3.4/folimeld/__init__.py)。ローカル証拠は`C:\Users\takum\Documents\Codex\2026-10-31\pc-folimeld-0-3-3-3\outputs\folimeld-linux-0.3.4-review\release-nokbd-r1\`の配布記録・対応ソース・梱包スクリプト。

### WSL既存依存環境での追加確認（2026-11-12）

- 既定UbuntuのシステムPythonにpipはなく、今回の作業ツリーに`.venv-linux`は存在しない。既存の`dist`は存在するため、直接ビルドによる上書きは避ける。
- 既存0.3.4用環境`/home/tyamada22/folimeld-linux-amd64-0.3.4-110f95a/source/.venv-linux`を変更せず使用。Python 3.12.3、PySide6 6.11.2、PyMuPDF 1.28.2、Pillow 12.3.0、cryptography 50.0.2、PyInstaller 6.22.2を確認した。主要5依存は現在のconstraints-release.txtと一致する。推移依存全体の照合は未実施。
- 作業ツリーをimportし、Qt offscreen初期化、メモリ内PDF保存・再読込、PdfDocumentの回転・白紙挿入・ページ削除・Undo/Redoが成功。ディスク上のPDFは作成・削除していない。tests/test_version.pyの3件も成功した。実GUIやパッケージの合格を意味しない。
- build_linux.shの版取得で仮想環境Pythonのパスを引用符で囲み、空白を含むパスでの単語分割を防いだ。git diff --checkは成功。
- source_bundle.pyにはZIPのrename、ビルドスクリプトには一時ディレクトリ削除、アイコン生成には複数既存アセットの上書きがある。実ビルドには新規専用作業コピーを使用し、その中の一時ファイル削除・名前変更の許可を得てから進める。既存作業ツリー・配布物・VM/ISOの移動・削除・公開は実施しない。

### 専用コピーでのamd64実ビルド（2026-11-12）

- ユーザーが新規専用コピー内だけの一時ファイル削除・生成ファイル名変更を許可した。元の作業ツリー、既存配布物、VM/ISOの移動・削除・公開は禁止のまま保持した。
- WSLの専用コピー: `/home/tyamada22/folimeld-candidates/20261111T203954Z`。末尾は実行ホストのUTC時計から生成した識別子であり、本記録の作業日はクライアント指定の日本時間2026-11-12を用いる。既存未コミット変更込みの入力ファイルをコピーし、入力ハッシュを`SOURCE-MANIFEST.json`、元コミット・Git状態・使用Pythonを`candidate-input.json`に保存した。
- 既存仮想環境を更新せず、`python -m PyInstaller --noconfirm Folimeld-linux.spec`を専用コピーで実行し成功。既存アイコンを使用し、アイコン再生成とpip更新は実行していない。従ってbuild_linux.sh全体の実行検証ではない。
- `dist/folimeld`: ELF x86-64、106671288 bytes。SHA-256: `f15c0d92f869f3243f312734ed8b131999e67ba359f6e89d04d05dd9e87d5bae`。
- CArchive内のVirtual Keyboard関連エントリ0件。埋め込み`licenses/Build-source.txt`が参照するソースZIPのSHA-256を照合し一致: `58d1f20f69a237f8369aaf8412029c95f172326f9edced26da3d13704ca40ca4`。Gitなしのコピーのため埋め込み記録のgit_commitは未設定で、元コミットは外部のcandidate-input.jsonに記録される。配布用にはコミット情報を維持したソース対応付けが必要。
- 既存環境にpytestがなかったため、専用コピーの`test-dependencies/`へconstraints-release.txtに従うpytest 9.1.1等を導入。既存仮想環境は変更していない。QT_QPA_PLATFORM=offscreen、キャッシュ無効、専用コピー内basetempでtest_history.py、test_model_validation.py、test_image_import.py、test_pdf_save.py、test_password.pyを実行し、70件成功（3.48秒）。ログ: `pytest-linux.log`。
- 生成バイナリをoffscreenで起動。TMPDIR・XDG設定/キャッシュ先を専用コピーに限定し、12秒生存後にテスト側から終了した。ログはfitz API非推奨とoffscreenのpropagateSizeHints警告。GUI操作合格とは扱わない。記録: `binary-startup.json`。
- 同コピー内で現行DEBと同じ配置・controlテンプレートを用いて`dpkg-deb --root-owner-group --build`を実行。候補: `candidate-packages/folimeld_0.3.3_amd64.deb`（105117274 bytes）。SHA-256: `b4efd2c286cd70d8e25782ce7b2be443731789b26e64ca1e6248834b64ae4a28`。libc6最低版はビルド環境から2.39。インストールは未実施。
- DEB内の実行ファイルをメモリ内で読み、検証済みELFとのハッシュ一致を確認。tools/source_bundle.pyでDEBと対応ソースの関連JSONも生成した。内部版・パッケージ版は0.3.3のままで、公開済み0.3.3の再現物でも新リリースでもない。
- 次工程: コミット情報を維持した専用ソース準備とbuild_linux.sh全体の実行確認、クリーン検証環境の識別、DEB導入・WSLg GUI/IME回帰、Kali検証。その後にFedora RPMへ進む。今回クリーン環境の変更、Kali/Fedora導入、RPM実装、公開は実施していない。

### ビルドスクリプト全体と既存検証環境での追加確認（2026-11-12）

- 新規専用領域`/home/tyamada22/folimeld-candidates/script-validation-20261112`で、元Gitコミットを参照するコピーと`build venv`（空白を含む名前）を作成した。既存未コミット変更もコピーした。Git clone --no-checkout直後はインデックスが空で、初回はLICENSE収録チェックで停止した。コピー側だけでgit read-tree HEADを行い、再実行は成功した。元リポジトリのGitインデックスは変更していない。
- build_linux.shのdebとbinaryを、それぞれ専用仮想環境・専用出力先・専用TMPDIR/キャッシュで全体実行し、ともに終了0。依存導入、アイコン生成、PyInstaller --clean、DEB一時領域の後片付けも専用領域に限定した。
- deb実行後、同じ出力先へ再実行して終了1と上書き拒否メッセージを確認し、DEBハッシュも不変だった。ソース対応付けとLinuxリリース準備の既存テストは14件成功（0.27秒）。
- スクリプト生成DEBのSHA-256は`ede8751b69311f57d26783099923a7742207af6ce018967e16b59c25929d30af`。収録ELFのSHA-256は`b021d344c29849eaf2e67ba969b1c3df954bba69a0caa3b33b79eb305c77cf00`。その後のbinaryモード生成ELFは別ビルドのため`069c37286f892e1ff1242ab65be56b8ac0e408cc22996c2783ffcd1c6723e17d`。DEBは再ビルド・上書きしていない。
- 最新ELFの埋め込みgit_commitは`423e59471b576e4732c7d6ec0ad9ab25cbf19582`、working_tree_changed=true。専用コピーは配布物等を含まない部分コピーなので、未コミット差分に加えて未配置の追跡ファイルもdirty判定の理由になる。Virtual Keyboard関連0件、対応ソースZIPのハッシュ一致を確認した。
- 既存Ubuntu検証WSLはUbuntu 24.04.4で、build-essential等が残っており、クリーン環境とは扱わない。Ubuntu/Debian両検証WSLの新規専用ディレクトリへDEBを転送・展開し、通常ユーザーでoffscreen起動。Ubuntu 24.04.4とDebian 13（13.6）の両方で12秒生存後にテスト側から終了した。既存インストールはどちらも0.3.4のまま不変。これはインストール・更新・削除試験ではない。
- WSLgで候補と非ASCII名の検証PDFを起動し、対象ウィンドウの存在を確認した。しかしComputer Useの対象画面取得は別のChatGPT領域を返し、再選択・再取得でも改善しなかった。座標操作は実行せず、起動した候補プロセスを終了した。実画面表示・編集・日本語IMEは未検証。
- 検証JSON: [linux-amd64-verification-2026-11-12.json](linux-amd64-verification-2026-11-12.json)。コミット、依存一覧、ハッシュ、テスト結果、各環境の起動結果と制約を保存した。内部版・パッケージ版は0.3.3の検証用であり、公開用ではない。
- ユーザーの追加許可により、新規Kali専用WSL環境内だけで依存の導入・更新・削除とFolimeld導入試験を行う。登録名`Folimeld-Kali-Amd64-Test`、配置`C:\Users\takum\WSL\Folimeld-Kali-Amd64-Test`として新規作成した。既存WSL登録名とディレクトリの未使用、Cの空き15 GiB超を確認してから実行した。
- Kali初期イメージは2026.2、APTはkali-last-snapshotだった。初期パッケージ一覧・取得先設定を保存し、[Kali公式手順](https://www.kali.org/docs/general-use/kali-apt-sources/)に従って新規環境だけをkali-rollingへ切り替えて更新している。既存Ubuntu/Debian、WindowsのWSL設定は変更していない。

### 新規Kali Rollingでの導入・更新・削除試験（2026-11-12）

- 新規Kaliだけでkali-rollingへの切り替えとapt-get full-upgradeが成功。検証時のOSはKali Rolling 2026.3、x86_64、glibc 2.43。初期状態の2026.2/kali-last-snapshotと区別する。
- スクリプト生成DEB（SHA-256 `ede8751b69311f57d26783099923a7742207af6ce018967e16b59c25929d30af`）を新規環境へ転送し照合。apt-get --no-install-recommendsで初回導入に成功した。build-essential、python3-pip、python3-venvはいずれも未導入。推奨のfonts-noto-cjkも未導入なので日本語フォント表示の合格とはしない。
- パスワードを設定しない一般検証ユーザー`folimeld-test`（uid 1000）を作成。導入済み/usr/bin/folimeldを通常ユーザーでoffscreenとWSLgのxcb（DISPLAY=:0）の各方式で起動し、いずれも12秒生存後にテスト側から終了した。xcbの出力はfitz非推奨警告のみで、Qtプラグインのロード失敗はなかった。これはGUIの画面・編集操作やIMEの合格を意味しない。
- 更新試験では同じELFのままcontrolのパッケージ版だけを`0.3.3-1.test1`へ変えたローカル試験専用DEBを作成し、APT更新に成功。新しいアプリ版への更新試験ではない。試験専用revisionは公開しない。
- 新規Kali内だけでapt-get purge folimeldが成功し、実行ファイル、デスクトップ項目、アイコンの削除を確認。その後元の0.3.3候補を再導入し成功。再導入後のELFハッシュは`b021d344c29849eaf2e67ba969b1c3df954bba69a0caa3b33b79eb305c77cf00`と一致し、dpkg --auditも成功した。最終状態は候補0.3.3が導入済み。
- 検証JSON: [linux-amd64-kali-verification-2026-11-12.json](linux-amd64-kali-verification-2026-11-12.json)。初期/最終パッケージ一覧、APT取得先、起動結果、更新・削除・再導入コマンドと終了コードを保存した。詳細ログは新規Kaliの`/root/folimeld-verification/`、一般ユーザー起動結果は`/home/folimeld-test/verification/`に保存。
- 残るKali検証: GUI上のPDF編集・日本語表示・IME・非ASCII保存・ファイル関連付け。画面取得問題があるため対応済みとは表記しない。これらの後にFedora RPM検証へ進む。既存Ubuntu/Debianと配布物は保持し、公開は実施していない。

### Kali WSLg GUI・IME検証の追加（2026-11-12）

- Windows側の対象画像取得をLinux側のX11ウィンドウ識別・撮影で補い、導入済みDEBの実画面を確認した。新規Kaliへ日本語フォント・IBus/Mozc・GUI/MIME検証ツールを追加し、独立D-BusセッションでIMEを検証した。前回の最小依存試験とは環境が異なる。
- 日本語UI/PDF表示、右回転、白紙挿入、Undo/Redo、挿入白紙削除、Mozcのnihongo→日本語変換、非ASCII名での別名保存とGUI再読込を確認した。保存後PDFをデータ照合し、3ページ・回転[90,0,0]・文字内容保持・原本ハッシュ不変を確認した。
- 自作AES-256 PDFの閲覧パスワード入力と表示、画像フォルダからのPDF作成・保存、GIOのPDF関連付けからの候補起動も確認した。画像PDFは1ページ・画像1枚・中央RGB[0,0,255]で、元画像と暗号化PDFは不変。
- サムネイル・日本語UI・ファイル選択の既存テスト16件と16サブテストが専用Ubuntu環境で成功。GUI検証で使用した候補プロセスは識別して終了した。
- 詳細と制約: [Kali GUI検証](linux-amd64-kali-gui-verification_ja.md)、[検証JSON](linux-amd64-kali-gui-verification-2026-11-12.json)。画面証拠はdocumentation/linux-amd64-kali-gui-verification/に保存。
- 残る確認は回転直後の描画応答、ページ移動の実画面、暗号化PDFの再保存、完全なLinuxデスクトップ操作。合成入力のダイアログ破棄時にキー解放が失敗する場合があり、明示解放して再観測した。拡張子省略時は自動で.pdfが付かないことも記録した。アプリコード・既存配布物・版・公開設定は今回変更していない。

### Fedora 45 RPM実装と新規環境検証（2026-11-12）

- ユーザーの追加許可により、新規Fedora45のビルド用・クリーン導入試験用WSL2を作成した。登録名はFolimeld-Fedora45-Amd64-Build/Test、配置はC:\Users\takum\WSL\の各同名ディレクトリ。既存登録名・導入先の未使用とCの空き20 GiB超を確認してから作成した。
- build_linux.shにFedora限定rpmモードとFOLIMELD_LINUX_PYTHONを追加。tools/package_linux_rpm.py、packaging/linux/folimeld-fedora.spec.in、tests/test_linux_rpm.pyを追加した。DEB既定とbinaryモードを維持し、RPMはOS/版/CPU/revision別のファイル名・出力先、同名上書き/出力リンク拒否、ELF無改変、対応ソース関連付けを実装した。
- Fedora45の標準Python3.15とは別にPython3.14.10をビルドに選択し、固定依存がwheelだけで解決することを確認。glibc2.44、RPM6.1.0、x86_64で実ビルドが成功した。
- 最初のRPMはDBus不足で起動失敗を再現。必須ライブラリ宣言とビルド環境を修正し、試験環境にはRPM依存解決だけで導入した。推奨日本語フォント名も実在するgoogle-noto-sans-cjk-fontsへ修正した。
- 最終候補はfolimeld-0.3.3-3.fc45.x86_64.rpm。SHA-256は5a9b6c030a676fedea1b7c2b11ab7d30d50cdfe2c807872b9e738e8b95409516。ELFのSHA-256は161121ac4dd7531b42deb0995246bbe5ca310c8a0cee8a1fc801c7220041d521で、ビルド直後とRPM導入後が一致。Virtual Keyboard関連0件と対応ソースZIPのハッシュも確認した。
- 開発依存未導入・推奨依存無効の新規Fedoraで、一般ユーザーのoffscreen/xcb起動、revision更新、削除・再導入、rpm -V、dnf checkを検証した。削除再導入はrevision2、最終revision3では更新と最小依存起動を確認している。
- Fedoraの既存/追加回帰テスト106件と24サブテストが成功。GUIツールと日本語フォントは最小依存試験の後に追加し、最終RPMの実画面で日本語PDF表示・ページ移動・回転・別名保存・GUI再読込が成功。保存データのページ順[2,1,3]・回転[0,90,0]・文字保持・原本ハッシュ不変を照合した。
- 詳細・再実行手順・制約: [Fedora RPM記録](linux-fedora-rpm_ja.md)、[検証JSON](linux-amd64-fedora45-verification-2026-11-12.json)。スクリーンショットはdocumentation/linux-amd64-fedora45-gui-verification/へ保存した。
- 回転直後のプレビュー描画、日本語IME、画像取込・暗号化PDFのFedora実画面、完全なLinuxデスクトップ操作、Fedora44/ARM64/他RPM系OSは残る。新しいオンライン一覧にはFedora44もあるが、今回は作成・検証していない。アプリ版・READMEの対応済み表記・既存配布物は変更せず、公開も実施していない。

### 回転プレビューの原因特定と修正（2026-11-12）

- 画像生成タイマーとPDF画素は正常だった。Qt自身のウィジェット画像でも空白を再現し、幅312pxのグリッドに対して画像項目がx=133,width=294（右端426）となる配置ずれを確認した。非同期アイコン生成後、空アイコン時の位置が残っていた。
- folimeld/thumbnails.pyでアイコン設定後にdelegateのsizeHintChangedを通知するよう修正した。tests/test_thumbnails.pyへ実際のQtイベントループでグリッド内への収まりを検証する回帰テストを追加し、修正前失敗・修正後成功を確認した。
- Fedoraの対象回帰107件・24サブテスト、xcbでの関連9件、Ubuntu/Python3.12での関連9件、ruffが成功。大文書・キャッシュ・スクロールの既存確認も通った。
- 新規Fedora試験環境だけを通常候補0.3.3-4.fc45へ更新。診断コードを含まない実行ファイルで、回転直後に保存や別操作を挟まず表示し、Undo/Redoでも表示することを確認した。初回サムネイルの位置も修正された。
- RPM SHA-256: 8cd4a8a4257a0543f1b6f40a3848711c14711ce67f54efe14fbd9394a65c4090。ELF SHA-256: 88d3979a88ebdefb59cc064c01bb7a1d14ce81a3832407cf488111310a659800。ソースZIP・導入済みELF・通常main.py・描画コードの対応を照合した。原本PDFも不変。
- 詳細: [描画修正記録](linux-thumbnail-redraw-verification_ja.md)、[検証JSON](linux-thumbnail-redraw-verification-2026-11-12.json)。診断バイナリは別コピーにのみ作成し、通常RPMには含めていない。
- この時点ではUbuntu/Kaliの修正入りDEB再ビルド、FedoraのIME・画像/暗号化PDF実画面、完全なLinuxデスクトップ操作が残った。DEBの続報は下記。既存配布物とアプリ版は保持し、公開は実施していない。

### 修正入りDEBの再ビルドとKali再検証（2026-11-12）

- Ubuntu 24.04の専用作業コピーでサムネイル修正入りDEBを生成した。Python3.12.3、glibc下限2.39、非公開版0.3.3。旧候補は保持した。
- 新規Kaliへ同一版を再導入し、導入ELFと生成ELFの一致、dpkg監査、初期配置・回転直後・Undo/Redo・別名保存・GUI再読込を確認した。保存PDFは3ページ・回転[90,0,0]・文字保持で、原本は不変。
- 既存Ubuntu試験環境の導入済み0.3.4は保持した。新しい専用ディレクトリにDEBを展開し、offscreenで12秒間の起動を確認した。
- DEB SHA-256: bb531236e78c9195245a88d6620e840f232b505b97d82968719528f415573875。ELF SHA-256: 752d4f389a671196aa15a1b673b08b88d8ebbcc26b67f04822a58fe05102bbc6。
- 詳細と制約: [DEB追加検証](linux-deb-thumbnail-fix-verification_ja.md)、[検証JSON](linux-deb-thumbnail-fix-verification-2026-11-12.json)。今回はクリーン導入・削除再導入やIME等の再試験は行っていない。
- この時点ではFedoraのIME・画像/暗号化PDF実画面、完全なLinuxデスクトップ、他OS版・アーキテクチャ等が未検証だった。Fedora GUIの続報は下記。既存配布物・README・版は変更せず、公開も行っていない。

### Fedoraの画像・暗号化PDF・日本語IME追加検証（2026-11-12）

- 新規Fedora試験環境のrevision4で、自作AES-256 PDFの閲覧パスワード入力・回転・別名保存・再認証とGUI再読込を確認した。データ照合ではパスワード必須・誤パスワード拒否・回転[90,0,0]・文字保持が成功。
- 合成PNG1枚のフォルダ取込・保存を確認。生成PDFは1ページ・画像1枚、中央画素RGB[0,0,255]。元PDF・暗号化PDF・画像は保持した素材とバイト単位で一致した。
- 最小依存試験後の新規FedoraだけへIBus/Mozcと独立D-Busセッション用ツールを追加し、通常候補のQtファイル名欄でnihongo→にほんご→日本語の変換・確定を確認。試験GUIと専用IBusを終了した。
- rpm -Vとdnf checkが成功。詳細・画面証拠・制約: [Fedora追加GUI記録](linux-fedora-extended-gui-verification_ja.md)、[検証JSON](linux-fedora-extended-gui-verification-2026-11-12.json)。以前の最小依存導入試験と環境を区別する。
- 完全なLinuxデスクトップ、Fedora44/ARM64/他RPM系OS、他の入力方式や幅広い画像・暗号化設定は未検証。公開前の依存ソース・ライセンス確認と版の統合も残る。既存配布物・版・READMEは保持し、公開は行っていない。

### Fedoraの非ASCIIパス・PDF関連付け（2026-11-12）

- 専用XDG設定内だけでPDFの既定アプリをfolimeld.desktopへ設定し、日本語と空白を含むパスの合成PDFをGIOから起動した。
- セッションバスなしでは終了コード0でもGUIが現れなかった。独立D-Busセッションでは通常候補が起動し、プロセス引数の対象パスと3ページの表示を確認した。
- 原本・コピーはハッシュ不変。試験GUIと専用セッションを終了した。通常デスクトップのファイルマネージャー操作は未確認。
- 詳細: [Fedora GUI記録の追加節](linux-fedora-extended-gui-verification_ja.md)、[関連付け検証JSON](linux-fedora-mime-verification-2026-11-12.json)。既存のユーザー設定と配布物は保持し、公開は実施していない。

### Fedora44の専用環境・RPM基礎検証（2026-11-12）

- ユーザーの追加許可後、専用Build/Test WSL2を新規作成。既存環境・配布物を保持し、現在のソースからFedora44向けRPMを生成した。
- glibc下限2.43、非公開版0.3.3-1.fc44。RPM SHA-256はa2dd4769bb8030c2b28a0c98568a89311bbc91982aab05c49e77dcef3b2254d8。
- 開発依存なし・推奨依存無効の試験環境で導入、一般ユーザーのoffscreen/xcb起動各12秒、削除・再導入、ELF一致、rpm -V/dnf checkが成功した。
- ビルド側のQt実行用DBus不足を補い、回帰85件・8サブテストが成功。RPM経由の試験側は手動補完不要だった。失敗ログを保持した。
- 詳細: [Fedora44基礎検証](linux-fedora44-rpm-verification_ja.md)、[検証JSON](linux-amd64-fedora44-verification-2026-11-12.json)。GUI編集・IME等は次の検証として残り、Fedora45の結果は流用しない。公開は実施していない。

### Fedora44のPDF編集GUI検証（2026-11-12）

- 最小依存検証後の新規試験環境へGUIツールと日本語フォントを追加し、通常候補で日本語PDF表示・回転直後・Undo/Redo・ページ移動・白紙挿入削除・別名保存・GUI再読込を確認した。
- 保存データは3ページ・元ページ順[2,1,3]・回転[0,90,0]・文字保持で、原本SHA-256不変。保存PDF SHA-256は7b54eee33d7c281a015dae02e2941dd59c317af66d9ec19605cfcf0d2491bab6。
- [Fedora44 GUI記録](linux-fedora44-gui-verification_ja.md)、[検証JSON](linux-fedora44-gui-verification-2026-11-12.json)と9画面を保存。識別した試験GUIを終了した。
- IME・画像・暗号化PDF・関連付け等は未確認として保持。既存配布物・版は変更せず、公開は実施していない。

### Fedora44の暗号化PDF・画像・IME追加検証（2026-11-12）

- 通常候補で合成AES-256 PDFの読込・回転・別名保存・再認証・GUI再読込を確認。保存データはパスワード必須・誤パスワード拒否・3ページ・回転[90,0,0]・文字保持。
- ASCII名でコピーした合成PNG1枚をフォルダから取り込み保存。生成PDFは1ページ・画像1枚・中央RGB[0,0,255]。元のPDF・暗号化PDF・PNGは保持した素材と一致。
- 新規試験環境内の独立IBus/Mozcでnihongo→にほんご→日本語の変換確定を確認。rpm -V/dnf check成功。検証GUIと専用IBusを終了した。
- 詳細・制約・7画面: [Fedora44追加GUI記録](linux-fedora44-extended-gui-verification_ja.md)、[検証JSON](linux-fedora44-extended-gui-verification-2026-11-12.json)。関連付け・非ASCII保存・更新試験等は残る。公開は実施していない。

### Fedora44の関連付け・日本語名保存・梱包revision更新（2026-11-12）

- 専用XDG/D-Bus環境のGIO関連付けから日本語・空白入りパスのPDFを起動し、日本語名の別名保存・GUI再読込を確認。保存データは3ページ・回転[90,0,0]・文字保持、原本とコピーは不変。
- 同一ELFを0.3.3-2.fc44として別名梱包し、revision1からdnf upgrade成功。ELF一致、rpm -V/dnf check、更新後offscreen/xcb各12秒の起動が成功。revision1は保持。
- 詳細・制約: [関連付け・保存・更新記録](linux-fedora44-update-nonascii-verification_ja.md)、[検証JSON](linux-fedora44-update-nonascii-verification-2026-11-12.json)。通常ファイルマネージャーやアプリ版間移行を確認した結果ではない。公開は実施していない。

### openSUSE Leap 16.1の次工程案（2026-11-12）

- WSLオンライン一覧にopenSUSE-Leap-16.1があることを再確認。専用登録名Folimeld-openSUSE-Leap16.1-Amd64-Build/Testと、C:\Users\takum\WSL\配下の同名配置先は未使用。Cの空きは約253.8 GiB。
- 新規2環境だけで依存更新・導入・削除試験を行い、既存環境は保持する案。環境作成は許可確認後に行う。
- 現在のRPMヘルパーはFedora以外を拒否する。SUSE用のOS識別、出力名、spec、推奨フォント、依存パッケージ、PyInstallerアーカイブ保護を別途確認する。Fedora RPMを流用した合格扱いはしない。
- Python版・固定依存wheel・glibcを新規ビルド環境で評価し、専用コピーで生成、開発依存のない試験環境で導入・一般ユーザー起動・更新削除・GUIを順に検証する。公開・既存配布物上書きは行わない。

### openSUSE Leap16.1のRPM実装・基礎検証（2026-11-12）

- ユーザーの追加許可後、専用Build/Test WSL2を新規作成し、標準リポジトリを更新。Python3.13.13・glibc2.40で固定依存を取得した。
- suse-rpmモード、Leap16.1限定ヘルパー・spec・OS拒否テストを追加。Fedoraモードの既定とOS制限を維持し、一時梱包処理を共用した。
- GLibスレッド依存不足を特定し、ビルド環境とSUSE specを修正。revision1を保持してrevision2を実ビルド。89件・17サブテスト、ruff、シェル構文検査が成功。
- 試験環境は開発依存・推奨フォントなし。未署名ローカルRPMに限定した許可オプションで導入、一般ユーザーoffscreen/xcb各12秒の起動、削除再導入、ELF一致、rpm -Vとzypper verifyが成功した。
- RPM SHA-256: a1eb907c59bbe82f553e97e1cd374c693b4860d6574f2a422f872504d3819ebd。ELF SHA-256: 53fb285ac9efa231e4abf40d82bb69be0b411c04de21890cfd609fd3366cf567。
- 詳細・制約: [Leap16.1 RPM記録](linux-opensuse-leap161-rpm_ja.md)、[検証JSON](linux-opensuse-leap161-verification-2026-11-12.json)。実画面・更新試験は残る。TumbleweedやARM64の合格とは扱わず、公開は実施していない。

### Leap16.1のPDF編集GUI検証（2026-11-12）

- 最小依存試験後の新規環境へGUIツール・日本語フォント等を追加し、通常候補で日本語PDF表示・回転直後・Undo/Redo・ページ移動・白紙挿入削除・別名保存・GUI再読込を確認。
- 保存データは3ページ・元順[2,1,3]・回転[0,90,0]・文字保持。原本は不変。保存PDF SHA-256: bb37633d4d03124f190e34a815f16b99414b6a0235a2acf7a05f11e9133e9e9b。
- 初期の未選択状態の画面は合格証拠から除外して保持。選択後の確認画面、データ照合、ログを[GUI記録](linux-opensuse-leap161-gui-verification_ja.md)と[検証JSON](linux-opensuse-leap161-gui-verification-2026-11-12.json)へ保存した。検証GUIを終了した。
- IME・画像・暗号化PDF・関連付け・更新等は引き続き未確認。既存配布物・版を保持し、公開は実施していない。

### Leap16.1の暗号化PDF・画像・IME追加検証（2026-11-12）

- 通常候補で自作AES-256 PDFの読込・回転・別名保存・再認証・GUI再読込を確認。保存データはパスワード必須・誤パスワード拒否・3ページ・回転[90,0,0]・文字保持。
- ASCII名の合成PNG1枚をフォルダから取込み保存。生成PDFは1ページ・画像1枚・中央RGB[0,0,255]。元PDF・暗号化PDF・PNGは保持素材と一致。
- 新規環境内の独立IBus/Mozcでnihongo→にほんご→日本語の変換確定を確認。dbus-run-session不足は標準のdbus-1-daemonを追加して解決。rpm -Vとzypper verify成功、試験GUIと専用IBusを終了した。
- 詳細・7画面・制約: [Leap追加GUI記録](linux-opensuse-leap161-extended-gui-verification_ja.md)、[検証JSON](linux-opensuse-leap161-extended-gui-verification-2026-11-12.json)。関連付け・非ASCII保存・更新等は残る。公開は実施していない。

### Leap16.1の関連付け・日本語名保存・梱包revision更新（2026-11-12）

- 専用XDG/D-Bus環境のGIO関連付けから日本語・空白入りパスのPDFを起動。日本語名でGUI別名保存・再読込、3ページ・回転[90,0,0]・文字保持、原本不変を確認した。
- 合成入力で一文字欠けた実際の保存名は「保 結果.pdf」。意図した文字列どおりの入力成功とは扱わず、実ファイルを照合した。
- 同一ELFをrevision3として別名梱包。revision2から3へzypperで更新し、ELF一致、rpm -V、zypper verify、更新後offscreen/xcb各12秒の起動が成功。既存候補を保持。
- RPM SHA-256: 0dc2dc75899bc1c6cffe6503e735e690c8c71a25161884c2151df34bf5add004。詳細・制約: [保存・更新記録](linux-opensuse-leap161-update-nonascii-verification_ja.md)、[検証JSON](linux-opensuse-leap161-update-nonascii-verification-2026-11-12.json)。試験GUIと専用セッションを終了。公開は実施していない。

### Tumbleweedの次工程案（2026-11-12）

- WSLオンライン一覧にopenSUSE-Tumbleweedがあることを再確認。専用登録名Folimeld-openSUSE-Tumbleweed-Amd64-Build/Testと、C:\Users\takum\WSL\配下の同名配置先は未使用。Cの空きは約249.0 GiB。
- 許可後に新規2環境を作成し、その中だけで標準リポジトリ更新、ビルド/実行依存の導入、候補の導入・更新・削除試験を行う。既存Leap/Fedora/Kali/Ubuntu/Debianは保持する。
- 現SUSEヘルパーはLeap16.1以外を拒否する。TumbleweedのOS識別・スナップショット版を実環境で取得し、Leapと出力名・配置先を分離する。Python/Qt固定依存の取得可否、glibc、RPM処理とGLib等の依存は個別確認する。
- ローリング更新のためビルド/試験時のOS版、rpm一覧、依存版とハッシュを記録し、単なる実施日をスナップショット版として代用しない。専用コピーで生成し、開発依存のない試験環境へ必須依存だけで導入する。
- 最小依存起動・削除再導入の後、GUI編集、IME、画像、暗号化PDF、非ASCII保存、関連付けを個別検証する。Leapの結果をTumbleweedの合格として流用しない。既存候補上書き・公開・VM/ISO移動は行わない。

### Tumbleweedの専用環境・RPM基礎検証（2026-11-12）

- ユーザーの追加許可後、専用Build/Test WSL2を作成。初期20261102から標準リポジトリのdupで両環境とも20261110へ更新した。Python3.14.8・glibc2.44で固定依存を取得。
- tumbleweed-rpmモードと専用ヘルパー・日付/OS拒否テストを追加。出力は実VERSION_IDのtw20261110を含み、Leap/Fedoraと分離。SUSE specのRelease識別子を引数化し、Leapはlp161を維持。
- ビルド側DBus不足を補完し、共通ビルドへQt/PyMuPDFのimport事前検査を追加。最初のrevision1を保持してrevision2を再ビルド。回帰93件・26サブテスト、ruffとシェル構文検査が成功。
- 開発依存・推奨フォントのない試験環境へ必須依存だけで導入、一般ユーザーoffscreen/xcb各12秒の起動、削除再導入、ELF一致、rpm -Vとzypper verifyが成功。
- RPM SHA-256: ef4ff9f2f6de37e224aa449b2bc6ce6275fb5279fddcba8179f2179b11d8296f。ELF SHA-256: d5395dec696d6a001633ec642da8a784ac0220ab02ac1a8973392fdde0a20d43。
- 詳細・制約: [Tumbleweed RPM記録](linux-opensuse-tumbleweed-rpm_ja.md)、[検証JSON](linux-opensuse-tumbleweed-verification-2026-11-12.json)。実画面・更新等は未確認として残す。他スナップショット・ARM64の合格とは扱わず、公開は実施していない。

### Tumbleweed 20261110のPDF編集GUI検証（2026-11-12）

- 最小依存検証後の新規試験環境へGUIツール・日本語フォントを追加。通常候補で日本語PDF表示・回転直後・Undo/Redo・ページ移動・白紙挿入削除・別名保存・GUI再読込を確認した。
- 保存データは3ページ・元の順[2,1,3]・回転[0,90,0]・文字保持。原本はハッシュ不変。保存PDF SHA-256: 1787b4b474f16e980d4ff2a8dfa1b8e1dbee09672babccb82046276d61b211ff。
- [Tumbleweed GUI記録](linux-opensuse-tumbleweed-gui-verification_ja.md)、[検証JSON](linux-opensuse-tumbleweed-gui-verification-2026-11-12.json)と9画面を保存。試験GUIだけを識別して終了した。
- IME・画像・暗号化PDF・関連付け・更新等は未確認として残す。既存配布物・版を保持し、公開は実施していない。

### Tumbleweed 20261110の暗号化PDF・画像・IME追加検証（2026-11-12）

- 通常候補で自作AES-256 PDFの読込・回転・別名保存・再認証・GUI再読込を確認。保存データはパスワード必須・誤パスワード拒否・3ページ・回転[90,0,0]・文字保持。
- ASCII名の合成PNG1枚をフォルダから取込み保存。生成PDFは1ページ・画像1枚・中央RGB[0,0,255]。元PDF・暗号化PDF・PNGは保持素材と一致。
- 新規環境内の独立IBus/Mozcでnihongo→にほんご→日本語の変換確定を確認。実際のDBusパッケージ名で記録し、rpm -Vとzypper verify成功。試験GUIと専用IBusを終了した。
- 詳細・7画面・制約: [Tumbleweed追加GUI記録](linux-opensuse-tumbleweed-extended-gui-verification_ja.md)、[検証JSON](linux-opensuse-tumbleweed-extended-gui-verification-2026-11-12.json)。依存導入時のsystemdトリガー警告は区別し、OS/Windows設定は変更していない。関連付け・非ASCII保存・更新等は残る。公開は実施していない。

### Tumbleweed 20261110の関連付け・日本語名保存・梱包revision更新（2026-11-12）

- 専用XDG/D-Bus設定でGIO関連付けから日本語・空白入りパスのPDFを起動。「保存 結果.pdf」へGUI別名保存・再読込、3ページ・回転[90,0,0]・文字保持、原本不変を確認した。
- 同一ELFをrevision3として別名梱包し、revision2からzypperで更新。ELF一致、rpm -V、zypper verify、更新後offscreen/xcb各12秒の起動が成功。既存候補を保持した。
- RPM SHA-256: 7c7dba88bac92b1c8dcbcab6031f496812ba687a2f5c04eec7c2f77606b3f6bb。詳細・追加3画面・制約: [保存・更新記録](linux-opensuse-tumbleweed-update-nonascii-verification_ja.md)、[検証JSON](linux-opensuse-tumbleweed-update-nonascii-verification-2026-11-12.json)。試験GUIと専用セッションを終了。公開は実施していない。

### AlmaLinux9の次工程案（2026-11-12）

- WSLオンライン一覧にAlmaLinux-9とAlmaLinux-10があることを確認。まず9を一単位として進め、10の環境は同時には増やさない。
- 専用登録名Folimeld-AlmaLinux9-Amd64-Build/Testと、C:\Users\takum\WSL\配下の同名配置先は未使用。Cの空き約241.6 GiB。新規環境の変更許可はまだない。
- 許可後に専用2環境を作成し、その中だけで標準リポジトリ更新、Python/Qt/ビルド依存の導入、候補の導入・更新・削除試験を実施する。既存環境・配布物は保持する。
- Python版・固定依存wheel・glibc・CPU条件を実環境で確認する。固定制約で成立しない場合は制約を無断で緩めず、取得ログと原因を記録して対応案を整理する。
- 現RPMヘルパーはFedora/Leap/Tumbleweedを個別識別し、AlmaLinuxを拒否する。Alma用OS・版識別、EL版/CPU/revisionを含む出力名と配置、spec、Qt実行依存・日本語フォントを個別に実装・確認する。他EL系OSへの互換性を対応済みの根拠にしない。
- 専用コピーで実ビルドし、開発依存なしの試験環境で最小依存導入・一般ユーザー起動・削除再導入、次にGUI編集・IME・画像・暗号化PDF・非ASCII保存・関連付け・更新を確認する。ソース対応・版・依存一覧・終了コード・SHA-256を保存し、公開・既存候補上書き・VM/ISO移動は行わない。

### AlmaLinux9の専用環境・RPM基礎検証（2026-11-12）

- ユーザーの追加許可後、専用Build/Test WSL2を作成。AlmaLinux9.8・glibc2.34、ビルド側の標準Python3.12で固定依存wheelの取得が成功。制約緩和・追加リポジトリは不要だった。
- alma-rpmモード、AlmaLinux9限定ヘルパー・spec・拒否テストを追加。出力は小版を含むalma9_8で分離。他EL系OSやAlmaLinux10は拒否する。
- ネイティブimport事前検査、回帰97件・35サブテスト、ruff、シェル構文検査が成功。専用コピーで0.3.3-1.alma9_8を実ビルドした。
- 開発依存・Python3.12・推奨フォントなしの試験環境へ必須依存だけで導入。一般ユーザーoffscreen/xcb各12秒、削除再導入、ELF一致、rpm -V/dnf checkが成功。
- RPM SHA-256: e8f7564c95f1a4692de9555c2b37e20eae22ee27e72a21eb802777153becf970。ELF SHA-256: e7df5b946593a785d5d2c68ba15caa110903ee86b70b30eea784ba8a56f34914。
- 詳細・制約: [AlmaLinux9 RPM記録](linux-almalinux9-rpm_ja.md)、[検証JSON](linux-almalinux9-verification-2026-11-12.json)。実画面・更新等は未確認。他EL系OS・AlmaLinux10・ARM64の合格とは扱わず、公開は実施していない。

### AlmaLinux9.8のPDF編集GUI検証（2026-11-12）

- 最小依存試験後の新規Test環境だけへGUIツール・日本語フォントを追加。標準リポジトリにxdotool/ImageMagickがないためextras提供epel-releaseを追加し、署名検証を維持して取得。標準リポジトリだけで通った本体導入と区別する。
- 通常候補で日本語PDF表示・回転直後・Undo/Redo・ページ移動・白紙挿入削除・別名保存・GUI再読込を確認。保存PDFは3ページ・元順[2,1,3]・回転[0,90,0]・文字保持、原本ハッシュ不変。
- 保存PDF SHA-256: a4b59c294f738774a0974003b6fdd50e747d21bb71d78f1c056326cfe6b87cdd。[GUI記録](linux-almalinux9-gui-verification_ja.md)、[検証JSON](linux-almalinux9-gui-verification-2026-11-12.json)へ9画面とツール版・有効リポジトリを保存した。試験GUIだけを終了。
- IME・画像・暗号化PDF・関連付け・更新等は未確認として残す。既存環境・配布物・版を保持し、公開は実施していない。

### AlmaLinux9.8の暗号化PDF・画像・IME追加検証（2026-11-12）

- 通常候補で自作AES-256 PDFの読込・回転・別名保存・再認証・GUI再読込を確認。保存データはパスワード必須・誤パスワード拒否・3ページ・回転[90,0,0]・文字保持。
- ASCII名の合成PNG1枚をフォルダから取込み保存。生成PDFは1ページ・画像1枚・中央RGB[0,0,255]。元PDF・暗号化PDF・PNGは保持素材と一致。
- EPEL追加後の新規試験環境でIBus/Mozcを導入し、独立セッションでnihongo→にほんご→日本語の変換確定を確認。rpm -V/dnf check成功、試験GUIと専用IBusを終了した。
- 詳細・7画面・制約: [AlmaLinux9追加GUI記録](linux-almalinux9-extended-gui-verification_ja.md)、[検証JSON](linux-almalinux9-extended-gui-verification-2026-11-12.json)。標準リポジトリの最小依存試験とは区別する。関連付け・非ASCII保存・更新等は残る。公開は実施していない。

### AlmaLinux9.8の関連付け・日本語名保存・梱包revision更新（2026-11-12）

- 専用XDG設定のGIO経由で日本語・空白入りパスのPDFを開き、「保存 結果.pdf」へ別名保存・GUI再読込。3ページ・回転[90,0,0]・文字保持・原本不変を確認した。
- 初回のD-Bus警告とGIO待機、準備前セッションの失敗、出力パイプ取得のタイムアウトを保持。独立D-Busとファイル出力でGIO終了コード0・PDF表示を確認した。通常ファイルマネージャーの合格とは扱わない。
- 同一ELFをrevision2へ別名梱包し、専用Test内でdnf更新。ELF一致、rpm -V、dnf check、更新後offscreen/xcb各12秒の起動が成功した。
- RPM SHA-256: bd93161bca6ed6cd45f0b23a1591dc4f5d0f356608a26eaa679536ad6fa772f9。詳細・追加4画面・制約: [保存・更新記録](linux-almalinux9-update-nonascii-verification_ja.md)、[保存・更新JSON](linux-almalinux9-update-nonascii-verification-2026-11-12.json)、[関連付けJSON](linux-almalinux9-mime-verification-2026-11-12.json)。試験GUIと専用セッションを終了した。既存候補を保持し、公開は実施していない。
