# NetBSDのインストール・ビルド

[English](netbsd-install.md) | [日本語](netbsd-install_ja.md)

このページのコマンドとビルド手順はamd64向けです。aarch64版は[専用Release](https://github.com/tyamada/Folimeld/releases/tag/netbsd-aarch64-v0.3.3)の[導入手順](https://github.com/tyamada/Folimeld/releases/download/netbsd-aarch64-v0.3.3/INSTALL_ja.txt)を使用してください。対応ソース・SHA-256・検証記録も同じReleaseに掲載しています。

対象はNetBSD 11.1 / amd64、Python 3.12、X11デスクトップ。Folimeld独自の試験配布パッケージであり、NetBSD公式パッケージではない。[GitHub Release](https://github.com/tyamada/Folimeld/releases/tag/netbsd-v0.3.3)からパッケージ・対応ソース・依存ソース・SHA-256一覧を取得する。

確認範囲は[パッケージ検証記録](netbsd-package-verification_ja.md)を参照。

## パッケージの導入

配布候補は `dist/netbsd/`。対応ソースZIP、依存ライブラリのソース、パッチ、ビルド記録、ライセンス、`SHA256SUMS.txt` を併せて保存する。`sha256 -r folimeld-0.3.3.tgz` の結果をチェックサム一覧の同名ファイルと照合する。

X11とデスクトップを構成したNetBSDで、rootとして実行する。依存は検証時と同じpkgsrcリポジトリから導入する。既存の別系列の依存と混在させない。

```sh
export PKG_PATH=https://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/x86_64/11.0_2026Q3/All
/usr/pkg/sbin/pkg_add ./folimeld-0.3.3.tgz
```

一般ユーザーで起動する。

```sh
/usr/pkg/bin/folimeld
/usr/pkg/bin/folimeld '/path/to/file.pdf'
```

削除はrootで `/usr/pkg/sbin/pkg_delete folimeld`。ユーザーのPDFと設定は保持する。共有する依存パッケージは削除しない。将来版からのアップグレードは未検証。

インストール先は `/usr/pkg/bin/folimeld` と `/usr/pkg/share/folimeld/`、デスクトップエントリー、アイコン。PySide6/shiboken6 6.11.2（Core/Gui/Widgets）とPyMuPDF/MuPDF 1.28.2をアプリ専用領域に同梱する。Python・Qt・Pillow・cryptography・psutil・日本語フォントは公式パッケージに依存する。公式依存は多数あるため、ネットワークとディスク容量が必要。

## ソースから構築

対応ソースZIPを展開し、そのディレクトリーで作業する。公式依存に加え、Pythonのpip、C/C++コンパイラー、LLVM/Clang、CMake、Ninja、Bash、GNU make、SWIG、pkg-configとQt開発ファイルが必要。検証済みの版とパッチは[検証記録](netbsd-verification_ja.md)を参照。

rootでビルド用依存を導入する。

```sh
/usr/pkg/sbin/pkg_add py312-pip llvm clang cmake ninja-build bash gmake swig4 pkgconf
/usr/pkg/sbin/pkg_add python312 qt6-qtbase qt6-qtsvg qt6-qtimageformats \
  qt6-qttranslations py312-Pillow py312-cryptography py312-psutil gettext-lib noto-cjk-fonts
```

一般ユーザーで実行する。空白やシェル特殊文字を含まない絶対パスを使用する。

```sh
sh tools/build_netbsd_native.sh
export LD_LIBRARY_PATH="$PWD/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib"
.venv-netbsd/bin/python main.py
```

`NETBSD_BUILD_DIR` と `NETBSD_NATIVE_PREFIX` でビルド先・仮想環境を変更できる。スクリプトは既存の検証用レシピとパッチを使用し、Qt公式ソースのハッシュを照合する。PyMuPDF/MuPDFの取得とハッシュ照合も行う。長時間のネイティブビルドが必要。

パッケージ化は同じNetBSD環境で行う。`--source` には配布対象のハッシュ付きソースZIPを指定する。

```sh
python3.12 -m tools.build_netbsd_package \
  --source /path/to/Folimeld-source-SHA256.zip \
  --native-prefix "$PWD/.venv-netbsd" \
  --dependency-sources /path/to/dependency-sources --output dist/netbsd
```

ビルダーはソースマニフェストを照合し、`pkg_create` で作成する。依存の正確な版、同梱ネイティブファイルとパッケージのSHA-256を `build-record.json` に記録する。

`--dependency-sources` のディレクトリーには配布されたPySide6、PyMuPDF、MuPDFの3つの原本ソースアーカイブを置く。ビルダーは固定SHA-256を照合する。一般化したビルド用ラッパーは構文確認済みで、別のパスでの依存全体の再コンパイルは未検証。元のVMでのネイティブビルド記録を併せて参照する。

参考: NetBSD公式 [pkg_create(1)](https://man.netbsd.org/pkg_create.1)、[pkg_add(1)](https://man.netbsd.org/pkg_add.1)。
