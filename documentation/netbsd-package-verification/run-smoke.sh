#!/bin/sh
set -eu
cd /tmp
export HOME=/tmp
export PYTHONNOUSERSITE=1
export PYTHONPATH=/usr/pkg/share/folimeld/vendor:/usr/pkg/share/folimeld
export LD_LIBRARY_PATH=/usr/pkg/share/folimeld/lib:/usr/pkg/lib:/usr/X11R7/lib
export QT_QPA_PLATFORM=offscreen
exec /usr/pkg/bin/python3.12 /tmp/smoke.py
