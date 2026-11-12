# AlmaLinux9 revision3の新規最小依存installroot確認

実施日: 2026-11-12（日本時間）。[削除再導入・GIO確認](linux-almalinux9-revision3-lifecycle_ja.md)の続き。許可済み`Folimeld-AlmaLinux9-Amd64-Test`の中に独立したDNFインストール先を作成した。新しいWSL登録や既存Test環境の再初期化は行っていない。

```text
/root/folimeld-verification/revision3-minroot-20261112/root
```

## 導入条件

空のディレクトリへ、標準BaseOS/AppStreamだけを当該コマンドで指定し、weak dependenciesを無効にして`folimeld-0.3.3-3.alma9_8.x86_64.rpm`を導入した。AlmaLinux9鍵は独立したRPMデータベースへ取り込み、既存Test環境の信頼鍵・リポジトリ・暗号ポリシーを変更していない。

```text
dnf -y --installroot=<上記root> --releasever=9
  --setopt=install_weak_deps=False --setopt=reposdir=/etc/yum.repos.d
  --disablerepo=* --enablerepo=baseos --enablerepo=appstream
  install <revision3 RPM>
```

この表示は読みやすさのため改行したもので、実際の引数配列は検証JSONに保存している。導入トランザクションは104パッケージ、鍵を含むRPM一覧は105件。fontconfig等の必須依存が選ぶDejaVu・英語基本フォントを含むため、完全なフォントなし環境とは扱わない。

新しいroot内に次がないことをRPM一覧で確認した。

- python3、python3.12、python3.12-libs、python3-pip
- gcc、rpm-build
- epel-release
- 推奨のgoogle-noto-sans-cjk-ttc-fonts

既存Test環境のGUIツールやPythonを、このroot内のアプリ実行依存として利用していない。

## 起動と整合性

必要最小限の`/dev/null/zero/random/urandom`と専用HOME・XDG設定を用意し、ホスト側のchrootコマンドから`--userspec=1000:1000 --groups=1000`で実行した。PATH/HOME/LANG等は明示した小さな環境変数集合に限定し、Qtはoffscreenを指定した。procやWSLgソケットのbind mountは行っていない。

```text
/usr/sbin/chroot --userspec=1000:1000 --groups=1000 <root> /usr/bin/folimeld
```

12秒後も起動しており、試験終了のため停止した。ログはfitzの非推奨警告とoffscreenプラグインの警告を保持する。root内のELF SHA-256は新候補と同じ`b0915988edbfcea48704cf013f5961b5c496d7b6689a888f019cff9034f46455`。`rpm --root <root> -V folimeld`と`dnf --installroot=<root> --releasever=9 check`が成功した。

既存Test環境側の候補ELFも同じハッシュのまま、前回のPDF・設定6ファイルも保持した。試験後にFolimeldプロセスが残っていないことを確認した。

## 試験準備時の修正

DNF scriptletが新root内に空の通常ファイル`dev/null`を作成していたため、初回のデバイス検査が停止した。新root内・非リンク・通常ファイル・0バイトであることを確認して、その1ファイルだけを削除し文字デバイスに置換した。既存WSL側の`/dev/null`には触れていない。

次の起動準備では、明示したPATHに`/usr/sbin`がないためchrootを見つけられなかった。ホストのchroot絶対パスを先に解決して再実行した。これらはアプリ起動前の試験準備の修正であり、アプリの実行失敗とは区別する。

導入コマンド・全ログ・RPM一覧・未導入確認・実行環境・終了コード・ハッシュ・既存ファイル保持は[検証JSON](linux-almalinux9-revision3-minroot-verification-2026-11-12.json)へ保存した。libgpg-errorというパッケージ名を警告と誤検出しない条件で、導入ログのwarning/error行を抽出した。

## 結果の範囲

新規DNF installrootで、Python・ビルド依存・EPEL・推奨CJKフォントの追加なしに凍結アプリを起動できた。独立したWSLのブート、通常デスクトップ、WSLg GUI/IMEをこのroot内で実施した結果ではない。chrootをセキュリティ隔離の保証としても扱わない。

新ELFの主要WSLg機能は[前回のGUI回帰](linux-almalinux9-revision3-regression_ja.md)で別に確認している。通常デスクトップ・アプリ版間/設定移行、公開版との差分統合・版決定、wheelビルド来歴とAlma8 libXau署名は引き続き残る。既存変更・候補・配布物を保持し、公開は行っていない。
