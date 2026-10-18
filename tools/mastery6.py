#!/usr/bin/env python3
"""Add Taiwan-specific doctrine mastery modifiers to the defense posture spirits.

Usage: python3 -I -B mastery6.py <ideas_file> [<ideas_file> ...]
Idempotent: a spirit that already has its first mastery modifier is left alone.
"""
import re
import sys

MASTERY = {
    "TAI_did_legacy": [("defence_in_depth_mastery_gain_factor", 0.05)],
    "TAI_did_legacy_reformed": [("defence_in_depth_mastery_gain_factor", 0.10)],
    "TAI_posture_active_defense": [("combined_arms_mastery_gain_factor", 0.10), ("green_water_mastery_gain_factor", 0.10)],
    "TAI_posture_hard_roc": [("defence_in_depth_mastery_gain_factor", 0.15), ("local_airspace_defense_mastery_gain_factor", 0.10)],
    "TAI_posture_asymmetric": [("mission_command_mastery_gain_factor", 0.15), ("jeune_ecole_mastery_gain_factor", 0.15)],
    "TAI_posture_hybrid": [("mission_command_mastery_gain_factor", 0.10), ("green_water_mastery_gain_factor", 0.10), ("local_airspace_defense_mastery_gain_factor", 0.10)],
}

for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    changed = 0
    for idea, mods in MASTERY.items():
        m = re.search(r"(\t+)" + idea + r" = \{\n(.*?)\n\1\}", text, re.S)
        assert m, (path, idea)
        block = m.group(0)
        if mods[0][0] in block:
            continue
        mm = re.search(r"(\t+)modifier = \{\n", block)
        assert mm, (path, idea, "no modifier block")
        ind = mm.group(1) + "\t"
        lines = "".join(f"{ind}{k} = {v}\n" for k, v in mods)
        new_block = block[: mm.end()] + lines + block[mm.end():]
        text = text.replace(block, new_block)
        changed += 1
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(path, "updated", changed)
