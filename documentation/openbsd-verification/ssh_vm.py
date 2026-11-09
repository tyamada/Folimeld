import argparse, subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--user', default='folimeld')
parser.add_argument('--script')
parser.add_argument('command', nargs='?', default='uname -a')
a=parser.parse_args()
cmd=['ssh','-i',str(Path.home()/'.ssh'/'folimeld_openbsd_ed25519'),'-o',f'UserKnownHostsFile={Path.home() / ".ssh" / "folimeld_openbsd_known_hosts"}','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10','-o','BatchMode=yes','-p','2225',f'{a.user}@127.0.0.1']
if a.script:
 data=Path(a.script).read_bytes().removeprefix(b'\xef\xbb\xbf').replace(b'\r\n',b'\n')
 r=subprocess.run(cmd+['sh','-s'],input=data)
else: r=subprocess.run(cmd+[a.command])
raise SystemExit(r.returncode)

