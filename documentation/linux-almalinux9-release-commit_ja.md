# AlmaLinux 9公開候補のローカルコミット固定

2026-11-12。[確定ツリー案](linux-almalinux9-release-tree_ja.md)を専用コピー内でローカルコミットへ固定した。元リポジトリへの反映、タグ作成、push、GitHub公開は行っていない。

## 固定した参照

```text
ブランチ: release/almalinux9-amd64-0.3.5
コミット: 03b14ec8c4410fbc7510aa9bedb27950e78cfc6e
ツリー: b6c719a04ab38ec9befb2ec61db7c37851f744bb
親: 423e59471b576e4732c7d6ec0ad9ab25cbf19582
```

コミットメッセージは`Prepare AlmaLinux 9 amd64 0.3.5 release candidate`。既存のユーザーGit設定の名前・メールを使用し、署名は付けていない。専用ブランチの旧参照が想定の親を指すことを検査し、その参照だけを更新した。

## 候補との一致

コミット内の686入力をGit blobとして読み出し、revision5対応ソースZIPの各SHA-256と全件一致することを確認した。親の追跡ファイル削除は0件、候補外の既存48パスも保持した。

対応するRPM SHA-256は`0ba2c7dfc397f61b1ca70679838c93589310d116a267249d67dd822b8cb654bc`、対応ソースZIP SHA-256は`f9a6add8b239c0da7f563128242023d880077f89e565cd38eb6ff2c51af4c079`。ビルド時のBuild-sourceが記録した親コミット・当時の作業状態は変更せず、このコミットとの関係を入力blob一致で追加証明した。[コミット検証JSON](linux-almalinux9-release-commit-2026-11-12.json)を参照。

## 増分bundle

同じ専用ディレクトリへ`Folimeld-almalinux9-amd64-0.3.5-local-incremental.bundle`を保存した。7,145,542バイト、SHA-256は`eaec445a294bd5c7f15f691cd8a1309d59748a68915d24912a4b105269fd4694`。`git bundle verify`とlist-headsが成功し、新コミットを指す専用ブランチを確認した。

このbundleは親423e594を前提とする増分で、リポジトリ全体のバックアップではない。shared cloneの作業場所だけに依存せず、親を持つリポジトリへ同じ変更を移せる資料として準備した。[bundle検証JSON](linux-almalinux9-release-bundle-2026-11-12.json)に実パス・前提・検証出力を保存した。元リポジトリへは取り込んでいない。

## 元作業ツリーと公開状態

元Windows側はmain、HEAD423e594のまま、既存の未コミット7ファイルを保持している。アプリ版・README・CHANGELOG・参照も変更していない。候補ソースのLinux固有告知や再生成資産をmainへ混ぜる操作は行っていない。

これで公開候補に対応する不変のローカルコミットを指定できる。公開用タグ名は引き続き`almalinux9-amd64-v0.3.5`の案であり、タグも公開も未作成。元の「公開はまだ実行しない」という指示は維持する。
