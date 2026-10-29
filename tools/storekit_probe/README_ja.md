# macOS StoreKit 技術検証

本番アプリから独立した、読み取り専用の試作です。購入・復元要求・取引の完了処理は実行しません。
Windows上ではStoreKitをコンパイル・実行できません。SwiftソースもmacOSでは未コンパイルです。

## 検証する構成

PySide6 → ctypes → 同一プロセスのSwift dylib → StoreKit 2。
SwiftのMainActorで非同期処理を行い、QtのタイマーでJSONの結果を回収します。
別プロセスにStoreKitを置かず、呼び出し元アプリのBundle IDを使います。
`@_cdecl` はアンダースコア付きの相互運用属性なので、採用するXcode版での検証が必要です。

## Macでの手順

前提：macOS 12以降、Xcode、プロジェクトのPython依存とPyInstaller。
Pythonと同じCPUアーキテクチャのターミナル環境で、リポジトリルートから実行します。

```sh
xcrun swiftc -swift-version 5 -parse-as-library -emit-library \
  -target "$(uname -m)-apple-macosx12.0" \
  -framework StoreKit tools/storekit_probe/StoreKitProbe.swift \
  -o tools/storekit_probe/libStoreKitProbe.dylib

.venv/bin/python -m PyInstaller --noconfirm --windowed \
  --name FolimeldStoreKitProbe --osx-bundle-identifier com.folimeld.Folimeld \
  --specpath build --workpath build/storekit-probe --distpath build/storekit-probe-dist \
  --add-binary 'tools/storekit_probe/libStoreKitProbe.dylib:.' \
  tools/storekit_probe/probe.py
```

これはローカル疎通用のバンドルです。商品取得の成功を保証する署名済みSandbox配布物ではありません。
本番と同じBundle IDを使うので、本番アプリと同時には起動しないでください。
App Store Connectの商品IDを入力し、Queryボタンを押します。
実商品の検証には、対応する契約・商品設定・署名・プロビジョニング・Sandbox環境が必要です。
TestFlightを使う場合は検証用ビルドとして正しく署名・提出する工程が別途必要です。
既存build_appstore.shは本番のエントリーポイントを使うため、そのままではこの試作をビルドしません。

## 判定

- UIが操作でき、products、entitlement、completeの順に結果が表示される：QtとSwift非同期処理の接続が動作。
- productsが空：成功とはしない。商品ID、Bundle ID、契約、配布・テスト環境を確認。
- owned=trueかつunverified=false：対象の検証済み権利を取得。
- owned=false：現在の環境では有効な対象権利なし。商品が空の状態では未購入と断定しない。
- unverified=true：解放しない。取引検証エラーとして調査。
- タイムアウト：結果不明。未購入に変更しない。

## 次の段階

疎通をMacで確認後、購入ボタン、キャンセル・pending分岐、Transaction.updates監視、
検証済み権利の反映後のfinish、ユーザー操作によるAppStore.syncを追加します。
購入・再起動・再インストール復元・返金・オフラインをSandboxで確認します。
署名済みPyInstallerバンドルへのdylib同梱と最低OSバージョンも確認します。
本番の対応OSをmacOS 12未満から変更する必要があるかは別途判断します。

## 公式資料

- https://developer.apple.com/documentation/storekit/in-app-purchase
- https://developer.apple.com/documentation/storekit/transaction/currententitlements
- https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases/
