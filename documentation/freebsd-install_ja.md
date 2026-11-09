# FreeBSDのインストール・ビルド

[English](freebsd-install.md) | [日本語](freebsd-install_ja.md)

対象はFreeBSD 15.1 / amd64、Python 3.12、GUIデスクトップ。[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/freebsd-v0.3.3)で試験配布している。FreeBSD公式Portsへの登録や公式パッケージではない。

pkgの作成、クリーンなchrootでの導入・GUI起動・画像変換・保存・削除・再導入を確認済み。[検証記録](freebsd-package-verification_ja.md)を参照。

## パッケージの導入

Releaseから[パッケージ](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/folimeld-0.3.3_1.pkg)と[チェックサム](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/SHA256SUMS.txt)をダウンロードする。[対応ソースZIP](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/Folimeld-source-9ceb5ec75dcd3ddb60bb66f0b6996da5e700cf4400bd89b31808f5250b19f23b.zip)、`build-record.json`、PyMuPDF・MuPDFのソースアーカイブも同じReleaseに添付している。`sha256 -r folimeld-0.3.3_1.pkg` の結果を一覧の同名ファイルの値と照合する。ほかの配布ファイルも同様に照合する。ローカルの作成元は `dist/freebsd/`、公開用の整理済みファイルは `build/freebsd-release/` に保持している。

rootで依存関係を先に導入する。ローカルファイルの `pkg add` は公式リポジトリから不足依存を自動取得する手順として扱わない。

```sh
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./folimeld-0.3.3_1.pkg
```

一般ユーザーで起動する。

```sh
folimeld
folimeld /path/to/file.pdf
```

更新パッケージも `pkg add ./新しいパッケージ名.pkg` で導入する。将来の版からの更新は未検証。削除はrootで `pkg delete folimeld`。他のアプリも使用する依存パッケージは自動削除しない。ユーザーのPDFと設定は保持される。

`/usr/local/bin/folimeld`、`/usr/local/share/folimeld/`、デスクトップエントリーとアイコンを導入する。Python・Qt・Pillow・cryptography・psutilは公式pkgに依存し、PyMuPDF/MuPDF 1.28.2だけを専用の `vendor/` に同梱する。開発用仮想環境への参照は含めない。Qtの依存パッケージは大きいため、ネットワークとディスク空き容量が必要。

## ソースから実行

rootでランタイムとビルド用パッケージを導入する。

```sh
pkg install git python312 py312-pip py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp gmake swig pkgconf llvm19
```

このReleaseに添付された対応ソースZIPを使う。一般ユーザーで新しいディレクトリーに展開する。以下のファイル名は実際のハッシュ付きファイル名に置き換える。

```sh
python3.12 -m zipfile -e /path/to/Folimeld-source-SHA256.zip Folimeld
cd Folimeld
sh tools/build_freebsd_pymupdf.sh
python3.12 -m venv --system-site-packages .venv-freebsd
.venv-freebsd/bin/python -m pip install --no-deps \
  build/freebsd-pymupdf/wheels/pymupdf-1.28.2-*.whl
.venv-freebsd/bin/python main.py
```

システムの旧PyMuPDF 1.27.2.2ではフォーム読み込み時に異常終了する。[原因と修正](freebsd-forms-fix_ja.md)を参照。仮想環境のPythonを使う。

## パッケージの作成

対応ソースZIPと、そのFreeBSD環境でビルドしたwheelを指定する。`tools/source_bundle.py` の `source_datas()` により、Git作業ツリーからハッシュ付きのソースZIPを生成できる。作業中の変更がある場合はマニフェストに記録される。

```sh
python3.12 -c "from tools.source_bundle import source_datas; source_datas('.', 'freebsd-amd64')"
python3.12 tools/build_freebsd_package.py \
  --source dist/source/Folimeld-source-ACTUAL_SHA256.zip \
  --wheel build/freebsd-pymupdf/wheels/ACTUAL_WHEEL_NAME.whl \
  --output dist/freebsd
```

パッケージ作成自体にroot権限は不要。ビルダーはソースのマニフェストを照合し、依存の名称・版・originと、ソース・wheel・パッケージのSHA-256を記録する。インストールファイルはroot:wheel所有で作成する。パッケージの版はアプリ版に `_1` を付けたFreeBSDパッケージ改訂番号。

同梱ネイティブコードの対応ソースは、[PyMuPDF 1.28.2](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/pymupdf-1.28.2.tar.gz)、[MuPDF 1.28.2](https://github.com/tyamada/Folimeld/releases/download/freebsd-v0.3.3/mupdf-1.28.2-source.tar.gz)、対応ソースZIP内の `packaging/freebsd/pymupdf-1.28.2-freebsd.patch`。ビルドスクリプトで固定したハッシュと照合済み。外部の公式依存パッケージは同梱しない。

参考: FreeBSD pkgの公式 [pkg-create(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-create.8)、[pkg-add(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-add.8)。
