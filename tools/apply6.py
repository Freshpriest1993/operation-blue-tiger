#!/usr/bin/env python3
"""Apply Operation Blue Tiger party branches (milestone 6) to a Millennium Dawn checkout.

Usage: python3 -I -B apply6.py <repo_root> <focus_out_dir> <events_out_dir> [--dry-run]
Run gen.py and events_gen.py first.
"""
import os
import re
import sys

REPO, FOUT, EOUT = sys.argv[1:4]
DRY = "--dry-run" in sys.argv
done, skipped = [], []


def p(rel):
    return os.path.join(REPO, *rel.split("/"))


def rd(path, bom=False):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as fh:
        return fh.read()


def wr(rel, text, bom=False):
    if DRY:
        done.append("(dry) " + rel)
        return
    with open(p(rel), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)
    done.append(rel)


def keys(text):
    return dict(re.findall(r"^ ([A-Za-z0-9_.]+): (.*)$", text, re.M))


def append_loc(rel, src_text, marker):
    txt = rd(p(rel), True)
    have = keys(txt)
    add = []
    for k, v in keys(src_text).items():
        if k not in have:
            add.append(f" {k}: {v}")
        elif have[k] != v:
            sys.exit(f"{rel}: existing key {k} differs from generated text")
    if not add:
        skipped.append(rel + " current")
        return
    wr(rel, txt.rstrip("\n") + f"\n # {marker}\n" + "\n".join(add) + "\n", True)


focus = rd(os.path.join(FOUT, "05_taiwan.txt"))
cur = rd(p("common/national_focus/05_taiwan.txt"))
if focus == cur:
    skipped.append("focus tree current")
else:
    wr("common/national_focus/05_taiwan.txt", focus)
append_loc("localisation/english/MD_focus_TAI_l_english.yml", rd(os.path.join(FOUT, "focus_loc.yml")), "Operation Blue Tiger: party branches")

evs = rd(os.path.join(EOUT, "Taiwan_Blue_Tiger.txt"))
cur = rd(p("events/Taiwan_Blue_Tiger.txt"))
if evs == cur:
    skipped.append("events current")
else:
    assert evs.startswith(cur.rstrip("\n")), "generated events do not extend the current file"
    wr("events/Taiwan_Blue_Tiger.txt", evs)
append_loc("localisation/english/MD_focus_TAI_l_english.yml", rd(os.path.join(EOUT, "events_loc.yml")), "Operation Blue Tiger: party events")

ideas = rd(p("common/ideas/05_taiwan.txt"))
if "TAI_kmt_roc_on_taiwan = {" in ideas:
    skipped.append("ideas present")
else:
    tail = "\t}\n}\n"
    assert ideas.endswith(tail)
    wr("common/ideas/05_taiwan.txt", ideas[: -len(tail)] + rd(os.path.join(EOUT, "ideas6_block.txt")) + tail)

sl = rd(p("common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt"))
if "TAI.neutral_Social_TSU" in sl:
    skipped.append("TSU party name present")
else:
    for key in ("neutral_Social", "neutral_Social_desc"):
        anchor = f"\ttext = {{ trigger = {{ original_tag = TAI date < 2019.1.1 }} localization_key = TAI.{key} }}\n"
        assert sl.count(anchor) == 1, key
        sl = sl.replace(anchor, f"\ttext = {{ trigger = {{ original_tag = TAI date > 2001.8.12 date < 2019.1.1 }} localization_key = TAI.{key.replace('neutral_Social', 'neutral_Social_TSU')} }}\n" + anchor)
    wr("common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt", sl)

cl = rd(p("Changelog.txt"))
old = "Taiwan (Operation Blue Tiger), 247 focuses across the 2000 succession, democratic reform,"
new = "Taiwan (Operation Blue Tiger), 310 focuses across the 2000 succession, party branches for the KMT, DPP, PFP, Taiwan Solidarity Union and Green Party, democratic reform,"
if new in cl:
    skipped.append("changelog current")
else:
    assert cl.count(old) == 1
    wr("Changelog.txt", cl.replace(old, new))

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
