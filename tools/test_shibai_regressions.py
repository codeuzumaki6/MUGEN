#!/usr/bin/env python3
"""Check that delivered-file validation catches prior real MUGEN failure classes."""
from pathlib import Path
import re,shutil,struct,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
def edit(folder,name,old,new):
 p=folder/name;t=p.read_text();assert old in t;p.write_text(t.replace(old,new,1))
def empty(folder):
 with (folder/'Shibai.cns').open('a') as f:f.write('\n[Statedef 99999]\ntype=S\n')
def extension(folder):
 with (folder/'Shibai.cns').open('a') as f:f.write('\n[State -2, Unsupported native function]\ntype=VarSet\ntrigger1=1\nv=59\nvalue=Min(1,2)\n')
def wrongform(folder):edit(folder,'Shibai.air','[Begin Action 10000]\nClsn2: 1\n Clsn2[0] = -16,-74,16,-1\n1,0','[Begin Action 10000]\nClsn2: 1\n Clsn2[0] = -16,-74,16,-1\n0,0')
def infinite(folder):
 p=folder/'Shibai.air';text=p.read_text();m=re.search(r'(?ims)^\[Begin Action 5120\].*?(?=^\[Begin Action|\Z)',text);assert m
 text=text[:m.start()]+m[0].replace('0,23,0,0,4','0,23,0,0,-1')+text[m.end():];p.write_text(text)
def sound(folder):
 p=folder/'Shibai.snd';data=bytearray(p.read_bytes());count,off=struct.unpack_from('<II',data,16)
 for _ in range(count):
  nxt,size,g,n=struct.unpack_from('<IIII',data,off)
  if (g,n)==(1,21):struct.pack_into('<I',data,off+12,921);break
  off=nxt
 else:raise AssertionError('No startup sample')
 p.write_bytes(data)
def archive(folder):
 p=folder/'Shibai.sff';b=bytearray(p.read_bytes());b[0]=0;p.write_bytes(b)

with tempfile.TemporaryDirectory(prefix='shibai-regressions-') as temp:
 for name,mutation in [('empty state',empty),('unsupported MUGEN function',extension),('wrong awakened body',wrongform),('infinite getup',infinite),('missing actual activation sample',sound),('corrupt SFF header',archive)]:
  folder=Path(temp)/name;folder.mkdir()
  for p in (ROOT/'Shibai').iterdir():
   if p.is_file():shutil.copy2(p,folder/p.name)
  mutation(folder);run=subprocess.run([sys.executable,str(ROOT/'tools/validate_shibai.py'),str(folder)],capture_output=True,text=True)
  assert run.returncode!=0,(name,'corruption passed validation');print('PASS rejected',name)
print('PASSED 6 Shibai file/syntax regressions')
