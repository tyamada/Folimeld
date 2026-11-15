from types import SimpleNamespace
import ctypes
import pytest
import launch_desktop


@pytest.mark.parametrize("existing", [False, True])
def test_launcher_holds_and_closes_only_owned_mutex(monkeypatch, existing):
    closed = []
    calls = []
    messages = []
    def create(*args):
        calls.append(args)
        return 123
    def close(handle):
        closed.append(handle)
        return True
    kernel = SimpleNamespace(CreateMutexW=create, CloseHandle=close)
    monkeypatch.setattr(ctypes, "WinDLL", lambda *a, **k: kernel, raising=False)
    monkeypatch.setattr(ctypes, "get_last_error", lambda: 183 if existing else 0, raising=False)
    monkeypatch.setattr(ctypes, "windll", SimpleNamespace(user32=SimpleNamespace(
        MessageBoxW=lambda *args: messages.append(args))), raising=False)
    monkeypatch.setattr(launch_desktop.sys, "platform", "win32")
    monkeypatch.setattr("folimeld.desktop_profile.validate_desktop_environment", lambda: None)
    launches = []
    monkeypatch.setattr("folimeld.app.run", lambda **kw: launches.append(kw) or 0)
    assert launch_desktop.main() == (1 if existing else 0)
    assert closed == [123]
    assert calls[0][2] == "Local\\Folimeld-Desktop"
    assert launches == ([] if existing else [{"distribution": "desktop"}])
    assert bool(messages) == existing
