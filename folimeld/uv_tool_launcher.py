"""Windows uv tool entry point; separate from Store, Desktop, and source/uv."""
from importlib.metadata import PackageNotFoundError, version
import json
from multiprocessing import freeze_support
from pathlib import Path
import platform
import struct
import sys

from .resources import resource_root
from .windows_integration import is_packaged


def validate_uv_tool_environment(root: Path | None = None) -> None:
    if sys.platform != "win32" or struct.calcsize("P") != 8:
        raise RuntimeError("This launcher requires 64-bit Windows.")
    machine = platform.machine().lower()
    resolved_root = resource_root() if root is None else root
    if machine in {"arm64", "aarch64"}:
        profile_name = "windows-arm64-uv-runtime.json"
        expected_platform = "windows-arm64"
        if not (resolved_root / profile_name).exists() and (resolved_root / "windows-uv-runtime.json").exists():
            profile_name = "windows-uv-runtime.json"
            expected_platform = "windows-x86_64"
    elif machine in {"amd64", "x86_64"}:
        profile_name = "windows-uv-runtime.json"
        expected_platform = "windows-x86_64"
    else:
        raise RuntimeError("A native x64 or arm64 Python interpreter is required.")

    profile = json.loads((resolved_root / profile_name).read_text(encoding="utf-8"))
    if profile.get("schema_version") != 1 or profile.get("platform") != expected_platform:
        raise RuntimeError(f"Invalid {profile_name} profile.")
    if platform.python_implementation() != "CPython":
        raise RuntimeError("This launcher requires CPython.")
    expected_major_minor = tuple(int(part) for part in profile["python"]["version"].split(".")[:2])
    if tuple(sys.version_info[:2]) != expected_major_minor:
        raise RuntimeError(
            f"Python {expected_major_minor[0]}.{expected_major_minor[1]}.x is required by {profile_name}."
        )
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("An isolated uv tool virtual environment is required.")
    if getattr(sys, "frozen", False) or is_packaged():
        raise RuntimeError("This launcher cannot run with MSIX package identity or as a frozen app.")
    for name, expected in profile["dependencies"].items():
        try:
            actual = version(name)
        except PackageNotFoundError:
            raise RuntimeError(f"Required dependency is missing: {name}") from None
        if actual != expected:
            raise RuntimeError(f"Dependency version differs from the lock: {name}")


def main() -> int:
    freeze_support()
    try:
        validate_uv_tool_environment()
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
        kernel.CreateMutexW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        mutex = kernel.CreateMutexW(None, False, "Local\\Folimeld-UV-Tool")
        if not mutex:
            raise ctypes.WinError(ctypes.get_last_error())
        already_running = ctypes.get_last_error() == 183
        try:
            if already_running:
                raise RuntimeError(
                    "Folimeld (uv tool) is already running. Close it before starting another instance."
                )
            from .app import run
            return run(distribution="uv-tool")
        finally:
            kernel.CloseHandle(mutex)
    except Exception as error:
        message = f"Folimeld uv tool could not start.\n{error}"
        if sys.stderr is not None:
            print(message, file=sys.stderr)
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message, "Folimeld uv tool", 0x10)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
