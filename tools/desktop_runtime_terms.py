"""Pin the original Microsoft Runtime terms; this does not approve redistribution."""
import hashlib
import json
from pathlib import Path

RUNTIME_TERMS_RELATIVE = "microsoft-runtime/MICROSOFT-VC-RUNTIME-14.44-EN.original.rtf"
RUNTIME_TERMS_SHA256 = "8099dc3cf9502c335da829e5c755948a12e3e6de490eb492a99deb673d883d8b"
RUNTIME_TERMS_BYTES = 9235


def verify_runtime_terms(root: Path, *, require_reviewed=True, arch="x64"):
    root = root.resolve(strict=True)
    original = root / RUNTIME_TERMS_RELATIVE
    path = original.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("Microsoft Runtime terms escape the legal directory.")
    for entry in (original, *original.parents):
        if entry == root:
            break
        if entry.is_symlink() or entry.is_junction():
            raise ValueError("Linked Microsoft Runtime terms are not allowed.")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != RUNTIME_TERMS_SHA256 or len(raw) != RUNTIME_TERMS_BYTES:
        raise ValueError("Original Microsoft Runtime terms hash/size mismatch.")
    if require_reviewed:
        manifest = json.loads((root / "reviewed-files.json").read_bytes())
        expected_dist = f"windows-desktop-{arch}"
        if (manifest.get("distribution") != expected_dist
                or manifest.get("files", {}).get(RUNTIME_TERMS_RELATIVE) != digest):
            raise ValueError("Microsoft Runtime terms must be included in the reviewed legal ledger.")
    return {"relative_path": RUNTIME_TERMS_RELATIVE, "sha256": digest,
            "bytes": len(raw), "reviewed_manifest_checked": require_reviewed}
