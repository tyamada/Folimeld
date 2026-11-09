#!/bin/sh
set -eu
export PATH=/usr/local/bin:/usr/local/sbin:/usr/X11R6/bin:/usr/bin:/bin:/usr/sbin:/sbin
export QT_QPA_PLATFORM=offscreen
export PYTHONFAULTHANDLER=1
ulimit -c 0
cd /home/folimeld/Folimeld
mkdir -p build/openbsd-verification
py=.venv-openbsd/bin/python
"$py" /home/folimeld/record_environment.py > build/openbsd-verification/environment.txt
"$py" -m pip check > build/openbsd-verification/pip-check.txt
"$py" -m pytest -q -ra -p no:cacheprovider tests/test_pdf_forms.py tests/test_save_contents.py --junitxml=build/openbsd-verification/forms-early.xml > build/openbsd-verification/forms-early.txt 2>&1
"$py" -m pytest -q -ra -p no:cacheprovider --junitxml=build/openbsd-verification/pytest.xml > build/openbsd-verification/pytest.txt 2>&1
"$py" -m mypy > build/openbsd-verification/mypy.txt 2>&1
echo OPENBSD_TESTS_OK

