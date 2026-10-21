#!/usr/bin/env python3
"""Static integrity checks for the Eida MUGEN character."""

from __future__ import annotations

import configparser
import io
import re
import struct
import wave
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'Eida'
errors: list[str] = []
notes: list[str] = []

# MUGEN 1.1 expression calls. Ikemen accepts extensions (notably Min/Max)
# even for mugenversion=1.1; loading there alone cannot check this contract.
MUGEN11_CALLS = set('''abs acos animelem animelemno animelemtime animexist asin
atan ceil const const240p const480p const720p cos exp floor fvar gethitvar
helper hitvel ifelse ishelper ln log numexplod numhelper numprojid numtarget
playerid playeridexist projcanceltime projcontact projcontacttime projguarded
projguardedtime projhit projhittime selfanimexist sin sysfvar sysvar tan
var'''.split())


def check_mugen11_calls(path: Path) -> None:
    for line_number,line in enumerate(path.read_text(encoding='latin-1').splitlines(),1):
        code=line.split(';',1)[0]
        if '=' not in code or code.lstrip().startswith('['):
            continue
        expression=code.split('=',1)[1]
        expression=re.sub(r'"[^"\n]*"','',expression)
        check(re.search(r'(?:!?=)\s*\[[^\[\]\n]+,[^\[\]\n]+\]\s*(?:\|\||&&)',expression) is None,
              f'{path.name}:{line_number}: bare interval comparison before a logical operator; use separate trigger groups')
        for name in re.findall(r'\b([a-zA-Z_]\w*)\s*\(',expression):
            check(name.lower() in MUGEN11_CALLS,
                  f'{path.name}:{line_number}: expression call {name}() is not in the MUGEN 1.1 function list')


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_sff(path: Path) -> set[tuple[int, int]]:
    data = path.read_bytes()
    check(data[:12] == b"ElecbyteSpr\0", "Eida.sff: invalid signature")
    check(len(data) >= 512, "Eida.sff: truncated header")
    check(data[12:16] == bytes((0, 1, 0, 2)), "Eida.sff: expected SFF v2.0.1.0")
    (
        sprite_headers,
        count,
        palette_headers,
        palette_count,
        ldata_offset,
        ldata_size,
        tdata_offset,
        tdata_size,
    ) = struct.unpack_from("<IIIIIIII", data, 36)
    check(sprite_headers + count * 28 <= len(data), "Eida.sff: sprite header table outside file")
    check(palette_headers + palette_count * 16 <= len(data), "Eida.sff: palette header table outside file")
    check(ldata_offset + ldata_size <= len(data), "Eida.sff: local data outside file")
    check(tdata_offset + tdata_size <= len(data), "Eida.sff: translated data outside file")

    palettes: list[tuple[int, int]] = []
    for index in range(palette_count):
        group, number, colors, link, offset, size = struct.unpack_from(
            "<HHHHII", data, palette_headers + index * 16
        )
        check(colors == 256, f"Eida.sff: palette {index} does not have 256 colors")
        check(size == 1024, f"Eida.sff: palette {index} is not 256-color RGBA")
        check(offset + size <= ldata_size, f"Eida.sff: palette {index} data outside local block")
        palettes.append((group, number))

    sprites: set[tuple[int, int]] = set()
    for index in range(count):
        (
            group,
            number,
            width,
            height,
            axis_x,
            axis_y,
            link,
            image_format,
            color_depth,
            offset,
            size,
            palette_index,
            flags,
        ) = struct.unpack_from("<HHHHhhHBBIIHH", data, sprite_headers + index * 28)
        check(width > 0 and height > 0, f"Eida.sff: sprite {group},{number} has invalid dimensions")
        check(image_format == 0, f"Eida.sff: sprite {group},{number} is not raw format 0")
        check(color_depth == 8, f"Eida.sff: sprite {group},{number} is not 8-bit indexed")
        check(flags == 0, f"Eida.sff: sprite {group},{number} is not in local data")
        check(size == width * height, f"Eida.sff: sprite {group},{number} raw size mismatch")
        check(offset + size <= ldata_size, f"Eida.sff: sprite {group},{number} data outside local block")
        check(palette_index < palette_count, f"Eida.sff: sprite {group},{number} palette index outside table")
        check((group, number) not in sprites, f"Eida.sff: duplicate sprite {group},{number}")
        if group == 1000:
            check(height <= 51, f'Eida.sff: Daemon {number} exceeds child helper scale')
        if group == 8000:
            check((width,height)==(1280,720), f'Eida.sff: manga panel {number} lost its HD source resolution')
        if group == 340:
            check((width,height,axis_x,axis_y)==(96,72,48,70),
                  f'Eida.sff: support frame {number} changed its shared scale/origin')
        if group in (350,351):
            check((width,height,axis_x,axis_y)==(128,80,64,78),
                  f'Eida.sff: presentation frame {group},{number} lost its shared feet origin')
        if group == 8600:
            check((width,height,axis_x,axis_y)==(96,88,48,86) and number in (0,1),
                  f'Eida.sff: original embrace {number} changed native scale/origin')
        sprites.add((group, number))
    check(len(sprites) == count, f"Eida.sff: header says {count} sprites, parsed {len(sprites)}")
    return sprites


def parse_snd(path: Path) -> set[tuple[int, int]]:
    data = path.read_bytes()
    check(data[:12] == b"ElecbyteSnd\0", "Eida.snd: invalid signature")
    check(data[12:16] == bytes((1, 0, 1, 0)), "Eida.snd: invalid SND version fields")
    count, offset = struct.unpack_from("<II", data, 16)
    sounds: set[tuple[int, int]] = set()
    for index in range(count):
        next_offset, size, group, number = struct.unpack_from("<IIii", data, offset)
        payload = data[offset + 16 : offset + 16 + size]
        check(len(payload) == size, f"Eida.snd: sound {group},{number} truncated")
        try:
            with wave.open(io.BytesIO(payload), "rb") as wav:
                check(wav.getnchannels() == 1, f"Eida.snd: sound {group},{number} is not mono")
                check(wav.getsampwidth() == 2, f"Eida.snd: sound {group},{number} is not 16-bit PCM")
        except Exception as exc:
            errors.append(f"Eida.snd: sound {group},{number} invalid WAV: {exc}")
        check((group, number) not in sounds, f"Eida.snd: duplicate sound {group},{number}")
        sounds.add((group, number))
        if index < count - 1:
            check(next_offset > offset, f"Eida.snd: sound {group},{number} has invalid next offset")
            offset = next_offset
    check(len(sounds) == count, f"Eida.snd: header says {count} sounds, parsed {len(sounds)}")
    return sounds


def sections(text: str):
    current = None
    body: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*\[", line):
            if current is not None:
                yield current, body
            current, body = line.strip(), []
        elif current is not None:
            body.append(line)
    if current is not None:
        yield current, body


def field(body: list[str], name: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(name)}\s*=\s*([^;]+)", re.I)
    for line in body:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def integer(value: str | None) -> int | None:
    return int(value) if value and re.fullmatch(r"-?\d+", value) else None


def main() -> None:
    for filename in ("Eida.def", "Eida.air", "Eida.cmd", "Eida.cns", "common1.cns", "Eida.sff", "Eida.snd"):
        check((ROOT / filename).is_file(), f"missing {filename}")

    def_text = (ROOT / "Eida.def").read_text(encoding="utf-8")
    for key in ("sprite", "anim", "sound", "cmd", "cns", "stcommon"):
        match = re.search(rf"(?im)^\s*{key}\s*=\s*([^;\r\n]+)", def_text)
        check(bool(match), f"Eida.def: missing {key}")
        if match:
            check((ROOT / match.group(1).strip()).is_file(), f"Eida.def: {key} target missing")

    sprites = parse_sff(ROOT / "Eida.sff")
    sounds = parse_snd(ROOT / "Eida.snd")

    air_text = (ROOT / "Eida.air").read_text(encoding="utf-8")
    for counter in (1200,1300,1350):
        action=re.search(rf'(?ims)^\[Begin Action {counter}\].*?(?=^\[Begin Action|\Z)',air_text)
        check(bool(action and re.search(r'(?im)^Clsn1(?:Default)?:\s*[1-9]',action[0])),
              f'Eida.air: counter {counter} is missing its reversal collision box')
    actions: set[int] = set()
    idle_refs: list[tuple[int, int]] = []
    frame_times: dict[int,list[int]] = {}
    current_action = None
    for line in air_text.splitlines():
        match = re.match(r"^\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current_action = int(match.group(1))
            check(current_action not in actions, f"Eida.air: duplicate action {current_action}")
            actions.add(current_action)
            frame_times[current_action]=[]
            continue
        match = re.match(r"^\s*(\d+)\s*,\s*(\d+)\s*,", line)
        if match:
            ref = (int(match.group(1)), int(match.group(2)))
            check(ref in sprites, f"Eida.air: action {current_action} references missing sprite {ref[0]},{ref[1]}")
            if current_action == 0:
                idle_refs.append(ref)
            timing=re.match(r'^\s*\d+\s*,\s*\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*(-?\d+)',line)
            if timing and current_action is not None:
                frame_times[current_action].append(int(timing.group(1)))
    required_actions = {0, 10, 11, 12, 20, 21, 40, 41, 42, 43, 44, 47, 200, 210, 220, 500, 600, 1000, 1010, 1020, 1100, 1200, 1300, 3000, 8000, 8001, 8002, 8003, 5000, 5050, 5100, 5110, 5120}
    check(required_actions <= actions, f"Eida.air: missing actions {sorted(required_actions - actions)}")
    check(len(idle_refs) >= 4 and all(group == 0 for group, _ in idle_refs), "Eida.air: idle contains a non-idle sprite group")
    for action in (5100,5170,5120):
        times=frame_times.get(action,[])
        check(bool(times) and all(time>=0 for time in times) and sum(times)>0,
              f'Eida.air: recovery transition {action} must finish; an infinite frame can trap knockdown recovery')

    cmd_text = (ROOT / "Eida.cmd").read_text(encoding="utf-8")
    defined_commands: set[str] = set()
    for header, body in sections(cmd_text):
        if header.lower() == "[command]":
            name = field(body, "name")
            if name:
                defined_commands.add(name.strip('"').lower())
    used_commands = {m.group(1).lower() for m in re.finditer(r'(?i)command\s*=\s*"([^"]+)"', cmd_text)}
    check(used_commands <= defined_commands, f"Eida.cmd: undefined commands {sorted(used_commands - defined_commands)}")
    check(re.search(r'(?is)name\s*=\s*"Omnipotencia".*?command\s*=\s*x', cmd_text) is not None, "Eida.cmd: Omnipotencia is not mapped to internal x")
    check(re.search(r'(?is)name\s*=\s*"Carga".*?command\s*=\s*/s', cmd_text) is not None, "Eida.cmd: charge is not mapped to held internal s")

    cns_paths = tuple(ROOT / name for name in ('Eida.cns','Specials.cns','Omnipotencia.cns','common1.cns'))
    all_states: set[int] = set()
    parsed_sections = []
    for path in cns_paths:
        check_mugen11_calls(path)
        text = path.read_text(encoding="latin-1")
        for header, body in sections(text):
            match = re.match(r"\[Statedef\s+(-?\d+)\]", header, re.I)
            if match:
                state_number = int(match.group(1))
                check(state_number not in all_states or path.name == 'common1.cns', f'{path.name}: duplicate state {state_number}')
                all_states.add(state_number)
            parsed_sections.append((path.name, header, body))

    parsed_sections.extend(('Eida.cmd', header, body) for header,body in sections(cmd_text))
    check_mugen11_calls(ROOT/'Eida.cmd')
    local_refs: list[tuple[str, str, int]] = []
    for filename, header, body in parsed_sections:
        if filename in {'Eida.cns','Specials.cns','Omnipotencia.cns'}:
            # Check literal local animation references as well as sprite rows.
            # Common states retain legacy overrides; opponent-owned animations
            # in custom states and computed expressions are checked at runtime.
            animation=integer(field(body, 'anim'))
            if animation is not None and animation >= 0:
                check(animation in actions, f'{filename} {header}: references missing animation {animation}')
        controller = (field(body, "type") or "").lower().split(";")[-1].strip()
        if controller == 'assertspecial':
            flags=set('intro invisible roundnotover nobardisplay nobg nofg noshadow globalnoshadow nomusic noautoturn nowalk timerfreeze unguardable nojugglecheck noko nokosnd nokoslow noguarddist noairguard nocrouchguard nostandguard'.split())
            for key in ('flag','flag2','flag3'):
                value=field(body,key)
                if value:check(value.lower() in flags,f'{filename} {header}: invalid MUGEN AssertSpecial flag {value}')
        target = None
        if controller in {"changestate", "selfstate", "targetstate"}:
            target = integer(field(body, "value"))
        elif controller == "helper":
            target = integer(field(body, "stateno"))
        elif controller in {"hitdef", "reversaldef"}:
            for key in ("p1stateno", "p2stateno"):
                number = integer(field(body, key))
                if number is not None and number >= 0:
                    local_refs.append((filename, header, number))
        if target is not None and target >= 0:
            local_refs.append((filename, header, target))
    for filename, header, state in local_refs:
        check(state in all_states, f"{filename} {header}: references missing state {state}")

    eida_cns = '\n'.join(path.read_text(encoding='latin-1') for path in cns_paths)
    for state in (1000,1010,1020,1030,1050,1060,1100,1120,1140,1150,1160,1200,1300,1350):
        block=re.search(rf'(?ims)^\[Statedef {state}\].*?(?=^\[Statedef|\Z)',eida_cns)
        check(bool(block and re.search(r'(?ims)type = PlaySnd\ntrigger1 = Time = 0\nvalue = S1,21',block[0])),
              f'Eida: special {state} is missing its distinct activation sound')
    check((1,21) in sounds,'Eida.snd: missing special activation sample 1,21')
    for match in re.finditer(r"(?im)^\s*(?:value|hitsound|guardsound)\s*=\s*S(\d+)\s*,\s*(\d+)\s*$", eida_cns):
        ref = (int(match.group(1)), int(match.group(2)))
        check(ref in sounds, f"Eida.cns: references missing sound {ref[0]},{ref[1]}")

    notes.append(f"SFF v2.0.1.0: {len(sprites)} raw indexed sprites and palettes validated")
    notes.append(f"SND: {len(sounds)} mono PCM sounds, all WAV payloads decoded")
    notes.append(f"AIR: {len(actions)} actions; idle uses {len(idle_refs)} idle-only frames")
    notes.append(f"CNS: {len(all_states)} states across {len(cns_paths)} files")
    notes.append('CNS/CMD expression calls checked against MUGEN 1.1; Ikemen-only Min/Max calls rejected')
    notes.append('CNS/CMD interval comparisons checked for the reported MUGEN parsing failure')
    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
        raise SystemExit(1)
    print("VALIDATION PASSED")
    for item in notes:
        print(f"- {item}")


if __name__ == "__main__":
    main()
