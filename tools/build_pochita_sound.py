#!/usr/bin/env python3
"""Build Pochita's compact, non-verbal SND from the supplied Aitoro Denji.

The selected 1000,* entries are explicitly used as chainsaw SE in the original
attack states. No voice groups or source artwork are copied into this archive.
"""
from pathlib import Path
import hashlib
import io
import json
import struct
import subprocess
import tempfile
import wave
import sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source_material/Denji_original/DENJI.snd'
DEST=ROOT/'PochitaTrueForm'
CHOICES=[(0,'chainsaw_accel',1000,0),(1,'chainsaw_short',1000,1),
         (2,'chainsaw_cut',1000,2),(3,'chainsaw_long',1000,3),
         (4,'impact_light',5,0),(5,'impact_heavy',5,2),(6,'swing',4,0)]

samples={}
if SOURCE.is_file() and '--from-wav' not in sys.argv:
    data=SOURCE.read_bytes()
    assert data[:12]==b'ElecbyteSnd\0'
    count,offset=struct.unpack_from('<II',data,16)
    for index in range(count):
        next_offset,size,group,number=struct.unpack_from('<IIii',data,offset)
        assert offset+16+size<=len(data)
        samples[group,number]=data[offset+16:offset+16+size]
        offset=next_offset
previous=json.loads((DEST/'assets/sound/provenance.json').read_text()) if not samples else []

(DEST/'assets/sound').mkdir(parents=True,exist_ok=True)
records=[];manifest=[]
with tempfile.TemporaryDirectory(prefix='pochita-audio-') as directory:
    for number,name,group,source_number in CHOICES:
        destination=DEST/'assets/sound'/f'{name}.wav'
        if samples:
            original=samples[group,source_number]
            temporary=Path(directory)/'source.wav';temporary.write_bytes(original)
            subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(temporary),
                            '-ac','1','-ar','22050','-c:a','pcm_s16le',str(destination)],check=True)
        payload=destination.read_bytes()
        with wave.open(io.BytesIO(payload)) as stream:
            assert (stream.getnchannels(),stream.getsampwidth(),stream.getframerate())==(1,2,22050)
            duration=stream.getnframes()/stream.getframerate()
        records.append((1,number,payload))
        manifest.append(dict(group=1,number=number,filename=destination.name,
                             source_group=group,source_number=source_number,
                             source_sha256=hashlib.sha256(original).hexdigest() if samples else previous[number]['source_sha256'],duration=round(duration,4)))

header=bytearray(512);header[:12]=b'ElecbyteSnd\0'
struct.pack_into('<HHII',header,12,1,1,len(records),512)
chunks=[];offset=512
for index,(group,number,payload) in enumerate(records):
    next_offset=0 if index==len(records)-1 else offset+16+len(payload)
    chunks.append(struct.pack('<IIii',next_offset,len(payload),group,number)+payload)
    offset=next_offset
destination=DEST/'PochitaTrueForm.snd'
destination.write_bytes(bytes(header)+b''.join(chunks))
# Re-read the archive, independently of the writer's source list.
packed=destination.read_bytes();count,offset=struct.unpack_from('<II',packed,16)
assert count==len(CHOICES)
for index in range(count):
    nxt,size,group,number=struct.unpack_from('<IIii',packed,offset)
    with wave.open(io.BytesIO(packed[offset+16:offset+16+size])) as stream:
        assert stream.getnframes()>0 and stream.getnchannels()==1 and stream.getsampwidth()==2
    offset=nxt
assert offset==0
(DEST/'assets/sound/provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Validated {count} non-verbal samples in {destination.name}: {destination.stat().st_size} bytes')
