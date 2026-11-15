# Windowsソース＋uv版：ライセンスと版別ソース案内

この案内はWindows x64・CPython 3.12.16向けのソース＋uv版に適用する。
Microsoft Store版・Linuxの配布記録とは分けて扱う。

- [uv専用ライセンス告知全文](windows-uv-licenses/notices.txt)
- [固定物・対応ソース・確認範囲の台帳](windows-uv-licenses/sources.json)
- [導入・受入状況](windows-uv-source_ja.md)

## 配布物と取得物

FolimeldはAGPL-3.0-onlyで配布する。ソースZIPにはアプリソース、導入・起動処理、
固定入力、ライセンス全文と告知を含め、Python・uv・wheel・導入済み環境は含めない。
インストーラーは固定Pythonとuvを公式GitHub Release、依存wheelを公式PyPIから直接取得する。
台帳のwheel・アーカイブSHA-256を確認して導入し、取得元の告知は削除しない。

正式配布時は、Releaseから対応するコミット、ソースZIP、内部台帳、SHA-256、
本案内と告知を参照できるようにする。現在は未公開の準備段階であり、
未コミットの変更を既存タグや既存preview ZIPに含まれるものとして扱わない。

## 固定14件とソース提供先

| 固定パッケージ | 版 | 主なライセンス／ソース案内 |
| --- | --- | --- |
| cffi | 2.1.1 | MIT-0。libffiは個別条件。台帳のPyPI sdist |
| cryptography | 50.0.2 | Apache-2.0またはBSD-3-Clause。OpenSSL・Rust依存は個別条件。PyPI sdist |
| Pillow | 12.3.0 | MIT-CMUと内包物の個別条件。PyPI sdist |
| pycparser | 3.12 | BSD-3-Clause。PyPI sdist |
| PyMuPDF | 1.28.2 | AGPLv3を選択。実MuPDFも1.28.2。PyPI sdistと上流MuPDFソース |
| PySide6 / Addons / Essentials / shiboken6 | 各6.11.2 | Qtのコミュニティライセンス。下記公式QtForPythonとQtソース |
| typing-extensions | 4.16.0 | PSF-2.0。PyPI sdist |
| winrt-runtime / Windows.Foundation / Windows.Foundation.Collections / Windows.Services.Store | 各3.2.1 | MIT。各PyPI sdistとPyWinRT v3.2.1 |

各PyPIソースの正確なファイル名・URL・公開ハッシュは台帳の`packages[].sdists`にある。
10件にPyPI sdistがあり、Qt系4件にはない。ソースアーカイブ本体の全件取得・展開や、
wheelのビルドパッチとの完全な照合は未実施である。

- [QtForPython/PySide/Shiboken 6.11.2公式ソース](https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/)
- [Qt 6.11.2公式ソース](https://download.qt.io/archive/qt/6.11/6.11.2/single/)
- [MuPDF 1.28.2ソースタグ](https://github.com/ArtifexSoftware/mupdf/tree/1.28.2)
- [PyWinRT v3.2.1ソース](https://github.com/pywinrt/pywinrt/tree/v3.2.1)

Qtの全モジュールがLGPLとは限らない。stock AddonsにはVirtual Keyboard等のGPL対象も存在する。
Linux版の除外状態を本版へ転用せず、インストールされるもの・利用するもの・再配布するものを分ける。
商用Qt・Artifexライセンスを保有しているとは表示しない。

## Pythonとuv

- [CPython v3.12.16](https://github.com/python/cpython/tree/v3.12.16)：PSFと継承ライセンス。
- [python-build-standalone 20261110](https://github.com/astral-sh/python-build-standalone/tree/20261110)：
  固定Pythonのビルドスクリプト・パッチの案内。プロジェクトのライセンスをPython全体に適用しない。
- [uv 0.13.8](https://github.com/astral-sh/uv/tree/0.13.8)：MITまたはApache-2.0。本案内ではMITを選択し、両全文を告知に保持。

実PythonのLICENSE.txt、固定版のuvとPyWinRTの上流ライセンスをuv専用告知に含めた。
Python内のOpenSSL 3.5.9とcryptography内のOpenSSL 4.0.3は別の内包物として記録する。
PBSのfull archiveのPYTHON.jsonや全ビルド入力、uvのRust依存一式は完全照合していない。

## 改変・再配布と確認限界

LGPL経路では、適用ライセンスに従って改変ライブラリの利用やデバッグの権利を保つ。
現在のランチャーは依存の版メタデータを照合するが、起動時にQt DLLの実ハッシュを固定しない。
互換ABI・必要な版メタデータを維持した改変依存は、元環境を残した別コピーで差し替えて確認する。
改変ライブラリの受入や異なるABIの動作は未確認である。

自分でruntime・wheel・改変依存・オフライン環境を配る場合は、この直接取得方式の案内だけを流用しない。
著作権・許諾文・第三者告知に加え、AGPL/LGPL等に従う対応ソース、必要なビルド・導入情報と
改変利用の方法を、その配布物に対応させる。上流リンクだけで常に充足すると判断しない。
親パッケージのライセンスや実行時版だけから、内包する全成分の条件・ビルド由来を確定しない。

既存`licenses/crypto-native-sources.json`は以前のcp314環境の記録である。
cryptographyの一致する実ハッシュと、uvのcp312 CFFIの異なるハッシュをuv台帳に分けて記録した。
以前の記録を削除したり、uv環境全体の証明として表示したりしない。

[English](windows-uv-sources.md)
