#!/usr/bin/env python3
"""Guard against real load/identity/helper/audio regressions from this project."""
from pathlib import Path
import re,shutil,struct,subprocess,sys,tempfile,unittest

ROOT=Path(__file__).resolve().parents[1]
class Regressions(unittest.TestCase):
    def rejected(self,change):
        with tempfile.TemporaryDirectory(prefix='mamushi-regression-') as tmp:
            char=Path(tmp)/'Mamushi';shutil.copytree(ROOT/'Mamushi',char);change(char)
            run=subprocess.run([sys.executable,str(ROOT/'tools/validate_mamushi.py'),str(char)],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0,run.stdout+run.stderr)
    def test_empty_state_rejected(self):
        def change(p):
            f=p/'Mamushi.cns';s=f.read_text();s=re.sub(r'(?ims)^\[Statedef 170\].*?(?=^\[Statedef|\Z)','[Statedef 170]\ntype = S\n',s);f.write_text(s)
        self.rejected(change)
    def test_non_mugen_min_rejected(self):
        def change(p):
            f=p/'Mamushi.cns';s=f.read_text().replace('IfElse(', 'Min(',1);f.write_text(s)
        self.rejected(change)
    def test_idle_attack_rejected(self):
        def change(p):
            f=p/'Mamushi.air';f.write_text(f.read_text().replace('0,4,0,0,10','0,25,0,0,10',1))
        self.rejected(change)
    def test_clone_hit_override_cannot_be_only_global(self):
        def change(p):
            f=p/'Mamushi.cns';s=f.read_text();start=s.index('[Statedef 9500]');n=s.index('type = HitOverride',start);s=s[:n]+s[n:].replace('type = HitOverride','type = Null',1);f.write_text(s)
        self.rejected(change)
    def test_counter_needs_reversal_box(self):
        def change(p):
            f=p/'Mamushi.air';s=f.read_text();start=s.index('[Begin Action 1200]');tail=s[start:].replace('Clsn1Default: 1\n Clsn1[0] = -20,-67,33,0\n','',1);f.write_text(s[:start]+tail)
        self.rejected(change)
    def test_activation_sample_must_exist(self):
        def change(p):
            f=p/'Mamushi.snd';b=bytearray(f.read_bytes());count,off=struct.unpack_from('<II',b,16)
            for i in range(count):
                nxt,size,g,n=struct.unpack_from('<IIII',b,off)
                if (g,n)==(1,21):struct.pack_into('<I',b,off+12,22);break
                off=nxt
            f.write_bytes(b)
        self.rejected(change)

if __name__=='__main__':unittest.main()
