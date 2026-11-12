# AlmaLinux 9候補のPillow構成要素・パッチ・LZW告知確認

2026-11-12。[公開準備](linux-almalinux9-release-readiness_ja.md)の続きとして、保存済みwheel SBOMと対応ソースを具体的なファイル単位で照合した。

## 対応が確認できた項目

- Pillow公式固定コミットの`.github/generate-sbom.py`を取得し、保存済みGit treeのblob IDと照合。コードを実行せず、SBOMのハッシュ対象を読んで特定した。
- `fribidi-shim/fribidi.c`、`pythoncapi_compat.h`、`raqm/raqm.c`の3ファイルについて、収集済みPillow sdistのSHA-256が実wheelのSBOMに記載された値と一致した。
- upstream libraqm v0.10.5の2ファイルへ、wheel SBOM由来の2パッチをfuzzなしで適用。生成内容はPillow sdistの`raqm.c`・`raqm-version.h`とバイト一致した。GNU patchは異なる旧新ファイル名のパッチを旧名に適用したため、名前ではなく生成内容を照合した。
- 収集済みLibTIFF 4.7.1の`libtiff/tif_getimage.c`へ、SBOM由来の変更パッチがfuzzなしで適用できた。これは適用可能性の確認であり、wheelのビルドフラグの証明ではない。

初回のraqm生成ファイル名の想定、続くLibTIFFパッチの`-p1`指定で検査が失敗した。旧コピーは保持し、新規監査コピーで前者の内容照合と後者の`-p0`指定を修正して成功した。外部のビルドスクリプトは実行していない。

## 見つかった告知漏れ

0.3.5 revision1候補内の`pillow.libs`のLibTIFFには`TIFFInitLZW`が存在する。一方、候補内の全`licenses/*.txt`を調べても、LibTIFFソースのLZW部分にあるBerkeley告知全文は見つからなかった。wheelのLICENSE本文にもBerkeleyの記載はなかった。

収集済み`tiff-4.7.1/libtiff/tif_lzw.c`から、先頭の著作権・許諾文とBerkeley由来コードの著作権・許諾文をそのまま抽出し、`licenses/LibTIFF-LZW.txt`を追加した。既存の告知を削除・置換せず、日英公開説明案にもBerkeleyへの謝辞を追加した。

取得先、ファイルハッシュ、パッチコマンド結果、告知抽出元、旧候補での検索結果は[検証JSON](linux-almalinux9-pillow-component-review-2026-11-12.json)を参照。

## 候補への反映

既存0.3.5 revision1は保持し、新しい専用`alma9-035-lzw-r2-20261112`コピーで補足告知を含むrevision2を作成した。アプリの機能コード・版は保持し、補足告知と監査状態の説明のみを変更した。revision1の配布準備物は履歴として残し、そのまま公開しない。

ライセンス・ソース・Alma RPMの15テスト・9サブテストが成功。初回のPyInstaller実行は新コピーにGit情報もSOURCE-MANIFEST.jsonもなく停止したため、専用コピー内へGit情報のコピーを補い、再実行で成功した。失敗ログは保持した。元作業ツリーのGit情報は変更していない。

実行ファイル内と対応ZIP内の補足告知が原文と一致し、対応ソース679入力の全ハッシュが一致した。全`folimeld/`入力と210 ELFはrevision1とバイト一致し、Virtual Keyboard関連は0件。RPMとELF・対応ソースの関連も照合した。[revision2ビルド検証JSON](linux-almalinux9-035-lzw-r2-verification-2026-11-12.json)に記録した。

```text
folimeld-0.3.5-2.alma9_8.x86_64.rpm
RPM SHA-256: 9f36b61f85fe6fbd32cce94af2b727f7fb62e0b4286ab977ea21498583498a70
ELF SHA-256: 5b18292874ed3ec0b7865f26b83baae5fa4a7c79e62163c82ab22704cd52d587
```

専用Testでrevision1からrevision2への更新、ELF一致、`rpm -V folimeld`、`dnf check`が成功した。一般ユーザーの新規プロフィールでoffscreen・xcb各12秒の起動も成功し、試験プロセスを終了した。[更新・起動JSON](linux-almalinux9-035-lzw-r2-update-2026-11-12.json)を参照。新候補のライセンス画面・配布準備物の再作成と最終照合は後続とし、旧候補の機能回帰を新候補の全項目再試験とは呼ばない。

この確認で、vendored 3ファイルとraqmパッチの対応を具体化できた。可変取得先を含むwheel全体の過去入力、Qt/MuPDF等の内包第三者コード、すべての必要告知の確認が完了したという意味ではない。公開は行っていない。

後続の[revision2公開準備](linux-almalinux9-release-readiness_ja.md#revision2の画面確認資料再作成)で、補足告知タブ・Berkeley本文の実表示、配布準備物の再作成、全添付物のチェックサム確認まで完了した。
