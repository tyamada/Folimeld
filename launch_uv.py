"""Windows source/uv entry point; never installs or updates dependencies."""
from importlib.metadata import PackageNotFoundError, version
import hashlib
import json
from multiprocessing import freeze_support
from pathlib import Path
import struct
import sys


def validate_environment(root: Path) -> None:
    profile = json.loads((root / 'windows-uv-runtime.json').read_text(encoding='utf-8'))
    lock_text = (root / 'requirements-windows-uv.lock').read_text(encoding='utf-8')
    lock_hash = hashlib.sha256(lock_text.encode('utf-8')).hexdigest()
    if lock_hash != profile['lock_sha256']:
        raise RuntimeError('The dependency lock differs from windows-uv-runtime.json.')
    if sys.platform != 'win32' or struct.calcsize('P') != 8:
        raise RuntimeError('This launcher requires Windows x64.')
    import platform
    if platform.machine().lower() not in {'amd64', 'x86_64'}:
        raise RuntimeError('A native x64 Python interpreter is required.')
    if platform.python_implementation() != 'CPython':
        raise RuntimeError('This launcher requires CPython.')
    actual_python = '.'.join(map(str, sys.version_info[:3]))
    if actual_python != profile['python']['version']:
        raise RuntimeError('Python version differs from windows-uv-runtime.json.')
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
