#!/usr/bin/env python3
"""Real autonomous attacks, finite lifetime, hit reactions and puppet defeat."""
from pathlib import Path
import json, os, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    proof = []
    for damage in [False, True]:
        name = 'OugaYatsume_puppet_'+('damage' if damage else 'expiry')+'_checks.json'
        env = os.environ.copy()
        env.update(OUGA_CASES='["Vortice"]', OUGA_TICKS='440' if damage else '1100',
                   OUGA_HELPER_TRACE='1', OUGA_REPORT=name)
        if damage:
            env['OUGA_PUPPET_DAMAGE'] = '1'
        else:
            env.pop('OUGA_PUPPET_DAMAGE', None)
        subprocess.run([sys.executable, str(ROOT/'tools/check_ouga_in_engine.py')], cwd=ROOT, env=env, check=True)
        trace = Path(json.loads(Path('/tmp/Ouga_puppet_latest_trace.json').read_text())['trace'])
        rows = [l.split() for l in trace.read_text().splitlines()]
        report = json.loads((ROOT/'previews'/name).read_text())
        for case, r in enumerate(report['cases']):
            data = [q for q in rows if int(q[0]) == case]
            assert data and r['helpers'] == 0 and r['minimum_life'] == 1100
            assert all(1 <= int(q[1]) <= (440 if damage else 1100) for q in data)
            ages = [int(q[12]) for q in data]
            assert r['damage'] > 0 and any(int(q[13]) > 0 for q in data)
            entry = dict(kind='destroyed_by_hits' if damage else 'autonomous_expiry',
                         form=r['case']['form'], face=r['case']['face'],
                         maximum_age=max(ages), helpers_after=r['helpers'],
                         root_life=r['minimum_life'], damage=r['damage'])
            if damage:
                entry['hurt_frames'] = sum(q[2] == '9790' for q in data)
                entry['minimum_puppet_health'] = min(int(q[11]) for q in data)
                assert entry['hurt_frames'] > 0 and entry['minimum_puppet_health'] <= 100
                assert max(ages) < 300
            else:
                assert max(ages) == 899 and r['damage'] >= 400
            proof.append(entry)
    output = dict(runtime_sha256=report['runtime_sha256'], maximum_puppets=1,
                  health=300, lifetime_ticks=900, cases=proof)
    (ROOT/'previews/OugaYatsume_puppet_checks.json').write_text(json.dumps(output, indent=2)+'\n')
    print('PASS: eight native puppet expiry/defeat cases, both forms and facings')

if __name__ == '__main__':
    main()
