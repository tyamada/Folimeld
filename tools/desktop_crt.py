"""Desktop-only CRT inputs and TOC normalization; never modifies input files."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct

CRT_NAMES = frozenset({"vcruntime140.dll", "vcruntime140_1.dll", "msvcp140.dll",
    "msvcp140_1.dll", "msvcp140_2.dll", "concrt140.dll", "msvcp140_codecvt_ids.dll"})


def _basename(value):
    return PurePosixPath(str(value).replace("\\", "/")).name.lower()


def _is_crt(value):
    name = _basename(value)
    return (bool(re.fullmatch(r"(?:vcruntime|msvcp|msvcr|concrt|vcamp|vccorlib|vcomp)[0-9][\w.-]*\.dll", name))
            or name in {"ucrtbase.dll", "ucrtbased.dll", "msvcrt.dll", "msvcp_win.dll"}
            or name.startswith("api-ms-win-crt-"))


def load_crt_manifest(repo_root: Path, arch: str = "x64"):
    manifest_name = "packaging/windows/desktop-arm64-crt.json" if arch == "arm64" else "packaging/windows/desktop-crt.json"
    raw = (repo_root / manifest_name).read_bytes()
    manifest = json.loads(raw)
    expected_dist = f"windows-desktop-{arch}"
    expected_source_kind = f"official-vs-redist-desktop-{arch}"
    expected_version = "14.52.37029.0" if arch == "arm64" else "14.44.35211.0"
    if (manifest.get("schema_version") != 1
            or manifest.get("distribution") != expected_dist
            or manifest.get("source_kind") != expected_source_kind
            or manifest.get("version") != expected_version
            or set(manifest.get("files", {})) != CRT_NAMES):
        raise ValueError("Invalid Desktop CRT manifest.")
    for entry in manifest["files"].values():
        if (not re.fullmatch(r"[0-9a-f]{64}", entry.get("sha256", ""))
                or not isinstance(entry.get("bytes"), int) or entry["bytes"] <= 0):
            raise ValueError("Invalid Desktop CRT hash/size.")
    return manifest, hashlib.sha256(raw).hexdigest()


def verify_crt_inputs(input_root: Path, manifest: dict, arch: str = "x64"):
    if set(manifest.get("files", {})) != CRT_NAMES:
        raise ValueError("Invalid CRT file set.")
    root = input_root.resolve(strict=True)
    entries = list(root.iterdir())
    if (len(entries) != len(CRT_NAMES)
            or {_basename(p.name) for p in entries} != CRT_NAMES):
        raise ValueError("CRT directory must contain exactly the seven approved files.")
    verified = {}
    for name, expected in manifest["files"].items():
        expected_pe = (b"PE\0\0\x64\x86" if name == "vcruntime140_1.dll" else b"PE\0\0\x64\xaa") if arch == "arm64" else b"PE\0\0\x64\x86"
        path = (root / name).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("CRT input escapes its dedicated directory.")
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
            source.seek(0)
            header = source.read(64)
            if len(header) < 64 or header[:2] != b"MZ":
                raise ValueError(f"Invalid CRT PE: {name}")
            source.seek(struct.unpack_from("<I", header, 0x3c)[0])
            pe = source.read(6)
        if (digest != expected["sha256"] or path.stat().st_size != expected["bytes"]):
            raise ValueError(f"CRT hash/size mismatch: {name}")
        if pe != expected_pe:
            raise ValueError(f"CRT must be an {arch} PE: {name}")
        verified[name] = {"path": str(path), "sha256": digest, "bytes": expected["bytes"]}
    return verified


def normalize_crt_payload(binaries, datas, input_root: Path, manifest: dict, arch: str = "x64"):
    # Recheck immediately before collection, even if preflight already succeeded.
    verified = verify_crt_inputs(input_root, manifest, arch=arch)
    removed = []
    retained = [[], []]
    for rows, target in zip((binaries, datas), retained):
        for row in rows:
            name, source, kind = row
            dest_crt, source_crt = _is_crt(name), _is_crt(source)
            if not (dest_crt or source_crt):
                target.append(row)
                continue
            if (_basename(name) not in CRT_NAMES or _basename(source) not in CRT_NAMES
                    or _basename(name) != _basename(source)):
                raise ValueError(f"Unapproved or renamed CRT payload: {name}")
            removed.append({"destination": name, "source": source, "kind": kind})
    for name, entry in sorted(verified.items()):
        # PyInstaller places these top-level TOC names under its _internal directory.
        retained[0].append((name, entry["path"], "BINARY"))
    return sorted(retained[0]), sorted(retained[1]), {"files": verified, "removed_duplicates": removed}


def verify_collected_crt(payload_root: Path, manifest: dict):
    """Audit an already authorized COLLECT result without running the app."""
    root = payload_root.resolve(strict=True)
    found = {}
    for path in root.rglob("*"):
        if not path.is_file() or not _is_crt(path.name):
            continue
        relative = path.relative_to(root).as_posix()
        if relative not in {"_internal/" + name for name in CRT_NAMES}:
            raise ValueError(f"Unexpected CRT location: {relative}")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"Collected CRT escapes payload: {relative}")
        name = path.name.lower()
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        if (not path.resolve().is_relative_to(root) or digest != manifest["files"][name]["sha256"]
                or path.stat().st_size != manifest["files"][name]["bytes"]):
            raise ValueError(f"Collected CRT mismatch: {relative}")
        found[name] = digest
    if set(found) != CRT_NAMES:
        raise ValueError("Collected payload is missing approved CRT files.")
    return found
