#!/usr/bin/env python3
"""Close distance by running forward, retaining the normal body and saw sprites."""
import re

def apply_approach_runtime(char):
 cns=(char/'PochitaTrueForm.cns').read_text()
 for state,speed,until in [(1000,4.5,20),(1030,6.5,20),(1060,5.5,16),(1100,6,16)]:
  match=re.search(rf'(?is)\[Statedef {state}\].*?(?=\[Statedef|\Z)',cns);assert match;block=match[0]
  motion=f'''[State {state}, Maintain physical approach speed]
type = VelSet
triggerall = Time < {until}
trigger1 = P2Dist X > 40
x = {speed}
[State {state}, Stop approach at contact distance]
type = VelSet
triggerall = Time < {until}
trigger1 = P2Dist X <= 40
x = 0
'''
  at=block.index(f'[State {state}, End]');block=block[:at]+motion+block[at:];cns=cns[:match.start()]+block+cns[match.end():]
 (char/'PochitaTrueForm.cns').write_text(cns.rstrip()+'\n')
 print('Built four forward approaches using the original body and normal-size saws')
