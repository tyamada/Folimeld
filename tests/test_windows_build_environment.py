import pytest

from tools.windows_build_environment import build_environment, validate_binary_sources


def test_build_path_excludes_unrelated_tools_and_keeps_git(tmp_path):
    vendor = tmp_path / 'unrelated-image-tools'
    git = tmp_path / 'git' / 'cmd' / 'git.exe'
    environment = build_environment({'Path': str(vendor), 'SystemRoot': str(tmp_path / 'Windows'),
                                     'LANG': 'ja_JP'},
                                    executable=str(tmp_path / 'venv' / 'Scripts' / 'python.exe'),
                                    base_prefix=str(tmp_path / 'Python'), git_executable=str(git))
    assert str(vendor) not in environment['PATH']
    assert str(git.parent) in environment['PATH']
    assert 'Path' not in environment
    assert environment['LANG'] == 'ja_JP'


def test_build_requires_windows_root():
    with pytest.raises(ValueError, match='SystemRoot'):
        build_environment({}, executable='python.exe', base_prefix='Python', git_executable=None)


def test_binary_provenance_accepts_python_and_system_files(tmp_path):
    roots = [tmp_path / 'venv', tmp_path / 'Python', tmp_path / 'Windows']
    binaries = [('Qt6Core.dll', str(roots[0] / 'Lib' / 'Qt6Core.dll'), 'BINARY'),
                ('python314.dll', str(roots[1] / 'python314.dll'), 'BINARY'),
                ('msvcp140.dll', str(roots[2] / 'System32' / 'msvcp140.dll'), 'BINARY')]
    validate_binary_sources(binaries, roots)


@pytest.mark.parametrize('directory', ['unrelated-image-tools', 'venv-unrelated'])
def test_binary_provenance_rejects_external_and_similar_prefixes(tmp_path, directory):
    with pytest.raises(ValueError, match='ucrtbase.dll'):
        validate_binary_sources([('ucrtbase.dll', str(tmp_path / directory / 'ucrtbase.dll'),
                                  'BINARY')], [tmp_path / 'venv'])
