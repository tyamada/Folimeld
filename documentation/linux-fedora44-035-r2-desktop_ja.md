# Fedora 44 revision2のデスクトップ連携・導入回帰

2026-11-13。許可済み専用Fedora44 Testの0.3.5 revision2で確認した。実行ELFのSHA-256は `c5fea766f7f508255a1c1bfdd68e1e59230d448b564f818d7a4150f0876da7f8`。Fedora44版は未公開。既存の作業変更・旧候補・配布物・素材は保持した。

## GIO・ライセンス・IME

新規XDG設定と独立D-Busを用意し、日本語・空白を含む `日本語 パス/関連付け 試験.pdf` をGIOで開いた。終了コード0、アプリのタイトルと3ページ表示を確認した。MIME関連付けは今回の専用XDG設定だけに限定した。元PDFと今回のコピーはSHA-256不変。

ライセンス画面ではFolimeld、ICU-73.2、LibTIFF-LZW、Fedora44 OS、MuPDFソース告知、Qt追加ライセンス、Qtソース告知の各タブを実際に表示した。大きなQt告知も描画された。告知の表示確認と、全ライセンス条件への適合認定は区別する。

IMEは別の新規XDG/D-Busプロフィールを使い、IBus/Mozcを接続した。設定コマンドは終了値1を返したが、現在のエンジン照会は終了値0・`mozc-jp` だった。実際にQtファイル名欄を日本語入力モードへ切り替え、`nihongo` → `にほんご` → `日本語` の変換・確定を確認した。試験後はキャンセルし、ファイルを開いたり保存したりしていない。

完了後は今回の専用プロファイル環境変数とUIDを照合して試験プロセスを終了した。[デスクトップ連携JSON](linux-fedora44-035-r2-desktop-2026-11-13.json)にログ・入力と画面のハッシュを保存した。[GIO表示](linux-fedora44-035-r2-desktop/01-gio-loaded.png)、[Fedora44 OS告知](linux-fedora44-035-r2-desktop/05-os.png)、[IME確定](linux-fedora44-035-r2-desktop/11-ime-committed.png)も参照。

## 削除・再導入

既存の専用GUI試験環境で、`rpm -V`・`dnf check` の成功後、依存の自動削除を抑止してFolimeldだけを削除した。実行ファイル・desktop entry・アイコン・LICENSEの4ファイルとRPM登録の消失を確認し、同一RPMを再導入した。

4ファイルは削除前と同じハッシュで復元し、前回のPDF回帰プロフィール内のPDF・設定6件は削除前後・再導入後とも不変だった。再導入後の整合性検査と、新規一般ユーザープロファイルでのoffscreen/xcb各12秒起動も成功し、試験後に停止した。[ライフサイクルJSON](linux-fedora44-035-r2-lifecycle-2026-11-13.json)を参照。

## 新規最小依存installroot

専用Test内の新規 `/root/folimeld-verification/version035-r2-minroot-20261113/root` に、標準fedora/updatesリポジトリ、Fedora44の署名鍵、weak dependencies無効で導入した。DNF5の `--installroot`・`--use-host-config`・`--releasever=44` を用い、既存rootや信頼鍵・repo設定は変更していない。

Python・GCC・rpm-build・追加CJKフォントがないことを全パッケージ一覧で確認した。UID/GID1000のoffscreenで12秒起動し、試験のため停止。ELFハッシュ一致、`rpm -V`・`dnf check` も成功した。デバイスノードとユーザーディレクトリは新規root内に限定し、マウントや新規WSL登録はしていない。[最小依存JSON](linux-fedora44-035-r2-minroot-2026-11-13.json)に全パッケージ・導入ログ・起動環境を保存した。

## 範囲と残作業

GUI/IMEはWSLg X11と既存の試験ツール入り環境、最小依存はchroot/offscreenの試験。通常デスクトップ・ファイルマネージャーのダブルクリック・独立WSLブート・最小環境の日本語GUI/IME・ARM64は未検証。既存のWSL設定、systemdユーザーセッション、portal、PyMuPDFの非推奨警告は保持した。

公式wheelとの実体照合、Fedora44 OSの正確な対応SRPMと署名検証、最終配布資料の統合・照合、公開用Gitスナップショットと案内は残る。Fedora45やAlmaの成功をFedora44の検証として代用しない。公開・タグ・pushは実施していない。
