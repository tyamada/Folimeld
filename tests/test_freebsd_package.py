from pathlib import Path
from zipfile import ZipFile, ZipInfo

import pytest

from tools.build_freebsd_package import extract


@pytest.mark.parametrize('name', ['../escape.py', '/escape.py'])
def test_package_inputs_cannot_escape_staging(tmp_path, name):
    archive = tmp_path / 'source.zip'
    with ZipFile(archive, 'w') as bundle:
        bundle.writestr(name, 'bad input')
    with pytest.raises(ValueError, match='Unsafe archive member'):
        extract(archive, tmp_path / 'stage')
    assert not (tmp_path / 'escape.py').exists()


def test_package_inputs_cannot_create_symlinks(tmp_path):
    archive = tmp_path / 'source.zip'
    info = ZipInfo('link')
    info.create_system = 3
    info.external_attr = 0o120777 << 16
    with ZipFile(archive, 'w') as bundle:
        bundle.writestr(info, '/etc/passwd')
    with pytest.raises(ValueError, match='Symlink archive member'):
        extract(archive, Path(tmp_path / 'stage'))


def test_freebsd_version_resolution():
    import ast
    root = Path(__file__).resolve().parent.parent
    init_file = root / 'folimeld' / '__init__.py'
    tree = ast.parse(init_file.read_text(encoding='utf-8'))
    version = next(ast.literal_eval(node.value) for node in tree.body
                   if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in node.targets)) + '_1'
    assert version == '0.3.6_1'

