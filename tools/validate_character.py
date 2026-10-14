#!/usr/bin/env python3
"""Static integrity checks for the Eida MUGEN character."""

from __future__ import annotations

import configparser
import io
import re
import struct
import wave
from pathlib import Path

from PIL import Image


ROOT = Path("/workspace/MUGEN/Eida")
errors: list[str] = []
notes: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_sff(path: Path) -> set[tuple[int, int]]:
    data = path.read_bytes()
    check(data[:12] == b"ElecbyteSpr\0", "Eida.sff: invalid signature")
    check(len(data) >= 512, "Eida.sff: truncated header")
    check(data[12:16] == bytes((1, 0, 0, 0)), "Eida.sff: invalid SFF v1 version bytes")
    count, first = struct.unpack_from("<II", data, 20)
    offset = first
    sprites: set[tuple[int, int]] = set()
    for index in range(count):
        check(offset + 32 <= len(data), f"Eida.sff: sprite {index} header outside file")
        if offset + 32 > len(data):
            break
        next_offset, size, _, _, group, number = struct.unpack_from("<IIhhHH", data, offset)
        payload = data[offset + 32 : offset + 32 + size]
        check(len(payload) == size, f"Eida.sff: sprite {group},{number} truncated")
        check(len(payload) >= 4 and payload[3] == 8, f"Eida.sff: sprite {group},{number} is not 8-bit PCX")
        try:
            Image.open(io.BytesIO(payload)).verify()
        except Exception as exc:
            errors.append(f"Eida.sff: sprite {group},{number} PCX invalid: {exc}")
        check((group, number) not in sprites, f"Eida.sff: duplicate sprite {group},{number}")
        sprites.add((group, number))
        if index < count - 1:
            check(next_offset > offset, f"Eida.sff: sprite {group},{number} has invalid next offset")
            offset = next_offset
    check(len(sprites) == count, f"Eida.sff: header says {count} sprites, parsed {len(sprites)}")
    return sprites


def parse_snd(path: Path) -> set[tuple[int, int]]:
    data = path.read_bytes()
    check(data[:12] == b"ElecbyteSnd\0", "Eida.snd: invalid signature")
    check(data[12:16] == bytes((1, 0, 0, 0)), "Eida.snd: invalid SND v1 version bytes")
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
    actions: set[int] = set()
    idle_refs: list[tuple[int, int]] = []
    current_action = None
    for line in air_text.splitlines():
        match = re.match(r"^\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current_action = int(match.group(1))
            check(current_action not in actions, f"Eida.air: duplicate action {current_action}")
            actions.add(current_action)
            continue
        match = re.match(r"^\s*(\d+)\s*,\s*(\d+)\s*,", line)
        if match:
            ref = (int(match.group(1)), int(match.group(2)))
            check(ref in sprites, f"Eida.air: action {current_action} references missing sprite {ref[0]},{ref[1]}")
            if current_action == 0:
                idle_refs.append(ref)
    required_actions = {0, 10, 11, 12, 20, 21, 40, 41, 42, 43, 44, 47, 200, 210, 220, 600, 1000, 1010, 1020, 1100, 1200, 1300, 3000, 8000, 8001, 8002, 8003, 5000, 5050, 5100, 5110, 5120}
    check(required_actions <= actions, f"Eida.air: missing actions {sorted(required_actions - actions)}")
    check(len(idle_refs) >= 4 and all(group == 0 for group, _ in idle_refs), "Eida.air: idle contains a non-idle sprite group")

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

    cns_paths = (ROOT / "Eida.cns", ROOT / "common1.cns")
    all_states: set[int] = set()
    parsed_sections = []
    for path in cns_paths:
        text = path.read_text(encoding="latin-1")
        for header, body in sections(text):
            match = re.match(r"\[Statedef\s+(-?\d+)\]", header, re.I)
            if match:
                all_states.add(int(match.group(1)))
            parsed_sections.append((path.name, header, body))

    local_refs: list[tuple[str, str, int]] = []
    for filename, header, body in parsed_sections:
        controller = (field(body, "type") or "").lower().split(";")[-1].strip()
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

    eida_cns = (ROOT / "Eida.cns").read_text(encoding="utf-8")
    for match in re.finditer(r"(?im)^\s*value\s*=\s*S(\d+)\s*,\s*(\d+)\s*$", eida_cns):
        ref = (int(match.group(1)), int(match.group(2)))
        check(ref in sounds, f"Eida.cns: references missing sound {ref[0]},{ref[1]}")

    notes.append(f"SFF: {len(sprites)} sprites, all PCX payloads decoded")
    notes.append(f"SND: {len(sounds)} mono PCM sounds, all WAV payloads decoded")
    notes.append(f"AIR: {len(actions)} actions; idle uses {len(idle_refs)} idle-only frames")
    notes.append(f"CNS: {len(all_states)} states across Eida.cns and common1.cns")
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
