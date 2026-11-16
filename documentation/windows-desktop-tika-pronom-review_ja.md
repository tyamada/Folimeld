# Tika / PRONOM / OGL3.0とQt加工版の対応（未承認）

2026-11-16。固定Tikaコミットc29724782854bb5a319f4a1940d0828a58ace3f9のNOTICE/元XMLと、Qt6.11.2公式ソースの加工XML/加工スクリプトを静的に点検しました。生成スクリプト・アプリ・DLLは実行していません。

## 適用範囲として確認できたこと

- 固定Tika NOTICEは、MIME定義にPRONOMから適応した部分があり、PRONOMはOGL3.0で公開されると記載しています。元XML/Qt加工版の双方にもPRONOMへの明示参照が残ります。
- 元XMLは1683、Qt加工版は1653種類の一意なMIME定義。Qtで7種類追加・37種類削除され、型/offsetの補完、値の変換、未対応ルールのコメント化等があります。定義数はルール数や配布物数ではありません。
- 明示PRONOMマーカーは5種類のMIME定義に6件あり、Qt版でも全6件の本文が保持されています。一部は_comment→commentへのタグ名変更があります。残るルールの全由来を示す完全台帳ではありません。

| MIME定義 | Qt加工版との対応 | 有効なmatch要素数（元→Qt） |
|---|---|---|
| application/x-fat-diskimage | 出典本文を保持。変換・コメント化は台帳参照。 | 3 → 2 |
| application/x-mach-o | 出典本文を保持。変換・コメント化は台帳参照。 | 4 → 4 |
| application/x-ms-compress-szdd | 出典本文を保持。変換・コメント化は台帳参照。 | 1 → 1 |
| application/x-ms-owner | 出典本文を保持。変換・コメント化は台帳参照。 | 1 → 0 |
| audio/mpeg | 出典本文を保持。変換・コメント化は台帳参照。 | 15 → 13 |

application/x-ms-ownerではmatch要素が0となっても、定義/出典コメントとコメント化したルールはソースに残ります。audio/mpegのPRONOM由来MP3ルールも残っています。削除/無効化した部分があることからOGL表示が不要とは判断しません。

## 必要な告知の案

OGL3.0公式原文は、提供者が指定する出典表示（指定がなければ標準文）と、可能な場合のライセンスリンクを求めています。改変や商用利用も扱いますが、公式性/推奨の誤認を許すものではありません。

今回確認したPRONOM aboutページと固定Tika NOTICEから専用の指定文は見つからなかったため、案には「PRONOM / The National Archives (UK)」の出典・URLに加え、OGLの標準文とv3.0リンクを記載します。専用文がどこにも存在しないという断定ではありません。ロゴの使用や新しい著作権年の推定は行いません。

[英語の告知下書き](windows-desktop-licenses/TIKA-PRONOM-NOTICE.draft.txt)を整備しました。Tika由来MIMEデータを一つの範囲として保守的に出典表示し、明示マーカー5定義だけに表示対象を狭めません。Qt全体・アプリ全体をOGLへ再許諾するものではなく、Apache2.0/Qt/Folimeld各条件は別に保持します。OGLへのリンクは案に含みます。OGL原文全文の同梱は本件の標準文/リンク条件とは区別して、点検資料として保管します。

Apache NOTICEから、Tika/ASF表示、PRONOM/OGL記載、IPTC表示を元の文面のまま抜粋して併記しました。Javaサーバー等、今回のMIMEデータと別の部品までQtへ含まれるとは扱いません。IPTCの正確な適用範囲は別途点検を継続し、OGLが第三者の全権利まで許諾するとはしません。

## 初回onedirビルド前に残る不足

1. この告知案をDesktop最終告知・ライセンス/ソース索引へ組み込み、提供者の追加指定文の有無と、IPTC等の必要表示を最終点検する。表示方法は既存の告知/同梱資料を使う案で、アプリ画面は変更していません。
2. Tika原XML・Qt加工XML・差分・必要な加工スクリプトを版別の対応ソース提供集合へ結び付ける。Qt側の追加変更とライセンス条件の充足を点検し、完了後にのみ点検済み資料台帳を作る。
3. 実wheelの構成/追加変更の説明は未完。QtCoreのQMimeDatabase APIの存在だけで加工XML全体の埋込を証明したとはしない。実payloadの収録確認は承認後の生成工程へ分ける。

この点検により「OGL原文未参照」「PRONOM由来の残存未確認」「告知案未作成」は解消しました。全配布資料の承認は未完です。

## 再現性・来歴の別調査

- 元となったPRONOMの歴史的リリースと、未標記ルール全件の個別来歴は未確定。component全体への出典表示を採るため、この全件同定を標準告知作成の前提にはしません。第三者権利/専用表示の具体的な不足が見つかれば、再現性だけの問題として棚上げしません。
- Qt加工スクリプトを実行した再生成一致、上流の生成環境、QtCore埋込データとの完全一致、全compiler/SDKとwheelバイト再生成は未確認です。今回のXML構造比較は生成処理の実行ではありません。

## 記録・制限

[適用範囲とハッシュ台帳](windows-desktop-licenses/TIKA-PRONOM-SCOPE.draft.json)に元入力・加工後・公式資料のSHA256、5定義のmatch構造/コメントを保存。OGLとPRONOM公式HTMLを原バイトで保持し、読取用テキストは派生物と明記。Web閲覧ツールではOGL本文が403でしたが、同じ公式URLを通常の読取取得で保存でき、条文本文を点検しました。検索結果だけで最終文面を作ったものではありません。

PREBUILD-DRAFT-NOT-APPROVED、reviewed-files.json未作成。uv開発中止を維持。新規課金・モデル呼出・ビルド・コミット・公開・試験PC更新・WACK・Hosted API比較なし。

公式一次資料：
- https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- https://pronom.nationalarchives.gov.uk/about
- https://raw.githubusercontent.com/apache/tika/c29724782854bb5a319f4a1940d0828a58ace3f9/NOTICE.txt


## Tika追加指定表示・IPTC範囲・提供集合（2026-11-16）

IPTC2010 Photo Metadata説明文の明示出所を固定Tika Java2クラスに特定。Qt MIME subsetにJavaはなく、IPTC名のMIME10定義と説明文を同一視しない。長文95ブロックの比較は完全一致0件（権利不存在の保証ではない）。追加でMIME情報のIan F. Darwin由来BSD原文を告知へ補完。PRONOMの調査範囲に専用文未検出のため名前付き出典/OGL標準文・リンクを維持。対応ソース補足19ファイル＋台帳を整備し全件サイズ/SHA一致。全Qt/Folimeldソースの承認や公開ではない。

[詳細と残件](windows-desktop-tika-delivery-review_ja.md)。資料は未承認・禁止事項/uv中止を維持。
