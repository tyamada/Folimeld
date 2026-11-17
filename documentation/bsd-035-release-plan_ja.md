# BSD・Linux（Debian/Ubuntu）0.3.5 パッケージ更新・ビルド手順書

[日本語](bsd-035-release-plan_ja.md) | [English](bsd-035-release-plan.md)

Folimeld 0.3.5（暗号化 Undo/Redo 履歴のディスク退避、大規模 PDF 保存高速化、画像フォルダー一括取り込み、サムネイル仮想化、GitHub Sponsors 案内）を適用した各 OS 向けパッケージの生成・受入検証・公開手順です。

---

## 1. 原本ソーススナップショットの取得

すべてのプラットフォームで、以下の確定ソースコードスナップショット ZIP を原本として使用します。

- **ファイル**: `dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`
- **SHA-256**: `E550BF65EC95B968DDCE59592F3EF4FD9E297A88B9E2B7364413592244A14E8A`
- **コミット**: `5d4ed15`（またはそれ以降の最新 `main`）

---

## 2. FreeBSD 15.1（amd64 / aarch64）

### 生成対象
- パッケージ: `folimeld-0.3.5_1.pkg`
- ビルド記録: `build-record.json`
- 対応ソース: `Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip`

### ビルド手順
FreeBSD 15.1 環境（amd64 または aarch64）にて実行します。

```sh
# 1. ビルド・ランタイム依存の導入
pkg install git python312 py312-pip py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp gmake swig pkgconf llvm19

# 2. PyMuPDF 1.28.2 wheel の準備（未作成の場合）
sh tools/build_freebsd_pymupdf.sh
# -> build/freebsd-pymupdf/wheels/pymupdf-1.28.2-*.whl が生成される

# 3. 0.3.5 パッケージの生成
python3.12 tools/build_freebsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --wheel build/freebsd-pymupdf/wheels/pymupdf-1.28.2-cp312-cp312-freebsd_*.whl \
  --output dist/freebsd
```

### 受入確認
```sh
# インストール試験
pkg install python312 py312-pyside6 py312-pillow py312-cryptography py312-psutil noto-sans-jp
pkg add ./dist/freebsd/folimeld-0.3.5_1.pkg

# 起動確認
folimeld
```
- メニュー「ヘルプ → 開発を応援する…」が表示され、GitHub Sponsors 画面が開くことを確認。
- PDF 読み込み、回転、大容量保存、画像一括取り込みを確認。

### ビルド・受入実績（VirtualBox VM / FreeBSD 15.1-RELEASE-p5 amd64）
- パッケージ: `dist/freebsd/folimeld-0.3.5_1.pkg`（26,168,773 bytes）
- SHA-256: `16d3d1801acae0f62bf99d89d53f8a679593e5896d1db60d46cc5b57c15946ae`
- ビルド記録: `dist/freebsd/build-record.json`（SHA-256: `cf06b58c538bf6ba54cf1afa34bd8f7c3035ca1c0b0ce2190fd43b8361d462f9`）
- 検証結果: `pkg add -f` による更新導入が成功（MIME・アイコンキャッシュトリガー実行完了）。`pkg info folimeld` で `0.3.5_1` を確認。`QT_QPA_PLATFORM=offscreen timeout 5s /usr/local/bin/folimeld` にてQt GUI初期化、PyMuPDF/fitz読み込み、ウィンドウ生成および正常稼働を確認。

---

## 3. NetBSD 11.1（amd64 / aarch64）

### 生成対象
- パッケージ: `folimeld-0.3.5.tgz`
- ビルド記録: `build-record.json`

### ビルド手順
NetBSD 11.1 環境にて実行します。

```sh
# 1. pkgsrc 依存の導入
/usr/pkg/sbin/pkg_add py312-pip llvm clang cmake ninja-build bash gmake swig4 pkgconf
/usr/pkg/sbin/pkg_add python312 qt6-qtbase qt6-qtsvg qt6-qtimageformats \
  qt6-qttranslations py312-Pillow py312-cryptography py312-psutil gettext-lib noto-cjk-fonts

# 2. native prefix の準備
sh tools/build_netbsd_native.sh

# 3. 0.3.5 パッケージの生成
python3.12 tools/build_netbsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --native-prefix .venv-netbsd \
  --dependency-sources /path/to/dependency_sources \
  --output dist/netbsd
```

### 受入確認
```sh
/usr/pkg/sbin/pkg_add ./dist/netbsd/folimeld-0.3.5.tgz
/usr/pkg/bin/folimeld
```

### ビルド・受入実績（VirtualBox VM / NetBSD 11.1 amd64）
- パッケージ: `dist/netbsd/folimeld-0.3.5.tgz`（37,074,914 bytes）
- SHA-256: `7dc5c7d68e41b5120a9345fd679e5c99d46fcd7b7b50cf4f49e22d55ffec6e6a`
- ビルド記録: `dist/netbsd/build-record.json`（SHA-256: `c1ce5d8574785b7f0af1aea20159a487349b45f7b5f2e04b633d43983f4124c4`）
- 検証結果: `/usr/pkg/sbin/pkg_add -u` による更新導入が成功。`/usr/pkg/sbin/pkg_info` で `folimeld-0.3.5` を確認。`QT_QPA_PLATFORM=offscreen timeout 5s /usr/pkg/bin/folimeld` にてQt GUI初期化、PyMuPDF/fitz読み込み、ウィンドウ生成および正常稼働を確認。

---

## 4. OpenBSD 8.0（amd64 / arm64）

### 生成対象
- パッケージ: `folimeld-0.3.5.tgz`（署名付き）
- 専用依存: `folimeld-mupdf-1.28.2.tgz`
- 署名ファイル: `SHA256SUMS.txt.sig`

### ビルド・署名手順
OpenBSD 8.0 環境（Python 3.14）にて実行します。

```sh
# 1. 専用 MuPDF wheel のビルド（未作成の場合）
sh tools/build_openbsd_native.sh /path/to/dependency_sources /tmp/work /tmp/out

# 2. 0.3.5 ports パッケージのビルド
python3.14 tools/build_openbsd_package.py \
  --source dist/source/Folimeld-source-e550bf65ec95b968ddce59592f3ef4fd9e297a88b9e2b7364413592244a14e8a.zip \
  --wheel /tmp/out/pymupdf-1.28.2-*.whl \
  --dependency-sources /path/to/dependency_sources \
  --output dist/openbsd \
  --work /tmp/pkgwork

# 3. signify による署名
cd dist/openbsd
sha256 -r folimeld-0.3.5.tgz folimeld-mupdf-1.28.2.tgz > SHA256SUMS.txt
signify -S -s /etc/signify/folimeld-80-pkg.sec -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
```

### 受入確認
```sh
signify -V -p packaging/openbsd/folimeld-80-pkg.pub -m SHA256SUMS.txt -x SHA256SUMS.txt.sig
pkg_add ./folimeld-mupdf-1.28.2.tgz ./folimeld-0.3.5.tgz
folimeld
```

### ビルド・署名・受入実績（VirtualBox VM / OpenBSD 8.0 amd64）
- 本体パッケージ（署名付き）: `dist/openbsd/folimeld-0.3.5.tgz`（6,009,111 bytes）
  - SHA-256: `6d0b68373f380622dc1bbbe4bad4d132648f8974fa7246ca9af0c22db9028e63`
- 専用MuPDF依存（署名付き）: `dist/openbsd/folimeld-mupdf-1.28.2.tgz`（26,822,825 bytes）
  - SHA-256: `1d537907faf92f11f2f701f967486c03643097e8dd5dff9199e6c6a6aa87bf8c`
- 署名ファイル: `dist/openbsd/SHA256SUMS.txt`、`dist/openbsd/SHA256SUMS.txt.sig`（`signify -V` 検証合格）
- ビルド記録: `dist/openbsd/build-record.json`（SHA-256: `b9a53586e99aa77f4e84f5633a73303a015a21ca7663a396cc001e9c83255bbc`）
- 検証結果: `pkg_add -r` による更新導入が署名照合通過のもと成功。`pkg_info` で `folimeld-0.3.5` および `folimeld-mupdf-1.28.2` を確認。`QT_QPA_PLATFORM=offscreen /usr/local/bin/folimeld` にてQt GUI初期化、PyMuPDF/fitz読み込み、ウィンドウ生成および正常稼働を確認。

---

## 5. Ubuntu 24.04 / Debian 13（amd64 / arm64）

### 生成対象
- DEB: `folimeld_0.3.5_amd64.deb`、`folimeld_0.3.5_arm64.deb`
- Snap: `folimeld_0.3.5_amd64.snap`、`folimeld_0.3.5_arm64.snap`

### ビルド手順
Ubuntu 24.04 / Debian 13 環境（または WSL2 / Docker）にて実行します。

```sh
# 1. 依存関係の導入
sudo apt update && sudo apt install -y python3 python3-pip python3-venv pyinstaller libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0

# 2. PyInstaller による実行ファイル生成
python3 -m venv .venv-linux
.venv-linux/bin/pip install -r requirements.txt -c constraints-release.txt pyinstaller
.venv-linux/bin/pyinstaller --noconfirm Folimeld-linux.spec

# 3. DEB パッケージの組み立て
dpkg-deb --build build/deb/folimeld_0.3.5_amd64 dist/folimeld_0.3.5_amd64.deb
```

### ビルド実績（WSL2 / Ubuntu 24.04）
`./build_linux.sh deb` によりビルドを実行し、確定パッケージおよび関連付けマニフェストを生成済み：
- パッケージ: `dist/ubuntu/folimeld_0.3.5_amd64.deb`
- サイズ: 105,690,904 bytes
- SHA-256: `5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174`
- 実行ファイル: `dist/folimeld`（SHA-256: `c799b852384f81839efcb79fa383a8ba3a6f8156d0d2b61501fb70803cd810b9`）
- 関連付け記録: `dist/source/folimeld_0.3.5_amd64.deb-5b64a696b69cdb7c9fada6e13cd100dd35d76470ecad1408800ee558c4362174.json`

### 受入確認結果
- **Ubuntu 24.04.4 LTS / 24.04.5 LTS (WSL2)**:
  `QT_QPA_PLATFORM=offscreen timeout 4s /usr/bin/folimeld` にて、Qt GUI初期化、PyMuPDF/fitz読み込み、ウィンドウ生成およびイベントループ起動を正常確認（プロセス正常稼働・正常終了）。
- **Debian 13.6 / 13.7 Trixie (WSL2)**:
  `libc6 (>= 2.39)` 依存を満たす環境（GLIBC 2.41）にて、同様に offscreen 起動、PyMuPDF/fitz読み込み、Qt GUIウィンドウ生成を確認（プロセス正常稼働・正常終了）。
