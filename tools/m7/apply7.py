#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 7 (Cross-Strait Tension meter) to a Millennium Dawn checkout.

Usage: python3 -I -B apply7.py <repo_root> <m7_dir> [--dry-run]
"""
import os
import re
import sys

REPO, M7 = sys.argv[1], sys.argv[2]
DRY = "--dry-run" in sys.argv
FW = "has_completed_focus = CHI_SAR_one_china_framework"
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


def src(name):
    return rd(os.path.join(M7, name))


def new_file(rel, text, bom=False):
    if os.path.exists(p(rel)):
        if rd(p(rel), bom) == text:
            skipped.append(rel + " current")
            return
        sys.exit(f"refusing to overwrite {rel}")
    wr(rel, text, bom)


new_file("common/decisions/OBT_strait_decisions.txt", src("TAI_strait_decisions.txt"))
new_file("common/dynamic_modifiers/99_OBT_strait_dynamic_modifiers.txt", src("dynmod.txt"))
new_file("common/scripted_guis/99_OBT_strait_scripted_guis.txt", src("99_OBT_strait_scripted_guis.txt"))
new_file("common/scripted_localisation/99_OBT_strait_scripted_localisation.txt", src("99_OBT_strait_scripted_localisation.txt"))
new_file("interface/OBT_strait_meter.gui", src("OBT_strait_meter.gui"))
new_file("interface/OBT_strait_meter.gfx", src("OBT_strait_meter.gfx"))
new_file("events/Taiwan_Strait_Meter.txt", src("Taiwan_Strait_Meter.txt"))
new_file("localisation/english/MD_OBT_strait_l_english.yml",
         "l_english:\n # Operation Blue Tiger milestone 7: Cross-Strait Tension meter\n" + src("loc_main.yml") + src("events_loc.yml"), bom=True)


def append_once(rel, marker, block):
    txt = rd(p(rel))
    if marker in txt:
        skipped.append(rel + " present")
        return
    wr(rel, txt.rstrip("\n") + "\n" + block.rstrip("\n") + "\n")


append_once("common/scripted_triggers/99_TAI_scripted_triggers.txt", "OBT_strait_at_least_friction = {", src("triggers.txt"))
append_once("common/scripted_effects/99_TAI_scripted_effects.txt", "OBT_strait_update = {", src("effects.txt"))
append_once("common/decisions/categories/99_TAI_decision_categories.txt", "OBT_cross_strait_category = {", """
OBT_cross_strait_category = {
	allowed = { original_tag = TAI }
	icon = GFX_decision_generic_taiwan
	scripted_gui = OBT_TAI_strait_meter
	priority = 591
	visible_when_empty = yes
}
""")

rel = "common/on_actions/99_TAI_on_actions.txt"
txt = rd(p(rel))
if "OBT_strait_update" in txt:
    skipped.append(rel + " present")
else:
    a1 = "\t\t\tTAI_update_reclamation = yes\n"
    a2 = "\ton_monthly_CHI = {\n\t\teffect = {\n"
    assert txt.count(a1) == 1 and txt.count(a2) == 1
    txt = txt.replace(a1, a1 + "\t\t\tOBT_strait_update = yes\n\t\t\tOBT_strait_snapshot = yes\n").replace(a2, a2 + "\t\t\tOBT_strait_update = yes\n")
    tail = txt.rstrip("\n")
    assert tail.endswith("}")
    txt = tail[:-1].rstrip("\n") + "\n\n\ton_startup = {\n\t\teffect = {\n\t\t\tOBT_strait_update = yes\n\t\t}\n\t}\n}\n"
    wr(rel, txt)

rel = "common/decisions/categories/99_CHI_decision_categories.txt"
txt = rd(p(rel))
old = "CHI_SAR_decisions_category = {\n\tallowed = { original_tag = CHI }\n\n\ticon = GFX_decision_generic_china\n\tvisible_when_empty = yes\n\n\tvisible = { has_completed_focus = CHI_SAR_one_china_framework }\n}\n"
new = "CHI_SAR_decisions_category = {\n\tallowed = { original_tag = CHI }\n\n\ticon = GFX_decision_generic_china\n\tscripted_gui = OBT_CHI_strait_meter\n\tvisible_when_empty = yes\n}\n"
if new in txt:
    skipped.append(rel + " current")
else:
    assert txt.count(old) == 1, "CHI_SAR category changed upstream"
    wr(rel, txt.replace(old, new))

rel = "common/decisions/05_CHI_decisions.txt"
raw = rd(p(rel))
bom = raw.startswith("﻿")
txt = raw.lstrip("﻿")
start = txt.index("\nCHI_SAR_decisions_category = {\n") + 1
depth, end = 0, None
for k in range(txt.index("{", start), len(txt)):
    if txt[k] == "{":
        depth += 1
    elif txt[k] == "}":
        depth -= 1
        if depth == 0:
            end = k
            break
block = txt[start:end + 1]
names = re.findall(r"\n\t([A-Za-z0-9_]+) = \{\n", block)
out, pos, changed, already = [], 0, 0, 0
for m in re.finditer(r"\n\t([A-Za-z0-9_]+) = \{\n", block):
    s = m.end()
    d, k = 1, s
    while d:
        if block[k] == "{":
            d += 1
        elif block[k] == "}":
            d -= 1
        k += 1
    body = block[s:k - 1]
    if "days_mission_timeout" in body:
        continue
    vm = re.search(r"(?m)^\t\tvisible = \{(.*)$", body)
    if vm:
        b0 = body.index("{", vm.start())
        dd, kk = 0, b0
        while True:
            if body[kk] == "{":
                dd += 1
            elif body[kk] == "}":
                dd -= 1
                if dd == 0:
                    break
            kk += 1
        if re.search(r"(?m)^\t\t\t" + re.escape(FW) + r"\s*$", body[b0:kk]) or body[b0:kk].strip("{} \t") == FW:
            already += 1
            continue
    if vm is None:
        new_body = "\t\tvisible = {\n\t\t\t" + FW + "\n\t\t}\n\n" + body
    elif vm.group(1).strip() == "":
        new_body = body[:vm.end()] + "\n\t\t\t" + FW + body[vm.end():]
    else:
        inner = vm.group(1).strip()
        assert inner.endswith("}"), (m.group(1), inner)
        inner = inner[:-1].strip()
        new_body = body[:vm.start()] + "\t\tvisible = {\n\t\t\t" + FW + "\n\t\t\t" + inner + "\n\t\t}" + body[vm.end():]
    out.append(block[pos:s])
    out.append(new_body)
    pos = k - 1
    changed += 1
out.append(block[pos:])
new_block = "".join(out)
if changed == 0:
    skipped.append(rel + f" current ({already} gated)")
else:
    txt = txt[:start] + new_block + txt[end + 1:]
    wr(rel, ("﻿" if bom else "") + txt)
    done.append(f"  gated {changed} decisions, {already} already gated, {len(names)} total")

rel = "common/decisions/TAI_blue_tiger_decisions.txt"
txt = rd(p(rel))
old = "\t\tavailable = {\n\t\t\tOR = {\n\t\t\t\thas_war_with = CHI\n\t\t\t\tcustom_trigger_tooltip = {\n\t\t\t\t\ttooltip = TAI_burden_above_19_tt\n"
new = "\t\tavailable = {\n\t\t\tOR = {\n\t\t\t\thas_war_with = CHI\n\t\t\t\tOBT_strait_at_least_crisis = yes\n\t\t\t\tcustom_trigger_tooltip = {\n\t\t\t\t\ttooltip = TAI_burden_above_19_tt\n"
if new in txt:
    skipped.append(rel + " current")
else:
    assert txt.count(old) == 1
    wr(rel, txt.replace(old, new))

rel = "Changelog.txt"
txt = rd(p(rel))
old = "and an optional alternate-history Return to the Mainland path"
new = "a shared Cross-Strait Tension meter for China and Taiwan with five stages, and an optional alternate-history Return to the Mainland path"
if new in txt:
    skipped.append("changelog current")
else:
    assert txt.count(old) == 1
    wr(rel, txt.replace(old, new))

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
