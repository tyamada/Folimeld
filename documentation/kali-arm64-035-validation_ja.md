# Kali ARM64 DEB0.3.5 公開前検証

対象はKali2026.3（標準kali-last-snapshot）aarch64の `folimeld_0.3.5_arm64.deb`。正確な本体ソース `7963998a6d4f7a2eebf4b40d5dae2246452efea7`（差分なし）、DEB SHA256 `75856ef173d4fd2c1933cdf9d8fcf1665195da00d4ee733d5d2c8e306aae3558`、ELF SHA256 `58bd3089af891e3bd9e1bc6c3645182e9749c870716e09e815143b1c9900747c`、対応ZIP SHA256 `fc82d6f1f0482ef84521439d38a04effb55d3ae5d871c38788c021fc80450241`。1011入力をGit/ZIP/埋込記録で照合。タグにはビルド後の本検証資料を含む。

公式Cloud2026.3 ARM64イメージは公式ページとHTTPSチェックサムにSHA256一致。該当Cloud配布一覧に別署名はなく、イメージPGP署名検証済みとは扱わない。週次版本体は401のため使用しなかった。Kali2026.3/Python3.14.7/glibc2.43、標準kali-last-snapshotを保持。ビルドkernel7.1.5+kali-cloud-arm64、GUI用にはGPUドライバーのある公式7.1.5+kali-arm64を追加し、Cloudカーネルも保持。インターフェイス名変更に専用VMのDHCP設定を対応させた。VMと大容量書込作業は専用SSD、静的な公開添付と再取得はUUID確認済み作業用HDD。重要更新はNASにも照合保管し、既存データ・公開物・Time Machine履歴を保持する。

410tests/69subtests成功、9skip、ruff成功。同じ固定CFFI wheelを使い同一VMの独立した2出力先でELF・DEBともバイト一致。独立ホストや全依存wheelの再現性は対象外。最小Kali rootで推奨なし・UID1000で15秒起動継続（timeout124は生存確認だけ）。

一般ユーザーUID1000/GID1000、Xorg21.1.24/IceWMで新規導入、回転/サムネイル更新、Undo/Redo、移動、白紙挿入/削除、別名保存、日本語パス再読込、画像2件のPDF変換/保存、purgeと同一候補再導入、文書/設定ハッシュ保持、保存画像PDF再表示を確認。GUI3回終了0、残存プロセスなし。新規Kali専用素材で順序2→1→3/回転0→90→0と復号画像画素、元素材不変を独立確認。日本語パスはシェルで作成したコピー。Qtファイルダイアログの日本語名表示と読込は成功するが、IceWMタイトルバーの日本語文字は欠ける。IME合格ではない。AppArmorモジュールは有効だが元環境にポリシーがなく、Folimeld専用制限はない。無効化操作はしていない。Cloudのローカルroot自動ログインは元イメージの設定で、アプリ試験は一般ユーザー。

173AArch64実体を公式wheel104/Kali DEB内容68/自前CFFI1へ照合。44binary DEBと30exact source package、146構成ファイルをPackages/Sourcesのサイズ・SHA256に照合し、索引の展開後ハッシュをKali署名付きInRelease（827C8569F2518CC677FECA1AED65462EC8D5E4C5）で検証。コピー索引はローカル再圧縮で、DSC個別署名を別途信頼したとはしない。公式PyInstaller起動部の元セクション一致。不足告知はKali copyrightと参照ライセンスで補足。

元CFFI wheelの静的libffi版を根拠付きで特定できないため、同梱用だけ公式CFFI2.1.1変更なしソースから構築し、正確なKali libffi3.8.0-2へ動的リンク。libffi-dev入力も公式DEBに照合。公式バックエンド219tests成功、8skip。例外/longオーバーフローを意図する試験の2warningsを保持。元wheel・先行候補・OSライブラリは保持。現行cp314 Pillowの部品名/版/ソースハッシュ/告知を先行ソース補足と新規比較した。共通0.3.4上流ソースTAR/Pillow補足と今回のKaliソース補足・告知・出所JSONを併用する。歴史的x64資料は現在の根拠にしない。その他wheelの独立再ビルドは未実施。

GitHubの未署名DEB試験版、glibc>=2.43。Kali公式パッケージではない。他Kali版/現在のrolling/他ディストリ/実機ARM/完全なXFCE・GNOME・KDE・Wayland/IME/暗号化・フォームGUI/関連付け/旧版更新・rollbackは今回未検証。amd64や他OSの合格は流用しない。詳細は添付BUILD/KNOWN-LIMITATIONS/検証記録へ。全添付の公開後再取得・main反映・X案内完了まで次の公開へ進まない。

公開完了: 全16添付を公開後に再取得し、サイズ/SHA256一致、既存公開添付とlatest保持を確認。main反映後にX案内を行う。
