#!/bin/sh
set -eu
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LD_LIBRARY_PATH=/home/folimeld/Folimeld/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib
export QT_QPA_PLATFORM=offscreen
export PYTHONFAULTHANDLER=1
ulimit -c 0
cd /home/folimeld/Folimeld
mkdir -p build/netbsd-verification
.venv-netbsd/bin/python -c 'import PySide6,pymupdf; from PySide6.QtWidgets import QApplication; print(PySide6.__version__,pymupdf.__version__)'
.venv-netbsd/bin/python -m pip check > build/netbsd-verification/pip-check.txt
.venv-netbsd/bin/python -m pip freeze > build/netbsd-verification/python-packages.txt
.venv-netbsd/bin/python -m pytest -q -ra -p no:cacheprovider --junitxml=build/netbsd-verification/pytest.xml > build/netbsd-verification/pytest.txt 2>&1
echo NETBSD_PYTEST_OK
