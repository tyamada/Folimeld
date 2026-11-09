# OpenBSDパッケージの検証・公開記録

検証・公開日: 2026-11-09（日本時間）。対象はOpenBSD 8.0 / amd64、Folimeld 0.3.3。[OpenBSD試験配布Release](https://github.com/tyamada/Folimeld/releases/tag/openbsd-v0.3.3)で公開し、公開URLからの再取得まで確認した。

## 配布構成

`tools/build_openbsd_package.py` は対応ソースのマニフェスト、原本PyMuPDF/MuPDFソース、ネイティブwheelのSHA-256を照合し、独自portsのfake・ライブラリ検査・packageを使う。

- 本体: `folimeld-0.3.3.tgz`、署名後SHA-256 `9e48f0653bb90a7d6a0e5c55cddbb004eef073d2062313848bb545d475914ddc`。
- 専用依存: `folimeld-mupdf-1.28.2.tgz`、署名後SHA-256 `fb89413134738238635fc8f9bec58815b772881e6ef221f827b9d8e16be5cc21`。
- PyMuPDF/MuPDFは `/usr/local/share/folimeld/vendor/` へ置き、システムのPyMuPDFを置き換えない。LLVM 22向けラッパー生成パッチは対応ソース内の `packaging/openbsd/` に含む。
- Python 3.14、PySide6/Qt、Pillow、cryptography、psutil、gettext-runtime、フォントは公式パッケージに依存する。検証時の[公式依存の閉包](openbsd-package-verification/official-packages.json)は168件。

[ビルド記録](openbsd-package-verification/build-record.json)は署名前のパッケージとソース・wheel・全収録ファイルのハッシュを記録する。[署名記録](openbsd-package-verification/signing-record.json)は配布する署名後のハッシュを記録する。

対応ソースは `Folimeld-source-f67bd8d6672b4e7377126bfc24e1c7d7661004d454693a3cd1fe622b02e75be9.zip`。Gitコミット `3b8e36f5dd30ebf39015a3c04abdc2ee06532cee` と未コミットのパッケージ工具・文書を含むため、ZIP自体を厳密なビルド入力とする。432ファイルのマニフェストと、公開準備時の実行・ビルド入力90ファイルの一致を確認した。

## 通常導入と実GUI

- `signify -Sz` で両パッケージを署名し、公開鍵を登録した通常の `pkg_add` で導入できた。未署名を許可する指定はしていない。
- 開発用venvを使わず、非特権ユーザーで[スモーク](openbsd-package-verification/smoke.py)を実行した。[結果](openbsd-package-verification/installed-smoke.txt)はフォーム値保持、90度回転、Undo/Redo、別プロセス保存、PNGと2フレームTIFFから3ページの生成・保存が成功。
- 一般ユーザーの実X11から `/usr/local/bin/folimeld` を起動し、[日本語PDFを表示](openbsd-package-verification/gui-open.png)。GUIで先頭ページを回転し、[別名保存](openbsd-package-verification/gui-saved.png)した。[独立照合](openbsd-package-verification/gui-save-result.json)では8ページ、回転 `90, 90, 0, 0, 0, 0, 0, 0`、原文書の内容ストリーム保持を確認。qpdfの構造検査も成功。
- 改変したコピーは `signify` が `signature mismatch` で拒否した。原本の署名済み配布物は変更していない。
- ホスト上の安全なアーカイブ展開・対応ソース保存に関する既存テスト8件と、新しいビルダーのRuff検査が成功。

## 独立環境の検証

署名を検証した公式のbase80、xbase80、xshare80、xfont80セットから `/home/folimeld/openbsd-clean` にchrootを作成した。公式依存は読み取り専用ISOから供給し、導入時にOpenBSDの署名を検証する。chrootはVMのカーネルを共有するため、別VMや実機での検証ではない。

[OSセットの準備](openbsd-package-verification/prepare-clean.sh)と[導入・削除・再導入スクリプト](openbsd-package-verification/verify-clean.sh)を保存する。初回は `/dev/fd`、乱数デバイス、`/var/run` とライブラリキャッシュの初期化が不足し、公式依存の初期化で診断が出た。chrootのある `/home` は既定でnodevのため、検証中だけdevへ変更し、終了時に戻す。これらはchroot構築の条件であり、通常の利用者向けインストール手順には加えない。

[最終ログ](openbsd-package-verification/clean-verification.txt)では、170パッケージの導入後にnobody権限で機能スモークが成功し、全175収録ファイルのハッシュが一致した。開発チェックアウトがない環境であることも確認した。OSセット・公式依存にはコンパイラーが含まれるため、コンパイラー不在の環境とは判定していない。

本体と専用依存の削除後に起動コマンドがなくなり、テスト用のユーザーPDFと設定が残ることを確認した。同じ署名済み配布物を再導入し、非特権の機能スモークが再び成功した。将来版へのアップグレードは未検証。

## 署名と公開資材

パッケージ公開鍵は[リポジトリ](../packaging/openbsd/folimeld-80-pkg.pub)とReleaseへ収録した。秘密鍵はGit管理外へ保存する。12資材のSHA-256一覧を別途署名し、一覧と署名を合わせた14資材をDraftへ添付した。公開前に全添付を取得し直し、[元ファイルとの一致](openbsd-package-verification/draft-downloads.json)と一覧の署名を確認した。

ソースZIP、原本PyMuPDF/MuPDFソース、ネイティブwheel、日英INSTALL、AGPL全文、ビルド記録、署名記録、公開鍵を両パッケージと共に配布する。

Releaseタグは `openbsd-v0.3.3`、公開準備コミットは `911d68e`。プレリリースとして公開し、安定版Linuxのlatest指定を維持した。[公開ダウンロード記録](openbsd-package-verification/public-downloads.json)の14資材すべてを認証なしで取得し直し、元ファイル・署名済みSHA-256一覧と一致した。署名付きtgz内の[全175ファイル](openbsd-package-verification/payload-check.json)もビルド記録と一致するため、公開物は導入・削除・再導入を確認したものと同一のバイト列である。

## 確認範囲

1 vCPU・16 GiBのVirtualBox VMを使用する。既存の[全件テスト・GUI・負荷試験](openbsd-verification_ja.md)と併用し、別CPU・OS版や4 vCPUでの起動には一般化しない。Qt終了時のGLib診断と、既存コードが使うfitz APIの非推奨警告は記録する。ソースビルド用の一般化したシェル工具は構文検査済みで、別ディレクトリーからのネイティブ全再コンパイルは今回未検証。元のネイティブビルドとパッチの成功記録を参照する。

導入手順: [日本語](openbsd-install_ja.md) / [English](openbsd-install.md)。

検証後は `/home` のnodevを復元し、VMを正常停止して一時ISOを取り外した。復旧点は `05-signed-packages-published`（UUID `f4b060cb-261f-44a2-bf71-39095d38ed18`）。[保存状態](openbsd-package-verification/snapshot.json)、[最終VM設定](openbsd-package-verification/vm-configuration.txt)、[証跡のSHA-256一覧](openbsd-package-verification/SHA256SUMS.txt)を参照。
