#!/usr/bin/env python3
"""Read-only checks for the supplied two-pose, finite Omnipotencia scene.

Without --trace these are file checks, not an engine test. With --trace the
extra assertions describe the existing live-review hook's observed states and
Explods. They do not infer visible style, victim hiding, or physical control
from absent telemetry.
"""
from pathlib import Path
import argparse,hashlib,json,re,struct
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def inspect_compact_scene(character=None,trace=None):
    char=Path(character or ROOT/'Eida')
    text=(char/'Omnipotencia.cns').read_text()
    match=re.search(r'(?ims)^\[Statedef 3001\].*?(?=^\[Statedef|\Z)',text)
    assert match,'missing confirmed ultimate state'
    scene=match[0]
    controls=re.findall(r'(?ims)^\[State [^\]]+\].*?(?=^\[State|\Z)',scene)
    def field(block,key):
        found=re.search(rf'(?im)^\s*{re.escape(key)}\s*=\s*([^;\n]+)',block)
        return found[1].strip() if found else None
    hugs=[b for b in controls if (field(b,'type') or '').lower()=='explod' and field(b,'anim')=='8600']
    assert len(hugs)==1,'expected one compact paired-sprite Explod'
    hug=hugs[0]
    assert (field(hug,'postype') or '').lower()=='p1','hug must be anchored to the fighter, not screen-sized'
    assert (field(hug,'space') or '').lower()!='screen','hug must not become a screen poster'
    assert field(hug,'scale') and [float(v.strip()) for v in field(hug,'scale').split(',')]==[1,1],'supplied hug must be drawn at its native scale'
    for b in controls:
        if (field(b,'type') or '').lower()=='explod':
            assert field(b,'anim') not in {'8090','8000','8001','8002','8003','8004','8005','8006','8007'},'compact scene still contains the old matte/manga background'
    recoveries=[b for b in controls if (field(b,'type') or '').lower()=='changestate' and field(b,'value')=='0']
    assert recoveries,'missing return to idle'
    recovery=re.search(r'(?im)^trigger\d+\s*=\s*Time\s*>=\s*(\d+)',recoveries[-1])
    assert recovery and 140<=int(recovery[1])<=180,'confirmed scene should finish around 160 ticks'
    recovery_time=int(recovery[1])
    assert field(recoveries[-1],'ctrl')=='1','recovery controller does not restore control'
    damages=[b for b in controls if (field(b,'type') or '').lower()=='targetlifeadd']
    assert len(damages)==1 and field(damages[0],'value')=='-350','total confirmed damage must stay 350'
    air=(char/'Eida.air').read_text()
    action=re.search(r'(?ims)^\[Begin Action 8600\].*?(?=^\[Begin Action|\Z)',air)
    assert action,'missing paired-sprite animation'
    rows=[tuple(map(int,m)) for m in re.findall(r'(?m)^\s*(\d+)\s*,\s*(\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)',action[0])]
    full_manifest=char/'assets/full_pack/manifest.json'
    full_hug=[]
    if full_manifest.exists():
        full_hug=[r for r in json.loads(full_manifest.read_text())['frames'] if r['key'].startswith('Chiyo_S5_PreUp_')]
    expected_keys={(r['group'],r['number']) for r in full_hug} if full_hug else {(8600,0),(8600,1)}
    assert rows and {(r[0],r[1]) for r in rows}==expected_keys,'embrace must use only the supplied original poses'
    if full_hug:
        assert len(full_hug)==10
        import plistlib
        for rec in full_hug:
            atlas=ROOT/rec['source'];source_meta=plistlib.loads(atlas.read_bytes())['frames'];meta=source_meta.get(rec['key']+'.png',source_meta.get(rec['key']));assert meta
            x,y,w,h=map(int,re.findall(r'-?\d+',meta['frame']))
            source_frame=Image.open(atlas.with_suffix('.png')).convert('RGBA').crop((x,y,x+w,y+h))
            if meta.get('rotated'):source_frame=source_frame.transpose(Image.Transpose.ROTATE_90)
            assert (char/rec['file']).is_file()
            actual=Image.open(char/rec['file']).convert('RGBA')
            assert np.array_equal(np.array(actual),np.array(source_frame)),'full-pack hug must preserve source RGBA pixels'
            assert actual.width<=100 and rec['axis'][1]<=110,'full-pack hug became oversized'
            assert rec['body_redrawn'] is False and rec['crop'] is None and rec['size'] is None
    assert len(rows)<=20,'too many authored repeats for a compact two-pose scene'
    assert all(r[4]>0 for r in rows),'embrace must not hold an infinite source pose'
    assert sum(r[4] for r in rows)<=120,'paired animation is still excessively long'
    b=(char/'Eida.sff').read_bytes();offset,count=struct.unpack_from('<II',b,36)
    sprites=[]
    for i in range(count):
        g,no,w,h,x,y=struct.unpack_from('<HHHHhh',b,offset+i*28)
        if g==8600:sprites.append(dict(group=g,number=no,width=w,height=h,axis=[x,y]))
    assert {r['number'] for r in sprites}=={0,1} and len(sprites)==2,'SFF still contains replacement embrace artwork'
    assert all((r['width'],r['height'],r['axis'])==(96,88,[48,86]) for r in sprites),'hug lost its native canvas/feet axis'
    source=ROOT/'design/Eida_omnipotencia/original/Eida_sprites_en_captura.png'
    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()
    original=Image.open(source).convert('RGBA')
    manifest=json.loads((char/'assets/omni_hug/manifest.json').read_text())
    assert len(manifest)==2 and {r['number'] for r in manifest}=={0,1},'source manifest must describe exactly the original two poses'
    provenance=[]
    for record,box in zip(sorted(manifest,key=lambda r:r['number']),[(8,624,64,709),(66,622,118,707)]):
        assert record['group']==8600 and record['native_scale']==1 and record['ai_redrawn'] is False,'source manifest does not preserve native original art'
        assert tuple(record['source_box'])==box and record['source_sha256']==source_sha256,'source crop/hash does not match supplied sheet'
        assert record['axis']==[48,86],'source manifest changed its shared feet axis'
        pixels=np.array(original.crop(box));r,g,b=[pixels[:,:,i].astype(float) for i in range(3)]
        green=(g>55)&(g>r*1.38)&(g>b*1.18);pixels[green,3]=0
        keyed=Image.fromarray(pixels);bounds=keyed.getbbox();assert bounds and list(bounds)==record['trim_box'],'source trim no longer matches the alpha key'
        figure=keyed.crop(bounds)
        feet=figure.getchannel('A').crop((0,figure.height-5,figure.width,figure.height)).getbbox();assert feet
        x=round(48-(feet[0]+feet[2])/2);y=86-figure.height
        expected=Image.new('RGBA',(96,88));expected.alpha_composite(figure,(x,y))
        asset=Image.open(char/record['file']).convert('RGBA')
        assert np.array_equal(np.array(asset),np.array(expected)),f"pose {record['number']} no longer matches source pixels/alpha at native size"
        provenance.append(dict(number=record['number'],source_box=list(box),trim_box=list(bounds),native_figure_size=list(figure.size),canvas=[96,88],feet_axis=[48,86],visible_pixels=int(np.count_nonzero(np.array(asset.getchannel('A')))),rgba_pixels_match_source=True))
    report=dict(kind='static file checks',source_frame_references=sorted(expected_keys),full_pack_native_hug_frames=len(full_hug),authored_rows=len(rows),authored_ticks=sum(r[4] for r in rows),recovery_controller_tick=recovery_time,sprites=sprites,damage=350)
    report['original_source']=dict(file=str(source.relative_to(ROOT)),sha256=source_sha256,poses=provenance,processing='Green alpha key and packing only; source RGBA comparison at native scale. SFF may quantize colors for its indexed palette.')
    if trace is not None:
        live=[list(map(float,row)) for row in trace]
        confirmed=[r for r in live if int(r[3])==3001]
        assert confirmed,'no confirmed scene observed in engine trace'
        visible=[r for r in confirmed if r[7]>0]
        assert visible,'no compact embrace observed'
        assert any(12<=r[4]<=109 for r in visible),'embrace was absent during its intended beat'
        assert all(r[7]==0 for r in confirmed if r[4]>=130),'embrace outlived its short scene'
        assert max(r[4] for r in confirmed)<=180,'observed scene still repeats for several seconds'
        last=max(r[0] for r in confirmed)
        returned=next((r for r in live if r[0]>last and int(r[3])==0),None)
        assert returned,'no return to idle observed after the scene'
        report['engine_trace']=dict(first_scene_frame=confirmed[0][0],last_scene_frame=last,last_scene_time=max(r[4] for r in confirmed),first_hug_time=min(r[4] for r in visible),last_hug_time=max(r[4] for r in visible),returned_idle_frame=returned[0],thumbnail_frame=next((r[0] for r in visible if r[4]>=45),visible[-1][0]),visible_frame_samples=len(visible))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--character',type=Path,default=ROOT/'Eida');parser.add_argument('--trace',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();trace=[line.split() for line in args.trace.read_text().splitlines()] if args.trace else None
    report=inspect_compact_scene(args.character,trace)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
