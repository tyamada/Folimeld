#!/bin/sh
set -eu
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LD_LIBRARY_PATH=/home/folimeld/Folimeld/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib
export QT_QPA_PLATFORM=offscreen
ulimit -c 0
cd /home/folimeld/Folimeld
.venv-netbsd/bin/python - <<'PY'
from pathlib import Path
from tools.benchmark_pdf import create_fixture
create_fixture(Path('build/netbsd-verification/large-1000.pdf'), 1000, 0)
PY
for run in 1 2 3; do
    .venv-netbsd/bin/python -m tools.benchmark_pdf --pages 100 --output build/netbsd-verification/text-100-$run.json
    .venv-netbsd/bin/python -m tools.benchmark_pdf --pages 100 --image-size 256 --output build/netbsd-verification/images-100-$run.json
    .venv-netbsd/bin/python -m tools.benchmark_pdf --pages 1000 --output build/netbsd-verification/text-1000-$run.json
done
echo NETBSD_BENCHMARKS_OK
