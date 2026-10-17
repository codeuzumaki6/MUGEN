"""Normal helpers do not execute negative states with keyctrl disabled.

Their cleanup must live in the states they actually run. HitOverride prevents
a hittable assist from entering the player's common hit/get-up states.
"""
import re


def install(text,states):
    for state in states:
        label=f'[State {state}, Helper interruption lifecycle]'
        if label in text:continue
        pattern=rf'(\[Statedef {state}\][\s\S]*?)(?=\[State )'
        match=re.search(pattern,text,re.I)
        assert match,f'helper state {state} missing'
        controllers=f'''{label}
type = DestroySelf
trigger1 = Root,MoveType = H
trigger2 = RoundState != 2
ignorehitpause = 1

[State {state}, Helper receive-hit lifecycle]
type = HitOverride
trigger1 = Time = 0
attr = SCA, NA, SA, HA, NP, SP, HP, NT, ST, HT
slot = 0
stateno = 1595
time = -1
ignorehitpause = 1

'''
        text=text[:match.end()]+controllers+text[match.end():]
    return text
