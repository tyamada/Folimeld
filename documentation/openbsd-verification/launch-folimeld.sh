#!/bin/sh
export DISPLAY=:0
export XAUTHORITY=/home/folimeld/.Xauthority
export LANG=ja_JP.UTF-8
export TZ=Asia/Tokyo
cd /home/folimeld/Folimeld
exec .venv-openbsd/bin/python main.py "$@"
