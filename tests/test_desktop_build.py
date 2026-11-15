import hashlib
import json
import pytest
from tools.desktop_build import reviewed_legal_datas


def legal(root, extra=None):
    files = {}
    for name in ["Installed-packages.txt", "THIRD-PARTY-NOTICES.txt", "DEPENDENCY-SOURCES.json"]:
        (root / name).write_text("example")
        files[name] = hashlib.sha256(b"example").hexdigest()
    if extra: files.update(extra)
    (root / "reviewed-files.json").write_text(json.dumps({"distribution": "windows-desktop-x64", "files": files}))


def test_reviewed_legal_inputs_are_exact(tmp_path):
    legal(tmp_path)
    assert len(reviewed_legal_datas(tmp_path)) == 3
    (tmp_path / "THIRD-PARTY-NOTICES.txt").write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"): reviewed_legal_datas(tmp_path)


def test_legal_inputs_cannot_escape_root(tmp_path):
    legal(tmp_path, {"../outside": "0" * 64})
    with pytest.raises(ValueError, match="Unsafe"): reviewed_legal_datas(tmp_path)


def test_missing_desktop_specific_legal_records_stop_build(tmp_path):
    (tmp_path / "reviewed-files.json").write_text(json.dumps({"distribution": "windows-uv", "files": {}}))
    with pytest.raises(ValueError, match="Desktop-specific"): reviewed_legal_datas(tmp_path)
