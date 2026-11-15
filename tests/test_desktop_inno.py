import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import desktop_inno


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    root = tmp_path / "inno"
    root.mkdir()
    files = {}
    for name in desktop_inno.PRIMARY_FILES:
        data = ("fixture " + name).encode()
        (root / name).write_bytes(data)
        files[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    script = tmp_path / "desktop.iss"
    script.write_text("[Setup]\n" + "\n".join(k + "=" + v for k, v in desktop_inno.SETUP_POLICY.items()))
    manifest = {"files": files, "engine_version": "7.1.1", "selected_stubs": desktop_inno.SELECTED_STUBS}
    calls = []
    def version(root):
        calls.append(root)
        return "7.1.1"
    monkeypatch.setattr(desktop_inno, "_engine_version", version)
    return root, manifest, script, calls


def test_pinned_manifest_and_real_script_selection():
    repo = Path(__file__).resolve().parents[1]
    manifest, digest = desktop_inno.load_inno_manifest(repo)
    assert len(manifest["files"]) == 133
    assert set(manifest["primary_files"]) == desktop_inno.PRIMARY_FILES
    assert manifest["selected_stubs"] == ["Setup.e32", "SetupLdr.e32"]
    assert len(digest) == 64
    assert desktop_inno.verify_setup_policy(repo / "packaging/windows/Folimeld-desktop.iss") == desktop_inno.SETUP_POLICY


def test_readonly_guard_records_selected_inputs(inputs):
    root, manifest, script, calls = inputs
    result = desktop_inno.verify_inno_inputs(root, manifest, script)
    assert len(result["files"]) == 9
    assert result["selected_stubs"] == ["Setup.e32", "SetupLdr.e32"]
    assert not result["compiled"]
    assert calls == [root]


@pytest.mark.parametrize("filename", ["ISCC.exe", "ISCmplr.dll", "ISPP.dll", "Setup.e32", "SetupLdr.e32", "Setup.e64"])
def test_tampered_input_stops_before_any_execution(inputs, filename):
    root, manifest, script, calls = inputs
    (root / filename).write_bytes(b"changed")
    with pytest.raises(ValueError, match="hash/size mismatch"):
        desktop_inno.verify_inno_inputs(root, manifest, script)
    assert calls == []


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_input_set_is_pinned(inputs, change):
    root, manifest, script, calls = inputs
    if change == "missing":
        (root / "SetupLdr.e32").unlink()
    else:
        (root / "injected.dll").write_bytes(b"unlisted")
    with pytest.raises(ValueError, match="Missing or extra"):
        desktop_inno.verify_inno_inputs(root, manifest, script)
    assert not calls


@pytest.mark.parametrize("change", ["arch", "loader", "style", "stylefile", "include", "spaced-include", "conditional", "duplicate"])
def test_policy_drift_stops_before_any_execution(inputs, change):
    root, manifest, script, calls = inputs
    text = script.read_text()
    if change == "arch": text = text.replace("SetupArchitecture=x86", "SetupArchitecture=x64")
    elif change == "loader": text = text.replace("UseSetupLdr=x86", "UseSetupLdr=no")
    elif change == "style": text = text.replace("classic light", "modern dynamic")
    elif change == "stylefile": text += "\nWizardStyleFile=custom.vsf"
    elif change == "include": text = '#include "other.iss"\n' + text
    elif change == "spaced-include": text = '# include "other.iss"\n' + text
    elif change == "conditional": text += "\n#if 1"
    else: text += "\nSetupArchitecture=x86"
    script.write_text(text)
    with pytest.raises(ValueError):
        desktop_inno.verify_inno_inputs(root, manifest, script)
    assert not calls


def test_wrong_engine_version_fails(inputs, monkeypatch):
    root, manifest, script, calls = inputs
    monkeypatch.setattr(desktop_inno, "_engine_version", lambda root: "7.2.0")
    with pytest.raises(ValueError, match="engine version mismatch"):
        desktop_inno.verify_inno_inputs(root, manifest, script)


def test_version_query_has_no_script_or_compile_argument(tmp_path, monkeypatch):
    calls = []
    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return SimpleNamespace(stdout="7.1.1\n")
    monkeypatch.setattr(desktop_inno.subprocess, "run", run)
    assert desktop_inno._engine_version(tmp_path) == "7.1.1"
    assert calls[0][0] == [str(tmp_path / "ISCC.exe"), "--version"]
    assert calls[0][1]["timeout"] == 15
