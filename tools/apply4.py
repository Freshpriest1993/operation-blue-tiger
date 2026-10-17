#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 4 (AI paths) to a Millennium Dawn checkout.

Usage: python3 -I -B apply4.py <repo_root> <m4_dir> [--dry-run]
Run gen.py + apply.py and events_gen.py + apply2.py first.
"""
import os
import sys

REPO, M4 = sys.argv[1], sys.argv[2]
DRY = "--dry-run" in sys.argv
done, skipped = [], []


def p(*a):
    return os.path.join(REPO, *a)


def rd(path, bom=False):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as fh:
        return fh.read()


def wr(path, text, bom=False):
    if DRY:
        done.append("(dry) " + os.path.relpath(path, REPO))
        return
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)
    done.append(os.path.relpath(path, REPO))


def blk(name):
    return rd(os.path.join(M4, name))


def insert_before(rel, marker, anchor, text, bom=False):
    fp = p(*rel.split("/"))
    txt = rd(fp, bom)
    if marker in txt:
        skipped.append(rel)
        return
    assert txt.count(anchor) == 1, f"{rel}: anchor"
    wr(fp, txt.replace(anchor, text + anchor), bom)


insert_before("common/game_rules/00_game_rules.txt", "TAI_ai_behavior = {", "SIA_ai_behavior = {\n", blk("rule.txt"))
insert_before("localisation/english/MD_game_rules_l_english.yml", "TAI_AI_BEHAVIOR:", " #Thailand\n", blk("rule_loc.yml"), bom=True)
insert_before("common/on_actions/999_game_rules_on_actions.txt", "rule = TAI_ai_behavior", "\t\t\tABK = {\n", blk("wiring.txt"))

fp = p("common", "scripted_triggers", "99_TAI_scripted_triggers.txt")
txt = rd(fp)
if "TAI_ai_alt_path = {" in txt:
    skipped.append("triggers")
else:
    wr(fp, txt.rstrip("\n") + "\n" + blk("triggers.txt"))

fp = p("events", "Taiwan.txt")
txt = rd(fp)
if "TAI_ai_historical_path" in txt:
    skipped.append("taiwan.3")
else:
    chances = {
        "2": "\t\tai_chance = {\n\t\t\tbase = 1\n\t\t\tmodifier = { factor = 25 OR = { TAI_ai_historical_path = yes has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH } }\n\t\t\tmodifier = { factor = 0 has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH }\n\t\t}\n",
        "1": "\t\tai_chance = {\n\t\t\tbase = 1\n\t\t\tmodifier = { factor = 25 has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH }\n\t\t\tmodifier = { factor = 0 OR = { TAI_ai_historical_path = yes has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH } }\n\t\t}\n",
        "14": "\t\tai_chance = {\n\t\t\tbase = 1\n\t\t\tmodifier = { factor = 0 OR = { TAI_ai_historical_path = yes TAI_ai_alt_path = yes } }\n\t\t}\n",
    }
    for idx, chance in chances.items():
        old = f"\t\tset_temp_variable = {{ rul_party_temp = {idx} }}\n\t\tset_temp_variable = {{ change_leader_temp = 1 }}\n\t\tchange_ruling_party_effect = yes\n\t}}\n"
        assert txt.count(old) == 1, f"taiwan.3 option {idx}"
        txt = txt.replace(old, old[:-3] + chance + "\t}\n")
    wr(fp, txt)

fp = p("Changelog.txt")
txt = rd(fp)
head = txt[:txt.find("\nv", 5)] if "\nv" in txt[5:] else txt
key = " - Country AI path game rules standardised to Historical / alternate paths / Random Path / No Path: "
i = head.find(key)
assert i != -1, "shared AI path changelog line missing"
j = head.index("\n", i)
line = head[i:j]
if ", TAI" in line or ": TAI" in line:
    skipped.append("changelog")
else:
    wr(fp, txt[:j] + ", TAI" + txt[j:])

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
