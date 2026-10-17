#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 1 to a Millennium Dawn checkout.

Usage: python3 -I apply.py <repo_root> <generated_dir> <blocks_dir> [--dry-run]
Edits are additive and guarded by markers, so a second run changes nothing.
"""
import os
import re
import sys

REPO, GEN, BLK = sys.argv[1], sys.argv[2], sys.argv[3]
DRY = "--dry-run" in sys.argv
MARK = "Operation Blue Tiger"
done, skipped, problems = [], [], []


def p(*parts):
    return os.path.join(REPO, *parts)


def read(path, bom=False):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as fh:
        return fh.read()


def write(path, text, bom=False):
    if DRY:
        done.append("(dry) " + os.path.relpath(path, REPO))
        return
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)
    done.append(os.path.relpath(path, REPO))


def block(name):
    return read(os.path.join(BLK, name))


# ---- pre-flight duplicate checks against the whole repo
focus_text = read(os.path.join(GEN, "05_taiwan.txt"))
new_focus_ids = re.findall(r"^\t\tid = (\S+)", focus_text, re.M)
new_idea_ids = re.findall(r"^\t\t(TAI_[A-Za-z0-9_]+) = \{", block("ideas_block.txt"), re.M)
new_trig = re.findall(r"^(TAI_[A-Za-z0-9_]+) = \{", block("triggers_block.txt"), re.M)
new_eff = re.findall(r"^(TAI_[A-Za-z0-9_]+) = \{", block("effects_block.txt"), re.M)
loc_new = block("ideas_loc.yml") + read(os.path.join(GEN, "focus_loc.yml")) + read(os.path.join(GEN, "var_loc.yml"))
new_keys = re.findall(r"^ ([A-Za-z0-9_.]+):", loc_new, re.M)

target_focus = p("common", "national_focus", "05_taiwan.txt")
already = os.path.exists(target_focus)

existing_defs = set()
for sub in ("common/national_focus", "common/ideas", "common/scripted_triggers", "common/scripted_effects", "common/decisions"):
    for fn in os.listdir(p(*sub.split("/"))):
        fp = p(*sub.split("/"), fn)
        if not fn.endswith(".txt") or (already and fp == target_focus):
            continue
        txt = read(fp)
        if MARK in txt and fn in ("05_taiwan.txt", "99_TAI_scripted_triggers.txt", "99_TAI_scripted_effects.txt"):
            txt = txt.split("# " + MARK)[0]
        existing_defs.update(re.findall(r"^\s*id = (TAI_\S+)", txt, re.M))
        existing_defs.update(re.findall(r"^\s*(TAI_[A-Za-z0-9_]+) = \{", txt, re.M))

existing_keys = set()
locdir = p("localisation", "english")
for fn in os.listdir(locdir):
    if fn.endswith(".yml"):
        txt = read(os.path.join(locdir, fn), bom=True)
        if fn == "MD_focus_TAI_l_english.yml" and MARK in txt:
            txt = txt.split(" # " + MARK)[0]
        existing_keys.update(re.findall(r"^ ([A-Za-z0-9_.]+):", txt, re.M))

for name, ids in (("focus", new_focus_ids), ("idea", new_idea_ids), ("trigger", new_trig), ("effect", new_eff)):
    for i in ids:
        if i in existing_defs:
            problems.append(f"{name} id already defined elsewhere: {i}")
for k in new_keys:
    if k in existing_keys:
        problems.append(f"loc key already exists: {k}")
seen = set()
for k in new_keys:
    if k in seen:
        problems.append(f"loc key duplicated in new text: {k}")
    seen.add(k)
for i in new_focus_ids:
    if i + "_desc" not in seen or i not in seen:
        problems.append(f"missing loc for focus {i}")
for i in new_idea_ids:
    if i not in seen:
        problems.append(f"missing loc for idea {i}")

if problems:
    print("PRE-FLIGHT FAILED")
    for x in problems:
        print("  " + x)
    sys.exit(1)

# ---- 1. focus tree (new file)
if already:
    if read(target_focus) == focus_text:
        skipped.append("focus file already current")
    else:
        write(target_focus, focus_text)
else:
    write(target_focus, focus_text)

# ---- 2. ideas: insert before the closing of ideas/country
ideas_fp = p("common", "ideas", "05_taiwan.txt")
ideas = read(ideas_fp)
if MARK in ideas:
    skipped.append("ideas already present")
else:
    tail = "\t}\n}\n"
    assert ideas.endswith(tail), "unexpected ideas file ending"
    ideas = ideas[: -len(tail)] + block("ideas_block.txt") + tail
    write(ideas_fp, ideas)

# ---- 3. triggers and effects: append
for sub, fn, blk in (("scripted_triggers", "99_TAI_scripted_triggers.txt", "triggers_block.txt"),
                     ("scripted_effects", "99_TAI_scripted_effects.txt", "effects_block.txt")):
    fp = p("common", sub, fn)
    txt = read(fp)
    if MARK in txt:
        skipped.append(fn + " already present")
    else:
        write(fp, txt.rstrip("\n") + "\n" + block(blk))

# ---- 4. localisation: append
loc_fp = p("localisation", "english", "MD_focus_TAI_l_english.yml")
loc = read(loc_fp, bom=True)
if MARK in loc:
    skipped.append("localisation already present")
else:
    write(loc_fp, loc.rstrip("\n") + "\n" + loc_new.lstrip("\n").rstrip("\n") + "\n", bom=True)

# ---- 5. history: starting spirits and variables
hist_fp = p("history", "countries", "TAI - Taiwan.txt")
hist = read(hist_fp)
if "TAI_young_democracy" in hist:
    skipped.append("history already present")
else:
    anchor_idea = "\t\tTAI_legacy_of_1949\n"
    assert hist.count(anchor_idea) == 1, "idea anchor not unique"
    start_ideas = ["TAI_young_democracy", "TAI_party_army", "TAI_did_legacy", "TAI_uneven_reserves", "TAI_limited_absorption"]
    hist = hist.replace(anchor_idea, anchor_idea + "".join(f"\t\t{i}\n" for i in start_ideas))
    anchor_var = "\tset_variable = { gdp_per_capita = 14.648 }\n"
    assert hist.count(anchor_var) == 1, "variable anchor not unique"
    obt_vars = [
        "\t# Operation Blue Tiger state (0-100 scales)",
        "\tset_variable = { TAI_us_confidence = 60 }",
        "\tset_variable = { TAI_military_confidence = 55 }",
        "\tset_variable = { TAI_reform_capacity = 50 }",
        "\tset_variable = { TAI_mainland_dependence = 30 }",
        "\tset_variable = { TAI_semiconductor_security = 85 }",
        "\tset_variable = { TAI_pressure_to_negotiate = 5 }",
        "\tset_variable = { TAI_taiwanese_identity = 40 }",
        "\tset_variable = { TAI_national_coordination = 40 }",
        "\tset_variable = { TAI_defense_posture = 1 }",
    ]
    hist = hist.replace(anchor_var, anchor_var + "\n".join(obt_vars) + "\n")
    write(hist_fp, hist)

# ---- 6. changelog: one BLUF line under the current version's Content section
ch_fp = p("Changelog.txt")
ch = read(ch_fp)
line = " - NEW FOCUS TREE: Taiwan (Operation Blue Tiger), 247 focuses across the 2000 succession, democratic reform, defense doctrine, semiconductors, cross-Strait relations, foreign partners and national resilience\n"
if "Operation Blue Tiger" in ch:
    skipped.append("changelog already present")
else:
    idx = ch.find("Content:\n")
    assert idx != -1 and idx < 200, "Content section not found near the top"
    idx += len("Content:\n")
    write(ch_fp, ch[:idx] + line + ch[idx:])

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
