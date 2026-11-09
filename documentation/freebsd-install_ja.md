# FreeBSDのインストール・ビルド

[English](freebsd-install.md) | [日本語](freebsd-install_ja.md)

対象はFreeBSD 15.1 / amd64、Python 3.12、GUIデスクトップ。現在はローカル配布候補の作成段階で、ダウンロード公開は未実施。FreeBSD公式Portsへの登録や公式パッケージではない。

pkgの作成、クリーンなchrootでの導入・GUI起動・画像変換・保存・削除・再導入を確認済み。[検証記録](freebsd-package-verification_ja.md)を参照。

## パッケージの導入

配布候補は `dist/freebsd/` にまとめる。Folimeldパッケージ、対応する `Folimeld-source-<SHA256>.zip`、`build-record.json`、`SHA256SUMS.txt`、`dependency-sources/` を一緒に保管する。`sha256 -r folimeld-0.3.3_1.pkg` の結果を一覧の同名ファイルの値と照合する。ほかの配布ファイルも同様に照合する。

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

現在は公開前のため、更新済みの作業ツリーまたはローカル配布候補の対応ソースZIPを使う。一般ユーザーで対応ソースZIPを新しいディレクトリーに展開する。以下のファイル名は実際のハッシュ付きファイル名に置き換える。

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
  --source dist/source/Folimeld-source-実際のSHA256.zip \
  --wheel build/freebsd-pymupdf/wheels/実際のwheel名.whl \
  --output dist/freebsd
```

パッケージ作成自体にroot権限は不要。ビルダーはソースのマニフェストを照合し、依存の名称・版・originと、ソース・wheel・パッケージのSHA-256を記録する。インストールファイルはroot:wheel所有で作成する。パッケージの版はアプリ版に `_1` を付けたFreeBSDパッケージ改訂番号。

同梱ネイティブコードの対応ソースは、[PyMuPDF 1.28.2](https://pypi.org/project/PyMuPDF/1.28.2/)、[MuPDF 1.28.2](https://mupdf.com/downloads/archive/mupdf-1.28.2-source.tar.gz)、リポジトリの `packaging/freebsd/pymupdf-1.28.2-freebsd.patch`。ビルドスクリプトで固定したハッシュと照合し、配布候補にも保存する。外部の公式依存パッケージは同梱しない。

参考: FreeBSD pkgの公式 [pkg-create(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-create.8)、[pkg-add(8)](https://github.com/freebsd/pkg/blob/main/docs/pkg-add.8)。
