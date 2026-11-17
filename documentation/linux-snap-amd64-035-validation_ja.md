# Ubuntu amd64 strict Snap 0.3.5 の検証

[日本語](linux-snap-amd64-035-validation_ja.md) | [English](linux-snap-amd64-035-validation.md)

2026-11-17（日本時間）。Ubuntu 24.04.5 LTS amd64（WSL2 / WSLg）環境にて、Folimeld 0.3.5 amd64 向け strict Snap パッケージのビルド、インストールおよび動作確認を実施しました。

## パッケージ情報

- **パッケージ名**: `folimeld_0.3.5_amd64.snap`
- **ファイルサイズ**: 106,164,224 bytes
- **SHA-256**: `ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570`
- **内包実行ファイル**: `dist/folimeld`（SHA-256: `65852198ae2282b8b49e52e4bd3583b0ee131e287a52aa73368f03c2817a47aa`）
- **対応ソーススナップショット**: `dist/source/Folimeld-source-a7683298b15e7326d100b54e0c1083e7fc12af3b5e3d19d329cfc417032ee545.zip`（SHA-256: `a7683298b15e7326d100b54e0c1083e7fc12af3b5e3d19d329cfc417032ee545`）
- **関連付け記録**: `dist/source/folimeld_0.3.5_amd64.snap-ff71a176dba771542998b5bf48f7d89e9d118f34c937c620de897af0e4dc4570.json`

## ビルド環境および設定

- **OS**: Ubuntu 24.04.5 LTS (Noble Numbat) amd64
- **Snapcraft**: 9.2.1
- **Base**: `core24`
- **Confinement**: `strict`
- **Grade**: `stable`
- **Extensions**: `gnome` (`gnome-46-2404`, `gtk-common-themes`, `mesa-2404`)

## 受入確認結果

1. **インストール検証**:
   - `sudo snap install --dangerous releases/ubuntu/folimeld_0.3.5_amd64.snap` にて導入完了。
   - `snap list folimeld` にてバージョン `0.3.5`（リビジョン `x2`）を確認。
2. **インターフェース接続確認**:
   - `snap connections folimeld` にて `desktop`, `desktop-legacy`, `wayland`, `x11`, `opengl`, `gsettings`, `home`, `gnome-46-2404`, `gpu-2404`, `gtk-3-themes`, `icon-themes`, `sound-themes` のスロット接続を確認。
3. **オフスクリーンGUI実行確認**:
   - `QT_QPA_PLATFORM=offscreen timeout 5s snap run folimeld` にて PySide6 Qt GUI 初期化、PyMuPDF ロード、ウィンドウ生成および正常稼働を確認。
