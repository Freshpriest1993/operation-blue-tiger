#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 5 (Return to the Mainland) to a Millennium Dawn checkout.

Usage: python3 -I -B apply5.py <repo_root> <m5_dir> [--dry-run]
Run rec_gen.py and roc_gen.py into <m5_dir>/out first.
"""
import os
import shutil
import sys

REPO, M5 = sys.argv[1], sys.argv[2]
OUTD = os.path.join(M5, "out")
DRY = "--dry-run" in sys.argv
done, skipped = [], []


def p(rel):
    return os.path.join(REPO, *rel.split("/"))


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


def src(name, out=False):
    return rd(os.path.join(OUTD if out else M5, name))


def new_file(rel, text, bom=False):
    fp = p(rel)
    if os.path.exists(fp):
        if rd(fp, bom) == text:
            skipped.append(rel + " current")
            return
        sys.exit(f"refusing to overwrite existing {rel}")
    wr(fp, text, bom)


new_file("common/bop/TAI.txt", src("bop_TAI.txt"))
new_file("common/decisions/TAI_reclamation_decisions.txt", src("TAI_reclamation_decisions.txt"))
new_file("common/ideas/99_TAI_reclamation_ideas.txt", src("ideas.txt"))
new_file("common/dynamic_modifiers/99_TAI_dynamic_modifiers.txt", src("dynmod.txt"))
new_file("common/national_focus/05_roc_mainland.txt", src("05_roc_mainland.txt", True))
new_file("events/Taiwan_Reclamation.txt", src("Taiwan_Reclamation.txt", True))
loc = "l_english:\n # Operation Blue Tiger milestone 5: Return to the Mainland\n" + src("loc_main.yml") + src("events_loc.yml", True) + src("focus_loc.yml", True)
new_file("localisation/english/MD_TAI_reclamation_l_english.yml", loc, bom=True)


def append_once(rel, marker, block):
    fp = p(rel)
    txt = rd(fp)
    if marker in txt:
        skipped.append(rel + " present")
        return
    wr(fp, txt.rstrip("\n") + "\n" + block.rstrip("\n") + "\n")


append_once("common/scripted_triggers/99_TAI_scripted_triggers.txt", "TAI_reclamation_allowed = {", src("triggers.txt"))
append_once("common/scripted_effects/99_TAI_scripted_effects.txt", "TAI_update_reclamation = {", src("effects.txt"))
append_once("common/decisions/categories/99_TAI_decision_categories.txt", "TAI_reclamation_category = {", src("category.txt"))


def insert_once(rel, marker, anchor, text, after=True, bom=False):
    fp = p(rel)
    txt = rd(fp, bom)
    if marker in txt:
        skipped.append(rel + " present")
        return
    assert txt.count(anchor) == 1, (rel, anchor, txt.count(anchor))
    new = anchor + text if after else text + anchor
    wr(fp, txt.replace(anchor, new), bom)


insert_once("common/on_actions/99_TAI_on_actions.txt", "TAI_update_reclamation", "\t\t\tTAI_update_pressure = yes\n", "\t\t\tTAI_update_reclamation = yes\n")
insert_once("common/game_rules/00_game_rules.txt", "TAI_return_to_mainland = {", "SIA_ai_behavior = {\n", src("rule.txt"), after=False)

fp = p("localisation/english/MD_game_rules_l_english.yml")
txt = rd(fp, True)
if "RULE_TAI_RETURN_TO_MAINLAND:" in txt:
    skipped.append("rule loc present")
else:
    lines = txt.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(" RULE_OPTION_TAI_ISLAND_FORTRESS_DESC:")]
    assert len(idx) == 1
    lines[idx[0] + 1:idx[0] + 1] = src("rule_loc.yml").rstrip("\n").split("\n")
    wr(fp, "\n".join(lines), True)

fp = p("common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt")
txt = rd(fp)
if "ROC_restored_mainland" in txt:
    skipped.append("party loc present")
else:
    for key in ("conservatism", "conservatism_desc", "conservatism_icon"):
        anchor = f"\ttext = {{ trigger = {{ original_tag = CHI }} localization_key = CHI.{key} }}\n"
        assert txt.count(anchor) == 1, key
        txt = txt.replace(anchor, f"\ttext = {{ trigger = {{ original_tag = CHI has_country_flag = ROC_restored_mainland }} localization_key = TAI.{key} }}\n" + anchor)
    wr(fp, txt)

for sub in ("", "medium/", "small/"):
    dst = p(f"gfx/flags/{sub}CHI_ROC.tga")
    if os.path.exists(dst):
        skipped.append(f"flag {sub}present")
    elif DRY:
        done.append(f"(dry) gfx/flags/{sub}CHI_ROC.tga")
    else:
        shutil.copyfile(p(f"gfx/flags/{sub}TAI_democratic.tga"), dst)
        done.append(f"gfx/flags/{sub}CHI_ROC.tga")

fp = p("Changelog.txt")
txt = rd(fp)
old = "and staged talks with Beijing that replace automatic annexation\n"
new = "staged talks with Beijing that replace automatic annexation, and an optional alternate-history Return to the Mainland path with a postwar settlement, successor states and a mainland Republic of China focus tree\n"
if new in txt:
    skipped.append("changelog current")
else:
    assert txt.count(old) == 1
    wr(fp, txt.replace(old, new))

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
