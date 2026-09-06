// Read-only StoreKit 2 probe. Build with macOS 12+ SDK; Swift 5 language mode.
import Foundation
import StoreKit

private let lock = NSLock()
private var messages: [String] = []

private func emit(_ value: [String: Any]) {
    guard let data = try? JSONSerialization.data(withJSONObject: value),
          let json = String(data: data, encoding: .utf8) else { return }
    lock.lock()
    messages.append(json)
    lock.unlock()
}

// Copy the argument before returning to Python. No callback crosses runtimes.
@_cdecl("folimeld_probe_start")
public func startProbe(_ identifier: UnsafePointer<CChar>) {
    let productID = String(cString: identifier)
    Task { @MainActor in
        do {
            let products = try await Product.products(for: [productID])
            emit(["event": "products", "products": products.map {
                ["id": $0.id, "name": $0.displayName,
                 "price": $0.displayPrice, "type": String(describing: $0.type)]
            }])
            var owned = false
            var unverified = false
            for await result in Transaction.currentEntitlements {
                switch result {
                case .verified(let transaction):
                    if transaction.productID == productID && transaction.revocationDate == nil {
                        owned = true
                    }
                case .unverified(let transaction, _):
                    if transaction.productID == productID { unverified = true }
                }
            }
            emit(["event": "entitlement", "owned": owned, "unverified": unverified])
        } catch {
            emit(["event": "error", "message": error.localizedDescription])
        }
        emit(["event": "complete"])
    }
}

// Caller owns the returned allocation and must use folimeld_probe_free.
@_cdecl("folimeld_probe_poll")
public func pollProbe() -> UnsafeMutablePointer<CChar>? {
    lock.lock()
    defer { lock.unlock() }
    guard !messages.isEmpty else { return nil }
    return strdup(messages.removeFirst())
}

@_cdecl("folimeld_probe_free")
public func freeProbe(_ pointer: UnsafeMutablePointer<CChar>?) {
    free(pointer)
}
