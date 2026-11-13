# openSUSE Leap16.1 ARM64 RPM0.3.5 公開前検証

対象は `folimeld-0.3.5-1.lp161.aarch64.rpm`。本体ソース `fa0f0f5d5e04d4a88fe3dde827fbf1b9d843a207`（差分なし）、RPM SHA256 `2007446be6e0de760af5904bab3264450065b55d29c5471dc838cb8aac354679`、実行ファイル SHA256 `5ebd7a5b21e7eb1a4017fce33b20ed7eb1bdd88803bb83adabe4b2eadc38a79e`。対応ZIP SHA256 `000d1f69eeb3c081cbed53b73422b76c8cd7284b55c7f1f81b7137efaa7bd6f8`。999入力をGit/ZIP/埋込記録で照合。タグには本体ビルド後の本記録を追加する。

公式Leap16.1 aarch64 Cloud Build3.16、kernel6.12.0-160100.9-default、glibc2.40、Python3.13.13。最終ビルドと画面検証は内蔵上の専用ARM64 VM、UID1000/Xorg21.1.21/IceWM3.6.0、SELinux Enforcing。通常ユーザードメインでありSnap同様のアプリ単位制限はない。

410テスト成功、9スキップ、69サブテスト成功、ruff成功。同一VMの別出力先2件でELF一致。RPMヘッダー時刻と独立ホスト再現性は対象外。最小依存構成（recommendsなし）でも一般ユーザーoffscreen起動15秒継続、timeout124は起動継続だけの合格。

新規導入・回転・即時サムネイル・Undo/Redo・移動・白紙挿入/削除・別名保存・日本語パス再読込・画像フォルダー変換保存・正常終了を確認。RPM完全削除と同一候補再導入後も文書と設定ハッシュを保持し、画像PDFを再表示。GUI3回終了0、プロセス残存なし。ページ順2→1→3、回転0→90→0、画像PDFと元PNGの画素一致。日本語コピーはシェルで作成したものでIME試験ではない。素材のUbuntu/Debian表記は履歴で、合格結果の流用ではない。

同梱202AArch64実体のうち公式wheel105、署名付きopenSUSE RPM内容95（47binary/32対応SRPM）、Google公式Brotli1.1.1ソースビルド2。公式PyInstaller起動部の元セクション一致。不足告知は対応SRPMから補足。Brotliは変更なし公式コミットdb0631dfea829194206d269bc7b25d0908cdb97d、14公式テスト成功。OSに入っている修正版1.1.0-160100.3.1は保持。該当RPM/SRPMが公開リポジトリにないため、古い2.1へ戻さず同梱用だけ1.1.1を構築した。

共通0.3.4依存ソースTAR/Pillow補足は依存版共通のため再利用し、現在cp313 Pillowの部品名・版・ソースハッシュ・ライセンスを照合。今回のLeap32SRPM/Brotli補足と現行告知・出所JSONを併用する。歴史的余剰資料はLeap対応表に数えない。

GitHub配布の未署名試験版。glibc2.40以上。実機ARM・完全なGNOME/KDE/Wayland・IME・関連付け・暗号化/フォームGUI・旧版更新・旧Leap/SLE/Tumbleweedは今回未検証。詳細はRelease添付BUILD/KNOWN-LIMITATIONS/verification-recordsへ。既存公開物とlatestを保持し、全添付の公開後再取得とX案内が完了してから次の対象へ進む。

公開完了: 全16添付を公開後に取得しサイズ/SHA256一致、既存公開添付とlatest保持を確認。main791a791へ日英案内を反映後、[X案内](https://x.com/tyamada22/status/2121163624484053498)の公開表示を確認。
