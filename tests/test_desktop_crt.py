import hashlib
from pathlib import Path
import shutil
import struct

import pytest

from tools.desktop_crt import (CRT_NAMES, load_crt_manifest, normalize_crt_payload,
                               verify_collected_crt, verify_crt_inputs)


@pytest.fixture
def inputs(tmp_path):
    root = tmp_path / "crt"
    root.mkdir()
    files = {}
    for i, name in enumerate(sorted(CRT_NAMES)):
        data = bytearray(128)
        data[:2] = b"MZ"
        struct.pack_into("<I", data, 0x3c, 64)
        data[64:70] = b"PE\0\0\x64\x86"
        data[100] = i
        (root / name).write_bytes(data)
        files[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    return root, {"files": files}


def test_manifest_is_exact_desktop_set():
    manifest, digest = load_crt_manifest(Path(__file__).resolve().parents[1])
    assert set(manifest["files"]) == CRT_NAMES
    assert len(digest) == 64


def test_input_hash_and_exact_set_are_required(inputs):
    root, manifest = inputs
    assert len(verify_crt_inputs(root, manifest)) == 7
    file = root / "msvcp140.dll"
    data = file.read_bytes()
    file.write_bytes(data[:-1] + b"x")
    with pytest.raises(ValueError, match="hash/size mismatch"):
        verify_crt_inputs(root, manifest)
    file.write_bytes(data)
    (root / "vcruntime140d.dll").write_bytes(data)
    with pytest.raises(ValueError, match="exactly the seven"):
        verify_crt_inputs(root, manifest)


def test_wrong_architecture_is_rejected_even_if_hash_matches(inputs):
    root, manifest = inputs
    file = root / "msvcp140.dll"
    data = bytearray(file.read_bytes())
    data[68:70] = b"\x64\xaa"
    file.write_bytes(data)
    manifest["files"][file.name]["sha256"] = hashlib.sha256(data).hexdigest()
    with pytest.raises(ValueError, match="x64 PE"):
        verify_crt_inputs(root, manifest)


def test_binaries_and_data_duplicates_become_one_canonical_set(inputs):
    root, manifest = inputs
    binaries = [("PySide6/MSVCP140.DLL", "old/msvcp140.dll", "BINARY"),
                ("python312.dll", "python/python312.dll", "BINARY")]
    datas = [("winrt/msvcp140.dll", "old/MSVCP140.dll", "DATA"),
             ("licenses/note.txt", "legal/note.txt", "DATA")]
    kept, data, record = normalize_crt_payload(binaries, datas, root, manifest)
    assert len(kept) == 8
    assert len(record["removed_duplicates"]) == 2
    assert data == [datas[1]]
    assert {row[0] for row in kept} == CRT_NAMES | {"python312.dll"}
    assert binaries[0][0] == "PySide6/MSVCP140.DLL"  # No caller/input mutation.
    assert all((root / name).is_file() for name in CRT_NAMES)


@pytest.mark.parametrize("dest,source", [
    ("vcomp140.dll", "vcomp140.dll"),
    ("ucrtbase.dll", "ucrtbase.dll"),
    ("api-ms-win-crt-runtime-l1-1-0.dll", "api-ms-win-crt-runtime-l1-1-0.dll"),
    ("hidden.dll", "msvcp140.dll"),
    ("msvcp140.dll", "hidden.dll"),
])
def test_unapproved_crt_or_renaming_stops_collection(inputs, dest, source):
    root, manifest = inputs
    with pytest.raises(ValueError, match="Unapproved or renamed"):
        normalize_crt_payload([(dest, source, "BINARY")], [], root, manifest)


def test_collected_files_must_have_exact_paths_and_hashes(inputs, tmp_path):
    root, manifest = inputs
    payload = tmp_path / "payload"
    internal = payload / "_internal"
    internal.mkdir(parents=True)
    for name in CRT_NAMES:
        shutil.copyfile(root / name, internal / name)
    assert len(verify_collected_crt(payload, manifest)) == 7
    nested = internal / "PySide6"
    nested.mkdir()
    shutil.copyfile(root / "msvcp140.dll", nested / "msvcp140.dll")
    with pytest.raises(ValueError, match="Unexpected CRT location"):
        verify_collected_crt(payload, manifest)


def test_collected_tampering_and_missing_files_stop(inputs, tmp_path):
    root, manifest = inputs
    payload = tmp_path / "payload"
    internal = payload / "_internal"
    internal.mkdir(parents=True)
    for name in CRT_NAMES:
        shutil.copyfile(root / name, internal / name)
    file = internal / "msvcp140.dll"
    file.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="Collected CRT mismatch"):
        verify_collected_crt(payload, manifest)
    file.unlink()
    with pytest.raises(ValueError, match="missing approved"):
        verify_collected_crt(payload, manifest)
