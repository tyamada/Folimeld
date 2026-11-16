import ctypes
from importlib.metadata import PackageNotFoundError
import json
from types import SimpleNamespace
import pytest
from folimeld import uv_tool_launcher


@pytest.fixture
def tool_env(tmp_path, monkeypatch):
    profile = {
        "schema_version": 1,
        "platform": "windows-x86_64",
        "python": {"version": "3.12.16"},
        "dependencies": {"example": "1.0"},
    }
    (tmp_path / "windows-uv-runtime.json").write_text(json.dumps(profile), encoding="utf-8")
    monkeypatch.setattr(uv_tool_launcher.sys, "platform", "win32")
    monkeypatch.setattr(uv_tool_launcher.sys, "version_info", (3, 12, 16))
    monkeypatch.setattr(uv_tool_launcher.sys, "prefix", str(tmp_path / "tool-venv"))
    monkeypatch.setattr(uv_tool_launcher.sys, "base_prefix", str(tmp_path / "base-python"))
    monkeypatch.setattr(uv_tool_launcher.sys, "frozen", False, raising=False)
    monkeypatch.setattr(uv_tool_launcher.struct, "calcsize", lambda _: 8)
    monkeypatch.setattr(uv_tool_launcher.platform, "machine", lambda: "AMD64")
    monkeypatch.setattr(uv_tool_launcher.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(uv_tool_launcher, "is_packaged", lambda: False)
    monkeypatch.setattr(uv_tool_launcher, "version", lambda _: "1.0")
    return tmp_path


@pytest.mark.parametrize("patch_ver", [0, 5, 15, 16, 20])
def test_cpython_312_minor_series_is_accepted(tool_env, monkeypatch, patch_ver):
    monkeypatch.setattr(uv_tool_launcher.sys, "version_info", (3, 12, patch_ver))
    uv_tool_launcher.validate_uv_tool_environment(tool_env)


@pytest.mark.parametrize("ver", [(3, 11, 9), (3, 13, 0), (3, 14, 1)])
def test_other_python_minor_series_is_rejected(tool_env, monkeypatch, ver):
    monkeypatch.setattr(uv_tool_launcher.sys, "version_info", ver)
    with pytest.raises(RuntimeError, match="Python 3.12.x"):
        uv_tool_launcher.validate_uv_tool_environment(tool_env)


def test_non_isolated_base_prefix_is_rejected(tool_env, monkeypatch):
    monkeypatch.setattr(uv_tool_launcher.sys, "prefix", uv_tool_launcher.sys.base_prefix)
    with pytest.raises(RuntimeError, match="virtual environment"):
        uv_tool_launcher.validate_uv_tool_environment(tool_env)


def test_dependency_drift_or_missing_is_rejected(tool_env, monkeypatch):
    monkeypatch.setattr(uv_tool_launcher, "version", lambda _: "2.0")
    with pytest.raises(RuntimeError, match="Dependency version"):
        uv_tool_launcher.validate_uv_tool_environment(tool_env)

    def missing(name):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(uv_tool_launcher, "version", missing)
    with pytest.raises(RuntimeError, match="Required dependency is missing"):
        uv_tool_launcher.validate_uv_tool_environment(tool_env)


@pytest.mark.parametrize("existing", [False, True])
def test_uv_tool_launcher_holds_and_closes_mutex(monkeypatch, existing):
    closed = []
    calls = []
    messages = []

    def create(*args):
        calls.append(args)
        return 456

    def close(handle):
        closed.append(handle)
        return True

    kernel = SimpleNamespace(CreateMutexW=create, CloseHandle=close)
    monkeypatch.setattr(ctypes, "WinDLL", lambda *a, **k: kernel, raising=False)
    monkeypatch.setattr(ctypes, "get_last_error", lambda: 183 if existing else 0, raising=False)
    monkeypatch.setattr(ctypes, "windll", SimpleNamespace(user32=SimpleNamespace(
        MessageBoxW=lambda *args: messages.append(args))), raising=False)
    monkeypatch.setattr(uv_tool_launcher.sys, "platform", "win32")
    monkeypatch.setattr(uv_tool_launcher, "validate_uv_tool_environment", lambda: None)
    launches = []
    monkeypatch.setattr("folimeld.app.run", lambda **kw: launches.append(kw) or 0)
    assert uv_tool_launcher.main() == (1 if existing else 0)
    assert closed == [456]
    assert calls[0][2] == "Local\\Folimeld-UV-Tool"
    assert launches == ([] if existing else [{"distribution": "uv-tool"}])
    assert bool(messages) == existing
