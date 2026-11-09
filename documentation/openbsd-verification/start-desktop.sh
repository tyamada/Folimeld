#!/bin/sh
set -eu
export PATH=/usr/local/bin:/usr/local/sbin:/usr/X11R6/bin:/usr/bin:/bin:/usr/sbin:/sbin
install -d -o folimeld -g folimeld /home/folimeld/.config/autostart
printf '[Desktop Entry]\nType=Application\nName=Verification session screensaver override\nHidden=true\n' > /home/folimeld/.config/autostart/xfce4-screensaver.desktop
chown folimeld:folimeld /home/folimeld/.config/autostart/xfce4-screensaver.desktop
if ! pgrep -x Xorg >/dev/null; then
 cookie=$(openssl rand -hex 16)
 touch /home/folimeld/.Xauthority
 xauth -f /home/folimeld/.Xauthority add :0 . "$cookie"
 cp /home/folimeld/.Xauthority /var/run/folimeld-Xauthority
 chown root:_x11 /var/run/folimeld-Xauthority
 chmod 640 /var/run/folimeld-Xauthority
 chown folimeld:folimeld /home/folimeld/.Xauthority
 chmod 600 /home/folimeld/.Xauthority
 nohup /usr/X11R6/bin/Xorg :0 -noreset -nolisten tcp -auth /var/run/folimeld-Xauthority > /var/log/folimeld-Xorg-launch.txt 2>&1 < /dev/null &
 for attempt in $(jot 30); do
  if env DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority /usr/X11R6/bin/xdpyinfo >/dev/null 2>&1; then break; fi
  sleep 1
 done
fi
su -l folimeld -c 'env DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority /usr/X11R6/bin/xset s off -dpms'
if ! pgrep -u folimeld -x xfce4-session >/dev/null; then
su -l folimeld -c 'env DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority LANG=ja_JP.UTF-8 TZ=Asia/Tokyo nohup /usr/local/bin/startxfce4 > /home/folimeld/xfce-session.txt 2>&1 < /dev/null &'

fi
for attempt in $(jot 30); do
 if env DISPLAY=:0 XAUTHORITY=/home/folimeld/.Xauthority /usr/X11R6/bin/xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q 'window id #'; then exit 0; fi
 sleep 1
done
echo 'Xfce window manager not ready' >&2
exit 1
