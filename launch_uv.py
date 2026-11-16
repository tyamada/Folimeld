"""Windows source/uv entry point; never installs or updates dependencies."""
from importlib.metadata import PackageNotFoundError, version
import hashlib
import json
from multiprocessing import freeze_support
from pathlib import Path
import struct
import sys


def validate_environment(root: Path) -> None:
    if sys.platform != 'win32' or struct.calcsize('P') != 8:
        raise RuntimeError('This launcher requires 64-bit Windows.')
    import platform
    machine = platform.machine().lower()
    if machine in {'arm64', 'aarch64'}:
        runtime_name = 'windows-arm64-uv-runtime.json'
        lock_name = 'requirements-windows-arm64-uv.lock'
        if not (root / runtime_name).exists() and (root / 'windows-uv-runtime.json').exists():
            runtime_name = 'windows-uv-runtime.json'
            lock_name = 'requirements-windows-uv.lock'
    elif machine in {'amd64', 'x86_64'}:
        runtime_name = 'windows-uv-runtime.json'
        lock_name = 'requirements-windows-uv.lock'
    else:
        raise RuntimeError('A native x64 or arm64 Python interpreter is required.')

    profile = json.loads((root / runtime_name).read_text(encoding='utf-8'))
    lock_text = (root / lock_name).read_text(encoding='utf-8')
    lock_hash = hashlib.sha256(lock_text.encode('utf-8')).hexdigest()
    if lock_hash != profile['lock_sha256']:
        raise RuntimeError(f'The dependency lock differs from {runtime_name}.')
    if platform.python_implementation() != 'CPython':
        raise RuntimeError('This launcher requires CPython.')
    actual_python = '.'.join(map(str, sys.version_info[:3]))
    if actual_python != profile['python']['version']:
        raise RuntimeError(f'Python version differs from {runtime_name}.')
    if Path(sys.prefix).resolve() != (root / '.venv').resolve() or sys.prefix == sys.base_prefix:
        raise RuntimeError('Use this release directory\'s .venv Python interpreter.')
    from folimeld.windows_integration import is_packaged
    if getattr(sys, 'frozen', False) or is_packaged():
        raise RuntimeError('This launcher cannot run with MSIX package identity or as a frozen app.')
    for name, expected in profile['dependencies'].items():
        try:
            actual = version(name)
        except PackageNotFoundError:
            raise RuntimeError(f'Required dependency is missing: {name}') from None
        if actual != expected:
            raise RuntimeError(f'Dependency version differs from the lock: {name}')


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        validate_environment(root)
        from folimeld.app import run
        return run(source_uv=True)
    except Exception as error:
        message = f'Folimeld uv could not start.\n{error}'
        if sys.stderr is not None:
            print(message, file=sys.stderr)
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message, 'Folimeld uv', 0x10)
        return 1


if __name__ == '__main__':
    freeze_support()
    raise SystemExit(main())
