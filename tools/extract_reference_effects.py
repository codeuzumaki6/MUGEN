#!/usr/bin/env python3
"""Extract supplied Nezuko's non-character effects, retaining original axes.

Usage: python3 tools/extract_reference_effects.py /path/to/Nezuko/sff.sff
The blue coloring and transparency are applied by MUGEN, not baked into PNGs.
"""
import json
import sys
from pathlib import Path
from make_combo_preview import Sff2, ROOT

source = Sff2(Path(sys.argv[1]))
out = ROOT / 'Eida/assets/effects/reference'
out.mkdir(parents=True, exist_ok=True)
axes = {}
for group, source_group, count in ((8300,510,13),(8400,7010,4),(8410,6120,14),(8420,520,6)):
    for index in range(count):
        sprite, axis = source.image(source_group,index)
        sprite.save(out / f'{group}_{index}.png')
        axes[f'{group},{index}'] = axis
(out/'axes.json').write_text(json.dumps(axes,indent=2)+'\n')
print(f'Extracted {len(axes)} effect frames with original axes')
