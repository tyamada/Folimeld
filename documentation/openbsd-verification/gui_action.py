import argparse,subprocess,time,shutil
from pathlib import Path
p=Path(__file__).resolve().parent
vbox=shutil.which('VBoxManage')
vm='Folimeld-OpenBSD-8.0-amd64'
a=argparse.ArgumentParser();a.add_argument('action',choices=['open','saveas','type','enter','keys','capture']);a.add_argument('value',nargs='?',default='');a.add_argument('--delay',type=float,default=1);args=a.parse_args()
def run(*words):subprocess.run([vbox,'controlvm',vm,*words],check=True,stdout=subprocess.DEVNULL)
def key(value):run('keyboardputscancode',*value.split())
def text(value):
 assert value.isascii(), 'Use GUI file selection for Unicode paths'

 for start in range(0,len(value),16):
  run('keyboardputstring',value[start:start+16]);time.sleep(.05)
if args.action in ['open','saveas']:
 import sys
 check=subprocess.run([sys.executable,str(p/'ssh_vm.py'),'sh /home/folimeld/xdo.sh getactivewindow getwindowname'],check=True,capture_output=True)
 title=check.stdout.decode('utf-8').strip()
 if not title.endswith('Folimeld') or (args.action=='open' and '*' in title):
  raise SystemExit(f'Observe pending GUI state before proceeding: {title}')
 key('1d 18 98 9d' if args.action=='open' else '1d 2a 1f 9f aa 9d')
 deadline=time.monotonic()+30
 expected='開く' if args.action=='open' else '名前を付けて保存'
 while time.monotonic()<deadline:
  check=subprocess.run([sys.executable,str(p/'ssh_vm.py'),'sh /home/folimeld/xdo.sh getactivewindow getwindowname'],check=True,capture_output=True)
  title=check.stdout.decode('utf-8').strip()
  if title==expected:break
  time.sleep(.3)
 else:raise SystemExit(f'File dialog not ready: {title}')
 time.sleep(.5);key('1d 1e 9e 9d');text(args.value);key('1c 9c')
 if args.action=='saveas':
  expected=Path(args.value).name
  deadline=time.monotonic()+30
  while time.monotonic()<deadline:
   check=subprocess.run([sys.executable,str(p/'ssh_vm.py'),'sh /home/folimeld/xdo.sh getactivewindow getwindowname'],check=True,capture_output=True)
   title=check.stdout.decode('utf-8').strip()
   if title.startswith(expected) and title.endswith('Folimeld') and '*' not in title:break
   if title=='エラー':raise SystemExit('Observe save error')
   time.sleep(.3)
  else:raise SystemExit(f'Save has not completed: {title}')
elif args.action=='type':text(args.value)
elif args.action=='enter':key('1c 9c')
elif args.action=='keys':key(args.value)
time.sleep(min(max(args.delay,0),30))
run('screenshotpng',str(p/'gui.png'))
