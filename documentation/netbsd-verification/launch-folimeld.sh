#!/bin/sh
set -eu
export PATH=/usr/pkg/bin:/usr/pkg/qt6/bin:/usr/X11R7/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/home/folimeld/Folimeld/.venv-netbsd/lib:/usr/pkg/lib:/usr/X11R7/lib
export DISPLAY=:0
export XAUTHORITY=/home/folimeld/.Xauthority
export LANG=ja_JP.UTF-8
export TZ=Asia/Tokyo
export QT_QPA_PLATFORM=xcb
ulimit -c 0
cd /home/folimeld/Folimeld
exec .venv-netbsd/bin/python main.py "${1:-build/netbsd-verification/source.pdf}"
