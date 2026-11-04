"""Keep unrelated tools on the developer's PATH out of Windows releases."""
from collections.abc import Mapping, Sequence
import os
from pathlib import Path
import shutil
import subprocess
import sys


def build_environment(environment: Mapping[str, str], *, executable: str,
                      base_prefix: str, git_executable: str | None) -> dict[str, str]:
    system_root = next((value for key, value in environment.items()
                        if key.lower() == 'systemroot'), None)
    if not system_root:
        raise ValueError('Windows builds require SystemRoot.')
    paths = [Path(executable).resolve().parent, Path(base_prefix).resolve(),
             Path(system_root) / 'System32', Path(system_root)]
    if git_executable:
        paths.append(Path(git_executable).resolve().parent)
    result = {key: value for key, value in environment.items() if key.lower() != 'path'}
    result['PATH'] = os.pathsep.join(dict.fromkeys(str(path) for path in paths))
    return result


def validate_binary_sources(binaries: Sequence[tuple[str, str, str]],
                            allowed_roots: Sequence[str | Path]) -> None:
    roots = [Path(root).resolve() for root in allowed_roots]
    unexpected = []
    for name, source, kind in binaries:
        if kind not in {'BINARY', 'EXTENSION'}:
            continue
        if not any(Path(source).resolve().is_relative_to(root) for root in roots):
            unexpected.append(f'{name}: {source}')
    if unexpected:
        raise ValueError('Unexpected native binary sources outside Python/Windows roots:\n'
                         + '\n'.join(unexpected))


def main() -> int:
    environment = build_environment(os.environ, executable=sys.executable,
                                    base_prefix=sys.base_prefix,
                                    git_executable=shutil.which('git'))
    return subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                           'Folimeld.spec'], cwd=Path(__file__).resolve().parents[1],
                          env=environment, check=False).returncode


if __name__ == '__main__':
    raise SystemExit(main())
