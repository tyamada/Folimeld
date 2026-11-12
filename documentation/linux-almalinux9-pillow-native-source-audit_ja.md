# AlmaLinux9候補のPillow画像ライブラリ・SBOM・ソース確認

実施日: 2026-11-12（日本時間）。[ランタイム調査](linux-almalinux9-native-runtime-source-audit_ja.md)の続き。専用AlmaLinux9 Build環境へ資料を追加した。既存候補・アプリ版・配布物を保持し、再ビルド・公開は実施していない。

## 固定した入力

Pillow12.3.0の公式タグを解決したコミット`bb1d8e8ab8d29048624d96e3ee53cecf7c13d13d`から、依存版定義・wheelワークフロー・依存取得スクリプト・告知を保存した。Git treeのblob IDとも照合した。ビルダーが固定するmultibuildは`4546f4d4820ffd0104b872c3b6187260b3e64edc`で、関連スクリプト3件をそのコミットから保存した。取得したスクリプトは実行していない。

参照した一次資料は[公式12.3.0タグ](https://github.com/python-pillow/Pillow/tree/12.3.0)、[wheel依存取得スクリプト](https://github.com/python-pillow/Pillow/blob/12.3.0/.github/workflows/wheels-dependencies.sh)、[依存版定義](https://github.com/python-pillow/Pillow/blob/12.3.0/.github/dependencies.json)。スクリプトは一部ソースをpillow-dependsのmainから取得するため、固定したPillowタグだけでは過去の全取得内容は確定しない。

今回のpillow-dependsは取得時のコミット`70c5bf5e940f5f1aee75ddb0421f0abfd9581261`を固定した。そこからのアーカイブは、保存したGit treeのblob IDとSHA-256で照合した。上流開発元の署名付きチェックサムを独立検証したという意味ではない。

## ソースとパッチの収集

```text
/home/folimeld-build/folimeld-candidates/alma9-20261112/pillow-native-audit-20261112/
  sources/   ソースアーカイブ21件、SBOM由来パッチ3件
```

21件は合計79,759,585バイト。FreeType2.14.3、HarfBuzz14.2.1、libjpeg-turbo3.1.4.1、LittleCMS2.19.1、libavif1.4.2、libwebp1.6.0、libxcb1.17.0、OpenJPEG2.5.4、libtiff4.7.1、xz5.8.3、zstd1.5.7、brotli1.2.0、bzip2 1.0.8、libpng1.6.58、libimagequant4.4.1、zlib-ng2.3.3、FriBiDi1.0.16を含む。libavifのextスクリプトで指定されたAOM3.14.1、dav1d1.5.3、libyuvコミット644251f25も取得した。残り1件は後述のlibXauソースRPM。

これらはビルドレシピ・SBOMから広めに集めた集合であり、候補にすべてリンクされているという主張ではない。zlib-ngと追加コーデック等の公式HTTPSアーカイブについては取得時のハッシュを記録し、独立した配布元署名・公開チェックサムの検証と区別した。

wheelには`pillow-12.3.0.cdx.json`と`auditwheel.cdx.json`が付属していた。前者のraqm用2件・libtiff用1件のパッチ本文をデコードして保存し、ハッシュを記録した。適用・ビルドはしていない。Pillow sdist内のraqm等のコードも先行収集で保持済み。

全アーカイブを再ハッシュし、tar内でLICENSE/LICENCE/COPYING/NOTICE/COPYRIGHTから始まる文書55件のパス・サイズ・ハッシュを一覧化した。ファイル名に基づく一覧であり、必要な法的文書を網羅したとの判定ではない。

## wheel告知とlibXau

固定タグの`wheels/dependency_licenses/`22文書は、改行を正規化して前後空白を除いた内容がすべて導入済みwheelのLICENSEに含まれていた。wheelのLICENSEが既存候補のInstalled-packagesに含まれることは先行調査で確認済み。今回、同じ告知を重ねて追加したり、過去の候補を書き換えたりしていない。

auditwheel側SBOMはlibXau1.0.9-3.el8を記録しており、AlmaLinux9のlibXau1.0.9-8.el9とは別に扱った。候補内のpillow.libsのlibXauは導入済みwheelと一致する。SBOMのbom-ref末尾は明示的なcomponent hashesフィールドではないため、その識別子とELFハッシュの差を、チェックサム異常やバイナリ/ソース対応の確定に使わない。

公式AlmaLinux8.10 AppStreamのvaultから`libXau-1.0.9-3.el8.src.rpm`を取得し、名前・版・RPMのpayloadダイジェストを確認した。SHA-256は`f9e5775417473caa6b5699171eec64253ef90473f36f0efe81d020b52a5de49a`。SRPMのARCHヘッダーはi686だったため、src.rpmというファイル種別と混同せず記録した。

公式AlmaLinux8鍵を監査用の独立RPMデータベースへ取り込もうとしたが、鍵のSHA1がAlmaLinux9のポリシーで拒否された。SRPM署名はNOKEYで未検証、payload等のダイジェストはOK。鍵の取得元とハッシュ・失敗出力を保存した。システムの信頼鍵や暗号ポリシーを変更していない。この1件を、先行調査で署名検証済みのAlmaLinux9 SRPM42件と同列に扱わない。

## 記録と残作業

収集資料は[告知入り新候補の準備](linux-almalinux9-notices-candidate_ja.md)で別添目録に含めた。未検証事項を保持した非公開候補であり、下記のwheel来歴・署名確認や全回帰を完了したものではない。

版・取得先・コミット・全ソースのハッシュ、wheel付属SBOM、レシピ、パッチ、告知22件の照合、文書一覧、libXau署名の未完了結果は[検証JSON](linux-almalinux9-pillow-native-source-audit-2026-11-12.json)へ保存した。ソース本体は上記WSL内に保持しており、JSONだけでソース一式とは扱わない。

残る主な工程は、可変取得先を含むwheelビルド来歴の確認、libXauの署名・バイナリ/ソース来歴の追加確認、収集資料の次候補への反映と再ビルド・導入・GUI・ライセンス表示の検証。Qt等も含め、完全なビルド来歴やライセンス適合性を認定したものではない。公開版との差分統合・版決定と、通常デスクトップ・アプリ版間移行の残試験も別途必要。
