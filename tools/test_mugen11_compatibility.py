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
    def test_missing_senrigan_reversal_box_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-counter-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Eida.air';text=path.read_text()
            text,count=re.subn(r'(\[Begin Action 1200\]\n)Clsn1Default: 1\n Clsn1\[0\] = [^\n]*\n',r'\1',text,count=1)
            self.assertEqual(count,1);path.write_text(text)
            result=validate(character);self.assertNotEqual(result.returncode,0)
            self.assertIn('counter 1200 is missing its reversal collision box',result.stdout)

    def test_missing_jutsu_activation_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-sound-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Specials.cns';text=path.read_text();self.assertIn('value = S1,21',text)
            path.write_text(text.replace('value = S1,21','value = S1,16',1))
            result=validate(character);self.assertNotEqual(result.returncode,0)
            self.assertIn('special 1000 is missing its distinct activation sound',result.stdout)

    def test_invalid_victory_flag_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-victory-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Eida.cns'
            text=path.read_text();self.assertIn('flag = RoundNotOver',text)
            path.write_text(text.replace('flag = RoundNotOver','flag = WinPose',1))
            result=validate(character)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('invalid MUGEN AssertSpecial flag WinPose',result.stdout)

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

    def test_infinite_ground_impact_animation_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='eida-getup-regression-') as directory:
            character=Path(directory)/'Eida';character.mkdir()
            for source in (ROOT/'Eida').iterdir():
                if source.is_file():shutil.copy2(source,character/source.name)
            path=character/'Eida.air'
            text,count=re.subn(r'(\[Begin Action 5100\][\s\S]*?170,0,0,0,)6',r'\g<1>-1',path.read_text(),count=1)
            self.assertEqual(count,1)
            path.write_text(text)
            result=validate(character)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('recovery transition 5100 must finish',result.stdout)

if __name__=='__main__':unittest.main()
