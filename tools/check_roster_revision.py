#!/usr/bin/env python3
"""Run the accepted combat contracts serially against the new runtime."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews/roster_regressions';OUT.mkdir(exist_ok=True)
ENGINE='/workspace/.eida-tools/ikemen-nightly'
jobs=[('Eida',['check_moves_in_engine.py',ENGINE],{}),
      ('PochitaTrueForm',['check_pochita_in_engine.py',ENGINE],{}),
      ('Mamushi',['check_mamushi_in_engine.py',ENGINE],{}),
      ('Shibai',['check_shibai_in_engine.py',ENGINE],{}),
      ('JuraShinju',['check_jura_in_engine.py',ENGINE],{}),
      ('MitsukiTBV',['check_mitsuki_in_engine.py'],{}),
      ('RyuShinju',['check_ryu_in_engine.py'],{}),
      ('HidariShinju',['check_hidari_in_engine.py'],{}),
      ('HidariSusanoo',['check_hidari_susanoo_in_engine.py'],{}),
      ('MatsuriShinju',['check_matsuri_in_engine.py'],{}),
      ('MamushiCloneHealth',['check_mamushi_in_engine.py',ENGINE],{'MAMUSHI_CLONE_HEALTH_CHECK':'1'})]
if __name__=='__main__':
    wanted=set(sys.argv[1:]);summary=OUT/'summary.json'
    previous=json.loads(summary.read_text()) if wanted and summary.exists() else []
    by_name={r['character']:r for r in previous};reports=list(previous)
    for name,cmd,extra in jobs:
        if wanted and name not in wanted:continue
        env=os.environ.copy();env.update(extra);log=OUT/(name+'.log')
        with log.open('w') as f:r=subprocess.run([sys.executable]+[str(ROOT/'tools'/cmd[0])]+cmd[1:],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
        report=dict(character=name,passed=r.returncode==0,command=cmd,environment=extra,log=str(log.relative_to(ROOT)),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest());by_name[name]=report
        reports=[by_name[job[0]] for job in jobs if job[0] in by_name]
        print(name,'PASS' if report['passed'] else 'FAIL',flush=True)
        if r.returncode:print(log.read_text()[-7500:],flush=True)
        summary.write_text(json.dumps(reports,indent=2)+'\n')
    assert all(r['passed'] for r in reports),reports
