# Linux ARM64 strict Snap 0.3.4+fix1 公開前確認

2026-11-13 JST。DEBの公開・全16添付の公開後再ダウンロード照合完了後に次順位のSnapを公開する。DEBのX案内も投稿・表示確認済み。

105000960 bytes、SHA-256 b1df00de5554b65757ab643a08ad191dd04532fb96d4d548ff9e9d8b15844b53。保存入力から今回再ビルドしたSnapは独立2VMの過去候補とバイト一致。DEBと同一のAArch64 ELF、同一の対応ソースZIP f7f69ff38f55294d5cc682a98d319a5e92a8fc1f1a0f951905c60d0f49dad522を使用する。

Snap全ファイルを公開ARM64 0.3.4と比較し、変更はbin/folimeldとmeta/snap.yamlだけ。外側11ネイティブ実体の22パス（symlink含む）は同一SHA-256。内部210ネイティブ実体はDEBと同じ照合済みソース、外側は既存Snapの正確な対応資料を引き継ぐ。AppArmor enforce、Seccomp2/2フィルターを実行中に確認。外部content/base snapは同梱ファイルと区別し、snap connectionsを保存した。

一般ユーザーXorg/HVF上で画像2件から2ページPDFを生成・保存・終了0。x5からx6への同一候補の再導入でDocuments/common/current設定のハッシュ保持を確認し、保存PDFを再読込した。次の再変換中、apt-daily-upgradeによりsystemd/Xorgを含むサービスが再起動され、X11接続切断・終了1となった。この試行は成功件数に含めない。自動更新を中断せず完了を待ち、更新後のXorgセッションで保存PDF再読込・再変換・破棄・終了0を確認した。成功2件、環境による中断1件として元ログを保持する。

フル削除再導入、IME、フォーム、暗号化、ファイルマネージャー、GNOME/Wayland、実機等は今回未再試験。portal/compose/fitz警告を残す。2026-11-11の通常PDF受入、誤った黒サムネイル解釈と訂正も資料に保持する。

GitHubからローカル導入するSnapで、Snap Storeの署名はない。既存公開版を変更せず、prerelease/latest=false、新規専用ブランチ・タグと確定16添付で公開する。公開後は全添付を再ダウンロードして照合し、X tyamada22へ案内する。VMは内蔵でのみ実行。元VM保管庫、公開版ファイル、旧候補、試験PDFは保持した。snapdの保持規則で無効x1は一覧から外れ、x5/x6となったが、公開0.3.4のSnap原本と外付けの元VMは保持している。
