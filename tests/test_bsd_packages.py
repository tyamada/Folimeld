import ast
from pathlib import Path

from folimeld import __version__
from tools.build_netbsd_package import DEPENDENCY_SOURCES as NETBSD_DEPS
from tools.build_openbsd_package import DEPENDENCY_SOURCES as OPENBSD_DEPS


ROOT = Path(__file__).resolve().parent.parent


def test_bsd_target_version():
    assert __version__ == '0.3.7'


def test_freebsd_version_format():
    tree = ast.parse((ROOT / 'folimeld/__init__.py').read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in n.targets)) + '_1'
    assert version == '0.3.7_1'


def test_netbsd_version_format():
    tree = ast.parse((ROOT / 'folimeld/__init__.py').read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in n.targets))
    assert version == '0.3.7'


def test_openbsd_version_format():
    tree = ast.parse((ROOT / 'folimeld/__init__.py').read_text(encoding='utf-8'))
    version = next(ast.literal_eval(n.value) for n in tree.body
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in n.targets))
    assert version == '0.3.7'


def test_bsd_dependency_sources_declared():
    assert 'pymupdf-1.28.2.tar.gz' in NETBSD_DEPS
    assert 'mupdf-1.28.2-source.tar.gz' in NETBSD_DEPS
    assert 'pymupdf-1.28.2.tar.gz' in OPENBSD_DEPS
    assert 'mupdf-1.28.2-source.tar.gz' in OPENBSD_DEPS
