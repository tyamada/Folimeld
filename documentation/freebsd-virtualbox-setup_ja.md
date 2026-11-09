# FreeBSD VirtualBox検証環境

作業日: 2026-11-09（日本時間）。この文書は構築記録であり、FreeBSD対応の宣言ではない。

## 動作確認結果（初回構築時）

フォーム読み込みの異常終了は後続作業で修正済み。[原因・修正・全件テスト結果](freebsd-forms-fix_ja.md) を参照。現在の起動先はPyMuPDF 1.28.2を導入した `.venv-freebsd`。

後続の実GUI操作による確認は [FreeBSDでのGUI操作確認](freebsd-gui-verification_ja.md) を参照。

- Xfceの日本語デスクトップを一般ユーザーで起動。Guest Additionsのサービス起動と解像度変更を確認。
- VM移動・スナップショット保存後の再起動でも、永続保存した鍵でSSH接続でき、日本時間の表示とGUI起動を確認。初回はFolimeldで `testdata/tameshibu_episode3_ja.pdf`（8ページ）の表示を確認。
- 実画面のFolimeldをスクリプトから操作し、4ページPDFの読み込み、先頭ページの90度回転、日本語・空白を含む名前への保存、再読込を確認。
- pytest全件実行は `tests/test_save_contents.py` のフォーム情報読み込みで `Illegal instruction` により終了。**全件合格ではない**。
- 同ファイルの4パラメーターケースを明示的に除いた実行は **374 passed、9 skipped、32 subtests passed**。
- Ruff、mypy（対象3ファイル）、`pip check` は成功。
- 初回のフォーム情報の異常終了は、FolimeldとQtを使わないPyMuPDF単独コードでも再現（終了コード132）。その時点では原因の特定と修正は未実施だった。

証跡は [freebsd-verification/](freebsd-verification/) に保存。[GUI画像](freebsd-verification/gui-smoke.png)、[残りのテスト結果](freebsd-verification/pytest-excluding-save-contents.log)、[全件実行時の異常終了](freebsd-verification/pytest.log)、[最小再現コード](freebsd-verification/pymupdf-form-reproducer.py)、[mypy結果](freebsd-verification/mypy.log) を参照。
[再起動後のデスクトップ画像](freebsd-verification/desktop.png) にはリポジトリ付属の上記サンプルPDFを表示している。

## ホストとVM

- Windows 11、Intel Core i7-10700K、16論理CPU、メモリ約64 GB。
- VirtualBox 7.2.16r174877。新規VMを作成。既存の `FreeBSD15` は専用VDIが実使用約2 MBの未導入構成で、ユーザーの削除指示を受けて登録解除・専用ディスクの削除を完了。
- VirtualBoxログはVT-x直接利用からNEM（Windows Hypervisor Platform）へのフォールバックを記録。ホスト設定は変更していない。
- VM名: `Folimeld-FreeBSD-15.1-amd64`。
- メモリ8 GB、4 vCPU、VBoxSVGA、VRAM 128 MB、3D無効、BIOS起動。
- ディスク: 可変容量VDI 80 GB。最終保存先は `C:\Users\takum\VirtualBox VMs\Folimeld-FreeBSD-15.1-amd64`。構築用の `build/` から移動済み。
- RTCはUTC。GUIセッションの `LANG=ja_JP.UTF-8`、`TZ=Asia/Tokyo` を設定。
- NAT。SSH転送は `127.0.0.1:2223` → ゲスト22番。既存VMの2222番とは独立。

## インストールメディア

[公式配布情報](https://www.freebsd.org/where/)で正式版を確認し、[公式ISOディレクトリ](https://download.freebsd.org/releases/amd64/amd64/ISO-IMAGES/15.1/)から取得。

- `FreeBSD-15.1-RELEASE-amd64-disc1.iso`
- SHA-256: `fa27646f05a1440fd26ffbb85e06a50bc86e128242a4e9cb7bb3ea76e1aa5fd9`
- 公式 `CHECKSUM.SHA256-FreeBSD-15.1-RELEASE-amd64` と実ファイルのハッシュが一致。

## 構築方法

ISOのWelcome画面からShellを選び、`bsdinstall script` を使用する。
対象はこの新規VMの `ada0` のみ。GPT、4 GB swap、残りをUFSルートに割り当てる。
インストール設定は `build/freebsd-vm/http/install.conf` に保存。

ISO内には従来形式の `base.txz` と `kernel.txz` がなく、Shell起動時の `/etc/resolv.conf` も存在しなかったため、最初の配布取得はDNSエラーで失敗。
作成済みパーティションを使い、公式の配布ファイルをホストで取得し、ISO内MANIFESTのSHA-256と照合して展開する復旧手順を `build/freebsd-vm/http/resume.sh` に保存。
メディアの `/tmp` は小容量なので、配布ファイルは仮想ディスク上の `/mnt/.install-dist/` に置く。
復旧時には `/etc/fstab` も明示的に作成する必要があった。最終設定は次のとおり。

```text
/dev/ada0p3 / ufs rw 1 1
/dev/ada0p1 none swap sw 0 0
```

- ホスト名 `folimeld-freebsd`、`em0` はDHCP、タイムゾーン `Asia/Tokyo`。
- 一般ユーザー `folimeld` と専用SSH鍵を用意。
- SSH秘密鍵は `C:\Users\takum\.ssh\folimeld_freebsd_ed25519`。公開鍵と専用known_hostsも同ディレクトリへ保管。Gitへ追加しない。
- rootのSSH接続は鍵認証のみ。ローカル初期パスワードはゲストのroot専用ファイルに保存し、公開文書には記載しない。
- 設定転送用HTTPサーバーはホストのloopbackのみで待受し、インストール設定だけを提供。転送後に停止する。

SSH接続例（PowerShell）:

```powershell
ssh -i "$env:USERPROFILE/.ssh/folimeld_freebsd_ed25519" -o "UserKnownHostsFile=$env:USERPROFILE/.ssh/folimeld_freebsd_known_hosts" -p 2223 folimeld@127.0.0.1
```

## 構築と検証の手順

1. ISOを外して仮想ディスクから起動し、SSHとバージョンを確認。
2. OS更新を適用し、再起動後にOSとカーネルの版を確認。
3. Xorg、Xfce、CJKフォント、適合するGuest Additionsを導入。
4. 一般ユーザーのXfceセッションで画面表示・解像度変更を確認。
5. Git、Python、PySide6、PyMuPDF、Pillow、cryptographyとテスト依存を導入。
6. 対象コミットと依存バージョンを記録してFolimeldを配置。起動・PDF保存・pytest実行後、既知の異常終了を記録して正常停止。`03-folimeld-ready` を取得済み（UUID `daade0ee-5ea7-453a-8a41-c80e591d8592`）。

FreeBSD用パッケージ名とPython flavorは、実際のパッケージリポジトリで確認してから確定する。
既存のWindows向け制約と異なる版を使用する場合、その差分を記録する。

## ソースとパッケージ

ソースはコミット `d0f22517c65e41d9259fa634f8e0da3722f5a97e` を `git archive` で転送。
配布済みバイナリを含む `releases/` は転送対象外。配置先は `/home/folimeld/Folimeld`。
コミットは同ディレクトリの `SOURCE-COMMIT` にも記録。

公式quarterlyリポジトリでPython 3.12向けPySide6 6.11.2、PyMuPDF 1.27.2.2、Pillow 13.0.0、cryptography 50.0.1の提供を確認。
これはWindows用 `constraints-release.txt` の完全再現ではない。

OS更新は疑似端末を付けたSSHで `env PAGER=cat freebsd-update fetch install` を実行。
進行ログはゲストの `/root/freebsd-update.log` に保存。

更新適用後はインストール済みカーネルが `15.1-RELEASE-p5`、ユーザーランドが `15.1-RELEASE-p6` となった（再起動前の確認値）。
ライブスナップショット `01-base` の作成は `LiveSnapshotting` で停止し、SSHと通常の停止要求にも応答しなくなった。
新規VMのUUIDに一致するプロセスのみを終了し、再起動。スナップショットは作成されていない。
以後のスナップショットは正常シャットダウンした状態で作成する。

GUI構築スクリプトは `build/freebsd-vm/setup-desktop.sh`。一般ユーザー `folimeld` でデスクトップを自動起動するローカル検証用構成とし、デスクトップにFolimeld起動アイコンを配置する。

実行環境の導入コマンド:

```sh
pkg install -y xorg-minimal xfce slim virtualbox-ose-additions-72 \
  noto-sans-jp noto-sans-sc noto-sans-tc noto-sans-kr \
  git-lite python312 py312-pip py312-pyside6 py312-pymupdf \
  py312-pillow py312-cryptography py312-pytest py312-psutil ruff
sysrc dbus_enable=YES slim_enable=YES vboxguest_enable=YES vboxservice_enable=YES
```

FreeBSDパッケージのPySide6は多くのQtモジュールを依存に含み、コンパイラー等も間接依存として取得される。
`requirements-dev.txt` をそのままpipに渡してPyInstallerまで導入する手順は、今回は使用しない。
既存テストのため `py312-pyinstaller` と `py312-ruff`、mypyのため `py312-sqlite3` を追加した。
PyInstallerパッケージの導入は配布用実行ファイルのビルド成功を意味しない。

一般ユーザーの検証環境:

```sh
cd /home/folimeld/Folimeld
python3.12 -m venv --system-site-packages .venv-freebsd
MYPY_USE_MYPYC=0 .venv-freebsd/bin/python -m pip install 'mypy>=1.18,<2'
.venv-freebsd/bin/python -m ruff check folimeld tests tools main.py
.venv-freebsd/bin/python -m mypy
.venv-freebsd/bin/python -m pip check
QT_QPA_PLATFORM=offscreen .venv-freebsd/bin/python -m pytest -q -p no:cacheprovider \
  --ignore=tests/test_save_contents.py
```

上記のpytestは既知の異常終了箇所を除外する診断用コマンド。完全な検証では、除外を外して再現状況を確認する。
`.venv-freebsd` はシステムパッケージを参照するため、`pkg upgrade` 後は検証をやり直す。

参考: [FreeBSDのVirtualBoxゲスト設定](https://docs.freebsd.org/en/books/handbook/virtualization/#virtualization-guest-virtualbox)、[bsdinstall(8)](https://man.freebsd.org/cgi/man.cgi?query=bsdinstall&sektion=8&format=html)。
