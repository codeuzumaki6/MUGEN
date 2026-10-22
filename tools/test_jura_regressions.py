#!/usr/bin/env python3
"""Check that delivered-file validation catches prior real MUGEN failure classes."""
from pathlib import Path
import re,shutil,struct,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
def edit(folder,name,old,new):
 p=folder/name;t=p.read_text();assert old in t;p.write_text(t.replace(old,new,1))
def empty(folder):
 with (folder/'JuraShinju.cns').open('a') as f:f.write('\n[Statedef 99999]\ntype=S\n')
def extension(folder):
 with (folder/'JuraShinju.cns').open('a') as f:f.write('\n[State -2, Unsupported native function]\ntype=VarSet\ntrigger1=1\nv=59\nvalue=Min(1,2)\n')
def wrongidle(folder):
 p=folder/'JuraShinju.air';text=p.read_text();m=re.search(r'(?ims)^\[Begin Action 0\].*?(?=^\[Begin Action|\Z)',text);assert m
 text=text[:m.start()]+m[0].replace('0,0,0,0,10','0,11,0,0,10')+text[m.end():];p.write_text(text)
def infinite(folder):
 p=folder/'JuraShinju.air';text=p.read_text();m=re.search(r'(?ims)^\[Begin Action 5120\].*?(?=^\[Begin Action|\Z)',text);assert m
 text=text[:m.start()]+m[0].replace('0,8,0,0,4','0,23,0,0,-1')+text[m.end():];p.write_text(text)
def sound(folder):
 p=folder/'JuraShinju.snd';data=bytearray(p.read_bytes());count,off=struct.unpack_from('<II',data,16)
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<IIII',data,off)
  if (g,n)==(1,21):struct.pack_into('<I',data,off+12,921);break
  off=nxt
 else:raise AssertionError('No startup sample')
 p.write_bytes(data)
def archive(folder):
 p=folder/'JuraShinju.sff';b=bytearray(p.read_bytes());b[0]=0;p.write_bytes(b)
def kokugan(folder):
 with (folder/'JuraShinju.air').open('a') as f:f.write('\n[Begin Action 8860]\n8830,0,0,0,1\n')

with tempfile.TemporaryDirectory(prefix='jura-regressions-') as temp:
 for name,mutation in [('empty state',empty),('unsupported MUGEN function',extension),('attack pose in idle',wrongidle),('infinite getup',infinite),('missing actual activation sample',sound),('corrupt SFF header',archive),('Kokugan action reintroduced',kokugan)]:
  folder=Path(temp)/name;folder.mkdir()
  for p in (ROOT/'JuraShinju').iterdir():
   if p.is_file():shutil.copy2(p,folder/p.name)
  mutation(folder);run=subprocess.run([sys.executable,str(ROOT/'tools/validate_jura.py'),str(folder)],capture_output=True,text=True)
  assert run.returncode!=0,(name,'corruption passed validation');print('PASS rejected',name)
print('PASSED 7 Jura file/syntax regressions')
