#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 3 to a Millennium Dawn checkout.

Usage: python3 -I -B apply3.py <repo_root> <events_out_dir> <m3_dir> [--dry-run]
Run events_gen.py and apply2.py first so the events file carries the new events.
"""
import os
import re
import sys

REPO, EVOUT, M3 = sys.argv[1], sys.argv[2], sys.argv[3]
DRY = "--dry-run" in sys.argv
MARK3 = "Operation Blue Tiger milestone 3"
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


def m3(name):
    return rd(os.path.join(M3, name))


def new_file(rel, text):
    fp = p(*rel.split("/"))
    if os.path.exists(fp):
        if rd(fp) == text:
            skipped.append(rel + " current")
            return
        sys.exit(f"refusing to overwrite existing {rel}")
    wr(fp, text)


ev = rd(p("events", "Taiwan_Blue_Tiger.txt"))
assert "id = blue_tiger.40" in ev, "run events_gen.py + apply2.py first"

# ---- new files
new_file("common/decisions/TAI_blue_tiger_decisions.txt", m3("TAI_blue_tiger_decisions.txt"))
new_file("common/on_actions/99_TAI_on_actions.txt", m3("99_TAI_on_actions.txt"))

# ---- ideas
fp = p("common", "ideas", "05_taiwan.txt")
txt = rd(fp)
if MARK3 in txt:
    skipped.append("ideas present")
else:
    tail = "\t}\n}\n"
    assert txt.endswith(tail)
    wr(fp, txt[: -len(tail)] + rd(os.path.join(EVOUT, "ideas3_block.txt")) + tail)

# ---- decision category
fp = p("common", "decisions", "categories", "99_TAI_decision_categories.txt")
txt = rd(fp)
if "TAI_blue_tiger_category" in txt:
    skipped.append("category present")
else:
    wr(fp, txt.rstrip("\n") + "\n" + m3("category_m3.txt"))

# ---- scripted effect
fp = p("common", "scripted_effects", "99_TAI_scripted_effects.txt")
txt = rd(fp)
if "TAI_update_pressure = {" in txt:
    skipped.append("pressure effect present")
else:
    wr(fp, txt.rstrip("\n") + "\n" + m3("effects_m3.txt"))

# ---- China decision
fp = p("common", "decisions", "05_CHI_decisions.txt")
txt = rd(fp)
if "CHI_TAI_offer_settlement = {" in txt:
    skipped.append("China decision present")
else:
    anchor = "\tCHI_TAI_lift_full_blockade = {\n"
    assert txt.count(anchor) == 1
    wr(fp, txt.replace(anchor, m3("chi_decision_m3.txt") + anchor))

# ---- China events: route surrender options into staged talks
fp = p("events", "05_china.txt")
txt = rd(fp)
if "blue_tiger.40" in txt:
    skipped.append("China events already rerouted")
else:
    old17 = "\t\tCHI = {\n\t\t\tcountry_event = { id = china_sar.018 days = 7 }\n\t\t}\n"
    old20 = "\t\tCHI = {\n\t\t\tcountry_event = { id = china_sar.022 days = 1 }\n\t\t}\n"
    talks = "\t\tcountry_event = { id = blue_tiger.40 days = 1 }\n"
    assert txt.count(old17) == 1 and txt.count(old20) == 1
    txt = txt.replace(old17, talks).replace(old20, talks)
    m = re.search(r"country_event = \{\n\tid = china_sar\.018\n.*?\n\}\n\n", txt, re.S)
    assert m and "annex_country = { target = TAI" in m.group(0)
    txt = txt[: m.start()] + txt[m.end():]
    old22 = "\t\tannex_country = { target = TAI transfer_troops = yes }\n\t\tif = {\n\t\t\tlimit = { has_dynamic_modifier = { modifier = CHI_TAI_shared_modifier } }"
    assert txt.count(old22) == 1
    txt = txt.replace(old22, "\t\tannex_country = { target = TAI transfer_troops = yes }\n\t\tclr_country_flag = CHI_TAI_full_blockade_active\n\t\tclr_country_flag = CHI_TAI_partial_blockade_active\n\t\tclr_country_flag = CHI_TAI_maritime_zone_active\n\t\tif = {\n\t\t\tlimit = { has_dynamic_modifier = { modifier = CHI_TAI_shared_modifier } }")
    assert "china_sar.018" not in txt
    wr(fp, txt)

# ---- China localisation
fp = p("localisation", "english", "MD_focus_CHI_l_english.yml")
txt = rd(fp, bom=True)
if " china_sar.018.t:" not in txt:
    skipped.append("China loc already updated")
else:
    txt = re.sub(r"^ china_sar\.018\.[tda]: .*\n", "", txt, flags=re.M)
    old = ' china_sar.020.b: "Accept the terms. The struggle is over."'
    assert txt.count(old) == 1
    txt = txt.replace(old, ' china_sar.020.b: "Open talks on Beijing\'s terms."')
    wr(fp, txt, bom=True)

# ---- Taiwan localisation: append keys not yet present
fp = p("localisation", "english", "MD_focus_TAI_l_english.yml")
txt = rd(fp, bom=True)
have = set(re.findall(r"^ ([A-Za-z0-9_.]+):", txt, re.M))
add = []
for line in (rd(os.path.join(EVOUT, "events_loc.yml")) + m3("loc_m3.yml")).splitlines():
    m = re.match(r"^ ([A-Za-z0-9_.]+):", line)
    if m and m.group(1) not in have:
        add.append(line)
        have.add(m.group(1))
if not add:
    skipped.append("Taiwan loc present")
else:
    wr(fp, txt.rstrip("\n") + "\n # " + MARK3 + "\n" + "\n".join(add) + "\n", bom=True)

# ---- history
fp = p("history", "countries", "TAI - Taiwan.txt")
txt = rd(fp)
if "TAI_blockade_burden" in txt:
    skipped.append("history present")
else:
    anchor = "\tset_variable = { TAI_defense_posture = 1 }\n"
    assert txt.count(anchor) == 1
    wr(fp, txt.replace(anchor, anchor + "\tset_variable = { TAI_blockade_burden = 0 }\n\tset_variable = { TAI_negotiation_stage = 0 }\n"))

# ---- changelog
fp = p("Changelog.txt")
txt = rd(fp)
old = "plus 22 historical and political events from the 2000 inauguration to the 2008 transition\n"
new = "plus 22 historical and political events from the 2000 inauguration to the 2008 transition, a cross-Strait pressure system with Blue Tiger Emergency decisions, a defensive war path, and staged talks with Beijing that replace automatic annexation\n"
if new in txt:
    skipped.append("changelog current")
else:
    assert txt.count(old) == 1
    wr(fp, txt.replace(old, new))

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
