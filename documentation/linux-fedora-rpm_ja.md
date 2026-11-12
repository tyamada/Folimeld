# Fedora 45 amd64向けRPMの実装・検証

実施日: 2026-11-12（日本時間）。公開済み成果物ではなく、内部版0.3.3の非公開候補を検証した。READMEの対応済みOS・ダウンロード案内は変更していない。

## 実装

- `bash build_linux.sh rpm`で、共通のPyInstallerビルド後にFedora用RPMを梱包する。引数なしのDEBと`binary`モードは維持する。
- `tools/package_linux_rpm.py`と`packaging/linux/folimeld-fedora.spec.in`を追加した。Fedora以外ではビルド前に拒否し、openSUSE/AlmaLinux等へ無条件流用しない。
- ファイル名にアプリ版、RPM revision、Fedora版、CPUを含める。既存同名ファイル・出力シンボリックリンクを拒否し、完成品のコピーも排他的に作成する。
- RPM側のstrip等を無効化し、PyInstallerがELFへ追加したアーカイブを保持する。自動依存生成は維持し、Qt用の必須共有ライブラリを明示した。
- 対応ソースZIPとRPMの関連JSONは既存`source_bundle`処理で生成する。SRPMは生成しない。今回、RPMから導入された実行ファイルのハッシュがビルド直後と一致することも検証した。

RPMのタグ・依存宣言は[RPM公式のspec形式資料](https://rpm.org/docs/latest/manual/spec.html)を参照した。これはFedora公式リポジトリへの登録用レシピではなく、独立した実行ファイルを配るためのローカル梱包である。

## 環境とビルド手順

既存環境とは別に、Cドライブへ次のWSL2を作成した。

| 用途 | 登録名 | Windows配置 |
| --- | --- | --- |
| ビルド | `Folimeld-Fedora45-Amd64-Build` | `C:\Users\takum\WSL\Folimeld-Fedora45-Amd64-Build` |
| 導入試験 | `Folimeld-Fedora45-Amd64-Test` | `C:\Users\takum\WSL\Folimeld-Fedora45-Amd64-Test` |

両方をFedora 45へ更新した。標準Pythonは3.15で、ビルドには別途Python 3.14.10を使用した。glibcは2.44、RPMは6.1.0、CPUはx86_64。固定依存がすべてwheelで解決することを事前確認した。PySide6 6.11.2、PyMuPDF 1.28.2、Pillow 12.3.0、cryptography 50.0.2、PyInstaller 6.22.2を使用した。

ビルド環境の準備例（専用Fedora環境内だけで実行）:

```bash
sudo dnf install python3.14 python3-pip rpm-build binutils git file dbus-libs \
  libglvnd-egl libglvnd-glx libxkbcommon-x11 xcb-util-cursor \
  xcb-util-wm xcb-util-keysyms libxcb fontconfig
```

未コミット差分を保持した専用ソースコピーのルートで、未使用の候補ディレクトリを指定する。通常の作業ツリーや既存配布物の上では実行しない。

```bash
candidate="$HOME/folimeld-candidates/fedora45-new-candidate"
mkdir -p "$candidate/tmp" "$candidate/cache/pip" "$candidate/cache/pyinstaller"
FOLIMELD_LINUX_PYTHON=python3.14 \
FOLIMELD_LINUX_VENV="$candidate/venv" \
FOLIMELD_LINUX_OUTPUT="$candidate/packages" \
FOLIMELD_RPM_REVISION=4 \
TMPDIR="$candidate/tmp" \
XDG_CACHE_HOME="$candidate/cache" \
PIP_CACHE_DIR="$candidate/cache/pip" \
PYINSTALLER_CONFIG_DIR="$candidate/cache/pyinstaller" \
bash build_linux.sh rpm
```

`FOLIMELD_LINUX_PYTHON`は新規仮想環境の作成に使う。既存仮想環境は作り直さないため、Python版を変える場合は新しい`FOLIMELD_LINUX_VENV`を指定する。`FOLIMELD_RPM_REVISION`は正の整数、既定値は1。出力先の既定は`releases/fedora/<Fedora版>/<RPM CPU名>/`。

## 候補と検証結果

最終候補:

```text
/home/folimeld-build/folimeld-candidates/fedora45-20261112/packages/folimeld-0.3.3-4.fc45.x86_64.rpm
SHA-256: 8cd4a8a4257a0543f1b6f40a3848711c14711ce67f54efe14fbd9394a65c4090
```

ビルド直後・RPM導入後のELFのSHA-256はともに`88d3979a88ebdefb59cc064c01bb7a1d14ce81a3832407cf488111310a659800`。埋め込みコミット情報を維持し、対応ソースZIPのハッシュ一致とVirtual Keyboard関連0件を確認した。revision4は後述の描画修正を含む。

| 項目 | 結果 |
| --- | --- |
| 単体・回帰テスト | 基礎検証106件・24サブテスト成功。描画修正後は107件・24サブテスト成功（5.95秒）。RPMの出力名・別OS拒否・上書き/リンク拒否の追加6件を含む |
| 静的確認 | 追加したRPM実装・テストのruff、シェル構文、git diff --check、記録の相対リンク確認が成功 |
| 必須依存のみの導入 | 新規Fedoraへ`install_weak_deps=False`で導入。gcc、rpm-build、pip、Python 3.14、日本語推奨フォントはいずれも未導入の状態を保存 |
| 一般ユーザー起動 | revision2/3でoffscreen/xcb各12秒の生存を確認。revision4は後段の実画面試験を実施 |
| 更新・削除・再導入 | revision1→2→3→4の更新が成功。revision2で削除時の実行ファイル・desktop項目・アイコン・ライセンス消失を確認し、再導入後のハッシュも一致 |
| RPM/DNF整合性 | `rpm -V folimeld`と`dnf check`が成功 |
| 実画面 | GUIツール・日本語フォント追加後、revision3で日本語PDF表示・ページ移動・回転・別名保存・GUI再読込を確認。revision4で回転直後とUndo/Redoの描画を確認 |
| 保存データ | revision3で3ページ、元のページ順`[2, 1, 3]`、回転`[0, 90, 0]`、文字内容保持、原本SHA-256不変 |

画面証拠: [初期表示](linux-amd64-fedora45-gui-verification/01-loaded.png)、[ページ移動](linux-amd64-fedora45-gui-verification/02-page-moved.png)、[保存後](linux-amd64-fedora45-gui-verification/03-saved.png)、[再読込](linux-amd64-fedora45-gui-verification/04-reopened.png)。Windows画面APIではなく、Linux側のX11ウィンドウを対象IDで識別・撮影した。

詳細なパッケージ一覧、依存、起動結果、更新・削除コマンドは[基礎検証JSON（revision1〜3）](linux-amd64-fedora45-verification-2026-11-12.json)を、最新候補の対応ソース・ハッシュ・描画試験は[描画修正記録（revision4）](linux-thumbnail-redraw-verification_ja.md)を参照する。

## 検証で修正した点と制約

- 最初のrevision1はDBusライブラリ不足で実行時に失敗した。ビルド環境のQt importでも再現し、`libdbus-1.so.3()(64bit)`を必須依存へ追加した。試験環境へ手動で補わず、revision2の依存解決で導入されることを確認した。
- 推奨フォント名をFedora 45で実在する`google-noto-sans-cjk-fonts`へ修正した候補がrevision3である。失敗候補とログは保持している。
- 回転直後の空白は、非同期アイコン生成後も配置位置が空アイコン時のまま残ることが原因と判明した。Qtへサイズ変更を通知する修正をrevision4へ含め、保存・別操作なしの表示を確認した。[詳細](linux-thumbnail-redraw-verification_ja.md)
- 続いてrevision4の日本語IME、画像取込、暗号化PDFの編集・保存・再認証をFedoraの実画面で確認した。[追加GUI検証](linux-fedora-extended-gui-verification_ja.md)。完全なLinuxデスクトップ操作は未検証。Kaliの結果をFedoraの合格として流用していない。
- Fedora 44、ARM64、他のRPM系OSは未検証。今回のRPMはビルド環境に合わせglibc 2.44以上を要求し、古いOSへの互換性を主張しない。
- `%changelog`がないため、RPMの`source_date_epoch_from_changelog`警告が残る。生成と検証は成功したが、再現ビルドの保証ではない。起動時のWSL systemdユーザーセッション警告についてWindows/WSL設定は変更していない。
- アプリ版は0.3.3の検証用のまま。依存ソース・ライセンスの公開前確認、版の統合、公開作業は未実施。既存Ubuntu/Debian/Kali、既存配布物、Windows/macOS/BSDの版は変更していない。
