# NetBSDパッケージの作成・導入確認

検証日: 2026-11-09（日本時間）。NetBSD 11.1 / amd64向けの試験配布候補。公開準備中。

`tools/build_netbsd_package.py` は対応ソースZIPのマニフェストと依存の原本ソースのSHA-256を照合して `pkg_create` を実行する。PySide6/shiboken6 6.11.2（Core/Gui/Widgets）とPyMuPDF/MuPDF 1.28.2を `/usr/pkg/share/folimeld/` に同梱する。Python、Qt、Pillow、cryptography、psutil、gettext-lib、フォントは公式パッケージに依存する。システムのPySide6やPyMuPDFを置き換えない。

## 検証

- 通常VMで候補tgzを導入し、開発用venvを使わずQtの読み込み・PDF生成と保存が成功。
- 公式NetBSD 11.1のbase、etc、xbase、xetc、xfontセットをSHA-512照合して新規chrootへ展開。公式pkgsrc `11.0_2026Q3` の依存と候補tgzを導入。
- chroot内で非特権のnobodyユーザーがMainWindowを生成し、フォーム読み込み、90度回転、Undo/Redo、保存・再読込を確認。
- PNGと2フレームTIFFから3ページ生成し、別プロセスの保存処理と再読込が成功。
- `pkg_admin check folimeld` が成功。削除で起動スクリプトがなくなり、ユーザーPDFが残ることを確認して再導入・機能テストが成功。
- ホスト上のアーカイブ展開・ソース記録テスト8件とRuffが成功。

[スモークスクリプト](netbsd-package-verification/smoke.py)、[実行環境](netbsd-package-verification/run-smoke.sh)、[chroot構築](netbsd-package-verification/prepare-clean.sh)を保存する。

最初のクリーン検証ではMuPDFの `libintl.so.8` が不足したため、`gettext-lib` を直接依存に追加した。chroot内の初期TLS設定にはコピーしたCAバンドルを `SSL_CERT_FILE` で指定し、証明書検証を維持した。chroot外からのpkg_add更新にはpkg_delete呼び出しの問題があったため、公式pkg_installをchroot内へ導入して更新・削除を実行した。

chrootはホストVMのカーネルを共有する。今回のパッケージ機能テストはQtのoffscreenプラットフォームを使用した。表示を伴う操作は既存の[ソース実行GUI検証](netbsd-verification_ja.md)を参照。別のOS版・CPU、別系列のpkgsrc依存、将来版からの更新、一般化したラッパーでの依存全体の再コンパイルは未検証。

インストール手順: [日本語](netbsd-install_ja.md) / [English](netbsd-install.md)。
