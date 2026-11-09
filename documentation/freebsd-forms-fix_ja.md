# FreeBSDのフォーム読み込み異常終了の修正

検証日: 2026-11-09（日本時間）。FreeBSD 15.1-RELEASE（カーネルp5、ユーザーランドp6）、amd64、Python 3.12.15、VirtualBox 7.2.16で確認。

## 結果

Folimeldの仮想環境をFreeBSD向けにビルドした **PyMuPDF / MuPDF 1.28.2** に切り替え、フォーム読み込み時の `SIGILL` を解消した。

| 確認 | 結果 |
| --- | --- |
| 修正前の最小再現 | PyMuPDF 1.27.2.2でSIGILL |
| Linuxの同版wheel | 最小再現は正常終了 |
| 修正前の新しい回帰テスト | 選択肢なしの6ケースが失敗、選択肢ありの2ケースが成功 |
| 修正後の回帰テストと保存内容テスト | 12ケース合格 |
| 通常VMでのpytest全件 | **386 passed、9 skipped、32 subtests passed**。フォーム関連の除外なし |
| 新しいディレクトリからビルドしたwheelでのpytest全件 | **386 passed、9 skipped、32 subtests passed** |
| Windowsでのpytest全件 | **395 passed、32 subtests passed** |
| Ruff・mypy・依存関係チェック | 成功 |
| 実GUI | フォームPDFの読込、90度回転、通常保存・再読込、暗号化保存・パスワード入力後の再読込が成功 |

FreeBSDの9スキップは既存のWindowsレジストリ・PowerShellビルド／パッケージ処理の条件によるもの。
GUIで保存した通常PDFと暗号化PDFを読み取り、テキスト欄、チェックボックス、選択肢あり・なしのコンボボックスの値と選択肢が保存前と一致し、回転角度も維持されることを照合した。

証跡: [通常VMの全テスト](freebsd-forms-fix/primary-all.log)、[クリーンビルド版の全テスト](freebsd-forms-fix/clean-all.log)、[Windowsの全テスト](freebsd-forms-fix/windows-all.log)、[GUI保存内容の照合](freebsd-forms-fix/gui-forms-verification.json)、[暗号化PDF再読込後の画面](freebsd-forms-fix/gui-encrypted-reopened.png)。

## 原因

PyMuPDFはフォームの種類にかかわらず `JM_choice_options()` からMuPDFの `pdf_choice_widget_options2()` を呼ぶ。
MuPDF 1.27.2のC++ラッパーは、選択肢数が0でも空の `std::vector` の `&opts[0]` を評価していた。
FreeBSDのバイナリでは、0件と判定した直後に境界チェックのトラップ命令 `ud2` へ分岐し、SIGILLになっていた。CPUの命令セット不足によるものではない。

[LLDB記録](freebsd-forms-fix/baseline-live-lldb.log)に発生位置と逆アセンブルを保存した。
[MuPDF 1.28.2の上流ソース](https://github.com/ArtifexSoftware/mupdf/blob/1.28.2/scripts/wrap/cpp.py)では当該箇所が `opts.data()` に変更されている。
[Linux比較記録](freebsd-forms-fix/linux-baseline.log)の正常終了だけでは、旧コードの空配列参照が安全とは判断できない。

## 変更

- [requirements.txt](../requirements.txt): FreeBSDではPyMuPDF 1.28.2以上を要求。ほかのOSの下限は維持。
- [ビルドスクリプト](../tools/build_freebsd_pymupdf.sh): ソースのハッシュ照合、隔離したビルド環境、ネイティブwheelの生成を実装。
- [FreeBSD用ビルドパッチ](../packaging/freebsd/pymupdf-1.28.2-freebsd.patch): `libmupdfcpp.so` のリンク用シンボリックリンクをFreeBSDでも生成する。フォーム処理の修正は上流1.28.2を使用。
- [回帰テスト](../tests/test_pdf_forms.py): 4種類のフォームを生成直後／シリアライズ後に読み込む8ケース。別プロセスに隔離し、ネイティブ異常終了をpytestの失敗として検出する。
- Windowsでの比較中に、`rglob('folimeld*.json')` が大文字・小文字を区別せずソースのサイドカーまで選ぶ既存テストの問題を発見。成果物の接頭辞 `folimeld_` に絞って修正した。
- 既存のGUI確認用スクリプトは、Qt翻訳オブジェクトを保持する変数名を `_translator` に変更し、Ruffの未使用変数判定を解消した。

Folimeld本体にネイティブシグナルを握りつぶす処理や、フォーム機能を無効化する回避策は追加していない。

## 再構築

[初回構築記録](freebsd-virtualbox-setup_ja.md)のGUI・Python実行環境を前提とする。追加のビルド用パッケージはrootで導入する。

```sh
pkg install -y python312 py312-pip gmake swig pkgconf llvm19
```

リポジトリのルートで一般ユーザーとして実行する。

```sh
sh tools/build_freebsd_pymupdf.sh
python3.12 -m venv --system-site-packages .venv-freebsd
.venv-freebsd/bin/python -m pip install --no-deps --force-reinstall \
  build/freebsd-pymupdf/wheels/pymupdf-1.28.2-*.whl
.venv-freebsd/bin/python -m pip check
QT_QPA_PLATFORM=offscreen .venv-freebsd/bin/python -m pytest -q -p no:cacheprovider
```

ビルドスクリプトは `build/freebsd-pymupdf/.venv` を作成し、pip 26.3、setuptools 84.2.1、wheel 0.48.0、pipcl 13、Clangバインディング19.1.7を使用する。
LLVM 19のlibclangをビルド中だけ参照する。BSD向け既定値が重複しないよう、ビルド時の `CXX` は解除する。
`FOLIMELD_FREEBSD_PYMUPDF_BUILD` で作業先、`FOLIMELD_FREEBSD_PYTHON` でPython、`FOLIMELD_FREEBSD_CLANG_LIBRARY_DIR` でlibclangの場所を指定できる。

検証したソースのSHA-256:

| ソース | SHA-256 |
| --- | --- |
| `pymupdf-1.28.2.tar.gz` | `5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249` |
| `mupdf-1.28.2-source.tar.gz` | `44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156` |

作成したwheelのタグは `cp312-abi3-freebsd_15_1_release_p5_amd64`。別のFreeBSD版・アーキテクチャでは、その環境で再ビルド・再検証する。
ソースとビルド手順の再現を確認しており、wheelのZIPタイムスタンプを含むバイト単位の再現性は保証していない。

## VMへの反映

通常VM `Folimeld-FreeBSD-15.1-amd64` の `.venv-freebsd` に導入済み。
デスクトップの `Folimeld.desktop` の起動先も同仮想環境へ変更し、GUIから起動できることを確認した。
実行中のアプリが仮想環境内のMuPDFライブラリを読み込むことも [実行環境記録](freebsd-forms-fix/environment.json) で確認した。
OS管理の `py312-pymupdf` 1.27.2.2は保持しているため、システムの `python3.12` を直接使うと旧版になる。アプリ起動とテストには `.venv-freebsd/bin/python` を使用する。

停止状態でスナップショット `04-forms-fixed` を保存済み（UUID `8d630923-f629-4d67-9faf-f1ded5a1544c`）。`03-folimeld-ready` は修正前の比較用として保持。
解析用VM `Folimeld-FreeBSD-forms-debug`（SSH転送2224番）は停止して保存した。

GUI検証用ファイルはゲストの `build/freebsd-forms/forms-source.pdf`、`forms-gui-normal.pdf`、`forms-gui-encrypted.pdf`。
暗号化サンプルのパスワードはテスト専用の `FreeBSD-form-test-2026` で、ユーザーの認証情報ではない。
