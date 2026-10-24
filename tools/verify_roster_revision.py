#!/usr/bin/env python3
"""Verify artifacts, original artwork, contact windows and native probe results."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from build_roster_revision import ROOT,CHARS,Archive,original,recolor,parse_action
from package_roster_revision import ARCHIVES

def sha(b):return hashlib.sha256(b).hexdigest()
def actions(text):
    return {int(m[1]):b for b in re.split(r'(?=\[Begin Action)',text,flags=re.I) if (m:=re.match(r'\[Begin Action (\d+)\]',b,re.I))}
def windows(frames,total,kind):
    return [next(f for f in reversed(frames) if f['start']<=tick)['boxes'][kind] for tick in range(total)]
def attack_contract(text):
    result=[]
    for b in re.split(r'(?=\[State\s+)',text,flags=re.I):
        m=re.search(r'(?im)^type\s*=\s*(HitDef|Projectile|TargetLifeAdd)\s*$',b)
        if not m:continue
        fields={}
        for k in ['attr','damage','kill','absolute','fall','air.velocity','ground.velocity']+(['value'] if m[1].lower()=='targetlifeadd' else []):
            f=re.search(r'(?im)^'+re.escape(k)+r'\s*=\s*([^;\r\n]+)',b)
            if f:fields[k]=re.sub(r'\s+','',f[1]).lower()
        result.append((m[1].lower(),fields))
    return result
def main():
    build=json.loads((ROOT/'design/roster_repair/build.json').read_text());delivery=json.loads((ROOT/'previews/roster_delivery_manifest.json').read_text())
    result={};total=0
    for ch in CHARS:
        folder=ROOT/ch;before=Archive(original(folder/(ch+'.sff')));after=Archive((folder/(ch+'.sff')).read_bytes())
        assert before.entries.keys()<=after.entries.keys()
        for key,entry in before.entries.items():
            if ch in ['Mamushi','RyuShinju','JuraShinju','HidariShinju','MatsuriShinju'] and key[0] in [0,1,2,9000]:
                im,ax=before.image(key);expected,_=recolor(im);actual,axis=after.image(key);a=np.array(actual);b=np.array(expected);mask=b[:,:,3]>0
                assert actual.size==expected.size and axis==ax,(ch,key,'source dimensions/axis')
                assert np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:,:,:3][mask],b[:,:,:3][mask]),(ch,key,'body changed beyond iris palette')
            else:assert entry==after.entries[key],(ch,key,'existing sprite changed')
        air=(folder/(ch+'.air')).read_text();old=actions(original(folder/(ch+'.air')).decode());new=actions(air)
        for n in build[ch]['updated_actions']:
            frames,duration=parse_action(old[n]);current,_=parse_action(new[n]);assert windows(frames,duration,1)==windows(current,duration,1),(ch,n,'attack window changed')
        for p in folder.glob('*.cns'):
            assert attack_contract(original(p).decode())==attack_contract(p.read_text()),(ch,p.name,'damage/trajectory contract changed')
        if ch=='MatsuriShinju':assert not re.search(r'(?m)^8600,',air),'Loose clothing still referenced'
        if ch in ['MatsuriShinju','JuraShinju']:
            records=json.loads((folder/'assets/senki/manifest.json').read_text())
            for r in records:
                if 'Mktn' not in r['key'] and 'Mokuton' not in r['key']:continue
                im,axis=after.image((r['group'],r['number']));assert im.getbbox()[3]-1==axis[1],(ch,r['key'],'floating ground rim')
        if ch=='Mamushi':
            for n in [5000,5001,5002,5010,5020,5030,5050,5060]:assert 'Clsn2' in new[n],('Missing reception',n)
        path=ROOT/ARCHIVES[ch];d=delivery['archives'][ch];assert path.stat().st_size==d['bytes'] and sha(path.read_bytes())==d['sha256']
        assert all(sha((folder/n).read_bytes())==s for n,s in d['files'].items())
        checks=json.loads((ROOT/'previews/roster_receiving'/(ch+'.json')).read_text());assert all(r['damage']>0 and r['hurt'] and r['recovered'] and (r['attack']!='combo' or r['hits_received']==3) for r in checks)
        total+=len(checks)
        result[ch]=dict(original_sprites=len(before.entries),additional_source_sprites=len(after.entries)-len(before.entries),source_body_geometry_preserved=True,old_body_changes='requested iris palette only' if ch in ['Mamushi','RyuShinju','JuraShinju','HidariShinju','MatsuriShinju'] else 'none',original_attack_windows_preserved=True,damage_and_ultimate_contracts_preserved=True,receiving_cases=len(checks),runtime_files={p.name:sha(p.read_bytes()) for p in sorted(folder.iterdir()) if p.is_file() and p.suffix in ['.def','.cns','.cmd','.air','.sff','.snd']})
    dash=json.loads((ROOT/'previews/roster_dash_checks.json').read_text());assert all(r['passed'] for rows in dash.values() for r in rows)
    pressure=json.loads((ROOT/'previews/roster_pressure_after.json').read_text());assert all(r['player_control_ticks']>0 and r['max_continuous_hurt_ticks']<240 and r['cpu_damage_received']>0 for r in pressure)
    general=json.loads((ROOT/'previews/roster_regressions/summary.json').read_text());assert len(general)==11 and all(r['passed'] for r in general)
    demo=json.loads((ROOT/'previews/MatsuriShinju_demo_checks.json').read_text());assert not demo['failures'] and demo['all_specials_shown'] and demo['specials_per_form']==13
    mfiles=[f'MatsuriShinju.{s}' for s in ['def','cns','cmd','air','sff','snd']]+['MatsuriShinju_common.cns']
    assert demo['runtime_sha256']==sha(b''.join((ROOT/'MatsuriShinju'/n).read_bytes() for n in mfiles)),'Video belongs to another runtime'
    ranges=json.loads((ROOT/'previews/MatsuriShinju_rays_1.0_0_checks.json').read_text())
    assert ranges['runtime_sha256']==demo['runtime_sha256'] and all(not r['failures'] for r in ranges['cases'])
    reception=json.loads((ROOT/'previews/roster_receiving_demo.json').read_text());assert len(reception['scenes'])==10
    for video,expected in [(ROOT/demo['video'],demo['video_sha256']),(ROOT/reception['video'],reception['sha256'])]:assert sha(video.read_bytes())==expected
    bundle=ROOT/delivery['bundle']['archive'];assert sha(bundle.read_bytes())==delivery['bundle']['sha256']
    report=dict(characters=result,receiving_cases=total,double_tap_cases=sum(map(len,dash.values())),cpu_cases=len(pressure),matsuri_range_cases=len(ranges['cases']),general_regressions=general,bundle=delivery['bundle'],proof_video=reception,matsuri_video=demo,engine='Ikemen GO',compatibility='MUGEN 1.1 static contracts and native engine loading; exact Jump Force MUGEN V14 binary/controller not run',failures=[])
    (ROOT/'previews/roster_revision_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(result),'characters;',total,'receiving cases;',sum(map(len,dash.values())),'double-tap cases; original attack contracts and artifacts verified')
if __name__=='__main__':main()
