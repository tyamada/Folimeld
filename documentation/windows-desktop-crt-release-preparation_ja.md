# Desktop初回候補：CRTと未署名方針の準備

2026-11-16。ユーザー確認により、個人開発者が自分のアプリを配布する区分、初回は未署名候補として準備し公開前に注意事項を確認する方針を記録しました。有料証明書は購入しません。

## 今回進めたこと

- 正規CRT14.44.35211.0の7ファイルをサイズ/SHA256で再照合。予定配置_internalを由来台帳へ結び付けました。
- 正規Redist埋込の英語Runtime条件（u4、9235bytes）を既存抽出台帳のSHAで照合し、原RTFのままDesktop資料へ配置。
- 現アプリソース0.3.5に合わせ、Desktop初回候補の数値版0.3.5.0と専用版情報入力をworkに準備。Store版のID/版/設定は変更しません。公開タグは未作成。
- 利用者向け案：未署名のため署名済み発行元を確認できないこと、SmartScreen等の表示が起こり得ること、HTTPSの正規公開先とSHA256を確認することを案内する。保護機能を一括無効にする手順は案内しない。一般的なSHA一致は発行元認証や安全性の証明とは分ける。

## CRT条件提示の残件

Microsoft公式Distributable Listは、適法に利用するVisual Studioの条件に従った未改変配布を対象とします。今回の個人開発という申告は利用区分の根拠で、契約上の全要件を自動完了するものではありません。

保存済みVS Community原文には、アプリへの主要機能の付加と、外部利用者/再配布者がDistributable Codeを保護する条件へ同意する要求があります。現在のInno候補はLicenseFileをまだ設定していないため、原文をコピーしただけで同意手続きを実装済みとは扱いません。

次に必要な具体化は、Microsoft Runtimeだけに適用する条件の提示/同意と、AGPLアプリ/他OSSの権利を制限しない分離です。VS開発者契約とRuntime利用者契約を同一視せず、RTF表示だけで全保護条件を満たしたと断定しません。現在のInno設定や固定ガードは今回変更していません。

## ビルド/試験公開まで

Qt wheel固有の変更/必要ソース、Pillow/MuPDF等の条件/ソース残件と、このCRT条件提示の点検を終え、実際に点検できた資料の台帳を用意する必要があります。承認済みを装うreviewed-files.jsonは作りません。
その後、onedir→実payload/資料突合→Inno→起動/PDF/画像/3ワーカー/DPI/インストール更新削除の受入→試験公開の順序です。ユーザーはビルドと試験公開を指示済みですが、現時点は前提整備中でビルド・公開はまだ実行していません。

コミット/プッシュ・試験PC更新・WACK・Hosted API比較は行いません。uv開発中止を維持。新規課金・モデル呼出なし。

公式根拠：
https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution
https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170
