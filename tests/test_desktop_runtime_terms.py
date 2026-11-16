import hashlib
import json
from pathlib import Path

import pytest
from tools import desktop_runtime_terms as terms
from tools.desktop_inno import verify_setup_policy


@pytest.fixture
def legal(tmp_path, monkeypatch):
    root = tmp_path / "legal"
    source = root / terms.RUNTIME_TERMS_RELATIVE
    source.parent.mkdir(parents=True)
    raw = b"{\\rtf1 Synthetic Runtime terms for unit test only}"
    source.write_bytes(raw)
    monkeypatch.setattr(terms, "RUNTIME_TERMS_SHA256", hashlib.sha256(raw).hexdigest())
    monkeypatch.setattr(terms, "RUNTIME_TERMS_BYTES", len(raw))
    manifest = {"distribution": "windows-desktop-x64", "files": {terms.RUNTIME_TERMS_RELATIVE: hashlib.sha256(raw).hexdigest()}}
    (root / "reviewed-files.json").write_text(json.dumps(manifest))
    return root


def test_original_terms_and_reviewed_entry(legal):
    record = terms.verify_runtime_terms(legal)
    assert record["reviewed_manifest_checked"]
    assert record["sha256"] == terms.RUNTIME_TERMS_SHA256


@pytest.mark.parametrize("change", ["modified", "missing", "wrong-distribution", "missing-entry", "wrong-entry", "missing-ledger"])
def test_invalid_runtime_terms_stop(legal, change):
    source = legal / terms.RUNTIME_TERMS_RELATIVE
    manifest = legal / "reviewed-files.json"
    if change == "modified":
        source.write_bytes(source.read_bytes() + b"x")
    elif change == "missing":
        source.unlink()
    elif change == "missing-ledger":
        manifest.unlink()
    else:
        data = json.loads(manifest.read_text())
        if change == "wrong-distribution":
            data["distribution"] = "windows-uv"
        elif change == "missing-entry":
            data["files"] = {}
        else:
            data["files"][terms.RUNTIME_TERMS_RELATIVE] = "0" * 64
        manifest.write_text(json.dumps(data))
    with pytest.raises((ValueError, FileNotFoundError)):
        terms.verify_runtime_terms(legal)


def test_collected_payload_check_does_not_fabricate_review(legal):
    (legal / "reviewed-files.json").unlink()
    record = terms.verify_runtime_terms(legal, require_reviewed=False)
    assert not record["reviewed_manifest_checked"]
    assert not (legal / "reviewed-files.json").exists()


def test_escaping_terms_path_is_rejected(legal, monkeypatch):
    outside = legal.parent / "outside.rtf"
    outside.write_text("outside")
    monkeypatch.setattr(terms, "RUNTIME_TERMS_RELATIVE", "../outside.rtf")
    with pytest.raises(ValueError, match="escape"):
        terms.verify_runtime_terms(legal, require_reviewed=False)


def test_runtime_license_path_is_fixed(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    original = (repo / "packaging/windows/Folimeld-desktop.iss").read_text(encoding="utf-8")
    script = tmp_path / "changed.iss"
    script.write_text(original.replace("LicenseFile={#PayloadRoot}", "LicenseFile=C:"), encoding="utf-8")
    with pytest.raises(ValueError):
        verify_setup_policy(script)


def test_runtime_consent_is_scoped_in_both_languages():
    repo = Path(__file__).resolve().parents[1]
    text = (repo / "packaging/windows/Folimeld-desktop.iss").read_text(encoding="utf-8")
    assert "english.LicenseLabel=" in text and "japanese.LicenseLabel=" in text
    assert "Folimeld and other open-source components retain their own licences" in text
    assert "Folimeldと他のOSSにはそれぞれのライセンスが適用" in text
    assert "Microsoft Runtimeの条件に同意しない" in text
