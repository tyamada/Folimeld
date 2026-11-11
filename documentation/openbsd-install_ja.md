# OpenBSDのインストール・ビルド

[English](openbsd-install.md) | [日本語](openbsd-install_ja.md)

このページのコマンドとビルド手順はamd64向けです。arm64版は[専用Release](https://github.com/tyamada/Folimeld/releases/tag/openbsd-aarch64-v0.3.3)の[導入手順](https://github.com/tyamada/Folimeld/releases/download/openbsd-aarch64-v0.3.3/INSTALL_ja.txt)を使用してください。対応ソース・SHA-256・検証記録も同じReleaseに掲載しています。

対象はOpenBSD 8.0 / amd64、Python 3.14、X11デスクトップ。Folimeld独自の試験配布であり、OpenBSD公式パッケージではない。配布先は[OpenBSD Release](https://github.com/tyamada/Folimeld/releases/tag/openbsd-v0.3.3)。

## パッケージの導入

Releaseから `folimeld-0.3.3.tgz`、`folimeld-mupdf-1.28.2.tgz`、`folimeld-80-pkg.pub`、`SHA256SUMS.txt`、`SHA256SUMS.txt.sig` を同じフォルダーへ保存する。公開鍵の2行目を、[リポジトリの公開鍵](../packaging/openbsd/folimeld-80-pkg.pub)と照合する。

```text
RWSM2obNrKjUbNGU8itgBN/nGVFG95tTaBrcV9pO8dTLQvihQtAdPkIy
```

一般ユーザーで署名を検証し、`sha256 -r` の結果を署名済み一覧の同名ファイルと照合する。

```sh
signify -V -p folimeld-80-pkg.pub -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
sha256 -r folimeld-0.3.3.tgz folimeld-mupdf-1.28.2.tgz
```

X11デスクトップを構成し、OpenBSD 8.0の公式パッケージを取得できる `/etc/installurl` を設定する。次をrootで実行する。`doas` が未設定ならrootのシェルを使用する。

```sh
install -m 644 folimeld-80-pkg.pub /etc/signify/folimeld-80-pkg.pub
pkg_add ./folimeld-mupdf-1.28.2.tgz ./folimeld-0.3.3.tgz
```

署名付きパッケージを使用し、未署名を許可するオプションは指定しない。Python、PySide6/Qt、Pillow、cryptography、psutil、gettext-runtime、日本語フォントは公式依存として導入する。ネットワークと空き容量が必要。

一般ユーザーのX11セッションで起動する。

```sh
folimeld
folimeld '/path/to/file.pdf'
```

削除はrootで `pkg_delete folimeld`、専用MuPDF依存も不要なら続けて `pkg_delete folimeld-mupdf` を実行する。ユーザーのPDFと設定を削除する処理は含まない。共有の公式依存はそのまま残る。

アプリは `/usr/local/share/folimeld/`、起動コマンドは `/usr/local/bin/folimeld` に配置する。専用依存のPyMuPDF/MuPDF 1.28.2は `share/folimeld/vendor/` に入り、システムのPyMuPDFを置き換えない。既存の[ソース実行検証](openbsd-verification_ja.md)は1 vCPU・16 GiBのVirtualBox VMで実施した。4 vCPU、別のOS版・CPUでの動作は保証しない。

## ソースから構築

Releaseのハッシュ付き `Folimeld-source-*.zip` とPyMuPDF/MuPDFの原本ソース2件を取得する。ビルド記録のハッシュと照合して対応ソースZIPを展開し、そのルートで作業する。GitHub自動生成ZIPではなく、パッケージに対応付けたZIPを使用する。

rootでビルド依存を導入する。OpenBSD基本システムのコンパイラー、開発・X11セットも必要。

```sh
pkg_add python py3-pip py3-virtualenv py3-llvm%22 swig gmake bash \
  pyside6 py3-Pillow py3-cryptography py3-psutil noto-cjk
```

一般ユーザーで、空白・シェル特殊文字を含まない絶対パスを指定する。

```sh
sh tools/build_openbsd_native.sh /path/to/dependency-sources \
  /path/to/new-native-work /path/to/wheels
python3 -m venv --system-site-packages .venv-openbsd
.venv-openbsd/bin/python -m pip install --no-deps /path/to/wheels/pymupdf-1.28.2-*.whl
.venv-openbsd/bin/python main.py
```

スクリプトは原本2件のSHA-256を確認し、LLVM 22対応パッチを適用してwheelを構築する。新しい作業ディレクトリーを使用し、長時間のネイティブビルドに備える。

パッケージ化には署名を確認したOpenBSD 8.0のportsツリーを `/usr/ports` に用意する。専用のビルドVMでrootとして実行する。既存の `print/folimeld`、`print/folimeld-mupdf` は上書きしない。

```sh
python3 -m tools.build_openbsd_package \
  --source /path/to/Folimeld-source-SHA256.zip \
  --wheel /path/to/wheels/pymupdf-1.28.2-cp314-abi3-openbsd_8_0_amd64.whl \
  --wheel-sha256 RECORDED_WHEEL_SHA256 \
  --dependency-sources /path/to/dependency-sources \
  --output /path/to/output --work /path/to/new-package-work
```

独自portsの定義とファイル一覧を生成し、portsのfake・共有ライブラリ検査・packageを使用する。ソース、wheel、依存ソース、パッケージ、収録ファイルのハッシュを `build-record.json` に保存する。生成物の署名は公開者が `sh tools/sign_openbsd_packages.sh /path/to/secret.sec /path/to/output /path/to/new-signed-output` で別工程として行う。秘密鍵はソースと配布フォルダーの外に置く。署名前後でパッケージのハッシュは変わるため、配布時の最終ハッシュはReleaseの署名済み一覧を基準とする。

参考: OpenBSD公式 [ports](https://www.openbsd.org/faq/ports/)、[pkg_add(1)](https://man.openbsd.org/pkg_add)、[signify(1)](https://man.openbsd.org/signify)。
