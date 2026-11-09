#!/bin/sh
set -eu
export PATH=/usr/pkg/bin:/usr/pkg/sbin:/usr/X11R7/bin:/usr/bin:/bin:/usr/sbin:/sbin
if [ ! -f /etc/rc.d/dbus ]; then cp /usr/pkg/share/examples/rc.d/dbus /etc/rc.d/dbus; fi
grep -q '^dbus=YES' /etc/rc.conf || echo dbus=YES >> /etc/rc.conf
/etc/rc.d/dbus onestart || true
auth=/home/folimeld/.Xauthority
touch "$auth"
chmod 600 "$auth"
cookie=$(openssl rand -hex 16)
xauth -f "$auth" add :0 . "$cookie"
chown folimeld:users "$auth"
nohup /usr/X11R7/bin/Xorg :0 -auth "$auth" -nolisten tcp vt05 > /home/folimeld/xorg-console.txt 2>&1 < /dev/null &
sleep 3
su - folimeld -c 'env DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority /usr/X11R7/bin/xrandr --output VGA-0 --mode 1280x1024'
su - folimeld -c 'env PATH=/usr/pkg/bin:/usr/X11R7/bin:/usr/bin:/bin DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority LANG=ja_JP.UTF-8 TZ=Asia/Tokyo dbus-run-session startxfce4' > /home/folimeld/desktop-console.txt 2>&1 < /dev/null &
echo DESKTOP_STARTED
