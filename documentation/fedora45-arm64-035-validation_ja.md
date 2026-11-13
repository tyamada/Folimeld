# Fedora 45 ARM64 RPM 0.3.5 検証記録

[Release](https://github.com/tyamada/Folimeld/releases/tag/fedora45-arm64-v0.3.5)

本体ソース0b2ee3e6e300510f53f78ab9bffd42a20b0f9aee（差分なし）。981入力をGit、ZIP、埋込記録で照合。RPM SHA256 38cb2f2b9e1ab76c50616d12fe35bd581bdc1740abaf66c267df70664a98b0ff、ELF SHA256 cb60897edc0592c4c1b3bc30db87539f6dafa7b7c4c3431149027709616962a6。タグは本体ビルド後のこの検証記録を含む。

Mac内蔵の別ビルド先2件でELF一致。RPMはヘッダー時刻が異なるため一致を主張しない。Fedora45 ARM64/Python3.14で409 passed、9 skipped、67 subtests、ruff成功。独立した実行VMはFedora45 ARM64、カーネル7.3.3-300、UID1000、Xorg/Openbox、SELinux Enforcing。新規導入、回転・Undo/Redo・移動・白紙挿入削除・別名保存・日本語名再読込・画像作成保存・終了を確認。完全削除と同一候補再導入で文書/設定ハッシュ保持、保存画像PDF再表示も成功。GUI3回終了0、後刻のプロセス残存なし。保存順2/1/3・回転0/90/0と元PNG画素を検査。最小依存構成はUID1000 offscreenで15秒継続しtimeout124（通常終了0とは別）。

同梱200 AArch64 ELFの公式wheel105/署名付きFedora RPM内容95を照合。38 binary RPM→34 exact signed SRPM、2件の不足告知を該当SRPMから補足。PyInstaller起動部の元セクションも公式wheelと一致。共通0.3.4ソースTAR/Pillow補足は依存版が共通で、今回のcp314 Pillow部品名・版・ソースハッシュと告知を照合。Fedora依存は今回のSRPM補足で対応し、古いUbuntu/amd64資料は流用しない。

GitHubの未署名RPM試験配布でFedora公式パッケージではない。glibc>=2.44。SELinuxは維持するが通常ユーザードメインでSnap型のアプリ制限はない。実機ARM、GNOME/Wayland、IME、暗号化/フォームGUI、関連付け、旧版からの更新/rollbackは未検証。日本語名コピーはシェルで作成し再読込したもの。合成入力のUbuntu/Debian表記は素材由来で合格結果の流用ではない。

Releaseの16添付はサイズ・SHA256一覧に固定。公開後の全添付再ダウンロード結果とX URLはmainに別途記録する。VM/ISOは内蔵に保持し、外付け起動や削除は行わない。既存公開物とlatestを保持。

Fedora45の標準Python3.15は固定PySide6 6.11.2の対応範囲外のため、公式python3.14（3.14.10）をビルド専用に利用。Requires-Pythonを無視しない。最小実行ルートにはPython/GCCなし。初期install/minrootスクリプトの完了マーカー文字列は44が残っていたが、OS・RPM・releaseverは45で実行し、別のplatform記録で明示確認。元ログは改変せず保持した。

共通運用ルール（/Users/tyamada22/.codex/AGENTS.md、2026-11-13追加）を確認。公式大容量イメージは削除していない。将来許可された削除を行う場合もHD-LS2.0TU2DまたはNAS「Codexバックアップ」の実体と容量を確認し、先にコピー・サイズ/SHA256照合と保管記録を作る。作業VM・ユーザーデータを再取得可能な配布イメージと同一視しない。

公開後に全16添付を再ダウンロードし、全サイズ/SHA256一致を確認。既存全公開Releaseの添付id/name/size/digestを保持し、latestはlinux-v0.3.4のまま。[公開後照合記録](fedora45-arm64-035-publication.json)。内蔵VM2台は通常停止しディスク一式を保持。X案内URLは別コミットで追加する。

X（@tyamada22）への案内を投稿し、公開本文・Releaseリンクを確認: [https://x.com/tyamada22/status/2121100298987221327](https://x.com/tyamada22/status/2121100298987221327)。公開・全添付照合・main反映後に投稿し、次パッケージの公開は開始していない。
