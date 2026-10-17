#!/usr/bin/env python3
"""Regression for a load-time error that Ikemen's compiler accepts."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def validate(character):
    return subprocess.run([sys.executable,str(ROOT/'tools/validate_character.py'),str(character)],
                          capture_output=True,text=True)

class CompatibilityRegression(unittest.TestCase):
    def test_current_runtime_passes(self):
        result=validate(ROOT/'Eida')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_ikemen_min_in_explod_alpha_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-mugen11-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Omnipotencia.cns'
            text,count=re.subn(r'(?m)^alpha = IfElse[^\n]*',
                              'alpha = Min(256,Time*24),0',path.read_text(),count=1)
            self.assertEqual(count,1,'Expected a real cinematic fade to exercise')
            path.write_text(text)
            result=validate(character)
            self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn('Min() is not in the MUGEN 1.1 function list',result.stdout)

    def test_reported_cmd_trigger2_parse_failure_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-cmd-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Eida.cmd'
            text,count=re.subn(r'(?m)^trigger2 = StateNo = 200$',
                'trigger2 = StateNo = [200,202] || StateNo = 210 || StateNo = 211 || StateNo = 220 || StateNo = 221',
                path.read_text(),count=1)
            self.assertEqual(count,1,'Expected a real special cancel to exercise')
            path.write_text(text)
            result=validate(character)
            self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn('Eida.cmd:304: bare interval comparison',result.stdout)

if __name__=='__main__':unittest.main()
