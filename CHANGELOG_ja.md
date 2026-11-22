# 変更履歴

[日本語](CHANGELOG_ja.md) | [English](CHANGELOG.md)

## 未リリース

- Microsoft Store次期リリース（Submission 3 / パッケージ版 1.0.3.0、アプリ版 0.3.7）に向けて、ARM64実機環境にてStore向けネイティブMSIXパッケージ（`Folimeld_1.0.3.0_arm64.msix`、PE Machine `0xAA64`）をビルドし、静的検査（`msix_preflight` 合格）およびソースバンドル関連付けを完了して公開計画書（`windows-store-release-plan_ja.md`）および受入試験表（`windows-store-acceptance_ja.md`）へハッシュを記録。

- FreeBSD 15.1、NetBSD 11.1、OpenBSD 8.0 の amd64 版 0.3.5 パッケージを公開: それぞれ `folimeld-0.3.5_1.pkg`（FreeBSD 15.1 amd64）、`folimeld-0.3.5.tgz`（NetBSD 11.1 amd64）、`folimeld-0.3.5.tgz` および `folimeld-mupdf-1.28.2.tgz`（OpenBSD 8.0 amd64、Signify署名付き）の各配布Releaseを公開し、日英のインストール手順書（`documentation/freebsd-install*.md`、`netbsd-install*.md`、`openbsd-install*.md`）およびREADMEのダウンロード表を更新・同期。

- Ubuntu amd64 strict Snap 0.3.5 パッケージを公開: Ubuntu 24.04.5 LTS amd64 環境にて core24 ベースの `folimeld_0.3.5_amd64.snap`（SHA-256: `ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570`）をビルドし、`snap install --dangerous` による更新導入、各種インターフェース接続（GNOME 拡張、Wayland、X11、OpenGL、Home 等）およびオフスクリーン GUI 起動を確認。日英の検証文書（`documentation/linux-snap-amd64-035-validation_ja.md`、`linux-snap-amd64-035-validation.md`）と検証レコードを整備。

- READMEのダウンロード一覧表から旧版となったUbuntuおよびDebian 0.3.4の記載を整理し、最新の0.3.5配布行へ一本化。

- macOS Homebrew版を 0.3.5 に更新: Python 3.14環境、ランチャー `launch_homebrew.py` を経由した配布元識別子（`homebrew`）の伝達と「ヘルプ → 開発を応援する…」メニューの有効化、5.7 MBの軽量ソースアーカイブ生成、`brew install --build-from-source tyamada/tap/folimeld` および `brew test tyamada/tap/folimeld` による動作確認・アンインストール検証を完了。

- FreeBSD 15.1 aarch64版パッケージを 0.3.5_1 に更新: ARM64向けビルドツール修正、`folimeld-0.3.5_1.pkg` ビルド、`pkg add` による導入、オフスクリーン実行および「開発を応援する…」アクションの動作確認を完了。

- OpenBSD 8.0 arm64版パッケージを 0.3.5 に更新: ARM64向けビルドツール（`tools/build_openbsd_package.py`）両対応化、Python 3.14 / LLVM 22 ベースでの `folimeld-0.3.5.tgz` ビルド、Signify による署名付与（埋め込み署名および `SHA256.sig`）、`pkg_add` による導入、オフスクリーン実行および「開発を応援する…」アクションの動作確認を完了。

- NetBSD 11.1 aarch64版パッケージを 0.3.5 に更新: ARM64向けビルドツール（`tools/build_netbsd_package.py`）両対応化、Python 3.12 / Qt6 / PySide6 6.11.2 ベースでの `folimeld-0.3.5.tgz` ビルド、`/usr/pkg/sbin/pkg_add` による導入、オフスクリーン実行および「開発を応援する…」アクションの動作確認を完了。

- Ubuntu / Debian / Kali Linux 0.3.5 パッケージの整備: 検証済み 0.3.5 DEB（amd64 / arm64）および strict Snap（arm64）のリリースステージングを準備。

- Debian、Ubuntu、およびBSD（FreeBSD、NetBSD、OpenBSD）の各パッケージをFolimeld 0.3.5ベースへ更新する計画を策定・遂行。決定論的ソースコードスナップショットZIP（`Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`）の確定と関連付け、FreeBSD（`0.3.5_1`）・NetBSD（`0.3.5`）・OpenBSD（`0.3.5`）のバージョン解決および依存ソース整合性テスト（`tests/test_bsd_packages.py`、`tests/test_freebsd_package.py`）を追加して全件パスを確認。
  - **Linux (amd64)**: WSL2環境にてUbuntu 24.04 amd64 DEBパッケージ（`folimeld_0.3.5_amd64.deb`、SHA-256: `5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174`）をビルドし、Ubuntu 24.04.4/24.04.5 LTS および Debian 13.6/13.7（Trixie）環境下にてoffscreen GUI初期化・PyMuPDF読み込み・実行ファイルの整合性を検証。READMEのダウンロード表を最新ポイントリリース（Ubuntu 24.04.5 / Debian 13.7）表記へ更新・同期。
  - **FreeBSD 15.1 (amd64)**: VirtualBox VM環境にて `folimeld-0.3.5_1.pkg`（SHA-256: `16d3d1801acae0f62bf99d89d53f8a679593e5896d1db60d46cc5b57c15946ae`）をビルドし、`pkg add -f` による更新インストールおよびoffscreen起動を検証。
  - **NetBSD 11.1 (amd64)**: VirtualBox VM環境にて `folimeld-0.3.5.tgz`（SHA-256: `7dc5c7d68e41b5120a9345fd679e5c99d46fcd7b7b50cf4f49e22d55ffec6e6a`）をビルドし、`pkg_add -u` による更新インストールおよびoffscreen起動を検証。
  - **OpenBSD 8.0 (amd64)**: VirtualBox VM環境にて ports ビルドにより `folimeld-0.3.5.tgz`（SHA-256: `6d0b68373f380622dc1bbbe4bad4d132648f8974fa7246ca9af0c22db9028e63`）および専用依存 `folimeld-mupdf-1.28.2.tgz`（SHA-256: `1d537907faf92f11f2f701f967486c03643097e8dd5dff9199e6c6a6aa87bf8c`）を生成。`pkg_sign` および `signify` による署名（`SHA256SUMS.txt.sig`）を完了し、署名検証を伴う `pkg_add -r` 更新およびoffscreen起動を検証。
  - 日英の更新・ビルド手順書（`documentation/bsd-035-release-plan_ja.md`、`bsd-035-release-plan.md`）へ確定パッケージ情報と受入結果を記録。

- Microsoft Store次期リリース（Submission 2 / パッケージ版 1.0.2.0）に向けて、Windows 11 ARM64ネイティブ対応の追加計画、PyInstaller spec（`Folimeld.spec`）のUPX無効化、日英のストア掲載文（新機能欄）および公開計画文書を整備。x64 および ARM64 実機環境にてStore向けネイティブMSIXパッケージ（`Folimeld_1.0.2.0_x64.msix`、`Folimeld_1.0.2.0_arm64.msix`）をビルドし、静的検査（`msix_preflight` 合格）およびソースバンドル関連付けを完了して公開計画書（`windows-store-release-plan_ja.md`）および受入試験表（`windows-store-acceptance_ja.md`）へ確定パッケージ情報を記録。2026年11月16日にPartner Center（Submission 2）へ審査提出を完了。無料アプリのみとして応援購入（アドオン）は無効を維持。

- Windows 11向けの3つのプレビューパッケージ（ソース＋uv版、`uv tool install`版、Desktopインストーラー版）について、x86_64とARM64共通の事前準備・ダウンロード・インストール・実行手順を統合・整理し、各アーキテクチャ別のハッシュ照合・Smart App Control対応案内を日英READMEおよびドキュメントに拡充。

- Windows 11 ARM64（Surface Pro 11等のCopilot+ PC / Snapdragon X Elite）向けに3つの試験公開パッケージ（ソース＋uv版、`uv tool install`版、PyInstaller onedir＋Inno Setup Desktopインストーラー版）を追加。
  - Python Software Foundation（PSF）公式署名済み CPython 3.12.10 ARM64（`pythonarm64.3.12.10.nupkg`）およびARM64ネイティブ uv 0.13.8 を採用し、Windows 11 の Smart App Control（スマート アプリ コントロール: SAC）有効環境下で未署名バイナリのロードブロック通知を抑止・防止する構成を確立。
  - `install_uv.ps1`、`launch_uv.py`、`folimeld.uv_tool_launcher`、`folimeld.desktop_profile`、`folimeld.uv_tool_profile`、`pyproject.toml`、`Folimeld-desktop.spec`、`tools.desktop_build`、`tools.desktop_compile`、`tools.uv_tool_build` をARM64ネイティブ（PE Machine `0xAA64`、ARM64 CRT 14.52.37029.0）へ両対応化。
  - 単体テストスイートを拡充し、ARM64プロファイル受容・未署名WebPのSAC環境下スキップ安全処理を検証。

- Windows 11 x86_64向けの`uv tool install`版（Pure Python Wheel / GitHub Releases配布）を追加。`pyproject.toml`、決定論的Wheel・対応ソースZIP生成と整合検査ツール（`tools.uv_tool_build`）、パッケージ内`_resources`解決（`folimeld.resources`）、専用プロファイル（`%LOCALAPPDATA%\Folimeld-UV-Tool`）、`Local\Folimeld-UV-Tool` MutexとCPython 3.12.xマイナー一致＋固定依存14件を検証する専用ランチャー（`folimeld` / `folimeld-console`）、日英手順書と単体テストを整備し、隔離環境での`uv tool install`導入と起動を確認。

- Linux ARM64 strict Snap 0.3.4+fix1試験版を公開。固有の画像変換/保存/終了、同一候補再導入、制限状態、外側ライブラリの対応資料を確認。自動更新によるXorg中断を別記し、更新後の再試験に成功。

- Linux ARM64 DEB 0.3.4+fix1修正試験版を公開。画像変換後の終了クラッシュ修正、再ビルドのバイト一致、Ubuntu ARM64の実画面/削除再導入、210ネイティブ実体の対応ソースを検証。Debianの受入は保存済み同一DEB記録で、今回未再試験。既存配布物を保持。

- Linux向けRPMビルド（Fedora・Leap16.1・Tumbleweed・AlmaLinux9）、既存パッケージの上書き拒否、非同期サムネイル回転の表示修正、PyInstaller全文・LibTIFF LZW告知をmainへ統合。ソース版を0.3.5へ同期（既存の他OS配布物は変更せず）。
- 公開済みDEB 0.3.5をUbuntu24.04.4で追加検証し、Mozc変換、GIO、暗号化PDFの編集保存・再認証、画像取込保存を確認。Debian/Kaliの追加機能は未再試験。

- OpenBSD 8.0 / amd64向けに本体・専用MuPDF依存の署名付きパッケージ、対応ソース、ビルド工具と日英インストール手順を追加

- WindowsビルドのDLL検索パスをPython・Windows・Gitの必要な場所に限定し、無関係なツール由来のDLL混入を防止。ネイティブバイナリの収集元を検査し、想定外の場所ならビルドを停止
- Windows実行ファイルにPer-Monitor V2のDPI対応マニフェストを追加。後続の実機試験でもWACKのDPI警告が残り、原因を継続調査
- 日英のStore掲載文下書き・スクリーンショット計画・公開情報確認表と、試験用Dynabook到着後の手順・結果記録テンプレートを追加
- 対応ソース・実行ファイルのハッシュを照合した短期署名の開発用MSIX試験一式と、別PCでの導入・記録・範囲を限定した後始末スクリプトを追加
- Windows x64の暗号化依存についてチェックサム照合済みのOpenSSL・Rustソースとネイティブ依存の告知を収集し、再収集ツール・整合性テスト・調査記録を追加
- 画像変換の中間PDFを直接暗号化して書き出し、認証後にメモリから開くよう変更。認証・変換失敗時の編集中文書の保持と一時ファイルの削除を検証
- 履歴退避と保存用の一時入力をAES-256-GCMで暗号化し、鍵をファイルや設定へ保存せず、認証完了後のみPDF処理へ渡すよう変更。改ざん・短い書き込み・異常終了・保存失敗時の復旧を検証し、暗号化メタデータを含む履歴容量計算と依存ライブラリの告知を更新
- Microsoftへの移行問い合わせの回答待ちに進める作業として、実装に基づく日英のプライバシーポリシー下書きと公開前の一時データ・ログ確認項目を追加
- Microsoft Store公開方針をMSIX方式として記録し、開発/Storeビルドの分離、提出版番号とIdentityの事前検証、生成MSIXの静的検査を追加。既存EXE/MSI登録からの移行・名前の扱いと実Identityの取得は確認待ち
- 補助文書・検証記録・README用画像を `docs/` から `documentation/` へ移動し、文書リンクと配布用ソースZIPの収集処理を更新
- ドキュメントのファイル名を英語版は `ベース名.md`、日本語版は `ベース名_ja.md` に統一し、文書間のリンクと翻訳同期ルールを更新
- PDF保存時のストリーム重複検査を省き、大きな画像PDFの保存を高速化。保存中の進捗画面と別プロセスでの書き出しを追加し、失敗時の編集内容・履歴の保持と、書き出し失敗時の既存保存先の保護を検証
- メモリ上限128 MiBを超えるUndo・Redo履歴をローカルの一時ファイルへ最大1 GiB退避し、大きな文書でも履歴を利用可能に変更。文書終了・履歴分岐時に不要な一時履歴を解放
- サムネイル管理を専用クラスへ分離し、スクロール時の表示範囲探索と連続選択ページの移動を効率化
- 配布・CI用の依存バージョン制約、未使用コード検査、モデル・履歴層の型検査、容量制限付きローカルエラーログを追加
- Windowsで画像変換プロセスが結果を返さず終了した場合のパイプ切断も検知し、待ち続ける問題を修正

- ファイルメニューに「終了」を追加。画像フォルダ選択で全種類のファイル名を表示し、Windowsでは設定済みOneDriveフォルダへのショートカットを追加

- 画像フォルダを一覧表示し、名前・作成日時・更新日時の昇順／降順で新規PDFへ一括取り込み。画像の除外、ページサイズ選択、進捗表示とキャンセルに対応

- 性能計測でUndo/Redoの実行有無を記録し、画像PDF3件の各3回の計測と3 OSのCI成功を記録
- 大きなPDFではサムネイルを表示範囲と前後に限定し、画面外の画像を解放してスクロール時に再描画。通常は最大64枚を保持し、64ページ以下の文書は全ページを保持
- 保存後、編集失敗時のロールバック後、プロパティ画面を閉じた際に、差し替えられたPDFとサムネイルを再同期
- 性能計測に全体スクロールと保持サムネイル数を追加し、1,000ページPDFで改善前後を各3回比較
- PDF操作の入力検証と編集エラー表示を強化し、失敗時の履歴・保存状態の保持を検証
- 単一ページの並べ替えを1回の移動に変更し、サムネイルの連続描画を約16msで区切る
- Windows・Linux・macOS向けのテストCI、静的チェック、PDF性能計測ツール、配布前の検証手順を追加
- 保存失敗後も編集内容とUndo・Redo履歴を保持し、再保存できるよう修正。一時ファイル名の衝突と失敗時の残留を防止
- スクロールする見開きレイアウトの表紙設定について、プロパティ画面と保存内容の不整合を修正
- サムネイルを再利用し、表示範囲を優先して少数ずつ描画。回転時は対象ページのみ再描画
- Undo・Redo履歴のPDFデータに合計128 MiBの上限を設定し、古い履歴から削除

## 0.3.7 Linux / BSD amd64 試験配布（全10ターゲット） - 2026-11-22

- 確定コミット `01501d7125419007420f2adb1cd503969684dacb`（ブランチ `release/linux-bsd-amd64-0.3.7`）を基点に、Linux / BSD amd64（x86_64）全10ターゲットを Pre-release として公開し、既存 `latest`（`macos-source-v0.3.5`）および旧 0.3.5 系・ARM64 配布物を維持。全10 Release の全42アセットを未認証 HTTPS で再取得し、サイズ・SHA-256 の一致を確認。
  - **Linux DEB / strict Snap**: [`linux-deb-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.7)（Ubuntu 24.04.5 / Debian 13.7 / Kali Rolling 2026.3 の各 Test WSL2 で更新導入・offscreen 起動を確認）、[`linux-snap-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/linux-snap-amd64-v0.3.7)（Ubuntu 24.04.5 で `snap install --dangerous`・offscreen 起動を確認）。
  - **Linux RPM**: [`opensuse-tumbleweed20261110-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.7)、[`opensuse-leap161-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.7)、[`fedora44-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/fedora44-amd64-v0.3.7)、[`fedora45-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.7)、[`almalinux9-amd64-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.7)（各ディストリビューションの専用 Test WSL2 で導入・offscreen 起動を確認）。
  - **BSD**: [`freebsd-v0.3.7_1`](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.7_1)（FreeBSD 15.1 VM で `pkg add -f`・offscreen 起動を確認）、[`netbsd-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/netbsd-v0.3.7)（NetBSD 11.1 VM で `pkg_add -u`・offscreen 起動を確認）、[`openbsd-v0.3.7`](https://github.com/tyamada/Folimeld/releases/tag/openbsd-v0.3.7)（OpenBSD 8.0 VM で Signify 署名付与・`signify -V` 検証・`pkg_add -r`・offscreen 起動を確認）。

## 0.3.7.0 Windows x64 Desktop インストーラー版プレビュー / 0.3.7 ソース＋uv版プレビュー - 2026-11-22

- 確定コミット `6841276fa3de03b039076c91cf947c8198c757df`（ブランチ `release/windows-x64-0.3.7-preview.1`）を基点に、[Windows 11 x64 Desktop インストーラー版 0.3.7.0 プレビュー](https://github.com/tyamada/Folimeld/releases/tag/windows-desktop-v0.3.7.0-preview.1)（12ファイル）および [Windows 11 x64 ソース＋uv版 0.3.7 プレビュー](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-v0.3.7-preview.1)（4ファイル）を Pre-release として公開し、既存 `latest`（`macos-source-v0.3.5`）および旧 0.3.5 系配布物を維持。公開先から未認証 HTTPS で全16ファイルを再取得し、サイズ・SHA-256の一致を確認。
- 0.3.5 以降に追加された「PDFを閉じる」操作・未読込時案内、および「ファイル → サンプルPDFを開く…」からのサンプルPDFマンガ1冊ずつのオンライン取得・SHA-256検証・作業コピー展開機能を両配布経路へ反映。
- Desktop インストーラー版 0.3.7.0 では、`Local\Folimeld-Desktop` Mutex 保持中の導入拒否（終了コード 1）、通常権限新規導入と全201ファイルの `payload-review.json` との SHA-256 一致、同一版上書き拒否（終了コード 7）、凍結 `FolimeldDesktop.exe` の起動・重複起動拒否（終了コード 1）・正常終了（終了コード 0）、`unins000.exe` による削除と設定データ保持を確認。
- ソース＋uv版 0.3.7 では、ZIP の SHA-256 照合・新規専用フォルダー展開、`install_uv.ps1` による固定環境（CPython 3.12.16・uv 0.13.8・依存14件）の導入・`uv pip check`・ショートカット生成、オンラインサンプルカタログ取得・日本語マンガ1冊のダウンロード／SHA-256検証・PDF保存再読込、`launch_uv.py` での GUI 起動とログ出力を確認。
- 3ワーカー実機 PID 観測、旧版（0.3.5 / 0.3.5.0）からの更新・復帰、本番 Store 版との併存、複数倍率・複数モニター移動、ARM64 は未確認。Store 版 1.0.1.0 への更新ではない。

## 0.3.7 preview.1 Windows x64 uv tool install 版プレビュー - 2026-11-21

- [Windows 11 x64 uv tool install版0.3.7 preview.1](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.7-preview.1)をPre-releaseとして公開し、Latestと既存の0.3.5／0.3.6配布物を維持。Wheel、対応ソース、台帳、依存ロック、告知など全10ファイルを公開先から再取得し、サイズ・SHA-256の一致を確認。
- ファイルメニューまたはPDF未読込時の案内の「サンプルPDFを開く…」から、サンプルPDFマンガを1冊ずつ取得する機能を追加。言語フィルター（初期値はアプリ／システム言語）、最新話から（既定）／1話からの表示順、著作権・CC BY 4.0表示に対応。取得したPDFのSHA-256を検証し、別の編集用コピーを開く。PDF本体は同梱せず、初回取得には通信が必要。検証済み原本はオフラインでも再利用できる。
- 新規の隔離uv tool環境への導入、GUI起動、オンライン一覧、日本語マンガ1冊の取得・検証、8ページ表示・別名保存・再読込・終了を確認。今回の候補での3ワーカー実機PID観測、更新／旧版復帰、Store併存、複数倍率、ARM64は未確認。
- 通常利用にはMicrosoft Store版を引き続き推奨。Store版1.0.1.0にはこの取得機能は含まれず、今回の公開はStore版の更新ではない。ARM64のuv tool install版は既存0.3.5の案内を維持。

## 0.3.5.0 Windows x64 Desktop インストーラー版プレビュー - 2026-11-16

- Windows 11 x64向けの[Desktopインストーラー版プレビュー](https://github.com/tyamada/Folimeld/releases/tag/windows-desktop-v0.3.5.0-preview.1)（PyInstaller onedir + Inno Setup 7.1.1）をPre-releaseとして公開（既存latestは保持）。Setup EXE・対応ソースZIP・ペイロード台帳・内部ソース台帳・コミット対応記録・第三者告知・依存ソース台帳・CRT利用者告知（日英）・SHA-256一覧の計12ファイルを配布し、公開後の全12添付の再取得とサイズ・SHA-256一致を確認。
- Microsoft Runtime（14.44.35211.0）に限定した同意ページと原文RTFハッシュガード、不要Qtモジュール除外と正規CRT 7件統一、`Local\Folimeld-Desktop` Mutex保護、`%LOCALAPPDATA%\Folimeld-Desktop` 設定・ログ分離を検証。実機でのMutex保持中インストール拒否、通常権限インストール後の全201ファイルSHA-256一致、同一版上書き拒否、凍結`FolimeldDesktop.exe`でのPDF起動・Per-Monitor V2 DPI・重複起動拒否・正常終了、`unins000.exe`による削除と設定保持を確認。

## 0.3.5 Windows x64 uv tool install 版プレビュー - 2026-11-16

- Windows 11 x86_64向けの[uv tool install版プレビュー](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-tool-v0.3.5-preview.1)（Pure Python Wheel / GitHub Releases配布）をPre-releaseとして公開（既存latestは保持）。Wheel・固定依存ロック・ランタイム定義・対応ソースZIP・内部台帳・コミット対応記録・第三者告知・依存ソース台帳・SHA-256一覧の計10ファイルを配布し、公開後の全10添付の再取得とサイズ・SHA-256一致を確認。
- `pyproject.toml`、決定論的Wheel・対応ソースZIP生成と整合検査ツール（`tools.uv_tool_build`）、パッケージ内`_resources`解決（`folimeld.resources`）、専用プロファイル（`%LOCALAPPDATA%\Folimeld-UV-Tool`）、`Local\Folimeld-UV-Tool` MutexとCPython 3.12.xマイナー一致＋固定依存14件を検証する専用ランチャー（`folimeld` / `folimeld-console`）を実装。隔離環境での`uv tool install`導入、実画面GUIでのPDF編集・画像変換・3ワーカー・Per-Monitor V2 DPI・再起動後の設定保持・Mutex二重起動拒否・他エディションおよびレジストリ非干渉を確認。

## 0.3.5 Windows x64 uv版プレビュー - 2026-11-15

- Windows 11 x64向けの[ソース＋uv版プレビュー](https://github.com/tyamada/Folimeld/releases/tag/windows-uv-v0.3.5-preview.1)をPre-releaseとして公開。ソースZIP・内部台帳・コミットとの対応記録・SHA-256一覧を配布。Microsoft Store配布は引き続き標準のWindows配布経路として維持。
- CPython 3.12.16・uv 0.13.8・依存14件を固定し、設定・ログを専用保存先へ分離。公開候補ZIPからの新規導入、正規起動、PDF表示・別名保存・再読込、画像変換・保存、3ワーカーの起動終了、再起動後の設定保持を確認。公開先から取得した4ファイルのサイズ・SHA-256が一致。
- 本番Store版との併存、異なる版への更新・旧版復帰、複数倍率・モニター移動、既知クラッシュへの修正効果は未確認。

## 0.3.5 Kali ARM64試験版 - 2026-11-14

- [Kali2026.3 ARM64 DEB0.3.5](https://github.com/tyamada/Folimeld/releases/tag/kali-arm64-v0.3.5)を公開。新規ARM64環境でPDF編集/画像変換/保存、完全削除再導入と文書/設定保持、最小依存起動を確認。一般ユーザーXorg/IceWM、GUI3回終了0。
- 410tests/69subtests成功、9skip、ruff成功。1011入力・173AArch64実体・30対応ソース、全16公開後添付再取得を照合。CFFIは公式ソースと動的Kali libffiで構築し公式219tests成功。ELF/DEBとも2出力先一致。未署名GitHub試験版、glibc>=2.43。他版/current rolling/実機/完全なデスクトップ/Wayland/IME/旧版更新未検証。既存公開物/latestを保持。

## 0.3.5 openSUSE Tumbleweed ARM64試験版 - 2026-11-14

- [Tumbleweed20261111 ARM64 RPM0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed-arm64-v0.3.5)を公開。一般ユーザーXorg/IceWM、SELinux EnforcingでGUI3回終了0、PDF編集/画像変換/保存、完全削除再導入と文書/設定保持、最小依存起動を確認。
- 410tests/69subtests成功、9skip、ruff成功、別出力先ELF一致。1001入力・201AArch64実体・32signed SRPM・全16公開後添付再取得を照合。未署名GitHub試験版、glibc>=2.44。別スナップショット/実機/Wayland/IME/旧版更新は未検証。最小デスクトップのCJK文字表示には追加フォントが必要。既存公開物/latestを保持。

## 0.3.5 openSUSE Leap 16.1 ARM64試験版 - 2026-11-13

- [Leap16.1 ARM64 RPM 0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-arm64-v0.3.5)を公開。ARM64固有の新規導入、PDF編集/画像変換/保存、完全削除再導入と文書・設定保持、最小依存起動を確認。SELinux Enforcing、GUI3回終了0。
- 410 passed/9 skipped/69 subtests、別出力先ELF一致、999入力、202AArch64実体（公式wheel105/署名付きOS内容95/修正版Brotliソースビルド2）、対応32SRPM、全16添付の公開後再取得を照合。未署名GitHub試験版、glibc>=2.40。実機/Wayland/IME/旧版更新等は未検証。既存公開物/latestを保持。

## 0.3.5 AlmaLinux 9 ARM64試験版 - 2026-11-13

- [AlmaLinux9.8 ARM64 RPM0.3.5-2](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-arm64-v0.3.5)を公開。glibc2.34上でQt/PySide6.11.2を必要モジュールに限定してソースビルド。Qt標準翻訳カタログは含まず、アプリ独自翻訳は同梱。revision2で最小環境のOpenGL依存不足を修正。
- ARM64実行VMで編集保存・画像PDF・完全削除再導入と文書/設定保持・GUI3回正常終了、最小依存起動を検証。410 passed/9 skipped/69 subtests、994入力・163実体・39署名付きSRPM・全16公開添付の再取得を照合。同じQt SDKの2ビルド先でELF一致、RPM時刻は異なる。未署名試験配布、受入は9.8のみ。実機/Wayland/IME/旧版更新等は未検証。既存公開物/latest保持。

## 0.3.5 Fedora 45 ARM64試験版 - 2026-11-13

- [Fedora45 ARM64 RPM 0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/fedora45-arm64-v0.3.5)を公開。ARM64固有の新規導入・編集保存・画像PDF・完全削除再導入と文書/設定保持、最小依存構成起動を確認。SELinux Enforcingを維持し、GUI3回正常終了。
- Fedora ARM64テスト409 passed/9 skipped/67 subtests、同一VMの別ビルド先でELF一致、981入力と200 AArch64実体の対応、34署名付きSRPM、全16添付の公開後再取得を照合。RPMヘッダー時刻は異なる。未署名GitHub試験配布で、実機/Wayland/IME/旧版更新等は未検証。既存公開物とlatestを保持。

## 0.3.5 Fedora 44 ARM64試験版 - 2026-11-13

- [Fedora44 ARM64 RPM 0.3.5-1](https://github.com/tyamada/Folimeld/releases/tag/fedora44-arm64-v0.3.5)を公開。ARM64固有の新規導入・編集保存・画像PDF・完全削除再導入と文書/設定保持、最小依存構成起動を確認。SELinux Enforcingを維持し、GUI3回正常終了。
- Fedora ARM64テスト409 passed/9 skipped/67 subtests、同一VMの別ビルド先でELF一致、974入力と200 AArch64実体の対応、34署名付きSRPM、全16添付の公開後再取得を照合。RPMヘッダー時刻は異なる。未署名GitHub試験配布で、実機/Wayland/IME/旧版更新等は未検証。既存公開物とlatestを保持。

## 0.3.5 Linux strict Snap ARM64試験版 - 2026-11-13

- [Ubuntu24.04向けARM64 strict Snap 0.3.5](https://github.com/tyamada/Folimeld/releases/tag/linux-snap-arm64-v0.3.5)を公開。Snap固有の編集・画像変換・保存・正常終了、旧版更新・同一候補再導入と文書/設定保持を今回確認。AppArmor enforce・Seccomp2と限定的な許可/拒否試験を記録。
- ARM64テスト409 passed/9 skipped、同一VM内の別ビルド先でSnap一致、968入力/内部210・外側11実体の対応資料、全16添付の公開後再取得照合を確認。完全削除再導入・IME/Wayland/実機等は未検証。Store署名のないGitHub配布として、既存公開物とlatestを保持。

## 0.3.5 Linux DEB ARM64試験版 - 2026-11-13

- [Ubuntu24.04／Debian13向けARM64 DEB 0.3.5](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-arm64-v0.3.5)を公開。両OSで主要PDF編集・画像変換・正常終了・削除再導入と文書/設定保持を今回検証し、保存PDFの順序/回転/画素を照合。
- ARM64テスト409 passed/9 skipped、最小Ubuntu起動、同一VM内の別ビルド先でDEB一致、961入力/210 AArch64実体の対応資料、全16添付の公開後再ダウンロード照合を記録。IME/Wayland/実機/暗号化・フォームGUIは今回未再試験。既存公開物とlatestを保持。

## 0.3.5 Linux DEB amd64試験版 - 2026-11-13

- Ubuntu 24.04.4・Debian 13.6・Kali Rolling 2026.3の専用WSL2/WSLgで更新・削除再導入・起動と日本語PDF回転/Undoを確認した[amd64 DEB試験版](https://github.com/tyamada/Folimeld/releases/tag/linux-deb-amd64-v0.3.5)を公開。Ubuntuでは追加の編集・保存再読込・最小chroot起動も確認。
- ソース870入力、実ネイティブ214項目、Ubuntu対応ソース61件、署名付きSourcesインデックス53件、公開12添付を照合。IME/GIO/暗号化PDF/画像GUIの未再試験を明記し、既存0.3.4・ARM64・Snapとlatestを保持。

## 0.3.5 openSUSE Tumbleweed 20261110 amd64試験版 - 2026-11-13

- 専用WSL2/WSLgで検証した0.3.5-1.tw20261110のamd64 RPMを[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-tumbleweed20261110-amd64-v0.3.5)で公開。主要GUI・日本語名保存/GIO・Mozc入力・暗号化PDF・画像PDF、更新・削除再導入・新規最小installroot起動を確認。
- 864入力を専用ソースコミットへ固定し、実配布206実体、署名検証済み35 SRPMと11添付を照合。最小rootは通常のローリングリポジトリを用いたchrootで、独立した20261110環境のブートではない。他スナップショット・通常デスクトップ・ARM64・公開0.3.4からの移行等は未検証。既存Releaseとlatestを保持。

## 0.3.5 openSUSE Leap 16.1 amd64試験版 - 2026-11-13

- 専用WSL2/WSLgで検証したamd64 RPM（0.3.5-1）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/opensuse-leap161-amd64-v0.3.5)で試験公開。PDF編集・日本語名保存/GIO再読込・暗号化PDF・画像PDF・Mozc日本語入力、更新・削除再導入・新規最小installroot起動を確認。
- 対応ソース858入力を専用コミットへ固定。実配布209ネイティブ実体、署名検証済み36 SRPMと11添付を照合。通常デスクトップ・ARM64・Tumbleweed・公開Ubuntu/Debian 0.3.4からの移行は対象外。合成入力での失敗と再試験・来歴上の制約を明記し、既存配布物とlatestを保持。

## 0.3.5 Fedora 44 amd64試験版 - 2026-11-13

- Fedora 44専用WSL2/WSLgで検証したamd64 RPM（0.3.5-2）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/fedora44-amd64-v0.3.5)で試験公開。PDF編集・日本語名保存再読込・暗号化PDF・画像PDF・日本語入力・GIO、更新・削除再導入・新規最小installroot起動を確認。
- 対応ソース822入力、実配布207ネイティブ実体、署名検証済み37 SRPMと11添付を照合。通常デスクトップ・ARM64・公開Ubuntu/Debian 0.3.4からの移行等は未検証。既存配布物とlatestを保持。

## 0.3.5 Fedora 45 amd64試験版 - 2026-11-13

- Fedora 45のWSL2／WSLgで検証したamd64 RPM（0.3.5-2）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/fedora45-amd64-v0.3.5)で試験公開（日本時間）。
- PDF編集・日本語名保存と再読込・暗号化PDF・画像PDF・日本語入力・GIO、更新・削除再導入・新規最小依存installrootでのoffscreen起動を確認。通常デスクトップ・Fedora 44・ARM64・公開Ubuntu／Debian 0.3.4からの移行は未検証。
- 対応ソース785入力を専用コミットへ固定し、依存ソース別添・第三者告知・検証記録・制限事項・SHA-256チェックサムを含む11件を添付。RPMとチェックサムは未署名。既存配布物とlatestは保持。

## 0.3.5 AlmaLinux 9 amd64試験版 - 2026-11-12

- AlmaLinux 9.8のWSL2／WSLgで検証したamd64 RPM（0.3.5-5）を[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/almalinux9-amd64-v0.3.5)で試験公開。
- PDF編集・日本語名での別名保存と再読込・日本語入力、候補間の更新・削除再導入・最小依存起動を確認。通常デスクトップ・ARM64・AlmaLinux 10・公開Ubuntu／Debian 0.3.4からの移行は未検証。
- サムネイル描画修正とPyInstaller・LibTIFF LZW・ICU・Qt/MuPDFの補足告知を反映。対応ソース、依存ソース資料、検証記録、既知の制約とSHA-256チェックサムを添付。既存Ubuntu／Debian 0.3.4や他OSの配布物は保持。

## 0.3.4 - 2026-11-10

- 2026年11月10日、Folimeld 0.3.4のLinux版を公開しました。
- Ubuntu 24.04・Debian 13向けにamd64／ARM64のDEB、Ubuntu 24.04向けにamd64／ARM64のSnapを公開しました。
- 対応ソースとSHA-256チェックサムは[Linux版0.3.4のGitHub Release](https://github.com/tyamada/Folimeld/releases/tag/linux-v0.3.4)で確認できます。

## 0.3.3_1 FreeBSD ARM64版の試験公開 - 2026-11-10

- FreeBSD 15.1 ARM64（aarch64）向けにFolimeld 0.3.3のパッケージ改訂1を試験公開しました。
- MacBook Air M5上のQEMU（HVF）で、Xorgデスクトップ環境での導入と動作を確認しました。
- パッケージ、対応ソース、導入手順は[FreeBSD ARM64版のGitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-aarch64-v0.3.3_1)で確認できます。

## 1.0.1.0 - 2026-11-09

- 2026年11月9日、Folimeld 1.0.1.0（Windows 11 x64）を日本と米国のMicrosoft Storeで無料公開しました。 [日本のMicrosoft Store](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=ja-JP&gl=JP) · [米国のMicrosoft Store](https://apps.microsoft.com/detail/9P5X2JFZRJC3?hl=en-US&gl=US)

## 0.3.3 - 2026-09-09

- 配布用debをUbuntu 22.04でビルドし、Ubuntu 22.04以降に対応。X11依存ライブラリの指定も補完
- ライセンス全文と第三者の告知をバージョン情報から専用画面へ移動し、ヘルプメニューに「ライセンス」を追加
- ARM64環境でWindows EXE / MSIX、Linux deb / Snapのビルドを検証
- Linux用スクリプトの改行、Snapの出力先、Debian最小構成でのフォント設定依存を修正
- ビルド時のソース保存と配布物の対応記録を追加し、ソースZIP名の記録を修正

## 0.3.2 - 2026-09-07

- 通常起動時、WinRTなどのパッケージ情報がなくてもバージョン情報を表示できるよう修正
- バージョン情報に著作権、ライセンス全文、第三者の告知、ソースコードへのリンクを追加
- 各OSのビルドにライセンス文書と依存パッケージの告知を同梱

## 0.3.1 - 2026-09-06

- 表紙のチェック状態に応じてページ表示の説明とレイアウト変更案内を即時更新
- 文書のプロパティの詳細に「ページを表示」を追加し、選択中のページレイアウトの説明をリアルタイムに表示
- ページ表示の説明を上端揃えに変更し、表紙選択時の翻訳エラーを修正

## 0.3.0 - 2026-09-04

- プロジェクトのライセンスをGNU Affero General Public License v3.0へ変更
- アプリのバージョンを一元管理し、各配布形式のメタデータへ自動反映
- Folimeldの新しいアプリアイコンと、各OS・Microsoft Store向け画像を追加
- PDFファイルの関連付けをMSIXマニフェストへ移行
- Microsoft Store向けx64 MSIXのビルドに対応
- ARM64 MSIXのビルド手順と、アーキテクチャ誤指定の検出を追加
- READMEをGitHub公開向けに再構成し、開発手順と変更履歴を別文書へ分離

## 0.2.5 - 2026-09-03

- スクロール動作を改善

## 0.2.4 - 2026-08-31

- Ubuntuに対応

## 0.2.3 - 2026-08-31

- PDFバージョンの自動変更に対応

## 0.2.2 - 2026-08-30

- macOS向けビルド手順、アイコン、署名を整備

## 0.2.1 - 2026-08-30

- macOS上でWindows依存処理を安全に無効化

## 0.2.0 - 2026-08-30

- アプリ名をFolimeldへ変更

## 0.1.0 - 2026-08-29

- 最初のリリース
