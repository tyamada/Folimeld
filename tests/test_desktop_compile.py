"""Synthetic compile fixtures only: never invoke the real compiler or approve inputs."""
import json
from pathlib import Path
import struct
from types import SimpleNamespace

import pytest
from tools import desktop_compile as dc


def pe(path, machine):
    data = bytearray(80)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 60, 64)
    data[64:70] = b"PE\0\0" + struct.pack("<H", machine)
    path.write_bytes(data)


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    source = Path(__file__).resolve().parents[1]
    for name in ("LICENSE", "packaging/windows/desktop-inno.json", "packaging/windows/desktop-crt.json",
                 "packaging/windows/desktop-runtime.json", "packaging/windows/Folimeld-desktop.iss"):
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((source / name).read_bytes())
    payload, legal, inno = [tmp_path / name for name in ("payload", "legal", "inno")]
    for directory in (payload / "_internal/licenses", legal, inno):
        directory.mkdir(parents=True)
    pe(payload / "FolimeldDesktop.exe", 0x8664)
    (payload / "_internal/python312.dll").write_bytes(b"synthetic runtime")
    (payload / "_internal/LICENSE").write_bytes((repo / "LICENSE").read_bytes())
    files = {}
    for name in ("Installed-packages.txt", "THIRD-PARTY-NOTICES.txt", "DEPENDENCY-SOURCES.json"):
        (legal / name).write_text("synthetic test-only " + name)
        files[name] = dc._sha(legal / name)
        (payload / "_internal/licenses" / name).write_bytes((legal / name).read_bytes())
    (legal / "reviewed-files.json").write_text(json.dumps({"distribution": "windows-desktop-x64", "files": files}))
    review = {"schema_version": 1, "distribution": "windows-desktop-x64",
              "status": "reviewed-for-desktop-compile", "version": "1.0.0.0",
              "files": dc._tree(payload)}
    for key, path in {"legal_manifest_sha256": legal / "reviewed-files.json",
                      "inno_manifest_sha256": repo / "packaging/windows/desktop-inno.json",
                      "crt_manifest_sha256": repo / "packaging/windows/desktop-crt.json",
                      "runtime_manifest_sha256": repo / "packaging/windows/desktop-runtime.json",
                      "setup_script_sha256": repo / "packaging/windows/Folimeld-desktop.iss"}.items():
        review[key] = dc._sha(path)
    review_path = tmp_path / "synthetic-review.json"
    review_path.write_text(json.dumps(review))
    monkeypatch.setattr(dc, "verify_runtime_terms", lambda *args: {"synthetic": "terms"})
    monkeypatch.setattr(dc, "verify_collected_crt", lambda *args: {"synthetic": "crt"})
    monkeypatch.setattr(dc, "verify_inno_inputs", lambda *args: {"selected_stubs": ["Setup.e32", "SetupLdr.e32"]})
    monkeypatch.setattr(dc.subprocess, "run", lambda *args, **kwargs: pytest.fail("Unexpected compiler execution"))
    return repo, dict(payload_root=payload, payload_review=review_path, legal_root=legal,
                      inno_root=inno, output=tmp_path / "new output", version="1.0.0.0")


def test_verify_is_read_only(fixture):
    repo, inputs = fixture
    state = dc.verify_compile_inputs(repo, **inputs)
    assert not inputs["output"].exists()
    assert state["version"] == "1.0.0.0"
    command = dc.compiler_command(repo, state)
    assert command[1] == "--no-ide-signtools"
    assert len(command) == 7


@pytest.mark.parametrize("change", ["extra", "missing", "modified", "legal", "binding", "review", "version", "existing"])
def test_changed_inputs_stop(fixture, change):
    repo, inputs = fixture
    payload = inputs["payload_root"]
    if change == "extra":
        (payload / "extra").write_text("unexpected")
    elif change == "missing":
        (payload / "FolimeldDesktop.exe").unlink()
    elif change == "modified":
        (payload / "_internal/python312.dll").write_text("changed")
    elif change == "legal":
        (inputs["legal_root"] / "THIRD-PARTY-NOTICES.txt").write_text("changed")
    elif change == "binding":
        (repo / "packaging/windows/Folimeld-desktop.iss").write_text("changed")
    elif change == "review":
        inputs["payload_review"].write_text("{}")
    elif change == "version":
        inputs["version"] = "0.3.4+fix1"
    else:
        inputs["output"].mkdir()
    with pytest.raises((ValueError, FileExistsError)):
        dc.compile_reviewed(repo, **inputs)


def test_changed_between_checks_never_compiles(fixture, monkeypatch):
    repo, inputs = fixture
    original = dc.verify_compile_inputs
    calls = []
    def verify(*args, **kwargs):
        calls.append(1)
        if len(calls) == 2:
            (inputs["payload_root"] / "extra").write_text("changed")
        return original(*args, **kwargs)
    monkeypatch.setattr(dc, "verify_compile_inputs", verify)
    with pytest.raises(ValueError):
        dc.compile_reviewed(repo, **inputs)
    result = json.loads((inputs["output"] / "compile-result.json").read_text())
    assert not result["compiler_attempted"]


@pytest.mark.parametrize("mode", ["success", "failed", "extra", "mutation", "missing"])
def test_mock_compiler_contract(fixture, monkeypatch, mode):
    repo, inputs = fixture
    def run(command, **kwargs):
        assert command[0] == str(inputs["inno_root"] / "ISCC.exe")
        assert "--define=PayloadReviewed=1" in command
        assert kwargs["cwd"] == str(inputs["inno_root"])
        assert kwargs["env"]["PATH"].startswith(str(inputs["inno_root"]))
        if mode != "missing":
            pe(inputs["output"] / "Folimeld-Desktop-1.0.0.0-x64-setup.exe", 0x14c)
        if mode == "extra":
            (inputs["output"] / "extra").write_text("bad")
        if mode == "mutation":
            (inputs["payload_root"] / "extra").write_text("changed")
        return SimpleNamespace(returncode=2 if mode == "failed" else 0)
    monkeypatch.setattr(dc.subprocess, "run", run)
    if mode == "success":
        result = dc.compile_reviewed(repo, **inputs)
        assert result["status"] == "compiled-not-release-approved"
        assert len(result["sha256"]) == 64
    else:
        with pytest.raises((ValueError, RuntimeError)):
            dc.compile_reviewed(repo, **inputs)
        assert json.loads((inputs["output"] / "compile-result.json").read_text())["status"] == "failed-not-approved"


@pytest.mark.parametrize("name", ["../bad", "a/../bad", "a\\b", "C:bad", "/bad", "./bad"])
def test_unsafe_review_path(name):
    with pytest.raises(ValueError):
        dc._relative(name)


def test_wrong_payload_machine(fixture):
    repo, inputs = fixture
    pe(inputs["payload_root"] / "FolimeldDesktop.exe", 0x14c)
    review = json.loads(inputs["payload_review"].read_text())
    review["files"] = dc._tree(inputs["payload_root"])
    inputs["payload_review"].write_text(json.dumps(review))
    with pytest.raises(ValueError, match="architecture"):
        dc.verify_compile_inputs(repo, **inputs)


def test_tool_guard_failure(fixture, monkeypatch):
    repo, inputs = fixture
    def fail(*args):
        raise ValueError("Tool or stub hash changed")
    monkeypatch.setattr(dc, "verify_inno_inputs", fail)
    with pytest.raises(ValueError, match="stub"):
        dc.compile_reviewed(repo, **inputs)
    assert not inputs["output"].exists()


def test_output_overlap(fixture):
    repo, inputs = fixture
    inputs["output"] = inputs["payload_root"] / "output"
    with pytest.raises(ValueError, match="separate"):
        dc.verify_compile_inputs(repo, **inputs)


def test_runtime_terms_failure_prevents_compiler(fixture, monkeypatch):
    repo, inputs = fixture
    def fail(*args):
        raise ValueError("Runtime terms invalid")
    monkeypatch.setattr(dc, "verify_runtime_terms", fail)
    with pytest.raises(ValueError, match="Runtime terms"):
        dc.compile_reviewed(repo, **inputs)
    assert not inputs["output"].exists()
