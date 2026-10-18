#!/usr/bin/env python3
"""Apply the RoC-development integration to a Millennium Dawn checkout (integration/obt-roc-unified).

Usage: python3 -I -B apply_roc.py <repo_root> <bundle_dir> [--dry-run]

<bundle_dir> holds:
  new/        files that do not exist yet in the repo (copied as-is; an existing file must already be identical)
  replace/    regenerated OBT files; the repo copy must match base_hashes.txt or already equal the new file
  base_hashes.txt   sha256 of the repo files that replace/ supersedes
Targeted edits (game rule options, AI path trigger, reserve demobilization, starting spirit, changelog,
leader portrait) are applied with exact anchors and are idempotent.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

REPO, BUNDLE = sys.argv[1], sys.argv[2]
DRY = "--dry-run" in sys.argv
done, skipped, problems = [], [], []


def p(rel):
    return os.path.join(REPO, *rel.split("/"))


def rd(path, bom=False):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as fh:
        return fh.read()


def wr(rel, text, bom=False):
    if DRY:
        done.append("(dry) " + rel)
        return
    os.makedirs(os.path.dirname(p(rel)), exist_ok=True)
    with open(p(rel), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)
    done.append(rel)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def files_under(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            full = os.path.join(d, f)
            yield os.path.relpath(full, root).replace(os.sep, "/"), full


# ---------------------------------------------------------------- pre-flight
base = {}
for line in open(os.path.join(BUNDLE, "base_hashes.txt"), encoding="utf-8"):
    h, rel = line.rstrip("\n").split("  ", 1)
    base[rel] = h

for rel, full in files_under(os.path.join(BUNDLE, "replace")):
    cur = sha(p(rel))
    if cur not in (base[rel], sha(full)):
        problems.append(f"{rel} has changed since the integration was built; rebuild before applying")

for rel, full in files_under(os.path.join(BUNDLE, "new")):
    if os.path.exists(p(rel)) and sha(p(rel)) != sha(full):
        problems.append(f"{rel} already exists with different content")

# duplicate definitions: new spirits, decisions, scripted triggers and loc keys must not exist elsewhere
new_root = os.path.join(BUNDLE, "new")
new_ideas = re.findall(r"^\t\t(TAI_[A-Za-z0-9_]+) = \{", rd(os.path.join(new_root, "common/ideas/99_TAI_roc_dev_ideas.txt")), re.M)
new_decs = re.findall(r"^\t([A-Za-z0-9_]+) = \{", rd(os.path.join(new_root, "common/decisions/ROC_dev_decisions.txt")), re.M)
new_trig = re.findall(r"^([A-Za-z0-9_]+) = \{", rd(os.path.join(new_root, "common/scripted_triggers/99_ROC_dev_scripted_triggers.txt")), re.M)
new_loc = re.findall(r"^ ([A-Za-z0-9_.]+):", rd(os.path.join(new_root, "localisation/english/MD_ROC_dev_l_english.yml"), True), re.M)
if len(new_loc) != len(set(new_loc)):
    problems.append("duplicate keys inside MD_ROC_dev_l_english.yml")
mine = {f"common/ideas/99_TAI_roc_dev_ideas.txt", "common/decisions/ROC_dev_decisions.txt", "common/scripted_triggers/99_ROC_dev_scripted_triggers.txt"}
defs = set()
for sub in ("common/ideas", "common/decisions", "common/scripted_triggers"):
    for fn in os.listdir(p(sub)):
        rel = f"{sub}/{fn}"
        if fn.endswith(".txt") and rel not in mine:
            defs.update(re.findall(r"^\s*([A-Za-z0-9_]+) = \{", rd(p(rel)), re.M))
for i in new_ideas + new_decs + new_trig:
    if i in defs and i not in ("OBT_reserve_category", "OBT_cross_strait_category"):
        problems.append(f"already defined elsewhere: {i}")
keys = set()
for fn in os.listdir(p("localisation/english")):
    if fn.endswith(".yml") and fn != "MD_ROC_dev_l_english.yml":
        keys.update(re.findall(r"^ ([A-Za-z0-9_.]+):", rd(p("localisation/english/" + fn), True), re.M))
for k in new_loc:
    if k in keys:
        problems.append(f"loc key already exists: {k}")
for fn in os.listdir(p("events")):
    if fn.endswith(".txt") and fn != "ROC_dev_events.txt" and "add_namespace = roc_dev" in rd(p("events/" + fn)):
        problems.append(f"namespace roc_dev already used in events/{fn}")

if problems:
    print("PRE-FLIGHT FAILED")
    for x in problems:
        print("  " + x)
    sys.exit(1)

# ---------------------------------------------------------------- 1. new files
for rel, full in files_under(os.path.join(BUNDLE, "new")):
    if os.path.exists(p(rel)):
        skipped.append(rel + " present")
    else:
        bom = rel.endswith(".yml")
        wr(rel, rd(full, bom), bom)

# ---------------------------------------------------------------- 2. regenerated OBT files
for rel, full in files_under(os.path.join(BUNDLE, "replace")):
    if sha(p(rel)) == sha(full):
        skipped.append(rel + " current")
    else:
        wr(rel, rd(full))


# ---------------------------------------------------------------- 3. targeted edits
def edit(rel, marker, old, new, bom=False):
    txt = rd(p(rel), bom)
    if marker in txt:
        skipped.append(f"{rel} ({marker[:40]}) present")
        return
    assert txt.count(old) == 1, f"{rel}: anchor not unique: {old[:60]}"
    wr(rel, txt.replace(old, new), bom)


# AUG's ROC_ai_behavior options join OBT's TAI_ai_behavior rule
rules = rd(p("common/game_rules/00_game_rules.txt"))
m = re.search(r"^TAI_ai_behavior = \{\n.*?^\}\n", rules, re.M | re.S)
assert m, "TAI_ai_behavior rule not found"
blockt = m.group(0)
if "PROJECT_NATIONAL_GLORY" in blockt:
    skipped.append("TAI_ai_behavior options present")
else:
    anchor = "\tdefault = {\n\t\tname = NO_PATH\n"
    assert blockt.count(anchor) == 1
    opts = "".join(f"\toption = {{\n\t\tname = {o}\n\t\ttext = \"RULE_OPTION_TAI_{o}\"\n\t\tdesc = \"RULE_OPTION_TAI_{o}_DESC\"\n\t}}\n"
                   for o in ("PROJECT_NATIONAL_GLORY", "UNITE_CHANNEL", "ROAD_TO_SPLIT"))
    wr("common/game_rules/00_game_rules.txt", rules.replace(blockt, blockt.replace(anchor, opts + anchor)))

edit("common/scripted_triggers/99_TAI_scripted_triggers.txt", "TAI_PNG_FOCUS_PATH",
     "TAI_ai_alt_path = {\n\tOR = {\n\t\thas_global_flag = TAI_ACCOMMODATION_FOCUS_PATH\n\t\thas_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH\n",
     "TAI_ai_alt_path = {\n\tOR = {\n\t\thas_global_flag = TAI_ACCOMMODATION_FOCUS_PATH\n\t\thas_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH\n"
     "\t\thas_global_flag = TAI_PNG_FOCUS_PATH\n\t\thas_global_flag = TAI_UNITE_CHANNEL_FOCUS_PATH\n\t\thas_global_flag = TAI_ROAD_TO_SPLIT_FOCUS_PATH\n")

edit("common/scripted_effects/99_OBT_reserve_scripted_effects.txt", "clr_country_flag = TAI_mob_north_second_level",
     "\tset_country_flag = { flag = OBT_mob_cooldown days = 365 value = 1 }\n}",
     "\tset_country_flag = { flag = OBT_mob_cooldown days = 365 value = 1 }\n\tclr_country_flag = TAI_mob_north_second_level\n"
     "\tclr_country_flag = TAI_mob_central_second_level\n\tclr_country_flag = TAI_mob_south_second_level\n\tclr_country_flag = TAI_total_mobilized\n}")

edit("history/countries/TAI - Taiwan.txt", "TAI_921_earthquake", "\t\tnuclear_energy\n", "\t\tnuclear_energy\n\t\tTAI_921_earthquake\n")

cl_old = "Taiwan (Operation Blue Tiger), 310 focuses across the 2000 succession,"
cl_new = "Taiwan (Operation Blue Tiger), 368 focuses (including AUG's RoC-development tree: Island Society, Southern Policy and Project National Glory) across the 2000 succession,"
edit("Changelog.txt", cl_new, cl_old, cl_new)

# AUG's John Chiang portrait, taken byte-exact from upstream/RoC-development
portrait = "gfx/leaders/TAI/John_Chiang.dds"
if os.path.exists(p(portrait)):
    skipped.append(portrait + " present")
elif "--no-portrait" in sys.argv:
    skipped.append(portrait + " (skipped on request)")
elif DRY:
    done.append("(dry) " + portrait)
else:
    data = subprocess.run(["git", "-C", REPO, "show", f"ceb1a0c1f5:{portrait}"], capture_output=True, check=True).stdout
    assert data[:4] == b"DDS ", "portrait is not a DDS file"
    with open(p(portrait), "wb") as fh:
        fh.write(data)
    done.append(portrait)

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
