# 回転後のサムネイル欠けの修正・検証

実施日: 2026-11-12（日本時間）。Kali/FedoraのWSLg検証で残っていた、回転直後にプレビューが空白になる問題を調査した。

## 原因と修正

PDF画素とQtアイコンには文字が残り、凍結バイナリでも回転後100ms時点で画像生成が完了していた。一方、アイコンが空だった時点の配置位置が残っていた。診断では幅312pxのグリッドに対し、項目が`x=133, width=294`（右端426px）となり、文字部分がセルの外で切れていた。レイアウト再計算後は`x=9, width=294`へ移動し、回転した文字を表示した。

`folimeld/thumbnails.py`で、非同期にアイコンを設定した直後にdelegateの`sizeHintChanged`を通知するよう修正した。Qtの標準通知により表示項目を再配置する。[Qt公式資料](https://doc.qt.io/qt-6/qabstractitemdelegate.html#sizeHintChanged)

テストも、描画処理を直接呼ぶ方式に加え、実際のQtイベントループで画像生成を待ってグリッド内への収まりを検証する方式を追加した。修正前は`426 < 312`の条件で失敗し、修正後は成功する。

## 検証結果

| 検証 | 結果 |
| --- | --- |
| Fedora / Python 3.14 / xcb | サムネイル関連9件成功。大文書、スクロール、画像再利用、描画キャンセルも含む |
| Fedora全体の対象回帰 | PDF編集・保存・画像・暗号化・表示・ソース対応付け等107件、24サブテスト成功（5.95秒） |
| Ubuntu / Python 3.12 | 専用ソースコピーで関連9件成功（1.29秒）。導入済みアプリは変更していない |
| lint | 変更した描画コードとテストのruff成功 |
| 通常の凍結バイナリ | Fedoraのrevision4で初期表示、回転直後、Undo/Redoの描画を実画面確認。保存・別編集・再起動を挟まず回転内容を表示 |
| 成果物の対応付け | RPM導入後とビルド直後のELFハッシュが一致。対応ソースZIPも照合。通常のmain.pyと描画コードのハッシュが作業ツリーと一致し、診断コードを含まないことを確認 |
| 原本 | 合成検証PDFのSHA-256は不変 |

画面証拠: [修正前](linux-thumbnail-redraw-verification/01-before-fix.png)、[修正後の初期表示](linux-thumbnail-redraw-verification/02-fixed-loaded.png)、[回転直後](linux-thumbnail-redraw-verification/03-fixed-rotated.png)、[Undo](linux-thumbnail-redraw-verification/04-fixed-undo.png)、[Redo](linux-thumbnail-redraw-verification/05-fixed-redo.png)。撮影対象は新規Fedora内の候補ウィンドウだけで、Linux X11経由で取得した。

診断用の凍結バイナリは通常候補とは別コピーにのみ作成した。タイマー・画素・レイアウトの診断結果とテストログは[検証JSON](linux-thumbnail-redraw-verification-2026-11-12.json)に保存している。

## 更新した非公開候補

```text
/home/folimeld-build/folimeld-candidates/fedora45-20261112/packages/folimeld-0.3.3-4.fc45.x86_64.rpm
RPM SHA-256: 8cd4a8a4257a0543f1b6f40a3848711c14711ce67f54efe14fbd9394a65c4090
ELF SHA-256: 88d3979a88ebdefb59cc064c01bb7a1d14ce81a3832407cf488111310a659800
```

新規Fedora試験環境だけをrevision3から4へ更新し、`rpm -V`と`dnf check`が成功した。revision4のGUI試験は、前回追加したGUIツールがある環境で実施した。最小依存での導入・削除・再導入は[従来の記録](linux-fedora-rpm_ja.md)と区別する。

続いてUbuntuで修正入りDEBを再ビルドし、新規Kaliへ再導入して回転直後・Undo/Redo・保存再読込を確認した。Ubuntuの導入済み0.3.4は保持し、専用ディレクトリで展開起動だけを確認した。[DEBの追加検証記録](linux-deb-thumbnail-fix-verification_ja.md)。Windows/macOSや完全なLinuxデスクトップの描画は未検証。アプリ版は0.3.3の非公開検証用のまま、READMEの対応済み表記や既存配布物を変更せず、公開も行っていない。
