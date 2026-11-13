# openSUSE Tumbleweed ARM64 RPM 0.3.5 公開前検証

対象はTumbleweed snapshot20261111 aarch64向け `folimeld-0.3.5-1.tw20261111.aarch64.rpm`。本体ソース `c8fb78a083e0392f955bf73f75be280d2c63d4f1`（差分なし）、RPM SHA256 `f4273f98aca2252419b2a8cd9a3ea2e9e5c79a9c846e4c718f38727769397c6a`、実行ファイル SHA256 `6daf7c690085eff008ed168ed9bcbca6ff39f5d9b1ae7a2d75a8683400656031`、対応ソースZIP SHA256 `6a8d14476a7c1cd11b2c7175346076b0705f085cb2e936d8217f55db191992eb`。1001入力をGit/ZIP/埋込記録で照合。タグにはビルド後の本検証資料を含む。

公式ARM64 Cloud Snapshot20261111のSHA256とopenSUSE署名を検証。kernel7.3.3-1-default、glibc2.44、実際のPythonは3.13.16（3.14.8も併設したが未使用）。QEMU/HVF、専用外付けAPFS SSD上の新規ビルド/受入VM。今回のユーザー指示でVM実行先を新SSDへ変更し、内蔵100GB待ちを解除。大容量データはSSDへ置き、既存データ・Time Machine履歴を保持。過去の内蔵限定記録は当時の履歴として保持する。

410tests/69subtests成功、9skips、ruff成功。同一VMの独立した2出力先でELFバイト一致。RPMヘッダー時刻や独立ホスト再現性は対象外。最小依存root（recommendsなし）のUID1000で15秒起動継続、timeout124は生存確認のみ。

新規導入、回転/サムネイル更新、Undo/Redo、移動、白紙挿入/削除、別名保存、日本語パス再読込、画像2件のPDF変換/保存、完全削除と同一候補再導入、文書/設定ハッシュ保持、保存画像PDF再表示を確認。一般ユーザーUID1000/GID1001、Xorg21.1.25/IceWM、SELinux Enforcing（通常のunconfinedドメイン）。GUI3回すべて終了0、残存プロセスなし。保存PDF順序2→1→3・回転0→90→0と画像の復号画素を独立照合。今回専用の合成素材を使用。日本語パスはシェルで作成したコピー。最小デスクトップにCJKフォントがなく、タイトルの日本語文字表示は欠けるが、パスの読込と内容を照合済み。IME合格ではない。

同梱201AArch64実体の内訳は公式wheel105・署名付きopenSUSE RPM内容96。48binary RPMの内容と32exact signed SRPMを照合し、不足告知は対応ソースから補足。公式PyInstaller起動部の元セクション一致。全14wheelが先行検証済みARM64入力とSHA256一致するため、共通0.3.4依存ソースTAR/Pillow補足を現在のTumbleweedソース補足・告知・出所JSONと組み合わせる。余剰の過去OS資料は今回の対応表や合格に数えない。wheelの独立再ビルドは未実施。

GitHubの未署名試験版、glibc>=2.44、openSUSE公式パッケージではない。別スナップショット・Leap/SLE・実機ARM・完全なGNOME/KDE/Wayland・IME・暗号化/フォームGUI・ファイル関連付け・旧版更新は今回未検証。通常ユーザードメインでSnap同様のアプリ単位制限はない。詳細は添付BUILD/KNOWN-LIMITATIONS/検証資料。amd64や他OSの合格は流用しない。全添付の公開後再取得照合・main反映・X案内完了まで次の公開へ進まない。
